
Catalog("/home/astro-util/projects/13B312/ramps/pilot_10p5_dir/Pilot_10p5_Sources.cat")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
Configure(vegas_config)
Slew("Field10p5OnOff")
Balance()
OnOff("Field10p5OnOff",Offset("Galactic",0.0,1.0),30,"1")

