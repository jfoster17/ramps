
Catalog("/home/astro-util/projects/13B312/ramps/pilot_29p5_dir/Pilot_29p5_Sources.cat")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
Configure(vegas_config)
Slew("Field29p5OnOff")
Balance()
OnOff("Field29p5OnOff",Offset("Galactic",0.0,1.0),30,"1")

