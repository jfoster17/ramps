#PointFocus for "Snake"

Catalog("/home/astro-util/projects/13B312/ramps/ramps_catalog.txt")
Catalog(kband_pointing)
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_pointing.py")
Configure(vegas_config)
peak_source = "1833-2103"
AutoPeakFocus(peak_source)
#peak_source = "1833-2103"
#AutoPeakFocus(location=peak_source, flux=1.5, configure=False)
