
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version

#Catalog("/home/astro-util/projects/13B312/ramps/pilot_39_dir/Pilot39_Sources.cat")
Catalog(kband_pointing)

#Use pre-defined target
AutoPeakFocus("1850-0001")
#Look near the peak
#AutoPeakFocus(location='L39OnOff')

