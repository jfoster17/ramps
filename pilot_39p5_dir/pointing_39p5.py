
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version

#execfile("/home/astro-util/projects/13B312/pilot_39p5_dir/ramps/Pilot_39p5_Sources.cat")
Catalog(kband_pointing)

#Do automatic lookup for peak/focus
AutoPeakFocus("1850-0001")

