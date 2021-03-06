#Quick OnOff observation of G34.43 peak

Catalog("/home/astro-util/projects/13B312/ramps/ramps_catalog-radec.txt")
execfile("/home/astro-util/projects/13B312/ramps/vegas_config_ramps.py")
#execfile("/home/astro-util/projects/13B312/ramps/vegas_config_kepley.py")
Configure(vegas_config)
ScanCordValues = {'blanking,1' : 0.006,
                  'blanking,2' : 0.006}
SetValues('ScanCoordinator', ScanCordValues)
SetValues('ScanCoordinator', {'state':'prepare'})
Slew("g34-peak")
Balance()
OnOff("g34-peak",Offset("Galactic",0.0,1.0),30,"1")
