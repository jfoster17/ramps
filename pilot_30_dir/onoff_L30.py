
Catalog("/home/astro-util/projects/13B312/ramps/pilot_30_dir/Pilot30_Sources.cat")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps_adv.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
Configure(vegas_config)
ScanCordValues = {'blanking,1' : 0.006,
                  'blanking,2' : 0.006}
SetValues('ScanCoordinator', ScanCordValues)
SetValues('ScanCoordinator', {'state':'prepare'})
Slew("L30OnOff")
Balance()
OnOff("L30OnOff",Offset("Galactic",0.0,1.0),30,"1")

