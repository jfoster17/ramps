import numpy as np

def strip(d,h):
    d = np.squeeze(d)
    h['NAXIS'] = 3
    try:
        del h['NAXIS4']
        del h['CTYPE4']
        del h['CRVAL4']
        del h['CDELT4']
        del h['CRPIX4']
        del h['CUNIT4']
    except:
        pass
    return(d,h)
