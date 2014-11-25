#!/usr/bin/env python
# encoding: utf-8
"""
Make a catalog and scripts for RAMPS to
fill in the gaps left by old versions of
the mapping software.

In the RAMPS pilot survey until 2014/11/21
the large 1-degree fields were not overlapping
with each other. This means that fields L10,
L28, L30, and L38 need some extra observing
on the edges so that they will overlap with 
other fields.

-p : Position    -- Field to create scripts for
                    (10 for L10, 28 for L28, etc.)
-h : Help        -- Display this help 
"""
import sys,os,getopt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from string import Template

def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:],"p:h")
    except getopt.GetoptError,err:
        print(str(err))
        print(__doc__)
        sys.exit(2)
    position = None
    dir_name = None
    for o,a in opts:
        if o == "-p":
            position = a
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
        dir_name = "fillin_dir"
        reg_name = str(int(position))+"_"
        print("Using "+dir_name)
    else:
        reg_name=dir_name
    try:
        os.mkdir(dir_name)
    except OSError:
        pass
    
    make_catalog(float(position),dir_name,reg_name)
    make_scripts(float(position),dir_name,reg_name)
    
def make_scripts(position,dir_name,reg_name):
    """Make scripts for the fill-in."""
    ff = open(dir_name+'/Fillin'+reg_name+'Sources.cat','r')
    all_lines = ff.readlines()
    strip_template = Template(ts)

    for i,line in enumerate(all_lines):
        if "Fillin" in line:
            name = line.split(' ')[0]
            off = all_lines[i+1].split(' ')[0]
            d = {"point_pos":"PointPos","off_pos":off,
                 "map_pos":name,"reg_name":reg_name,
                 "dir_name":dir_name}
            output = strip_template.substitute(d)
            gg= open(dir_name+"/map"+name+".py",'w')
            print >>gg,output
            gg.close()
    
    
    
def make_catalog(position,dir_name,reg_name):
    """ Make a catalog file for the fill-ins"""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    all_patches = []
    fullstring = """# RAMPS source list
coordmode=GALACTIC
head = NAME    GLON      GLAT
"""
    glat = 0.05
    glon = position + 0.5
    map_string = "L"+reg_name+"Fillin_L"+\
                 " "+str(glon)+" "+str(glat)
    off_string = "L"+reg_name+"FOFF_L"+\
                 " "+str(glon)+" "+str(glat+1.0)
    fullstring = fullstring+map_string+"\n"
    fullstring = fullstring+off_string+"\n"
    
    glat = 0.05
    glon = position - 0.5
    map_string = "L"+reg_name+"Fillin_R"+\
                 " "+str(glon)+" "+str(glat)
    off_string = "L"+reg_name+"FOFF_R"+\
                 " "+str(glon)+" "+str(glat+1.0)
    fullstring = fullstring+map_string+"\n"
    fullstring = fullstring+off_string+"\n"
    
    fullstring = fullstring[0:-1]
    fff = open(dir_name+"/Fillin"+reg_name+"Sources.cat",'w')
    print >>fff,fullstring
    fff.close()
    
catalog_template_1 = '''#RAMPS tile/stripe list
head = name coordmode GLON GLAT velocity
'''     
catalog_template_2 ='''
'''
ts = """
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#Nov   24, 2015 (JBF) This is a special fill-in script to cover edges of fields
#Nov   20, 2015 (JBF) Increased size of tiles for better overlap
#Oct    5, 2015 (JBF) Comment out blanking values (no longer needed)
#April 15, 2015 (JBF) Set blanking values manually to fix a VEGAS problem 
#March 10, 2014 (JBF) Initial Version
Catalog("/home/astro-util/projects/13B312/ramps/${dir_name}/Fillin${reg_name}Sources.cat")

##########  <<<< Do only one of these!!! >>>>> #########
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
##########  <<<< Do only one of these!!! >>>>> #########
Configure(vegas_config)
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

off = "${off_pos}" # define a map reference location, with no emission

Slew(off)
Balance()
Track(off, None, 30.0, "1")
mapTarget='${map_pos}'                # The map center is often not the peak location
DecLatMap( mapTarget, 
	   Offset("Galactic", 0.81, 0.0), # This is a galactic coordinate map
	   Offset("Galactic", 0.0, 0.048), 
	   Offset("Galactic", 0.0, 0.008), 
	   390.0, "1")
Track( off, None, 30.0, "1")
"""

if __name__ == '__main__':
    main()

