#Configuration for RAMPS
#commissioning tests on VEGAS

vegas_config = """
receiver  = 'RcvrArray18_26'          # select KFPA receiver
beam      = '1,2,3,4,5,6,7'           # use seven beams (KFPA)
obstype   = 'Spectroscopy'
backend   = 'VEGAS'
#xnwin      = 8                          # eight spectral windows
vegas.vfreq = [{"restfreq":23694.50,"beam":'1,2,3,4,5,6,7'},
    {"restfreq":23722.63,"beam":'1,2,3,4,5,6,7'},
    {"restfreq":23870.13,"beam":'1,2,3,4,5,6,7'},
    {"restfreq":24139.42,"beam":'1,2,3,4,5,6,7'},
    {"restfreq":24532.99,"beam":'1,2,3,4,5,6,7'},
    {"restfreq":23444.78,"beam":'1,2,3,4,5,6,7'},
    {"restfreq":23963.90,"beam":'1,2,3,4,5,6,7'},
    {"restfreq":23694.50,"beam":'1,2,3,4,5,6,7'},
    {"restfreq":21301.32,"beam":'1'},
    {"restfreq":21431.93,"beam":'1'},
    {"restfreq":21550.34,"beam":'1'},
    {"restfreq":21981.57,"beam":'1'},
    {"restfreq":22235.08,"beam":'1'},
    {"restfreq":22344.03,"beam":'1'},
    ]
deltafreq=0
vegas.vpol='self'
dopplertrackfreq=23694.50
bandwidth = 23.44                     # bandwidth (per window)
nchan     = 'medium'                     # 4096 channels = 0.07 km/s
swmode    = "tp"                      # set position switching
swtype    = "none"                    # no frequency switching
swper     = 1.0                       # one-half second cycle for switching
swfreq    = 0.0, 0.0                  # for freq switching
tint      = 1.0                       # integration time
vlow      = 0                         # set to zero on advice of Kepley
vhigh     = 0
vframe    = "lsrk"
vdef      = "Radio"
noisecal  = "lo"
pol       = "Circular"
broadband = 0
"""

#23694.50 #NH3 (1-1)
#23722.63 #NH3 (2-2)
#23870.13 #NH3 (3-3)
#24139.42 #NH3 (4-4)
#24532.99 #NH3 (5-5)
#23444.78 #CH3OH
#23963.90 #HC5N

#21301.32   #HC5N (J=8-7)
#21431.93   #HC7N (J=19-18)
#21550.34   #CH3OH (12(2,11) - 11(1,10))
#21981.57   #HNCO (1(0,1)-0(0,0))
#22235.08   #H2O maser
#22344.03   #CCS (J=2-1) 

