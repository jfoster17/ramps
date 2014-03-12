#Dummy Configuration for VEGAS
#used before AutoPeakFocus
#But AutoPeakFocus switches anyway

vegas_config = """
receiver  = 'RcvrArray18_26'          # select KFPA receiver
beam      = '1'           # use seven beams (KFPA)
obstype   = 'Spectroscopy'
backend   = 'VEGAS'
nwin      = 1                          # eight spectral windows
restfreq  = 23694.50
deltafreq = 0
bandwidth = 23.44                     # bandwidth (per window)
nchan     = 'medium'                     # 4096 channels = 0.07 km/s
swmode    = "tp"                      # set position switching
swtype    = "none"                    # no frequency switching
swper     = 0.5                       # one-half second cycle for switching
swfreq    = 0.0, 0.0                  # for freq switching
tint      = 1.0                       # integration time
vframe    = "lsrk"
vdef      = "Radio"
noisecal  = "lo"
pol       = "Circular"
"""
