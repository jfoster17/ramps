#!/usr/bin/env python
# encoding: utf-8
"""
fix_ramps_parallel.py

Fit baselines and remove glitches/spikes from RAMPS data.
Optionally transforms to velocity and outputs a (masked)
moment zero (integrated intensity map)

This version runs in parallel, which is useful because
the process is fairly slow.

Example:
python fits_ramps_parallel.py 
       -i L30_Tile01-04_23694_MHz_line.fits 
       -o L30_Tile01-04_fixed.fits

-i : Input      -- Input file (reduced by pipeline)
-o : Output     -- Output file 
-v : Velocity   -- Flag to convert to velocity 
-m : Moment Map -- Flag to produce a moment zero
                   map (called Ouput+_mom0.fits)
-h : Help       -- Display this help

"""



import sys,os,getopt
import pyfits
import scipy.ndimage as im
import numpy as np
import numpy.ma as ma
import scipy.signal as si
import multiprocessing, logging
import my_pad

def main():
    #Magic to prevent numpy from breaking multiprocessing
    #os.system("taskset -p 0xff %d" % os.getpid())
    
    output_file = "default.fits"
    do_vel = False
    do_mom = False
    try:
        opts,args = getopt.getopt(sys.argv[1:],"i:o:vmh")
    except getopt.GetoptError,err:
        print(str(err))
        print(__doc__)
        sys.exit(2)
    for o,a in opts:
        if o == "-i":
            input_file = a
        elif o == "-o":
            output_file = a
        elif o == "-v":
            do_vel = True
        elif o == "-m":
            do_mom = True
        elif o == "-h":
            print(__doc__)
            sys.exit(1)
        else:
            assert False, "unhandled option"
            print(__doc__)
            sys.exit(2)
        
    d,h = pyfits.getdata(input_file,header=True)   
    d = np.squeeze(d)
    
    ###################### numcores #########################
    # Set this value to the number of processers available  #
    numcores = 6
    s = np.array_split(d, numcores, 2)

    ps = []
    for num in range(len(s)):
        ps.append(multiprocessing.Process(target=do_chunk,args=(num,s[num])))
    for p in ps:
        p.start()
    for p in ps:
        p.join()
       # ,output_file=output_file
    dout = recombine(numcores)
    if do_vel:
        hout = downsample_header(change_to_velocity(strip_header(h,4)))
    else:
        hout = downsample_header(strip_header(h,4))
    pyfits.writeto(output_file,dout,hout,clobber=True)
    if do_mom:
        mom0_file = output_file[0:-5]+"_mom0.fits"
        mom0 = np.apply_along_axis(sum_over_signal,0,dout,3)
        mom0 *= 0.127 #Convert to K km/s. Needs to be better integrated!
        hmom = strip_header(h,3)
        pyfits.writeto(mom0_file,mom0,hmom,clobber=True)
        


def do_chunk(num,data):
    """
    Basic command to process data
    apply_along_axis is the fastest way
    I have found to do this.
    """
    ya =  np.apply_along_axis(baseline_and_deglitch,0,data)
    pyfits.writeto("temp"+str(num)+".fits",ya,clobber=True)
    
    
def recombine(numparts,output_file="test_final.fits"):
    """
    Recombine all the individual fits files into 
    one final image
    """
    indata = []
    for n in range(numparts):
        d = pyfits.getdata("temp"+str(n)+".fits")
        indata.append(d)
    final = np.dstack(indata)
    return(final)
    
def rolling_window(a,window):
    """
    Magic code to quickly create a second dimension
    with the elements in a rolling window. This
    allows us to apply numpy operations over this
    extra dimension MUCH faster than using the naive approach.
    """
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)    
    strides = a.strides+(a.strides[-1],)
    return np.lib.stride_tricks.as_strided(a, shape=shape, strides=strides)

def fit_baseline(masked,xx,ndeg=2):
    """
    Fit a polynomial baseline of
    arbitrary (ndeg) order.
    """
    ya = ma.polyfit(xx,masked,ndeg)
    basepoly = np.poly1d(ya)
    return(basepoly)

def find_best_baseline(masked,xx):
    """
    Consider polynomial baselines up to order 7 (which seems to 
    do a good job for the most complex baselines).
    Select the baseline with the lowest reduced chi-squared, 
    where we have added an extra penalty for increasing more
    degrees of freedom (prior_penalty). Without a prior,
    prior_penalty would be 1.
    """
    prior_penalty = 10.
    chisqs = np.zeros(7)
    ndegs = np.arange(7)
    for i,ndeg in enumerate(ndegs):
        basepoly = fit_baseline(masked,xx,ndeg=ndeg)
        base = basepoly(xx)
        chisqs[i] = np.sum((masked-base)**2)/(ma.count(masked)
                                              -1-prior_penalty*ndeg)
    return(np.argmin(chisqs))
    
def baseline_and_deglitch(orig_spec,
                          ww=300,
                          sigma_cut=1.5,
                          poly_n=2.,
                          filt_width=7.):
    """
    (1) Calculate a rolling standard deviation (s) in a window
        of 2*ww pixels
    (2) Mask out portions of the spectrum where s is more than
        sigma_cut times the median value for s. This seems to 
        be mis-calibrated (perhaps not independent?). A value 
        of 1.5 works well to remove all signal.
    (3) Downsample the masked spectrum (to avoid memory bug)
        and find the minimum order polynomial baseline that 
        does a good job of fitting the data.
    (3) Median filter (with a filter width of filt_width)
        to remove the single-channel spikes seen.
    """
    ya = rolling_window(orig_spec,ww*2)
    #Calculate standard dev and pad the output
    stds = my_pad.pad(np.std(ya,-1),(ww-1,ww),mode='edge')
    #Figure out which bits of the spectrum have signal/glitches
    med_std = np.median(stds)
    std_std = np.std(stds)
    sigma_x_bar = med_std/np.sqrt(ww)
    sigma_s = (1./np.sqrt(2.))*sigma_x_bar
    #Mask out signal for baseline
    masked = ma.masked_where(stds > med_std+sigma_cut*sigma_s,orig_spec)
    #Down-sample for the polyfit.
    #For speed, but mostly for memory
    masked = im.median_filter(masked,filt_width)[::filt_width]
    xx = np.arange(masked.size)
    npoly = find_best_baseline(masked,xx)
    basepoly = fit_baseline(masked,xx,ndeg=npoly)
    #Some kludgy code to refactor the baseline polynomial to
    #the full size spectra
    xxx = np.arange(orig_spec.size)
    params = np.asarray(basepoly)
    rr = filt_width
    newparams = []
    for i,p in enumerate(params[::-1]):
        newparams.append(p/rr**i)
    newparams = newparams[::-1]
    newpoly = np.poly1d(newparams)
    newbaseline = newpoly(xxx) 
    #Subtract off baseline
    sub = orig_spec-newbaseline
    #Filter out glitches in baseline-subtracted version
    final = im.median_filter(sub,filt_width)[::filt_width]
    return(final)

def downsample_header(h,filter_width=7):
    """
    Since we downsample our spectra by a factor 
    of filter_width we have to change the header as well.
    Currently this is not well-integrated. filter_width 
    here _needs_ to be the same as filt_width in
    baseline_and_deglitch
    """
    
    h['CDELT3'] = h['CDELT3']*filter_width
    h['CRVAL3'] = h['CRVAL3']/filter_width
    return(h)

def strip_header(h,n):
    """
    Remove the nth dimension from a FITS header
    """
    h['NAXIS'] = n-1
    try:
        del h['NAXIS'+str(n)]
        del h['CTYPE'+str(n)]
        del h['CRVAL'+str(n)]
        del h['CDELT'+str(n)]
        del h['CRPIX'+str(n)]
        del h['CUNIT'+str(n)]
        del h['CROTA'+str(n)]
    except:
        pass
    return(h)
    
    
def change_to_velocity(h):
    n = (h['RESTFREQ']-h['CRVAL3'])/h['CDELT3']+1
    h['CTYPE3'] = 'VELO-LSR'
    delta_freq = h['CDELT3']
    h['CDELT3'] = -299792.458/float(h['CRVAL3'])*delta_freq*1000
    h['CRVAL3'] = 0.
    h['CRPIX3'] = int(n)
    return(h)
    
def sum_over_signal(orig_spec,nsig=3.):
    """
    Sum over regions of significant signal.
    Could be modified to output a mask in order
    to enable quick calculation of multiple moments.
    """
    ww = 50
    ya = rolling_window(orig_spec,ww*2)
    stds = np.lib.pad(np.std(ya,-1),(ww-1,ww),mode='edge')
    med_std = np.median(stds)
    std_std = np.std(stds)
    sigma_x_bar = med_std/np.sqrt(ww)
    sigma_s = (1./np.sqrt(2.))*sigma_x_bar
    masked = ma.masked_where(stds < med_std+nsig*sigma_s,orig_spec)
    mom0 = ma.sum(masked)
    return(mom0)

if __name__ == '__main__':
    main()
