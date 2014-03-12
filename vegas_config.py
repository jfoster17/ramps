#Configuration for RAMPS
#commissioning tests on VEGAS

vegas_config = """
receiver  = 'RcvrArray18_26'          # select KFPA receiver
beam      = '1,2,3,4,5,6,7'           # use seven beams (KFPA)

obstype   = 'Spectroscopy'
backend   = 'VEGAS'
nwin      = 8                          # eight spectral windows
restfreq  = {23694.50:'1,2,3,4,5,6,7', # line frequencies
             23722.63:'1,2,3,4,5,6,7', # NH3 (1,1) - (5,5),CH3OH
             23870.13:'1,2,3,4,5,6,7', # and HC5N in beams 1-7
             24139.42:'1,2,3,4,5,6,7', # Other lines in beam 8
             24532.99:'1,2,3,4,5,6,7', 
             23444.78:'1,2,3,4,5,6,7',
             23963.90:'1,2,3,4,5,6,7', 
             23694.50:'1,2,3,4,5,6,7', #Duplicate NH3(1-1) line
             22344.03:'-1',				#CCS (J=2-1)
             22235.08:'-1',				#H2O maser
             21981.57:'-1',				#HNCO (1(0,1)-0(0,0))
             21550.34:'-1',				#CH3OH (12(2,11)- 11(1,10))
             21431.93:'-1',				#HC7N (J=19-18)
             21301.32:'-1',				#HC5N (J=8-7)
             25056.04:'-1',       #NH3 (6-6)
             25715.14:'-1',       #NH3 (7-7)
            "DopplerTrackFreq":23694.50} 

deltafreq = {23694.50:0,
           23722.63:0,
           23870.13:0,
           24139.42:0,
           24532.99:0,
           23444.78:0,
           23963.90:0,
           23694.50:0,
           22344.03:0,
           22235.08:0,
           21981.57:0,
           21550.34:0,
           21431.93:0,
           21301.32:0,
           25056.04:0,
           25715.14:0
           }

bandwidth = 23.44                     # bandwidth (per window)
nchan     = 'medium'                     # 4096 channels = 0.07 km/s

swmode    = "tp"                      # set position switching
swtype    = "none"                    # no frequency switching
swper     = 0.5                       # one-half second cycle for switching
                                      # (default is swper = 1.0)
swfreq    = 0.0, 0.0                  # for freq switching
tint      = 1.0                       # integration time

vlow      = -150
vhigh     = 150
vframe    = "lsrk"
vdef      = "Radio"

noisecal  = "lo"
pol       = "Circular"
vegas.vpol='cross'
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

