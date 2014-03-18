
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version
Catalog("/home/astro-util/projects/13B312/ramps/pilot_39p5_dir/Pilot_39p5_Sources.cat")

##########  <<<< Do only one of these!!! >>>>> #########
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
##########  <<<< Do only one of these!!! >>>>> #########
Configure(vegas_config)
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

off = "Pilot_TiOFF_39p5_19" # define a map reference location, with no emission

Slew(off)
Balance()
Track(off, None, 30.0, "1")
mapTarget='Pilot_Tiles_39p5_19'                # The map center is often not the peak location
RALongMap( mapTarget, 
	   Offset("Galactic", 0.25, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.20), 
	   Offset("Galactic", 0.0, 0.008), 
	   120.0, "1")
Track( off, None, 30.0, "1")

