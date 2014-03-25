#!/usr/bin/env python
# encoding: utf-8
"""
A work-around/add-on for the GBT pipeline to work with RAMPS data
Current problems with the pipeline:

Problem:  Cannot specify beam/polarization/windows with VEGAS 
Solution: Generate a script to run the pipeline separately on each of 
          the VEGAS banks

Problem:  mapDefault.py does not work well in galactic coordinates, 
          fails on big maps and has some wrong hard-coded header info
Solution: Run mapRAMPS.py instead, which takes care of these problems

Example:
python make_reduction_commands.py -i SNAKE-MAP.raw.vegas -m 36:56 -r 35,37 -w 8:10 -s 1:2 -b H -f "snake_scan" -x 11.148 -y "-0.104" -c 0.41 -d 0.16

"""

import sys,os,getopt
from string import Template

def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:],"i:m:r:w:s:b:f:x:y:c:d:")
    except getopt.GetoptError,err:
        print(str(err))
        print(__doc__)
        sys.exit(2)
    for o,a in opts:
        if o == "-i":
            inputfile = a
        elif o == "-m":
            maps = a
        elif o == "-r":
            refs = a
        elif o == "-w":
            windows = a
            window_list = parse_range(a)
        elif o == "-s":
            central_windows = a
            central_window_list = parse_range(a)
        elif o == "-b":
            exclude_banks = a.split(',')
        elif o == "-f":
            base = a
        elif o == "-x":
            xcen = a
        elif o == "-y":
            ycen = a
        elif o == "-c":
            width = str(int(float(a)/0.0016667))
        elif o == "-d":
            height = str(int(float(a)/0.0016667))
        
        #elif o == "-h":
        #    print(__doc__)
        #    sys.exit(1)
        else:
            assert False, "unhandled option"
            print(__doc__)
            sys.exit(2)
    output_pipeline_commands(inputfile,maps,refs,windows,central_windows,exclude_banks)
    feed_list = ["A","B","C","D","F","G","H"]
    bank_feed = {"H":6, "C":4, "G":2, "F":0, "D":5, "A":1, "B":3, "E":0}
    
    for window in window_list:
        files = []
        for feed in feed_list:
            if feed not in exclude_banks:
                feed_num = bank_feed[feed]
                files.append(output_do_window(base,maps,window,feed_num))
        make_map(files,xcen,ycen,width,height)
        print("\n")
        
    for window in central_window_list:
        files = []
        feed_num = 0
        files.append(output_do_window(base,maps,window,feed_num))
        make_map(files,xcen,ycen,width,height)
        print("\n")
        
        
def make_map(files,xcen,ycen,width,height):
    command_string = "doImage /home/gbtpipeline/release/contrib/dbcon.py 4363 "
    for file in files:
        command_string = command_string+file+" "
    print(command_string)
    print("""doImage /lustre/pipeline/scratch/jfoster/scripts/ramps/mapRAMPS.py 4363 1 """+xcen+" "+ycen+" "+width+" "+height)
    print("""doImage /home/gbtpipeline/release/contrib/clear_AIPS_catalog.py 4363""")
        
        
def output_do_window(base,maps,window,feed_num):
    """
    Output commands necessary to make a map out of a window
    
    Assume we want to use all polarizations and all feeds not excluded
    
    Assume scans are grouped with ":" ONLY. Dangerous assumption

    """
    command_string = """idlToSdfits -l -o ${base}_window${window}_feed${feed}_pol${pol}.sdf ${base}_window${window}_feed${feed}_pol${pol}.fits"""
    command_template = Template(command_string)
    file_string = """${base}_window${window}_feed${feed}_pol${pol}.sdf"""
    file_template = Template(file_string)
    
    scans = maps.split(":")
    base = base+"_"+scans[0]+"_"+scans[1]
    for pol in [0,1]:
        d = {"base":base, "window":window, "feed":feed_num, "pol":pol}
        output = command_template.substitute(d)
        print(output)
        return(file_template.substitute(d))
    
def output_pipeline_commands(inputfile,maps,refs,windows,central_windows,exclude_banks):
    """
    We assume a fixed order for the VEGAS banks
    
    Bank  Feed  Windows
    ----  ----  -------
     H      6   0,6,8,9,10,11,12,13
     C      4   "
     G      2   "
     F      0   "
     D      5   "
     A      1   "
     B      3   "
     E      0   1,2,3,4,5,7
    
    windows = Banks~E
    central_windows = BankE
    """
    
    command_string = """gbtpipeline -i  ${input}/${input}.${bank}.fits -m ${maps} --refscan ${refs} --imaging-off -w ${windows}"""
    command_template = Template(command_string)
    for bank in ["A","B","C","D","F","G","H"]:
        if bank not in exclude_banks:
            d = {"input":inputfile,"bank":bank,"maps":maps,"refs":refs,"windows":windows}
            output = command_template.substitute(d)
            print(output)
    for bank in ["E"]:
        if bank not in exclude_banks:
            d = {"input":inputfile,"bank":bank,"maps":maps,"refs":refs,"windows":central_windows}
            output = command_template.substitute(d)
            print(output)
    
    
def parse_range(rangelist):
    """Given a range string, produce a list of integers

    Inclusive and exclusive integers are both possible.

    The range string 1:4,6:8,10 becomes 1,2,3,4,6,7,8,10
    The range string 1:4,-2 becomes 1,3,4

    Keywords:
    rangelist -- a range string with inclusive ranges and
                 exclusive integers

    Returns:
    a (list) of integers

    >>> cl = CommandLine()
    >>> cl._parse_range('1:4,6:8,10')
    [1, 2, 3, 4, 6, 7, 8, 10]
    >>> cl._parse_range('1:4,-2')
    [1, 3, 4]

    """

    oklist = set([])
    excludelist = set([])

    rangelist = rangelist.replace(' ', '')
    rangelist = rangelist.split(',')

    # item is single value or range
    for item in rangelist:
        item = item.split(':')

        # change to ints
        try:
            int_item = [int(ii) for ii in item]
        except(ValueError):
            print repr(':'.join(item)), 'not convertable to integer'
            raise

        if 1 == len(int_item):
            # single inclusive or exclusive item
            if int_item[0] < 0:
                excludelist.add(abs(int_item[0]))
            else:
                oklist.add(int_item[0])

        elif 2 == len(int_item):
            # range
            if int_item[0] <= int_item[1]:
                if int_item[0] < 0:
                    print item[0], ',', item[1], 'must start with a '
                    'non-negative number'
                    return []

                if int_item[0] == int_item[1]:
                    thisrange = [int_item[0]]
                else:
                    thisrange = range(int_item[0], int_item[1]+1)

                for ii in thisrange:
                    oklist.add(ii)
            else:
                print item[0], ',', item[1], 'needs to be in increasing '
                'order'
                raise
        else:
            print item, 'has more than 2 values'

    for exitem in excludelist:
        try:
            oklist.remove(exitem)
        except(KeyError):
            oklist = [str(item) for item in oklist]
            print 'ERROR: excluded item', exitem, 'does not exist in '
            'inclusive range'
            raise

    return sorted(list(oklist))
    
    
if __name__ == '__main__':
    main()
    