#MAP of "IRDC43/G34.43"

Catalog("/home/astro-util/projects/13B312/ramps/ramps_catalog-radec.txt")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
Configure(vegas_config)
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")
Slew("g34")
Balance()
OffTrack("g34-off", None, 30.0, "1")    # get off-source obs.
SetValues("ScanCoordinator",{"scanId":"Map"})
DecLatMap("g34",                        # center of map
          Offset("J2000",.12,0.0, cosv = True),      # width of map
          Offset("J2000",0.0,.30, cosv = True),      # height of map
          Offset("J2000",0.008,0.0, cosv = True),    # column spacing
          293)                          # seconds per col
OffTrack("g34-off", None, 30.0, "1")
