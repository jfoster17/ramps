#!/usr/bin/env python
# encoding: utf-8
"""
Make catalogs and scripts for RAMPS Survey fields

Specify a central position in galactic longitude
The map will extend +/- 0.5 degrees in latitude

NEW -- Previously we did half the map in tiles and
half in stripes. Now we do all tiles.

python make_pilot_scripts.py -p 10 -s -c
python make_pilot_scripts.py -p 29 -s -c

To add new fields/positions this script must be edited by hand
Two changes are required:
make_scripts()
needs to be edited to put in the apporiate pointing source.
Consult the catalog or check K-band-points.pdf
make_catalog()
needs to be edited to put in a bright point in the field
that will be used for the on-off check. I use the brightest
spot in the Bolocam Galactic Plane Survey image. 

In both cases, just copy the existing format for the entries.

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
        dir_name = "pilot_"+str(int(position))+"_dir"
        reg_name = str(int(position))+"_"
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
    pointing_temp = Template(pointing_str)
    onoff_temp = Template(onoff_str)
        
    if position == 10:
        point_source = "1833-2103"
        onoff_source = "L10OnOff"
    elif position == 22:
        point_source = "1743-0350"
        onoff_source = "L22OnOff"
    elif position == 23:
        point_source = "1743-0350"
        onoff_source = "L23OnOff"
    elif position == 24:
        point_source = "1743-0350"
        onoff_source = "L24OnOff"
    elif position == 28:
        point_source = "1751+0939"
        onoff_source = "L28OnOff"
    elif position == 29:
        point_source = "1751+0939"
        onoff_source = "L29OnOff"
    elif position == 30:
        point_source = "1751+0939"
        onoff_source = "L30OnOff"
    elif position == 31:
        point_source = "1751+0939"
        onoff_source = "L31OnOff"
    elif position == 32:
        point_source = "1751+0939"
        onoff_source = "L32OnOff"
    elif position == 39:
        point_source = "1850-0001"
        onoff_source = "L39OnOff"
    elif position == 38:
        point_source = "1850-0001"
        onoff_source = "L38OnOff"
    elif position == 43:
        point_source = "1850-0001"
        onoff_source = "L43OnOff"
    elif position == 45:
        point_source = "1850-0001"
        onoff_source = "L45OnOff"
    elif position == 46:
        point_source = "1850-0001"
        onoff_source = "L46OnOff"
    elif position == 47:
        point_source = "1850-0001"
        onoff_source = "L47OnOff"


    
    #Make a separate peak script
    d = {"pointing_pos":point_source,"onoff_pos":onoff_source,
         "reg_name":reg_name,
         "dir_name":dir_name}
    
    point_out = pointing_temp.substitute(d)
    gg= open(dir_name+"/pointing_L"+reg_name[0:-1]+".py",'w')
    print >>gg,point_out
    gg.close()
    
    point_out = onoff_temp.substitute(d)
    gg= open(dir_name+"/onoff_L"+reg_name[0:-1]+".py",'w')
    print >>gg,point_out
    gg.close()
        
    for i,line in enumerate(all_lines):
        if "Tile" in line:
            name = line.split(' ')[0]
            off = all_lines[i+1].split(' ')[0]
            d = {"point_pos":"PointPos","off_pos":off,
                 "map_pos":name,"reg_name":reg_name,
                 "dir_name":dir_name}
            output = tile_template.substitute(d)
            gg= open(dir_name+"/map"+name+".py",'w')
            print >>gg,output
            gg.close()
            
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
    os.chmod(dir_name,0777)
            
    
def make_catalog(position,dir_name,reg_name):
    """ Make a catalog file describing the centers of all maps. """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    all_patches = []
    fullstring = """# RAMPS source list
coordmode=GALACTIC
head = NAME    GLON      GLAT
"""
    
    #I need to look up these points as the brightest points
    #within each region from Bolocam
    fullstring +=  "L10OnOff    10.1659      -0.3555\n"
    fullstring +=  "L22OnOff    21.8764      +0.0053\n"
    fullstring +=  "L23OnOff    23.4354      -0.1852\n"
    fullstring +=  "L24OnOff    24.3292      +0.1452\n"
    fullstring +=  "L28OnOff    28.1998      -0.0503\n"
    fullstring +=  "L29OnOff    29.9356      -0.0587\n"
    fullstring +=  "L30OnOff    29.9617      -0.0160\n"
    fullstring +=  "L39OnOff    37.8765      -0.3995\n"
    fullstring +=  "L31OnOff    31.4125      +0.3075\n"
    fullstring +=  "L32OnOff    32.0436      +0.0609\n"
    fullstring +=  "L38OnOff    37.7655      -0.2161\n"
    fullstring +=  "L43OnOff    43.1649      +0.0172\n"
    fullstring +=  "L45OnOff    45.4593      +0.0470\n"
    fullstring +=  "L46OnOff    45.4552      +0.0613\n"
    fullstring +=  "L47OnOff    47.0443      +0.2504\n"
    
    #Do some tiles (0.25 x 0.20)
    #Inclue 0.05 degree overlap
    i = 1


    #For historical reasons, the numbering
    #of tiles is a little odd, with
    # 13, 14, 15, 16
    # 09, 10, 11, 12
    # 01, 02, 03, 04
    # 05, 06, 07, 08
    glon_min = position-0.410
    glon_max = position+0.375
    for glat in np.arange(-0.10,0.35,.195):
        for glon in np.arange(glon_max,glon_min,-0.250):
            map_string = "L"+reg_name+"Tile"+str(i).zfill(2)+\
                         " "+str(glon)+" "+str(glat)
            off_string = "L"+reg_name+"TOFF"+str(i).zfill(2)+\
                         " "+str(glon)+" "+str(glat+1.0)
            fullstring = fullstring+map_string+"\n"
            rect = Rectangle((glon-0.13,glat-0.1),0.26,0.208,fill=True, 
                             fc='red', visible=True, alpha=0.4,lw=0)
            ax.plot(glon,glat,'ko')
            ax.text(glon-0.01,glat+0.02,"Tile"+str(i).zfill(2))
            #ax.add_artist(rect)
            #plt.show()                
            all_patches.append(rect)
            fullstring = fullstring+off_string+"\n"
            i += 1
            if i == 5:
                #This used to be a loop to do strips
                #Now it does tiles like the outer loop
                #but doing it this way preserves the
                #same sort of numbering scheme for the pilot
                #survey as a whole
                for glat2 in [-0.245-0.05]:
                    for glon2 in np.arange(glon_max,glon_min,-0.250):
                        map_string = "L"+reg_name+"Tile"+str(i).zfill(2)+\
                                     " "+str(glon2)+" "+str(glat2)
                        off_string = "L"+reg_name+"TOff"+str(i).zfill(2)+\
                                     " "+str(glon2)+" "+str(glat2+1.0)
                        fullstring = fullstring+map_string+"\n"
                        rect = Rectangle((glon2-0.13,glat2-0.1),0.26,0.208,fill=True, 
                             fc='red', visible=True, alpha=0.4,lw=0)
                        all_patches.append(rect)
                        ax.plot(glon2,glat2,'ko')
                        ax.text(glon2-0.01,glat2+0.02,"Tile"+str(i).zfill(2))
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
    ax.set_xticks(np.arange(position-0.5,position+0.7,0.5))
    plt.grid()
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
#Nov   20, 2015 (JBF) Increased size of tiles for better overlap
#Oct    5, 2015 (JBF) Comment out blanking values (no longer needed)
#April 15, 2015 (JBF) Set blanking values manually to fix a VEGAS problem 
#March 10, 2014 (JBF) Initial Version
Catalog("/home/astro-util/projects/13B312/ramps/${dir_name}/Pilot${reg_name}Sources.cat")

##########  <<<< Do only one of these!!! >>>>> #########
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
##########  <<<< Do only one of these!!! >>>>> #########
Configure(vegas_config)
#ScanCordValues = {'blanking,1' : 0.006,
#                  'blanking,2' : 0.006}
#SetValues('ScanCoordinator', ScanCordValues)
#SetValues('ScanCoordinator', {'state':'prepare'})

execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

off = "${off_pos}" # define a map reference location, with no emission

Slew(off)
Balance()
Track(off, None, 30.0, "1")
mapTarget='${map_pos}'                # The map center is often not the peak location
RALongMap( mapTarget, 
	   Offset("Galactic", 0.26, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.208), 
	   Offset("Galactic", 0.0, 0.008), 
	   125.0, "1")
Track( off, None, 30.0, "1")
"""
     
ts = """
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#Oct    5, 2015 (JBF) Comment out blanking values (no longer needed)
#April 15, 2015 (JBF) Set blanking values manually to fix a VEGAS problem 
#March 10, 2014 (JBF) Initial Version
Catalog("/home/astro-util/projects/13B312/ramps/${dir_name}/Pilot${reg_name}Sources.cat")

##########  <<<< Do only one of these!!! >>>>> #########
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
##########  <<<< Do only one of these!!! >>>>> #########
Configure(vegas_config)
#ScanCordValues = {'blanking,1' : 0.006,
#                  'blanking,2' : 0.006}
#SetValues('ScanCoordinator', ScanCordValues)
#SetValues('ScanCoordinator', {'state':'prepare'})
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

off = "${off_pos}" # define a map reference location, with no emission

Slew(off)
Balance()
Track(off, None, 30.0, "1")
mapTarget='${map_pos}'                # The map center is often not the peak location
RALongMap( mapTarget, 
	   Offset("Galactic", 1.0, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.058), 
	   Offset("Galactic", 0.0, 0.008), 
	   480.0, "1")
Track( off, None, 30.0, "1")
"""

onoff_str = """
Catalog("/home/astro-util/projects/13B312/ramps/${dir_name}/Pilot${reg_name}Sources.cat")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
Configure(vegas_config)
#ScanCordValues = {'blanking,1' : 0.006,
#                  'blanking,2' : 0.006}
#SetValues('ScanCoordinator', ScanCordValues)
#SetValues('ScanCoordinator', {'state':'prepare'})
Slew("${onoff_pos}")
Balance()
OnOff("${onoff_pos}",Offset("Galactic",0.0,1.0),30,"1")
"""


pointing_str = """
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#March 10, 2014 (JBF) Initial Version

#Catalog("/home/astro-util/projects/13B312/ramps/${dir_name}/Pilot${reg_name}Sources.cat")
Catalog(kband_pointing)

#Use pre-defined target
AutoPeakFocus("${pointing_pos}")
#Look near the peak
#AutoPeakFocus(location='${onoff_pos}')
"""

if __name__ == '__main__':
    main()

