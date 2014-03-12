#!/usr/bin/env python
# encoding: utf-8
"""
Make a GBT Catalog for the Pilot Survey fields

Specify a central position in galactic longitude
The map will extend +/- 0.5 degrees in latitude
Half the map will be done in blocks, half in stripes

python make_pilot_scripts.py -p 10.5 -s -c
python make_pilot_scripts.py -p 29.5 -s -c
python make_pilot_scripts.py -p 39.5 -s -c

-d : Directory   -- Name of directory into which to save files
-p : Position    -- Central position of map in Galactic longitude
-s : Scripts     -- Make scripts for this position
-c : Catalog     -- Make a catlog and visualization
-h : Help        -- Display this help 
"""

import sys,os,getopt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from string import Template

def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:],"d:p:sch")
    except getopt.GetoptError,err:
        print(str(err))
        print(__doc__)
        sys.exit(2)
    do_scripts = False
    do_catalog = False
    position = None
    dir_name = None
    for o,a in opts:
        if o == "-d":
            dir_name = a
        elif o == "-p":
            position = a
        elif o == "-s":
            do_scripts = True
        elif o == "-c":
            do_catalog = True
        elif o == "-h":
            print(__doc__)
            sys.exit(1)
        else:
            assert False, "unhandled option"
            print(__doc__)
            sys.exit(2)
    if not position:
        print("")
        print(">>> Must specify a central position <<<")
        print(__doc__)
        sys.exit(2)
    if not dir_name:
        print("No output directory specified...")
        dir_name = "pilot_"+str(round(float(position),1))+"_dir"
        reg_name = "_"+str(round(float(position),1))+"_"
        dir_name = dir_name.replace('.','p')
        reg_name = reg_name.replace('.','p')
        print("Using "+dir_name)
    else:
        reg_name=dir_name
    try:
        os.mkdir(dir_name)
    except OSError:
        pass
    
    if do_catalog:
        make_catalog(float(position),dir_name,reg_name)
    if do_scripts:
        make_scripts(float(position),dir_name,reg_name)

def make_scripts(position,dir_name,reg_name):
    ff = open(dir_name+'/Pilot'+reg_name+'Sources.cat','r')
    all_lines = ff.readlines()
    tile_template = Template(tt)
    strip_template = Template(ts)
        
    point_str = """
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version

execfile("/home/astro-util/projects/13B312/${dir_name}/ramps/Pilot${reg_name}Sources.cat")

mySource = "{$map_pos}"

#Do automatic lookup for peak/focus
AutoPeakFocus()
"""
 #   point_temp = Template(point_str)
    for i,line in enumerate(all_lines):
        if "Tiles" in line:
            name = line.split(' ')[0]
            off = all_lines[i+1].split(' ')[0]
            d = {"point_pos":"PointPos","off_pos":off,
                 "map_pos":name,"reg_name":reg_name,
                 "dir_name":dir_name}
            output = tile_template.substitute(d)
            gg= open(dir_name+"/map"+name+".py",'w')
            print >>gg,output
            gg.close()
            #Make a separate peak script
            #point_out = point_temp.substitute(d)
            #gg= open(dir_name+"/peak"+name+".py",'w')
            #print >>gg,point_out
            #gg.close()
            
        if "Strip" in line:
            name = line.split(' ')[0]
            off = all_lines[i+1].split(' ')[0]
            d = {"point_pos":"PointPos","off_pos":off,
                 "map_pos":name,"reg_name":reg_name,
                 "dir_name":dir_name}
            output = strip_template.substitute(d)
            gg= open(dir_name+"/map"+name+".py",'w')
            print >>gg,output
            gg.close()
            #Make a separate peak script
            #point_out = point_temp.substitute(d)
            #gg= open(dir_name+"/peak"+name+".py",'w')
            #print >>gg,point_out
            #gg.close()
            
            
    
def make_catalog(position,dir_name,reg_name):
    """ Make a catalog file describing the centers of all maps. """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    all_patches = []
    fullstring = ""
    
    #I need to look up these points as the brightest points
    #within each region from Bolocam
    fullstring += "PointPos GALACTIC 10.2976 -0.1482 50.0\n"
    
    #Do some tiles (0.25 x 0.20)
    #Inclue 0.05 degree overlap
    i = 1
        
    glon_min = position-0.375
    glon_max = position+0.375
    for glat in np.arange(-0.05,0.35,.195):
        for glon in np.arange(glon_max,glon_min,-0.245):
            map_string = "Pilot_Tiles"+reg_name+str(i).zfill(2)+\
                         " GALACTIC "+str(glon)+" "+str(glat)+" 50.0"
            off_string = "Pilot_TiOFF"+reg_name+str(i).zfill(2)+\
                         " GALACTIC "+str(glon)+" "+str(glat+1.0)+" 50.0"
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
                    for glon2 in [position]:
                        map_string = "Pilot_Strip"+reg_name+str(i).zfill(2)+\
                                     " GALACTIC "+str(glon2)+" "+str(glat2)+" 50.0"
                        off_string = "Pilot_StOFF"+reg_name+str(i).zfill(2)+\
                                     " GALACTIC "+str(glon2)+" "+str(glat2+1.0)+" 50.0"
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
    ax.set_xlim(position+0.6,position-0.6)
    ax.set_ylim(-0.5,0.5)
    plt.ylabel("GLat (deg)")
    plt.xlabel("GLon (deg)")
    fig.savefig(dir_name+"/Pilot"+reg_name+"Positions.pdf")
    #plt.show()
    fullstring = fullstring[0:-1]
    fff = open(dir_name+"/Pilot"+reg_name+"Sources.cat",'w')
    print >>fff,fullstring
    fff.close()
                 
catalog_template_1 = '''#RAMPS tile/stripe list
head = name coordmode GLON GLAT velocity
'''     
catalog_template_2 ='''
'''

tt = """
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version

#First load our catalog
Catalog("/home/astro-util/projects/13B312/ramps/${dir_name}/Pilot${reg_name}Sources.cat")

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

target = "${point_pos}"  # define location of peak emission, for test, not mapping
off = "${off_pos}" # define a map reference location, with no emission

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
mapTarget='${map_pos}'                # The map center is often not the peak location
RALongMap( mapTarget, 
	   Offset("Galactic", 0.25, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.20), 
	   Offset("Galactic", 0.0, 0.008), 
	   120.0, "1")

#perform the final position switched reference obs
OffTrack( off, None, 30.0, "1")
"""
     
ts = """
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version

#First load our catalog
Catalog("/home/astro-util/projects/13B312/ramps/${dir_name}/Pilot${reg_name}Sources.cat")

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

target = "${point_pos}"  # define location of peak emission, for test, not mapping
off = "${off_pos}" # define a map reference location, with no emission

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
mapTarget='${map_pos}'                # The map center is often not the peak location
RALongMap( mapTarget, 
	   Offset("Galactic", 1.0, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.058), 
	   Offset("Galactic", 0.0, 0.008), 
	   480.0, "1")

#perform the final position switched reference obs
OffTrack( off, None, 30.0, "1")
"""
     
if __name__ == '__main__':
    main()
