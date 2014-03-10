
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version

#First load our catalog
Catalog("/home/astro-util/project/13B312/Pilot_Sources.cat)

#Configure VEGAS
execfile("/home/astro-util/projects/13B312/vegas_config.py")
Configure("vegas_config")

#define procedures with scan anotations for the pipeline
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

target = "G030p00"  # define location of peak emission, for test, not mapping
off = "Pilot_TiOFF20" # define a map reference location, with no emission

Slew(target)
Balance(target)
#Check the levels are correct
Break("Balance IF-Rack and Spectrometer")

#Perform the Target source observation; then check spectra
TargetTrack( target, None, 30.0, "1")
#perform a position switched reference location obs.
OffTrack( off, None, 30.0, "1")

#To map at maximum antenna rate, turn of Cal Blinking (optional)
execfile("/home/astro-util/projects/TKFPA/configNoCal")

#Tell Pipeline that mapping is starting
SetValues("ScanCoordinator",{"scanId":"Map"})
mapTarget='Pilot_Tiles20'                # The map center is often not the peak location
RALongMap( mapTarget, 
	   Offset("Galactic", 0.25, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.20), 
	   Offset("Galactic", 0.0, 0.008), 
	   120.0, "1")

#Turn cals back on for calibration scan, only if they were turned off, above.
execfile("/home/astro-util/projects/TKFPA/configCal")

#perform the final position switched reference obs
OffTrack( off, None, 30.0, "1")

