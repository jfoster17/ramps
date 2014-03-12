#PointFocus for "IRDC43/G34.43"

Catalog("/home/astro-util/projects/13B312/ramps/ramps_catalog-radec.txt")
Catalog(kband_pointing)
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_pointing.py")
Configure(vegas_config)
peak_source = "1751+0939"
AutoPeakFocus(peak_source)