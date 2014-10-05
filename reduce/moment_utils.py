"""
Low-install requirement scripts to help make moment maps

1) Identify signal versus spikes
2) Remove a 2nd-order polynomial baseline
3) Find signal again
4) Make a 0th moment map
5?) Return a mask for futher moments


bestmask,mask = find_features(d,for_baseline=True)
fit_baseline(bestmask)
bestmask,mask = find_features(d,high_sig=True)
maps = calculate_moments(d,bestmask=bestmask,mask=mask)
save_maps(maps,hdout,out_base,out_dir,vel,minchan,maxchan,vwidth,"smallvel")
"""

import sys,os
import pyfits
import numpy as np
import idl_stats
import scipy.signal
import scipy.ndimage
import numpy.ma as ma

def find_features(d,minchan=False,maxchan=False,vel=False,low_sig=False,high_sig=False,for_baseline=False):
    """Identify significant features over which to calculate moments."""
    if for_baseline:
        sf = 1.
        threshold = 3.
        channel_trim = 1.
        sky_trim = 1.
        expansion_factor=1.
    if low_sig: #1/18 low_sig is now higher
        sf = 9. # Smoothing factor
        threshold = 2
        channel_trim = 5 #Mininum consequtive channels
        expansion_factor = 5 #Padding on edges of detection
        sky_trim = 2 #Minimum size on sky
    if high_sig:
        sf = 9. # Smoothing factor
        threshold = 5
        channel_trim = 5 #Mininum consequtive channels
        expansion_factor = 10 #Padding on edges of detection
        sky_trim = 3 #Minimum size on sky

    nglat = d.shape[1]
    nglon = d.shape[2]
    nspec = d.shape[0]

    mask = np.zeros(d.shape,dtype=np.int)

    for x in range(nglat):
        for y in range(nglon):
            spec = d[minchan:maxchan,x,y] #Exract a single spectrum, possibly trimmed by velocity
            #print(spec)
            #Smooth and identify significant chunks
            smoothspec = idl_stats.smooth(spec,window_len =sf,window='hamming')
            mean,sigma = idl_stats.iterstat(smoothspec)
            goodsignal = np.where(smoothspec > threshold*sigma,1,0)
            goodsignal = scipy.ndimage.binary_erosion(goodsignal,structure=np.ones(channel_trim)) #Erode ROI
            goodsignal_expanded = scipy.ndimage.binary_dilation(goodsignal,structure=np.ones(expansion_factor)) #Dilate ROI
            mask[minchan:maxchan,x,y] = goodsignal_expanded

    clean_struct = np.ones((sky_trim,sky_trim,channel_trim))
    mask = scipy.ndimage.binary_closing(mask,structure=clean_struct).astype(np.int)
    mask = scipy.ndimage.binary_dilation(mask,structure=clean_struct).astype(np.int)
    #Expand the area considered in velocity
    npix = np.sum(mask,axis=0)
    longpix = np.nanargmax(npix)
    pid = np.unravel_index(longpix,npix.shape)
    bestmask = mask[...,pid[0],pid[1]]

    return(bestmask,mask)

def calculate_moments(d,minchan=False,maxchan=False,vel=False,bestmask=False,mask=False):

    nglat = d.shape[1]
    nglon = d.shape[2]
    nspec = d.shape[0]


    maps = np.zeros((nglat,nglon),dtype={'names':['mean','sd','errmn',
            'errsd','skew','kurt','error','intint','npix'],
            'formats':['f4','f4','f4','f4','f4','f4','f4','f4','f4']})

    #These definitions for mask seem backward but are correct.
    noise_portion = ma.masked_where(mask == 1,d)
    good_d = d[minchan:maxchan,...]
    mask2 = mask[minchan:maxchan,...]
    #print(mask)
    #print(mask2)
    print(minchan)
    print(maxchan)
    signal_portion = ma.masked_where(mask2 == 0,good_d)
    maps['error']  = ma.std(noise_portion,axis=0)
    maps['intint'] = ma.sum(signal_portion,axis=0)
    #print(maps['error'])


    for x in range(nglat):
        for y in range(nglon):
            fullspec = d[...,x,y]#Exract a single spectrum
            ind = np.arange(nspec)
            velmask = mask[minchan:maxchan,x,y]
            if np.sum(velmask) != 0:
                velmask = bestmask
                npix = max(np.sum(velmask),1)
            ind = ind[velmask > 0]
            sigma = maps['error'][x,y]
            if ind.size > 2 and (sigma > 0):
                mom = idl_stats.wt_moment(vel[ind],fullspec[ind],
                                errors = np.zeros(ind.size)+sigma)
                maps['mean'][x,y]  = mom['mean']
                maps['sd'][x,y]    = mom['stdev']
                maps['errmn'][x,y] = mom['errmn']
                maps['errsd'][x,y] = mom['errsd']
                maps['npix'][x,y]  = npix
            else:
                maps['mean'][x,y]  = np.nan
                maps['sd'][x,y]    = np.nan
                maps['errmn'][x,y] = np.nan
                maps['errsd'][x,y] = np.nan
                maps['npix'][x,y]  = np.nan
    return(maps)


def save_maps(maps,hdout,out_base,out_dir,vel,minchan,maxchan,vwidth,name_mod):


#       badind = np.where((maps['errmn'] > 1e3) | (maps['errsd'] > 1e3)) #This trims out sources with sigma_v > 1 km/s, which is too harsh
    badind = np.where((maps['errmn'] > 1e6) | (maps['errsd'] > 1e6)) #This trims out sources with sigma_v > 1000 km/s
    if name_mod == "highsig":
        sh_name = "hs_"
    elif name_mod == "lowsig":
        sh_name = "ls_"
    elif name_mod == "fullvel":
        sh_name = "fv_"
    elif name_mod == "smallvel":
        sh_name = "sv_"
    elif name_mod == "medvel":
        sh_name = "mv_"


    try:
        maps['mean'][badind] = np.nan
        maps['sd'][badind]   = np.nan
    except IndexError:
        pass
    maps['skew'] = maps['skew']/maps['sd']**3
    maps['kurt'] = maps['kurt']/maps['sd']**4 - 3 #Really?
    hdout['NAXIS'] = 2
    hdout.update('CDELT1',hdout['CDELT1'],'DEGREES')
    hdout.update('CDELT2',hdout['CDELT2'],'DEGREES')
    hdout.update('CRVAL1',hdout['CRVAL1'],'DEGREES')
    hdout.update('CRVAL2',hdout['CRVAL2'],'DEGREES')
    hdout.update('BUNIT','KM/S')

    #hdout.update('VMIN',vel[minchan]/1e3,'km/s')
    #hdout.update('VMAX',vel[maxchan]/1e3,'km/s')

    maps['intint'] = maps['intint']*vwidth/1e3
    out_dir_full = os.path.join(out_dir,name_mod)
    try:
        os.mkdir(out_dir_full)
    except OSError:
        pass
        #print("Failed to make dir")
    os.chdir(out_dir_full)
    pyfits.writeto(out_base+sh_name+'mom1'+'.fits',maps['mean']/1e3,hdout,clobber=True)
    pyfits.writeto(out_base+sh_name+'mom2'+'.fits',maps['sd']/1e3,hdout,clobber=True)
    pyfits.writeto(out_base+sh_name+'err1'+'.fits',maps['errmn']/1e3,hdout,clobber=True)
    pyfits.writeto(out_base+sh_name+'err2'+'.fits',maps['errsd']/1e3,hdout,clobber=True)
    hdout.update('BUNIT','NONE')
    #pyfits.writeto(out_base+'mom3.fits',maps['skew'],hdout,clobber=True)
    #pyfits.writeto(out_base+'mom4.fits',maps['kurt'],hdout,clobber=True)

    #pyfits.writeto(out_base+'snr0.fits',maps['intint']/maps['error']*
    #       np.sqrt(maps['npix'])*vwidth/1e3,hdout,clobber=True)

    #As an absolute value, SNR is still useless.
    #maps['npix'] = (maps['sd'])/vwidth #Use width of line to estimate npix
    pyfits.writeto(out_base+sh_name+'npix'+'.fits',maps['npix'],clobber=True)
    pyfits.writeto(out_base+sh_name+'snr0'+'.fits',maps['intint']/(maps['error']*
            np.sqrt(maps['npix'])*vwidth/1e3),hdout,clobber=True)

    hdout.update('BUNIT','K.KM/S')

    #print(maps['error'][15,15])
    #print(np.sqrt(maps['npix'][15,15])*vwidth/1e3)

    pyfits.writeto(out_base+sh_name+'mom0'+'.fits',maps['intint'],hdout,clobber=True)
    pyfits.writeto(out_base+sh_name+'err0'+'.fits',maps['error']*np.sqrt(maps['npix'])*
                                    vwidth/1e3,hdout,clobber=True)
    pyfits.writeto(out_base+sh_name+'emap'+'.fits',maps['error']*
                                    vwidth/1e3,hdout,clobber=True)
    os.chdir("../../")
