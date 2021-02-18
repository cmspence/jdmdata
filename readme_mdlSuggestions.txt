!!*Note that anything placed with "!!* *!!" is a comment with an idea of suggestion for consideration.*!!

# jdmdata
This module and script analyze human-participants data collected during a series of experiments.
The experiments study how decisions made with tradeoff diagrams as a support tool vary in quality as the
decision at hand becomes more complex (i.e. more levers, more objectives). Each data point has had the
participants' name removed.

This set of analytical tools was developed with Python 3.!!*x*!!, specifically with Spyder in an Anaconda
virtual environment. See the "requirements.txt" file for the Python packages and versions needed to run
this tool set.

## Setup
This tool set draws on the Project Platypus Python library for multiobjective optimization (accessed
February 5, 2021). In order to function properly, please follow the step 1 and 2 instructions under the
'Setting up Rhodium' header found here:
https://github.com/Project-Platypus/Rhodium/blob/master/INSTALL.md. Once Rhodium has been installed, you
will need to find and open the included "*/rhodium/classification.py". Within "classification.py", comment
out the line that reads "from sklearn.externals.six import StringIO", and add a line that reads
"from six import StringIO". Save an close the file.

From within where jdmdata was downloaded, create a folder called "jdmtools". Move "jdmtools.py" and
"__init__.py" into the new directory. Uncompress the "download-3.zip" file. Open the "JDM.py" script and
change the directory in line 21 to point to the uncompressed "download-3" folder. On line 8, add "import os"
and on line 9, set the working directory to the folder in which "JDM.py" is stored.

!!*I am not really happy with the above pharagraph - mostly because it is a lot of easy stuff which we can do
to prevent a user from making mistakes. For example, we could already have the "jdmtools" folder created and
"jdmtool.py" and "__init__.py" saved within on Github. I would even argue to would not be that difficult to
create "setup.py" and "LICENSE.txt" files to turn it into a proper package. As a package, it would negate the
need to set the working directory. Thoughts?*!!

## Running
Run the "JDM.py" script.

## Output
!!*Coming Soon*!!
