# Observing script: MAP of "snake".
#
# Load catalog and configure VEGAS.
Catalog("/home/astro-util/projects/13B312/ramps/ramps_catalog.txt")

# Point and focus before observing map.
# See section 10.2 in observing manual.
# Suggested interval is every 1-2 hours.

#Simple configuration for auto-peak-focus
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_simple.py")
peak_source = "1833-2103"
AutoPeakFocus(location=peak_source, flux=1.5, configure=False)


##########  <<<< Do only one of these!!! >>>>> #########
execfile("/home/astro-util/projects/13B312/ramps/vegas_config.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_simple.py")
##########  <<<< Do only one of these!!! >>>>> #########
Configure(vegas_config)

# For KFPA pipeline, per 10.7.
# Define procedures with scan annotations
# and header values.
execfile("/home/astro-util/projects/TKFPA/kfpaMapInit")

# Recommended On/Off observation toward
# strong spectral source at beginning
# of observations.

# Observe source.
# Use GBT standard mapping mode.
# Incorporate tags/commands for
# KFPA pipeline(?). Ex. in 10.7.
Slew("snake")
Balance()
OnOff("snake-peak",Offset("Galactic", 0.0, 1.0, cosv=False), 30, "1")
#TargetTrack("snake-peak", None, 30.0, "1")     # check spectra
OffTrack("snake-off", None, 30.0, "1")    # get off-source obs.
SetValues("ScanCoordinator",{"scanId":"Map"})
RALongMap("snake",                        # center of map
          Offset("Galactic",0.41,0.0),    # width of map
          Offset("Galactic",0.0,0.16),    # height of map
          Offset("Galactic",0.0,0.008),   # vertical row spacing
          196)                            # seconds per row
OffTrack("snake-off", None, 30.0, "1")
