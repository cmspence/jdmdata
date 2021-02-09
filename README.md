# jdmdata
This module and script analyze human-participants data collected during a series of experiments.
The experiments study how decisions made with tradeoff diagrams as a support tool vary in quality as the 
decision at hand becomes more complex (i.e. more levers, more objectives). Each data point has had the 
participants' name removed.

See the "requirements.txt" file for the python packages and versions needed to run this script. 

This script draws on the Project Platypus python library for multiobjective optimization, accessed
February 5, 2021. To run the script, one line in the Rhodium module that draws on sklearn.six must
be modified to draw the same function from the "six" package listed in the requirements file.

This set of analytical tools was developed with Spyder in an Anaconda virtual environment.

