#Configuration for RAMPS
#commissioning tests on VEGAS

vegas_config = """
receiver  = 'RcvrArray18_26'          # select KFPA receiver
beam      = '1,2,3,4,5,6,7'           # use seven beams (KFPA)

obstype   = 'Spectroscopy'
backend   = 'VEGAS'
nwin      = 8                         # eight spectral windows
restfreq  = {23694.50:'1,2,3,4,5,6,7',# line frequencies
            23722.63:'1,2,3,4,5,6,7', # NH3,CH3OH and HC5N 
            23870.13:'1,2,3,4,5,6,7', # in beams 1-7
            24139.42:'1,2,3,4,5,6,7', # H2O in beam 8
            24.53299:'1,2,3,4,5,6,7', 
            23444.78:'1,2,3,4,5,6,7',
            23.96390:'1,2,3,4,5,6,7', 
            22235.08:'1',
            "DopplerTrackFreq":23694.50} 
            
bandwidth = 23.44                     # bandwidth (per window)
nchan     = 'low'                     # 4096 channels = 0.07 km/s

swmode    = "tp"                      # set position switching
swtype    = "none"                    # no frequency switching
swper     = 0.5                       # one-half second cycle for switching
                                      # (default is swper = 1.0)
swfreq    = 0.0, 0.0                  # for freq switching
tint      = 5.0                       # integration time

vlow      = -150
vhigh     = 150
vframe    = "lsrk"
vdef      = "Radio"

noisecal  = "lo"
pol       = "Circular"
"""
