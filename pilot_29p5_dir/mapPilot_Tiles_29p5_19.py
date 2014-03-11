
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version

#First load our catalog
Catalog("/home/astro-util/projects/13B312/ramps/pilot_29p5_dir/Pilot_29p5_Sources.cat")

#Simple configuration for auto-peak-focus
#Try to get a source automagically
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_simple.py")
Configure(vegas_config)
AutoPeakFocus()

##########  <<<< Do only one of these!!! >>>>> #########
execfile("/home/astro-util/projects/13B312/ramps/vegas_config.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_simple.py")
##########  <<<< Do only one of these!!! >>>>> #########
Configure(vegas_config)


#define procedures with scan anotations for the pipeline
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

target = "PointPos"  # define location of peak emission, for test, not mapping
off = "Pilot_TiOFF_29p5_19" # define a map reference location, with no emission

Slew(target)
Balance()
#Check the levels are correct
#Break("Balance IF-Rack and Spectrometer")

#Perform the Target source observation; then check spectra
TargetTrack(target, None, 30.0, "1")
#perform a position switched reference location obs.
OffTrack(off, None, 30.0, "1")

#Tell Pipeline that mapping is starting
SetValues("ScanCoordinator",{"scanId":"Map"})
mapTarget='Pilot_Tiles_29p5_19'                # The map center is often not the peak location
RALongMap( mapTarget, 
	   Offset("Galactic", 0.25, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.20), 
	   Offset("Galactic", 0.0, 0.008), 
	   120.0, "1")

#perform the final position switched reference obs
OffTrack( off, None, 30.0, "1")

