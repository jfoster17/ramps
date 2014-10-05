import sys,os,getopt
import pyfits
import scipy.ndimage as im
import numpy as np
import numpy.ma as ma
import scipy.signal as si
import multiprocessing
import my_pad

def main():
    #Magic to prevent numpy from breaking multiprocessing
    #os.system("taskset -p 0xff %d" % os.getpid())
    
    
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
    #pool = Pool(4)
    #print(d.shape)
    #results = pool.map(baseline_and_deglitch,d)
    #pool.close()
    #pool.join()
    #print(results.shape)
    #ya =  np.apply_along_axis(baseline_and_deglitch,1,d)
    #pyfits.writeto(output_file,ya,h,clobber=True)
    numcores = 8
    manager = multiprocessing.Manager()

    sequence = np.array_split(d, numcores, 2)
    ps = []
    for num in range(len(sequence)):
        ps.append(multiprocessing.Process(target=do_chunk,args=(num,sequence[num])))
    for p in ps:
        p.start()
    for p in ps:
        p.join()
    recombine(numcores)
    
    
def recombine(numparts):
    indata = []
    for n in range(numparts):
        d = pyfits.getdata("temp"+str(n)+".fits")
        indata.append(d)
    final = np.dstack(indata)
    pyfits.writeto("test_final.fits",final,clobber=True)
    
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

def naive_std(orig_spec,w):
    stds = orig_spec.copy()
    ss = orig_spec.size
    for x in np.arange(ss):
        mmin = max(0,x-ww)
        mmax = min(ss,x+ww)
        stds[x] = np.std(orig_spec[mmin:mmax])
    return(stds)    

def do_chunk(num,data):
    print(data.shape)
    ya =  np.apply_along_axis(baseline_and_deglitch,0,data)
    pyfits.writeto("temp"+str(num)+".fits",ya,clobber=True)

def baseline_and_deglitch(orig_spec):
    ww = 300
    ya = rolling_window(orig_spec,ww*2)
    #Calculate standard dev and pad the output
    stds = my_pad.pad(np.std(ya,-1),(ww-1,ww),mode='edge')
    #Figure out which bits of the spectrum have signal/glitches
    med_std = np.median(stds)
    std_std = np.std(stds)
    sigma_x_bar = med_std/np.sqrt(ww)
    sigma_s = (1./np.sqrt(2.))*sigma_x_bar
    #Mask out signal for baseline
    masked = ma.masked_where(stds > med_std+4*sigma_s,orig_spec)
    xx = np.arange(masked.size)
    ya = ma.polyfit(xx,masked,2)
    baseline = ya[0]*xx**2+ya[1]*xx+ya[2]
    sub = orig_spec-baseline
    #Filter out glitches in baseline-subtracted version
    final = im.median_filter(sub,7)[::7]
    return(final)

if __name__ == '__main__':
    main()
