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
    try:
        opts,args = getopt.getopt(sys.argv[1:],"i:o:h")
    except getopt.GetoptError,err:
        print(str(err))
        print(__doc__)
        sys.exit(2)
    for o,a in opts:
        if o == "-i":
            input_file = a
        elif o == "-o":
            output_file = a
        elif o == "-h":
            print(__doc__)
            sys.exit(1)
        else:
            assert False, "unhandled option"
            print(__doc__)
            sys.exit(2)
        
    d,h = pyfits.getdata(input_file,header=True)   
    d = np.squeeze(d)
    
    numcores = 6
    #manager = multiprocessing.Manager()

    s = np.array_split(d, numcores, 2)

    #pool = multiprocessing.Pool(processes=numcores)
    #pool.map_async(do_chunk,[s[0],s[1]])
    #from IPython import parallel
    #clients = parallel.Client()
    #clients.block = True
#    view = clients.load_balanced_view()
    #clients[0].apply(do_chunk,0,sequence[0])
    #pool.close()
    #pool.join()
    ps = []
    for num in range(len(s)):
        #print(num)
        ps.append(multiprocessing.Process(target=do_chunk,args=(num,s[num])))
    for p in ps:
       # print("Starting a process")
        p.start()
    for p in ps:
        p.join()
        #print("Process finished")
    recombine(numcores,output_file=output_file)
    
    
def recombine(numparts,output_file="test_final.fits"):
    indata = []
    for n in range(numparts):
        d = pyfits.getdata("temp"+str(n)+".fits")
        indata.append(d)
    final = np.dstack(indata)
    pyfits.writeto(output_file,final,clobber=True)
    
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

def do_chunk(num,data):
    #print(data.shape)
    ya =  np.apply_along_axis(baseline_and_deglitch,0,data)
    pyfits.writeto("temp"+str(num)+".fits",ya,clobber=True)
    #print("Finished chunk: "+str(num))

def fit_baseline(masked,xx,ndeg=2):
    ya = ma.polyfit(xx,masked,ndeg)
    basepoly = np.poly1d(ya)
    return(basepoly)

def find_best_baseline(masked,xx):
    chisqs = np.zeros(7)
    ndegs = np.arange(7)
    for i,ndeg in enumerate(ndegs):
        #print(i)
        basepoly = fit_baseline(masked,xx,ndeg=ndeg)
        base = basepoly(xx)
        chisqs[i] = np.sum((masked-base)**2)/(ma.count(masked)-1-10*ndeg)
        #print(chisqs)
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
        sigma_cut times the median value for s.
    (3) Fit and subtract-out a polynomial of order poly_n 
        (currently hard-coded to 2)
    (4) Median filter (with a filter width of filt_width)
        to remove the single-channel spikes seen.
    """
    #print("Getting here")
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
    #masked = orig_spec
    
    #Down-sample for the polyfit.
    #For speed, but mostly for memory
    masked = im.median_filter(masked,filt_width)[::filt_width]
    
    #print("Masked")
    xx = np.arange(masked.size)
    #ya = ma.polyfit(xx,masked,2)
    #baseline = ya[0]*xx**2+ya[1]*xx+ya[2]
    npoly = find_best_baseline(masked,xx)
    #npoly = 4
    #print("Best poly = "+str(npoly))
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
    sub = orig_spec-newbaseline
    #Filter out glitches in baseline-subtracted version
    final = im.median_filter(sub,filt_width)[::filt_width]
    #final = masked
    return(final)

if __name__ == '__main__':
    main()
