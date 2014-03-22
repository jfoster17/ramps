
Catalog("/home/astro-util/projects/13B312/ramps/pilot_10_dir/Pilot10_Sources.cat")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
Configure(vegas_config)
Slew("L10OnOff")
Balance()
OnOff("L10OnOff",Offset("Galactic",0.0,1.0),30,"1")

