
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version

#execfile("/home/astro-util/projects/13B312/pilot_10p5_dir/ramps/Pilot_10p5_Sources.cat")
Catalog(kband_pointing)

#Do automatic lookup for peak/focus
AutoPeakFocus("1833-2103")

