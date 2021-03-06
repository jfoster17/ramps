# Observing script: MAP of "IRDC43/G34.43".

# Load catalog and configure VEGAS.
Catalog("/home/astro-util/projects/13B312/ramps/ramps_catalog-radec.txt")

# Point and focus before observing map.
# See section 10.2 in observing manual.
# Suggested interval is every 1-2 hours.

#Simple configuration for auto-peak-focus
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_simple.py")
Configure(vegas_config)
peak_source = "1845+0953"
AutoPeakFocus(location=peak_source, flux=1.5, configure=False)


##########  <<<< Do only one of these!!! >>>>> #########
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config.py")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_simple.py")
##########  <<<< Do only one of these!!! >>>>> #########
Configure(vegas_config)

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
Slew("G43")
Balance()
OnOff("G43-peak",Offset("Galactic", 0.0, 1.0, cosv=False), 30, "1")
#TargetTrack("G43-peak", None, 30.0, "1")     # check spectra
OffTrack("G43-OFF", None, 30.0, "1")    # get off-source obs.
SetValues("ScanCoordinator",{"scanId":"Map"})
DecLatMap("G43",                        # center of map
          Offset("J2000",.12,0.0, cosv = True),      # width of map
          Offset("J2000",0.0,.30, cosv = True),      # height of map
          Offset("J2000",0.008,0.0, cosv = True),    # vertical row spacing
          293.)                          # seconds per row
OffTrack("G43-off", None, 30.0, "1")
