
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version
Catalog("/home/astro-util/projects/13B312/ramps/pilot_39_dir/Pilot39_Sources.cat")

##########  <<<< Do only one of these!!! >>>>> #########
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
##########  <<<< Do only one of these!!! >>>>> #########
Configure(vegas_config)
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

off = "L39_StOff10" # define a map reference location, with no emission

Slew(off)
Balance()
Track(off, None, 30.0, "1")
mapTarget='L39_Strip10'                # The map center is often not the peak location
RALongMap( mapTarget, 
	   Offset("Galactic", 1.0, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.058), 
	   Offset("Galactic", 0.0, 0.008), 
	   480.0, "1")
Track( off, None, 30.0, "1")
