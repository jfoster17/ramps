# Observing script: MAP of "snake".
#
# Load catalog and configure VEGAS.
c = Catalog("/home/astro-util/projects/XXXX/ramps_catalog.txt")
execfile("/home/astro-util/projects/XXXX/vegas_config.py")
Configure("vegas_config")

# For KFPA pipeline, per 10.7.
# Define procedures with scan annotations
# and header values.
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

# Point and focus before observing map.
# See section 10.2 in observing manual.
# Suggested interval is every 1-2 hours.

# Recommended On/Off observation toward
# strong spectral source at beginning
# of observations.

# Observe source.
# Use GBT standard mapping mode.
# Incorporate tags/commands for
# KFPA pipeline(?). Ex. in 10.7.
Slew("snake")
Balance()
TargetTrack("snake", None, 30.0, "1")     # check spectra
OffTrack("snake-off", None, 30.0, "1")    # get off-source obs.
SetValues("ScanCoordinator",{"scanId":"Map"})
RALongMap("snake",                        # center of map
          Offset("Galactic",0.41,0.0),    # width of map
          Offset("Galactic",0.0,0.16),    # height of map
          Offset("Galactic",0.0,0.008),   # vertical row spacing
          196)                            # seconds per row
OffTrack("snake-off", None, 30.0, "1")
