# jdmdata
This module and script analyze human-participants data collected during a series of experiments.
The experiments study how decisions made with tradeoff diagrams as a support tool vary in quality as the 
decision at hand becomes more complex (i.e. more levers, more objectives). Each data point has had the 
participants' name removed.

See the "requirements.txt" file for the python packages and versions needed to run this script. 

To set up the script, save "jdmtools.py" and "__init__.py" in a folder named "jdmtools". 
Save the "JDM.py" in the folder containing the jdmtools folder. Change the directory in the script
to the directory in which you have saved and unzipped the "jdmdata" file downloaded from this 
website.

This script draws on the Project Platypus python library for multiobjective optimization, accessed
February 5, 2021. To run the script, one line in the Rhodium module that draws on sklearn.six must
be modified to draw the same function from the "six" package listed in the requirements file.

This set of analytical tools was developed with Spyder in an Anaconda virtual environment.



