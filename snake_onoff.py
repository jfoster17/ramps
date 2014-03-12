#Quick OnOff observation of Snake peak

Catalog("/home/astro-util/projects/13B312/ramps/ramps_catalog.txt")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
Configure(vegas_config)
Slew("snake-peak")
Balance()
OnOff("snake-peak","snake-off",30,"1")