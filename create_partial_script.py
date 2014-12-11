#!/usr/bin/env python
# encoding: utf-8
"""
Create a new observing script to finish a partial RAMPS map

If a mapping script crashes or the end of the observing sesssion 
prevents completion of an individual tile or strip, run this 
program to generate a new self-contained script which can be 
run to finish a map. To make sure that the map always has
calibration/OFF data, this partial script will always do an
OFF before beginning (and another at the end)

When calculating the starting scan, ignore the first OFF scan
Thus, if you are making a map:
37 = OFF
38 = MAP
39 = MAP
41 -- map aborts during this scan
you want -s 3
This will start on the third _map_ scan.

Specifying s = 1 generates a warning error message
since it is exactly the same thing as running the 
original script again.

*** WARNING ***
By default this program only makes tiles for the new-style
method of filling our region. If you are completing the L10
field the program assumes you will be using the old-style 
method of filling a region. If you want to override this for
any reason, use -o.

Examples:
python create_partial_script.py -f L10_Tile14 -s 3
python create_partial_script.py -f L31_Tile04 -s 3


-o : OldStyle    -- Do the old-style (L10/L30) tiles+strips
-f : Field       -- Name of the field
-s : StartScan   -- Number of scan to start on
-h : Help        -- Display this help 
"""
import sys,os,getopt
from string import Template
import numpy as np

def main():
    field_name = None
    start_scan = None
    old_style = False
    try:
        opts,args = getopt.getopt(sys.argv[1:],"f:s:oh")
    except getopt.GetoptError,err:
        print(str(err))
        print(__doc__)
        sys.exit(2)
    for o,a in opts:
        if o == "-f":
            field_name = a
        elif o == "-s":
            start_scan = a
        elif o == "-o":
            old_style = True
        elif o == "-h":
            print(__doc__)
            sys.exit(1)
        else:
            assert False, "unhandled option"
            print(__doc__)
            sys.exit(2)
    if not field_name:
        print("")
        print(">>> Must specify a central position <<<")
        print(__doc__)
        sys.exit(2)
    if not start_scan:
        print("")
        print(">>> Must specify a starting scan <<<")
        print(__doc__)
        sys.exit(2)
        
    if int(start_scan) == 1:
        print("")
        print(">>> You specified -s 1 <<<")
        print(">>> That is the same as the original script <<<")
        print(__doc__)
        sys.exit(2)
    
    if ("L10" in field_name) or ("L30" in field_name):
        print("Using the OLD style of tiles and strips.")
        old_style = True
    if not old_style:
        print("Using the NEW style of just tiles.")
        
    make_cat(field_name,start_scan,old_style=old_style)
    make_script(field_name,start_scan)

def make_cat(field_name,start_scan,old_style=False):
    do_tile = False
    do_strip = False
    big_region = field_name[1:3]
    reg_name = field_name[1:3]
    print(big_region)
    little_region = field_name[-2:]
    print(little_region)
    if "Tile" in field_name:
        do_tile=True
    elif "Strip" in field_name:
        do_strip=True
    else:
        print(">>> Error: Field name does not seem to conform.")
    
    offset = 0.008*(int(start_scan)-1)
    
    position = int(big_region)
    i = 1
    fullstring = """# RAMPS source list
coordmode=GALACTIC
head = NAME    GLON      GLAT
"""
    glon_min = position-0.390
    glon_max = position+0.390
    for glat in np.arange(-0.05,0.35,.195):
        for glon in np.arange(glon_max,glon_min,-0.250):
            if i == int(little_region):
                offglat = glat-offset
                map_string = "L"+reg_name+"Tile"+str(i).zfill(2)+\
                             "-extra"+" "+str(glon)+" "+str(offglat)
                off_string = "L"+reg_name+"TOFF"+str(i).zfill(2)+\
                             "-extra"+" "+str(glon)+" "+str(offglat+1.0)
                fullstring = fullstring+map_string+"\n"
                fullstring = fullstring+off_string+"\n"
                
            i+=1
            if i == 5:
                if old_style:
                    #Do some Strips 1 degree x 0.058 degree (7 strips)
                    #Offset would be -0.058 for best practice. Inclue 0.05 degree overlap
                    for glat2 in np.arange(0,-0.41,-0.053):
                        for glon2 in [position]:
                            if i == int(little_region):
                                offglat = glat2-offset
                                map_string = "L"+reg_name+"Strip"+str(i).zfill(2)+\
                                            "-extra"+" "+str(glon2)+" "+str(offglat)
                                off_string = "L"+reg_name+"StOff-extra"+str(i).zfill(2)+\
                                            "-extra"+" "+str(glon2)+" "+str(offglat+1.0)
                                fullstring = fullstring+map_string+"\n"
                                fullstring = fullstring+off_string+"\n"

                            i += 1
                else:
                    #Just do tiles
                    for glat2 in [-0.245-0.05]:
                        for glon2 in np.arange(glon_max,glon_min,-0.250):
                            if i == int(little_region):
                                offglat = glat2-offset
                            
                                map_string = "L"+reg_name+"Tile"+str(i).zfill(2)+\
                                         " "+str(glon2)+" "+str(glat2)
                                off_string = "L"+reg_name+"TOff-extra"+str(i).zfill(2)+\
                                         " "+str(glon2)+" "+str(glat2+1.0)
                                fullstring = fullstring+map_string+"\n"
                                fullstring = fullstring+off_string+"\n"
                            i += 1
    fullstring = fullstring[0:-1]
    fff = open("extra/PilotL"+reg_name+"Sources-extra.cat",'w')
    print >>fff,fullstring
    fff.close()
    


def make_script(field_name,start_scan):
    reg_name = field_name[0:3]
    ff = open('extra/Pilot'+reg_name+'Sources-extra.cat','r')
    all_lines = ff.readlines()
    tile_template = Template(tt)
    strip_template = Template(ts)
    dir_name = 'extra'
    
    if "Tile" in field_name:
        do_tile=True
        glat_height = 0.208
    elif "Strip" in field_name:
        do_strip=True
        glat_height = 0.058
        
    glat_height = glat_height-0.008*(int(start_scan)-1)
    
    for i,line in enumerate(all_lines):
        if "Tile" in line:
            name = line.split(' ')[0]
            off = all_lines[i+1].split(' ')[0]
            d = {"point_pos":"PointPos","off_pos":off,
                 "map_pos":name,"reg_name":reg_name,
                 "dir_name":dir_name,"glat_height":glat_height}
            output = tile_template.substitute(d)
            gg= open(dir_name+"/map"+name+".py",'w')
            print >>gg,output
            gg.close()
            
        if "Strip" in line:
            name = line.split(' ')[0]
            off = all_lines[i+1].split(' ')[0]
            d = {"point_pos":"PointPos","off_pos":off,
                 "map_pos":name,"reg_name":reg_name,
                 "dir_name":dir_name,"glat_height":glat_height}
            output = strip_template.substitute(d)
            gg= open(dir_name+"/map"+name+".py",'w')
            print >>gg,output
            gg.close()
    
    
catalog_template_1 = '''#RAMPS tile/stripe list
head = name coordmode GLON GLAT velocity
'''     
catalog_template_2 ='''
'''

tt = """
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY
#April 15, 2015 (JBF) Set blanking values manually to fix a VEGAS problem 
#March 10, 2014 (JBF) Initial Version
Catalog("/home/astro-util/projects/13B312/ramps/${dir_name}/Pilot${reg_name}Sources-extra.cat")

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
	   Offset("Galactic", 0.0, ${glat_height}), 
	   Offset("Galactic", 0.0, 0.008), 
	   125.0, "1")
Track( off, None, 30.0, "1")
"""
 
ts = """
#RAMPS Astrid script using the KFPA/VEGAS
#HISTORY 
#April 15, 2015 (JBF) Set blanking values manually to fix a VEGAS problem 
#March 10, 2014 (JBF) Initial Version
Catalog("/home/astro-util/projects/13B312/ramps/${dir_name}/Pilot${reg_name}Sources-extra.cat")

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
	   Offset("Galactic", 0.0, ${glat_height}), 
	   Offset("Galactic", 0.0, 0.008), 
	   480.0, "1")
Track( off, None, 30.0, "1")
"""

if __name__ == '__main__':
    main()
    
