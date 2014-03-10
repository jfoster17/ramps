# Astrid script to point near a maser source
# HISTORY
# 10SEP02 GIL do not reconfigure before the pointing obs
# 10AUG?? J?B initial version

execfile("/home/astro-util/projects/11B030/Pilot_Sources.cat")

mySource = "{Pilot_Tiles03}"

AutoPeakFocus(location=mySource, flux=1.5, configure=False)

