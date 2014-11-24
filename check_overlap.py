import sys,os,getopt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from string import Template

def main():
    check_overlap()

def check_overlap():
    fig = plt.figure()
    ax = fig.add_subplot(111)
    all_patches = []
    
    position = 29.
    dir_name = "pilot_29_dir"
    reg_name = "29_"
    plot_catalog_old(float(position),dir_name,reg_name,ax,fig,all_patches,color='blue')
    position = 30.
    dir_name = "pilot_30_dir"
    reg_name = "30_"
    all_patches = []
    plot_catalog(float(position),dir_name,reg_name,ax,fig,all_patches,color='red')
    fig.savefig("Overlap_Check_old.pdf")


    fig = plt.figure()
    ax = fig.add_subplot(111)
    all_patches = []
    
    position = 29.
    dir_name = "pilot_29_dir"
    reg_name = "29_"
    plot_catalog(float(position),dir_name,reg_name,ax,fig,all_patches,color='blue')
    position = 30.
    dir_name = "pilot_30_dir"
    reg_name = "30_"
    all_patches = []
    plot_catalog(float(position),dir_name,reg_name,ax,fig,all_patches,color='red')


def plot_catalog_old(position,dir_name,reg_name,ax,fig,all_patches,color=None):
    """ Make a catalog file describing the centers of all maps. """
    #Do some tiles (0.25 x 0.20)
    #Inclue 0.05 degree overlap
    i = 1

    glon_min = position-0.375
    glon_max = position+0.375
    for glat in np.arange(-0.05,0.35,.195):
        for glon in np.arange(glon_max,glon_min,-0.245):
            rect = Rectangle((glon-0.125,glat-0.1),0.25,0.20,fill=True, 
                             fc=color, visible=True, alpha=0.4,lw=0)
            ax.plot(glon,glat,'ko')
            ax.text(glon-0.01,glat+0.02,"Tile"+str(i).zfill(2))
            all_patches.append(rect)
            i += 1
            if i == 5:
                for glat2 in [-0.245]:
                    for glon2 in np.arange(glon_max,glon_min,-0.245):
                        rect = Rectangle((glon2-0.125,glat2-0.1),0.25,0.20,fill=True, 
                             fc=color, visible=True, alpha=0.4,lw=0)
                        all_patches.append(rect)
                        ax.plot(glon2,glat2,'ko')
                        ax.text(glon2-0.01,glat2+0.02,"Tile"+str(i).zfill(2))
                        i += 1
    #Rectangle patches are defined from lower-left, not center?
    fillin_width = 0.048
    fillin_height = 0.81
    rect = Rectangle((position-0.5-fillin_width/2.,0.05-fillin_height/2.),fillin_width,fillin_height,fill=True, 
                     fc='green', visible=True, alpha=0.4,lw=0)
    all_patches.append(rect)
    
    rect = Rectangle((position+0.5-fillin_width/2.,0.05-fillin_height/2.),fillin_width,fillin_height,fill=True, 
                     fc='green', visible=True, alpha=0.4,lw=0)
    all_patches.append(rect)
    
    for patch in all_patches:
        ax.add_patch(patch)
    ax.set_xlim(30.6,28.4)
    ax.set_ylim(-0.5,0.5)
    plt.ylabel("GLat (deg)")
    plt.xlabel("GLon (deg)")

def plot_catalog(position,dir_name,reg_name,ax,fig,all_patches,color=None):
    """ Make a catalog file describing the centers of all maps. """
    #Do some tiles (0.25 x 0.20)
    #Inclue 0.05 degree overlap
    i = 1
    glon_min = position-0.410
    glon_max = position+0.375
    for glat in np.arange(-0.05,0.35,.195):
        for glon in np.arange(glon_max,glon_min,-0.250):
            rect = Rectangle((glon-0.13,glat-0.1),0.26,0.208,fill=True, 
                             fc=color, visible=True, alpha=0.4,lw=0)
            ax.plot(glon,glat,'ko')
            ax.text(glon-0.01,glat+0.02,"Tile"+str(i).zfill(2))
            all_patches.append(rect)
            i += 1
            if i == 5:
                for glat2 in [-0.245]:
                    for glon2 in np.arange(glon_max,glon_min,-0.250):
                        rect = Rectangle((glon2-0.13,glat2-0.1),0.26,0.208,fill=True, 
                             fc=color, visible=True, alpha=0.4,lw=0)
                        all_patches.append(rect)
                        ax.plot(glon2,glat2,'ko')
                        ax.text(glon2-0.01,glat2+0.02,"Tile"+str(i).zfill(2))
                        i += 1
    
    for patch in all_patches:
        #print("Adding patch")
        ax.add_patch(patch)
   # rect = Rectangle((0.0120,0),0.1,1000)
    #ax.add_patch(rect)
    ax.set_xlim(30.6,28.4)
    ax.set_ylim(-0.5,0.5)
    plt.ylabel("GLat (deg)")
    plt.xlabel("GLon (deg)")
    fig.savefig("Overlap_Check_new.pdf")
    #plt.show()

if __name__ == '__main__':
    main()
