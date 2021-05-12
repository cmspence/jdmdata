# jdmdata
This module and script analyze human-participants data collected during a series of experiments.
The experiments study how decisions made with tradeoff diagrams as a support tool vary in quality as the 
decision at hand becomes more complex (i.e. more levers, more objectives). Each data point has had the 
participants' name removed.

This set of analytical tools was developed with Python 3.8.3, specifically with Spyder in an Anaconda
virtual environment. See the "requirements.txt" file for the Python packages and versions needed to run
this tool set.

## Setup
This tool set draws on the Project Platypus Python library for multiobjective optimization (accessed
February 5, 2021). In order to function properly, please follow the step 1 and 2 instructions under the
'Setting up Rhodium' header found here:
https://github.com/Project-Platypus/Rhodium/blob/master/INSTALL.md. Once Rhodium has been installed, you
will need to find and open the included "*/rhodium/classification.py". Within "classification.py", comment
out the line that reads "from sklearn.externals.six import StringIO", and add a line that reads
"from six import StringIO". Save and close the file.

From within where jdmdata was downloaded, create a folder called "jdmtools". Move "jdmtools.py" and
"__init__.py" into the new directory. Uncompress the "download-3.zip" file. Open the "JDM.py" script and
change the directory in line 21 to point to the uncompressed "download-3" folder. On line 8, add "import os"
and on line 9, set the working directory to the folder in which "JDM.py" is stored.

## Running
Run the "JDM.py" script. 

## Output
The script will produce several output files, all of which will save in the working directory.
First, the script will produce twelve Python pickle-format files (.pkl) storing the hierarchically
structured data on participants' demonstrated preferences and Pareto dominance. 

The script will also create several pdf- and png-formatted figures. 

fig1: Example tradeoff diagram with reference Pareto set and example points.

fig5: Violin plots comparing contextual groups' Pareto scores at each number of objectives. Upper plot:
  two objectives. Lower plot: three objectives.
  
fig6: Three vertically-stacked Violin plots comparing contextual groups' Preference scores at each number of 
  objectives. Plots each display the comparison at one number of levers, moving from one lever to three levers
  from top to bottom.

fig7: Violin plot comparing evonomic benefits/A achieved at one-objective decision stage among different
  numbers of levers and between problem contextual framing groups.
  
fig8: Scatterplot on a tradeoff diagramcomparing strategies with "Other Objectives" flag in one-objective 
  stage with same participants' 2-objective strategies in 2-D space.
  
In the Python workspace, the script will produce several summary statistics. 
First, the script will store the results of the two-sided Kolmogorov-Smirnov test on the distributions of 
Pareto scores of the strategies at each number of levers compared between the two problem framints as 
"KS_scores_1obj." The first row of this array contains the results at the one-lever stage, the second row
the results of the test at the two-lever stage, and the third row the results at the three-lever stage.
The script will also calculate the percentage of strategies within each response code under the system dynamics
threshold and near the system dynamics threshold as as "percent_near_[code]" and "percent_under_[code]."

