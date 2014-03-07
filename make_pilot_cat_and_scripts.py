#!/usr/bin/env python
# encoding: utf-8
"""
Make a GBT Catalog for the Pilot Survey field centered on 29.5 degrees galactic longitude and extending +/- 0.5 degrees in latitude.
Half the map will be done in blocks, half in stripes. 
"""

import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from string import Template

def main():
    make_catalog()
    make_scripts()

def make_scripts():
    ff = open('Pilot_Sources.cat','r')
    all_lines = ff.readlines()
    tile_template = Template(tt)
    strip_template = Template(ts)
    
    point_str = """# Astrid script to point near a maser source
# HISTORY
# 10SEP02 GIL do not reconfigure before the pointing obs
# 10AUG?? J?B initial version

execfile("/home/astro-util/projects/11B030/Pilot_Sources.cat")

mySource = "{$map_pos}"

AutoPeakFocus(location=mySource, flux=1.5, configure=False)
"""
    point_temp = Template(point_str)
    for i,line in enumerate(all_lines):
        if "Tiles" in line:
            name = line.split(' ')[0]
            off = all_lines[i+1].split(' ')[0]
            d = {"point_pos":"G030p00","off_pos":off,"map_pos":name}
            output = tile_template.substitute(d)
            gg= open("map"+name,'w')
            print >>gg,output
            gg.close()
            point_out = point_temp.substitute(d)
            gg= open("peak"+name,'w')
            print >>gg,point_out
            gg.close()
            
        if "Strip" in line:
            name = line.split(' ')[0]
            off = all_lines[i+1].split(' ')[0]
            d = {"point_pos":"G030p00","off_pos":off,"map_pos":name}
            output = strip_template.substitute(d)
            gg= open("map"+name,'w')
            print >>gg,output
            gg.close()
            point_out = point_temp.substitute(d)
            gg= open("peak"+name,'w')
            print >>gg,point_out
            gg.close()
            
            
    
def make_catalog():
    """Just write to screen."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    all_patches = []
    fullstring = catalog_template_1
    
    fullstring += "G030p00 GALACTIC 30.0 0.0 50.0\n"
    
    #Do some tiles (0.25 x 0.20)
    #Inclue 0.05 degree overlap
    i = 1
    for glat in np.arange(-0.05,0.35,.195):
        for glon in np.arange(29.875,29.125,-0.245):
            map_string = "Pilot_Tiles"+str(i).zfill(2)+" GALACTIC "+\
                          str(glon)+" "+str(glat)+" 50.0"
            off_string = "Pilot_TiOFF"+str(i).zfill(2)+" GALACTIC "+\
                          str(glon)+" "+str(glat+1.0)+" 50.0"
            fullstring = fullstring+map_string+"\n"
            rect = Rectangle((glon-0.125,glat-0.1),0.25,0.20,fill=True, 
                             fc='red', visible=True, alpha=0.4)
            ax.plot(glon,glat,'ko')
            ax.text(glon-0.01,glat+0.02,"Tile"+str(i).zfill(2))
            #ax.add_artist(rect)
            #plt.show()                
            all_patches.append(rect)
            fullstring = fullstring+off_string+"\n"
            i += 1
            if i == 5:
                #Do some Strips 1 degree x 0.058 degree (7 strips)
                #Offset would be -0.058 for best practice. Inclue 0.05 degree overlap
                for glat2 in np.arange(0,-0.41,-0.053):
                    for glon2 in [29.5]:
                        map_string = "Pilot_Strip"+str(i).zfill(2)+" GALACTIC "+\
                                      str(glon2)+" "+str(glat2)+" 50.0"
                        off_string = "Pilot_StOFF"+str(i).zfill(2)+" GALACTIC "+\
                                      str(glon2)+" "+str(glat2+1.0)+" 50.0"
                        fullstring = fullstring+map_string+"\n"
                        rect = Rectangle((glon2-0.5,glat2-0.058/2.),1,0.058,fill=True, 
                                         fc='blue', visible=True,alpha = 0.4)
                        all_patches.append(rect)
                        ax.plot(glon2,glat2,'k.')
                        ax.text(glon2-0.05,glat2,"Strip"+str(i).zfill(2))
                        fullstring = fullstring+off_string+"\n"
                        i += 1
    for patch in all_patches:
        #print("Adding patch")
        ax.add_patch(patch)
   # rect = Rectangle((0.0120,0),0.1,1000)
    #ax.add_patch(rect)
    ax.set_xlim(30.1,28.9)
    ax.set_ylim(-0.5,0.5)
    plt.ylabel("GLat (deg)")
    plt.xlabel("GLon (deg)")
    fig.savefig("PilotPositions.pdf")
    #plt.show()
    fullstring = fullstring[0:-1]+catalog_template_2
    fff = open("Pilot_Sources.cat",'w')
    print >>fff,fullstring
    fff.close()
                 
    #for glat in [-0.5,0.5]:  
    #    for glon in np.arange(10.5,40,1):
    #        radec = ac.convertCoords("GALACTIC","J2000",glon,glat,2000.)
    #        name = "Pos_"+str(glat)+"_"+str(glon)
    #        ra  = ac.decimal2hms(radec[0],":")
    #        dec = ac.decimal2dms(radec[1],":")
     #       out_string = name+"; "+"Galactic Plane; Equatorial; J2000; "+ra+"; "+dec+"; "+"LSRK; Radio; 30;"
     #       print(out_string)
catalog_template_1 = '''#First put in your sources
Catalog(
"""
head = name coordmode GLON GLAT velocity
'''     
catalog_template_2 ='''
"""
)

SetValues("LO1", {"tolerance": 10})
'''

tt = """
#Example Map Astrid script using the KFPA
#HISTORY 
# 11FEB04 GIL clean up comments

#First put in your sources
execfile("/home/astro-util/projects/11B030/Pilot_Sources.cat")

#define procedures with scan anotations for the pipeline
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

target = "${point_pos}"  # define location of peak emission, for test, not mapping
off = "${off_pos}" # define a map reference location, with no emission

Slew( target)
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
mapTarget='${map_pos}'                # The map center is often not the peak location
RALongMap( mapTarget, 
	   Offset("Galactic", 0.25, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.20), 
	   Offset("Galactic", 0.0, 0.008), 
	   120.0, "1")

#Turn cals back on for calibration scan, only if they were turned off, above.
execfile("/home/astro-util/projects/TKFPA/configCal")

#perform the final position switched reference obs
OffTrack( off, None, 30.0, "1")
"""
     
ts = """
#Example Map Astrid script using the KFPA
#HISTORY 
# 11FEB04 GIL clean up comments

#First put in your sources
execfile("/home/astro-util/projects/11B030/Pilot_Sources.cat")

#define procedures with scan anotations for the pipeline
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

target = "Pilot_Strip13"  # define location of peak emission, for test, not mapping
off = "Pilot_StOFF13" # define a map reference location, with no emission

Slew( target)
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
mapTarget='Pilot_Strip13'                # The map center is often not the peak location
RALongMap( mapTarget, 
	   Offset("Galactic", 1.0, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.058), 
	   Offset("Galactic", 0.0, 0.008), 
	   480.0, "1")

#Turn cals back on for calibration scan, only if they were turned off, above.
execfile("/home/astro-util/projects/TKFPA/configCal")

#perform the final position switched reference obs
OffTrack( off, None, 30.0, "1")
"""
     
if __name__ == '__main__':
    main()

