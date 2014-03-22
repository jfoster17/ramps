
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version

#Catalog("/home/astro-util/projects/13B312/ramps/pilot_10_dir/Pilot10_Sources.cat")
Catalog(kband_pointing)

#Use pre-defined target
AutoPeakFocus("1833-2103")
#Look near the peak
#AutoPeakFocus(location='L10OnOff')

