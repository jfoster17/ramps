
Catalog("/home/astro-util/projects/13B312/ramps/pilot_39_dir/Pilot39_Sources.cat")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
Configure(vegas_config)
Slew("L39OnOff")
Balance()
OnOff("L39OnOff",Offset("Galactic",0.0,1.0),30,"1")

