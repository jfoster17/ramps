
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY
#Nov   20, 2015 (JBF) Increased size of tiles for better overlap
#Oct    5, 2015 (JBF) Comment out blanking values (no longer needed)
#April 15, 2015 (JBF) Set blanking values manually to fix a VEGAS problem 
#March 10, 2014 (JBF) Initial Version
Catalog("/home/astro-util/projects/13B312/ramps/pilot_29_dir/Pilot29_Sources.cat")

##########  <<<< Do only one of these!!! >>>>> #########
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
##########  <<<< Do only one of these!!! >>>>> #########
Configure(vegas_config)
#ScanCordValues = {'blanking,1' : 0.006,
#                  'blanking,2' : 0.006}
#SetValues('ScanCoordinator', ScanCordValues)
#SetValues('ScanCoordinator', {'state':'prepare'})

execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

off = "L29_TOFF02" # define a map reference location, with no emission

Slew(off)
Balance()
Track(off, None, 30.0, "1")
mapTarget='L29_Tile02'                # The map center is often not the peak location
RALongMap( mapTarget, 
	   Offset("Galactic", 0.26, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.208), 
	   Offset("Galactic", 0.0, 0.008), 
	   125.0, "1")
Track( off, None, 30.0, "1")

