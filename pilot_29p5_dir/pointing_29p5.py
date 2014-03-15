
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version

#Catalog("/home/astro-util/projects/13B312/ramps/pilot_29p5_dir/Pilot_29p5_Sources.cat")
Catalog(kband_pointing)

#Use pre-defined target
AutoPeakFocus("1751+0939")
#Look near the peak
#AutoPeakFocus(location='Field29p5OnOff')

