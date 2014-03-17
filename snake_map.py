#MAP of "Snake"

Catalog("/home/astro-util/projects/13B312/ramps/ramps_catalog.txt")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
Configure(vegas_config)
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")
Slew("snake")
Balance()
Track("snake-off", None, 30.0, "1")    # get off-source obs.
#SetValues("ScanCoordinator",{"scanId":"Map"})
RALongMap("snake",                        # center of map
          Offset("Galactic",0.41,0.0),    # width of map
          Offset("Galactic",0.0,0.16),    # height of map
          Offset("Galactic",0.0,0.008),   # vertical row spacing
          196)                            # seconds per row
OffTrack("snake-off", None, 30.0, "1")

