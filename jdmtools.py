#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 15:21:31 2018

@author: cms793
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 16:05:35 2018

This file is part of analysismodule, a private Python module for analyzing
data from a Penn State-funded human subjects experiment.

@author: cms793
"""

import os
import math
from scipy.spatial import distance
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d
from matplotlib.text import Annotation
from scipy.optimize import brentq as root
from scipy.stats import linregress
from scipy.stats import ks_2samp
import matplotlib.animation as animation
import seaborn as sns
from rhodium import *
## Make a class for each condition
class Condition(object):
    ''' A Condition is an organized data structure containing each of the nine 
    decisions, which contains the lever adjusting events and timestamps,
    final choice of lever settings, and strategy text for each subject. 
    Independent of the decision, the Condition object also contains the comprehension
    question answers for each participant.'''
    
    def __init__(self, folders):
        self.folders = folders
        
    def setup(self):
        
        comprehension = list()
        intro = list()
        ans_exit = list()

        # Initialize dictionaries
        obj1_lev1_events = list()
        obj1_lev1_strategy = list()
        obj1_lev1_test = list()
                 
        obj1_lev2_events = list()
        obj1_lev2_strategy = list()
        obj1_lev2_test = list()
                 
        obj1_lev3_events = list()
        obj1_lev3_strategy = list()
        obj1_lev3_test = list()
                 
        obj2_lev1_events = list()
        obj2_lev1_strategy = list()
        obj2_lev1_test = list()
                 
        obj2_lev2_events = list()
        obj2_lev2_strategy = list()
        obj2_lev2_test = list()
        
        obj2_lev3_events = list()
        obj2_lev3_strategy = list()
        obj2_lev3_test = list()
        
        obj3_lev1_events = list()
        obj3_lev1_strategy = list()
        obj3_lev1_test = list()
        
        obj3_lev2_events = list()
        obj3_lev2_strategy = list()
        obj3_lev2_test = list()
        
        obj3_lev3_events = list()
        obj3_lev3_strategy = list()
        obj3_lev3_test = list()
        
        # Hierarchicalize QC
        QC = pd.read_csv(('/Users/caitl/Documents/SCRiM/JDM/finalcodes.csv'))
        QC_ID = QC['ID']
        rowcount = 0
        QCs = dict()
        
        class Response(object):
            def __init__(self, Motivation, Confidence, ProblemInterpretation, Preference, Issues):
                self.Motivation = Motivation
                self.Confidence = Confidence
                self.ProblemInterpretation = ProblemInterpretation
                self.Preference = Preference
                self.Issues = Issues
                
        
        class Level(object):
            def __init__(self, Qa, Qb):
                '''Qa and Qb are Response objects'''
                self.Qa = Qa
                self.Qb = Qb
        
        class Participant(object):
            ''' A Participant is a tree-like data structure storing qualitative
            codes related to as ingle particpant at each decision stage and 
            open-response question.'''
            
            def __init__(self, D1L1, D1L2, D1L3, D2L1, D2L2, D2L3, D3L1, D3L2, D3L3):
                
                self.D1L1 = D1L1
                self.D1L2 = D1L2
                self.D1L3 = D1L3
                
                self.D2L1 = D2L1
                self.D2L2 = D2L2
                self.D2L3 = D2L3
                
                self.D3L1 = D3L1
                self.D3L2 = D3L2
                self.D3L3 = D3L3
                
        QCs = dict()
        
        while rowcount < len(QC_ID):
            if QC['ID'][rowcount] != 'NaN':
                name_QC = (str(QC['ID'][rowcount]) + str(QC['Unnamed: 1'][rowcount]))
                
                index = rowcount
                Qa = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                index = rowcount + 1
                Qb = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                D1L1 = Level(Qa, Qb)
                
                index = rowcount + 2
                Qa = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                index = rowcount + 3
                Qb = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                D1L2 = Level(Qa, Qb)
                
                index = rowcount + 4
                Qa = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                index = rowcount + 5
                Qb = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                D1L3 = Level(Qa, Qb)
                
                index = rowcount + 6
                Qa = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                index = rowcount + 7
                Qb = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                D2L1 = Level(Qa, Qb)
                
                index = rowcount + 8
                Qa = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                index = rowcount + 9
                Qb = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                D2L2 = Level(Qa, Qb)
                
                index = rowcount + 10
                Qa = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                index = rowcount + 11
                Qb = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                D2L3 = Level(Qa, Qb)
                
                index = rowcount + 12
                Qa = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                index = rowcount + 13
                Qb = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                D3L1 = Level(Qa, Qb)
                
                index = rowcount + 14
                Qa = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                index = rowcount + 15
                Qb = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                D3L2 = Level(Qa, Qb)
                
                index = rowcount + 16
                Qa = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                index = rowcount + 17
                Qb = Response(QC['Motivation'][index], QC['Confidence'][index], QC['Problem Interpretation'][index], QC['Preference'][index], QC['Issues'][index])
                D3L3 = Level(Qa, Qb)
                
                QCs[name_QC] = Participant(D1L1, D1L2, D1L3, D2L1, D2L2, D2L3, D3L1, D3L2, D3L3)
                
                rowcount = rowcount + 18
                
        obj1_lev1_motivation = list()
        obj1_lev1_confidence = list()
        obj1_lev1_probleminterp = list()
        obj1_lev1_preference = list()
        obj1_lev1_issues = list()
        
        obj1_lev2_motivation = list()
        obj1_lev2_confidence = list()
        obj1_lev2_probleminterp = list()
        obj1_lev2_preference = list()
        obj1_lev2_issues = list()
        
        obj1_lev3_motivation = list()
        obj1_lev3_confidence = list()
        obj1_lev3_probleminterp = list()
        obj1_lev3_preference = list()
        obj1_lev3_issues = list()
        
        obj2_lev1_motivation = list()
        obj2_lev1_confidence = list()
        obj2_lev1_probleminterp = list()
        obj2_lev1_preference = list()
        obj2_lev1_issues = list()
        
        obj2_lev2_motivation = list()
        obj2_lev2_confidence = list()
        obj2_lev2_probleminterp = list()
        obj2_lev2_preference = list()
        obj2_lev2_issues = list()
        
        obj2_lev3_motivation = list()
        obj2_lev3_confidence = list()
        obj2_lev3_probleminterp = list()
        obj2_lev3_preference = list()
        obj2_lev3_issues = list()
        
        obj3_lev1_motivation = list()
        obj3_lev1_confidence = list()
        obj3_lev1_probleminterp = list()
        obj3_lev1_preference = list()
        obj3_lev1_issues = list()
        
        obj3_lev2_motivation = list()
        obj3_lev2_confidence = list()
        obj3_lev2_probleminterp = list()
        obj3_lev2_preference = list()
        obj3_lev2_issues = list()
        
        obj3_lev3_motivation = list()
        obj3_lev3_confidence = list()
        obj3_lev3_probleminterp = list()
        obj3_lev3_preference = list()
        obj3_lev3_issues = list()

        # Set up participant-specific folders
        for names in self.folders: # e.g. '151202a'
            
            # Put together each QC
            obj1_lev1_motivation.append((QCs[names].D1L1.Qa.Motivation, QCs[names].D1L1.Qb.Motivation))
            obj1_lev1_confidence.append((QCs[names].D1L1.Qa.Confidence, QCs[names].D1L1.Qb.Confidence))
            obj1_lev1_probleminterp.append((QCs[names].D1L1.Qa.ProblemInterpretation, QCs[names].D1L1.Qb.ProblemInterpretation))
            obj1_lev1_preference.append((QCs[names].D1L1.Qa.Preference, QCs[names].D1L1.Qb.Preference))
            obj1_lev1_issues.append((QCs[names].D1L1.Qa.Issues, QCs[names].D1L1.Qb.Issues))
            
            obj1_lev2_motivation.append((QCs[names].D1L2.Qa.Motivation, QCs[names].D1L2.Qb.Motivation))
            obj1_lev2_confidence.append((QCs[names].D1L2.Qa.Confidence, QCs[names].D1L2.Qb.Confidence))
            obj1_lev2_probleminterp.append((QCs[names].D1L2.Qa.ProblemInterpretation, QCs[names].D1L2.Qb.ProblemInterpretation))
            obj1_lev2_preference.append((QCs[names].D1L2.Qa.Preference, QCs[names].D1L2.Qb.Preference))
            obj1_lev2_issues.append((QCs[names].D1L2.Qa.Issues, QCs[names].D1L2.Qb.Issues))
            
            obj1_lev3_motivation.append((QCs[names].D1L3.Qa.Motivation, QCs[names].D1L3.Qb.Motivation))
            obj1_lev3_confidence.append((QCs[names].D1L3.Qa.Confidence, QCs[names].D1L3.Qb.Confidence))
            obj1_lev3_probleminterp.append((QCs[names].D1L3.Qa.ProblemInterpretation, QCs[names].D1L3.Qb.ProblemInterpretation))
            obj1_lev3_preference.append((QCs[names].D1L3.Qa.Preference, QCs[names].D1L3.Qb.Preference))
            obj1_lev3_issues.append((QCs[names].D1L3.Qa.Issues, QCs[names].D1L3.Qb.Issues))
            
            
            # Put together each QC
            obj2_lev1_motivation.append((QCs[names].D2L1.Qa.Motivation, QCs[names].D2L1.Qb.Motivation))
            obj2_lev1_confidence.append((QCs[names].D2L1.Qa.Confidence, QCs[names].D2L1.Qb.Confidence))
            obj2_lev1_probleminterp.append((QCs[names].D2L1.Qa.ProblemInterpretation, QCs[names].D2L1.Qb.ProblemInterpretation))
            obj2_lev1_preference.append((QCs[names].D2L1.Qa.Preference, QCs[names].D2L1.Qb.Preference))
            obj2_lev1_issues.append((QCs[names].D2L1.Qa.Issues, QCs[names].D2L1.Qb.Issues))
            
            obj2_lev2_motivation.append((QCs[names].D2L2.Qa.Motivation, QCs[names].D2L2.Qb.Motivation))
            obj2_lev2_confidence.append((QCs[names].D2L2.Qa.Confidence, QCs[names].D2L2.Qb.Confidence))
            obj2_lev2_probleminterp.append((QCs[names].D2L2.Qa.ProblemInterpretation, QCs[names].D2L2.Qb.ProblemInterpretation))
            obj2_lev2_preference.append((QCs[names].D2L2.Qa.Preference, QCs[names].D2L2.Qb.Preference))
            obj2_lev2_issues.append((QCs[names].D2L2.Qa.Issues, QCs[names].D2L2.Qb.Issues))
            
            obj2_lev3_motivation.append((QCs[names].D2L3.Qa.Motivation, QCs[names].D2L3.Qb.Motivation))
            obj2_lev3_confidence.append((QCs[names].D2L3.Qa.Confidence, QCs[names].D2L3.Qb.Confidence))
            obj2_lev3_probleminterp.append((QCs[names].D2L3.Qa.ProblemInterpretation, QCs[names].D2L3.Qb.ProblemInterpretation))
            obj2_lev3_preference.append((QCs[names].D2L3.Qa.Preference, QCs[names].D2L3.Qb.Preference))
            obj2_lev3_issues.append((QCs[names].D2L3.Qa.Issues, QCs[names].D2L3.Qb.Issues))
                                      
            
            
            # Put together each QC
            obj3_lev1_motivation.append((QCs[names].D3L1.Qa.Motivation, QCs[names].D3L1.Qb.Motivation))
            obj3_lev1_confidence.append((QCs[names].D3L1.Qa.Confidence, QCs[names].D3L1.Qb.Confidence))
            obj3_lev1_probleminterp.append((QCs[names].D3L1.Qa.ProblemInterpretation, QCs[names].D3L1.Qb.ProblemInterpretation))
            obj3_lev1_preference.append((QCs[names].D3L1.Qa.Preference, QCs[names].D3L1.Qb.Preference))
            obj3_lev1_issues.append((QCs[names].D3L1.Qa.Issues, QCs[names].D3L1.Qb.Issues))
            
            obj3_lev2_motivation.append((QCs[names].D3L2.Qa.Motivation, QCs[names].D3L2.Qb.Motivation))
            obj3_lev2_confidence.append((QCs[names].D3L2.Qa.Confidence, QCs[names].D3L2.Qb.Confidence))
            obj3_lev2_probleminterp.append((QCs[names].D3L2.Qa.ProblemInterpretation, QCs[names].D3L2.Qb.ProblemInterpretation))
            obj3_lev2_preference.append((QCs[names].D3L2.Qa.Preference, QCs[names].D3L2.Qb.Preference))
            obj3_lev2_issues.append((QCs[names].D3L2.Qa.Issues, QCs[names].D3L2.Qb.Issues))
            
            obj3_lev3_motivation.append((QCs[names].D3L3.Qa.Motivation, QCs[names].D3L3.Qb.Motivation))
            obj3_lev3_confidence.append((QCs[names].D3L3.Qa.Confidence, QCs[names].D3L3.Qb.Confidence))
            obj3_lev3_probleminterp.append((QCs[names].D3L3.Qa.ProblemInterpretation, QCs[names].D3L3.Qb.ProblemInterpretation))
            obj3_lev3_preference.append((QCs[names].D3L3.Qa.Preference, QCs[names].D3L3.Qb.Preference))
            obj3_lev3_issues.append((QCs[names].D3L3.Qa.Issues, QCs[names].D3L3.Qb.Issues))
                                      
                        
            files = os.listdir('/Users/caitl/Documents/SCRiM/JDM/download-3/' + names)
            file_name = '/Users/caitl/Documents/SCRiM/JDM/download-3/'
            # Loop through each document in each subject in the condition
            for document in files: # e.g. 'decision_9_events.csv'
                if document.startswith('decision_1'):
                    # Inner ifs: Check which gathered data it is
                    if document.endswith('_events.csv'):
                        print(file_name + names+ '/' + document)
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj1_lev1_events.append(np.empty([1,12]))
                        else:
                            obj1_lev1_events.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    elif document.endswith('_test.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj1_lev1_test.append(np.empty([1,12]))
                        else:
                            obj1_lev1_test.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    else:
                        with open ((file_name + names+ '/' + document), "r") as myfile:
                            obj1_lev1_strategy.append(myfile.read())
                        
                elif document.startswith('decision_2'):
                    # Inner ifs: Check which gathered data it is
                    if document.endswith('_events.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj1_lev2_events.append(np.empty([1,12]))
                        else:
                            obj1_lev2_events.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    elif document.endswith('_test.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj1_lev2_test.append(np.empty([1,12]))
                        else:
                            obj1_lev2_test.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    else:
                        with open ((file_name + names+ '/' + document), "r") as myfile:
                            obj1_lev2_strategy.append(myfile.read())
                        
                elif document.startswith('decision_3'):
                    # Inner ifs: Check which gathered data it is
                    if document.endswith('_events.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj1_lev3_events.append(np.empty([1,12]))
                        else:
                            obj1_lev3_events.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    elif document.endswith('_test.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj1_lev3_test.append(np.empty([1,12]))
                        else:
                            obj1_lev3_test.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    else:
                        with open ((file_name + names+ '/' + document), "r") as myfile:
                            obj1_lev3_strategy.append(myfile.read())
                        
                elif document.startswith('decision_4'):
                    # Inner ifs: Check which gathered data it is
                    if document.endswith('_events.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj2_lev1_events.append(np.empty([1,12]))
                        else:
                            obj2_lev1_events.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    elif document.endswith('_test.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj2_lev1_test.append(np.empty([1,12]))
                        else:
                            obj2_lev1_test.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    else:
                        with open ((file_name + names+ '/' + document), "r") as myfile:
                            obj2_lev1_strategy.append(myfile.read())
                        
                elif document.startswith('decision_5'):
                    # Inner ifs: Check which gathered data it is
                    if document.endswith('_events.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size < 5:
                            obj2_lev2_events.append(np.empty([1,12]))
                        else:
                            obj2_lev2_events.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    elif document.endswith('_test.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size < 5:
                            obj2_lev2_test.append(np.empty([1,12]))
                        else:
                            obj2_lev2_test.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    else:
                        with open ((file_name + names+ '/' + document), "r") as myfile:
                            obj2_lev2_strategy.append(myfile.read())
                        
                elif document.startswith('decision_6'):
                    # Inner ifs: Check which gathered data it is
                    if document.endswith('_events.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj2_lev3_events.append(np.empty([1,12]))
                        else:
                            obj2_lev3_events.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    elif document.endswith('_test.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj2_lev3_test.append(np.empty([1,12]))
                        else:
                            obj2_lev3_test.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    else:
                        with open ((file_name + names+ '/' + document), "r") as myfile:
                            obj2_lev2_strategy.append(myfile.read())
                        
                elif document.startswith('decision_7'):
                    # Inner ifs: Check which gathered data it is
                    if document.endswith('_events.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj3_lev1_events.append(np.empty([1,12]))
                        else:
                            obj3_lev1_events.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    elif document.endswith('_test.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj3_lev1_test.append(np.empty([1,12]))
                        else:
                            obj3_lev1_test.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    else:
                        with open ((file_name + names+ '/' + document), "r") as myfile:
                            obj3_lev1_strategy.append(myfile.read())
                        
                elif document.startswith('decision_8'):
                    # Inner ifs: Check which gathered data it is
                    if document.endswith('_events.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj3_lev2_events.append(np.empty([1,12]))
                        else:
                            obj3_lev2_events.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    elif document.endswith('_test.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj3_lev2_test.append(np.empty([1,12]))
                        else:
                            obj3_lev2_test.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    else:
                        with open ((file_name + names+ '/' + document), "r") as myfile:
                            obj3_lev2_strategy.append(myfile.read())
                    
                elif document.startswith('decision_9'):
                    # Inner ifs: Check which gathered data it is
                    if document.endswith('_events.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj3_lev3_events.append(np.empty([1,12]))
                        else:
                            obj3_lev3_events.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    elif document.endswith('_test.csv'):
                        if os.stat(file_name + names+ '/' + document).st_size == 0:
                            obj3_lev3_test.append(np.empty([1,12]))
                        else:
                            obj3_lev3_test.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                    else:
                        with open ((file_name + names+ '/' + document), "r") as myfile:
                            obj3_lev3_strategy.append(myfile.read())
                            
                elif document.startswith('exit'):
                    ans_exit.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                elif document.startswith('intro'):
                    intro.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                else:
                    print((file_name + names+ '/' + document))
                    comprehension.append(pd.read_csv((file_name + names+ '/' + document), header=None))
                
        Result11 = dict()
        Result11['events'] = obj1_lev1_events
        Result11['test'] = obj1_lev1_test
        Result11['strategy'] = obj1_lev1_strategy
        Result11['Motivation'] = obj1_lev1_motivation
        Result11['Confidence'] = obj1_lev1_confidence
        Result11['ProblemInterpretation'] = obj1_lev1_probleminterp
        Result11['Preference'] = obj1_lev1_preference
        Result11['Issues'] = obj1_lev1_issues
        
        Result12 = dict()
        Result12['events'] = obj1_lev2_events
        Result12['test'] = obj1_lev2_test
        Result12['strategy'] = obj1_lev2_strategy
        Result12['Motivation'] = obj1_lev2_motivation
        Result12['Confidence'] =obj1_lev2_confidence
        Result12['ProblemInterpretation'] = obj1_lev2_probleminterp
        Result12['Preference'] = obj1_lev2_preference
        Result12['Issues'] = obj1_lev2_issues
        
        Result13 = dict()
        Result13['events'] = obj1_lev3_events
        Result13['test'] = obj1_lev3_test
        Result13['strategy'] = obj1_lev3_strategy
        Result13['Motivation'] = obj1_lev3_motivation
        Result13['Confidence'] =obj1_lev3_confidence
        Result13['ProblemInterpretation'] = obj1_lev3_probleminterp
        Result13['Preference'] = obj1_lev3_preference
        Result13['Issues'] = obj1_lev3_issues
        
        Result21 = dict()
        Result21['events'] = obj2_lev1_events
        Result21['test'] = obj2_lev1_test
        Result21['strategy'] = obj2_lev1_strategy
        Result21['Motivation'] = obj2_lev1_motivation
        Result21['Confidence'] =obj2_lev1_confidence
        Result21['ProblemInterpretation'] = obj2_lev1_probleminterp
        Result21['Preference'] = obj2_lev1_preference
        Result21['Issues'] = obj2_lev1_issues
        
        Result22 = dict()
        Result22['events'] = obj2_lev2_events
        Result22['test'] = obj2_lev2_test
        Result22['strategy'] = obj2_lev2_strategy
        Result22['Motivation'] = obj2_lev2_motivation
        Result22['Confidence'] =obj2_lev2_confidence
        Result22['ProblemInterpretation'] = obj2_lev2_probleminterp
        Result22['Preference'] = obj2_lev2_preference
        Result22['Issues'] = obj2_lev2_issues
        
        Result23 = dict()
        Result23['events'] = obj2_lev3_events
        Result23['test'] = obj2_lev3_test
        Result23['strategy'] = obj2_lev3_strategy
        Result23['Motivation'] = obj2_lev3_motivation
        Result23['Confidence'] =obj2_lev3_confidence
        Result23['ProblemInterpretation'] = obj2_lev3_probleminterp
        Result23['Preference'] = obj2_lev3_preference
        Result23['Issues'] = obj2_lev3_issues
        
        Result31 = dict()
        Result31['events'] = obj3_lev1_events
        Result31['test'] = obj3_lev1_test
        Result31['strategy'] = obj3_lev1_strategy
        Result31['Motivation'] = obj3_lev1_motivation
        Result31['Confidence'] =obj3_lev1_confidence
        Result31['ProblemInterpretation'] = obj3_lev1_probleminterp
        Result31['Preference'] = obj3_lev1_preference
        Result31['Issues'] = obj3_lev1_issues
        
        Result32 = dict()
        Result32['events'] = obj3_lev2_events
        Result32['test'] = obj3_lev2_test
        Result32['strategy'] = obj3_lev2_strategy
        Result32['Motivation'] = obj3_lev2_motivation
        Result32['Confidence'] =obj3_lev2_confidence
        Result32['ProblemInterpretation'] = obj3_lev2_probleminterp
        Result32['Preference'] = obj3_lev2_preference
        Result32['Issues'] = obj3_lev2_issues
        
        Result33 = dict()
        Result33['events'] = obj3_lev3_events
        Result33['test'] = obj3_lev3_test
        Result33['strategy'] = obj3_lev3_strategy
        Result33['Motivation'] = obj3_lev3_motivation
        Result33['Confidence'] =obj3_lev3_confidence
        Result33['ProblemInterpretation'] = obj3_lev3_probleminterp
        Result33['Preference'] = obj3_lev3_preference
        Result33['Issues'] = obj3_lev3_issues
        
        Result1 = dict()
        Result1['lev1'] = Result11
        Result1['lev2'] = Result12
        Result1['lev3'] = Result13
        
        Result2 = dict()
        Result2['lev1'] = Result21
        Result2['lev2'] = Result22
        Result2['lev3'] = Result23
        
        Result3 = dict()
        Result3['lev1'] = Result31
        Result3['lev2'] = Result32
        Result3['lev3'] = Result33
        
        Result = dict()
        Result['obj1'] = Result1
        Result['obj2'] = Result2
        Result['obj3'] = Result3
        
        data_group = dict()
        data_group['result'] = Result
        data_group['comprehension'] = comprehension
        data_group['intro'] = intro
        data_group['ans_exit'] = ans_exit
        
        return(data_group)
#        
#    
def onelev_unwind(data_dict):
    result = data_dict['result']
    obj1 = result['obj1']['lev1']['test']
    obj2 = result['obj2']['lev1']['test']
    obj3 = result['obj3']['lev1']['test']
    
    if len(obj1) != len(obj2):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    elif len(obj2) != len(obj3):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    
    setting1 = list()
    setting2 = list()
    setting3 = list()
    
    for k in range(len(obj1)):
        setting1.append(obj1[k].iloc[:,4])
        
    for k in range(len(obj2)):
        setting2.append(obj2[k].iloc[:,4])
        
    for k in range(len(obj3)):
        setting3.append(obj3[k].iloc[:,4])
        
    bespooled = dict()
    bespooled['obj1'] = setting1
    bespooled['obj2'] = setting2
    bespooled['obj3'] = setting3
    return(bespooled)
    
def twolev_unwind(data_dict):
    result = data_dict['result']
    obj1 = result['obj1']['lev2']['test']
    obj2 = result['obj2']['lev2']['test']
    obj3 = result['obj3']['lev2']['test']
    
    if len(obj1) != len(obj2):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    elif len(obj2) != len(obj3):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    
    setting1 = list()
    setting2 = list()
    setting3 = list()
    
    for k in range(len(obj1)):
#        if obj1[k].iloc[:,1][0] != obj2[k].iloc[:,1][0]: print(obj1[k].iloc[:,1][0])
        if issubclass(type(obj1[k]), np.ndarray):
            setting1.append(np.empty(3))
        else:
            setting1.append(obj1[k].iloc[:,4:6])
        
    for k in range(len(obj2)):
#        if obj1[k].iloc[:,1][0] != obj2[k].iloc[:,1][0]: print(obj2[k].iloc[:,1][0])
        if issubclass(type(obj2[k]), np.ndarray):
            setting2.append(np.empty(3))
        else:
            setting2.append(obj2[k].iloc[:,4:6])
        
    for k in range(len(obj3)):
#        if obj2[k].iloc[:,1][0] != obj3[k].iloc[:,1][0]: print(obj3[k].iloc[:,1][0])
        if issubclass(type(obj3[k]), np.ndarray):
            setting3.append(np.empty(3))
        else:
            setting3.append(obj3[k].iloc[:,4:6])
        
    bespooled = dict()
    bespooled['obj1'] = setting1
    bespooled['obj2'] = setting2
    bespooled['obj3'] = setting3
    return(bespooled)
    
def threelev_unwind(data_dict):
    result = data_dict['result']
    obj1 = result['obj1']['lev3']['test']
    obj2 = result['obj2']['lev3']['test']
    obj3 = result['obj3']['lev3']['test']
    
    if len(obj1) != len(obj2):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    elif len(obj2) != len(obj3):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    
    setting1 = list()
    setting2 = list()
    setting3 = list()
    
    for k in range(len(obj1)):
        setting1.append(obj1[k].iloc[:,4:7])
        
    for k in range(len(obj2)):
        setting2.append(obj2[k].iloc[:,4:7])
        
    for k in range(len(obj3)):
        setting3.append(obj3[k].iloc[:,4:7])
        
    bespooled = dict()
    bespooled['obj1'] = setting1
    bespooled['obj2'] = setting2
    bespooled['obj3'] = setting3
    return(bespooled)
    
def unwind_OOs_LP(data_dict):
    result = data_dict['result']
    obj1L_1 = result['obj1']['lev1']['test']
    obj1L_2 = result['obj2']['lev1']['test']
    
    obj2L_1 = result['obj1']['lev2']['test']
    obj2L_2 = result['obj2']['lev2']['test']
    
    obj3L_1 = result['obj1']['lev3']['test']
    obj3L_2 = result['obj2']['lev3']['test']
    
    if len(obj1L_1) != len(obj1L_2):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    
    PI_1L = result['obj1']['lev1']['ProblemInterpretation']
    PI_2L = result['obj1']['lev2']['ProblemInterpretation']
    PI_3L = result['obj1']['lev3']['ProblemInterpretation']
    
    
    # Make a list of participants who coded "O" at the one-objective stage
    names_OO = list()
    
    setting1L_1 = list()
    setting1L_2 = list()
    
    setting2L_1 = list()
    setting2L_2 = list()
    
    setting3L_1 = list()
    setting3L_2 = list()
    
    for k in range(len(PI_1L)):
        if ('O' in PI_1L[k] or 'O' in PI_2L[k] or 'O' in PI_3L[k]):
            names_OO.append(data_dict['intro'][k][0][0])
            setting1L_1.append(obj1L_1[k].iloc[:,4].values)
            setting1L_2.append(obj1L_2[k].iloc[:,4].values)
            
            setting2L_1.append(obj2L_1[k].iloc[:,4:6].values)
            setting2L_2.append(obj2L_2[k].iloc[:,4:6].values)
            
            setting3L_1.append(obj3L_1[k].iloc[:,4:7].values)
            setting3L_2.append(obj3L_2[k].iloc[:,4:7].values)


    bespooled_1obj = dict()
    bespooled_2obj = dict()
    b1obj_1L = list()
    b2obj_1L = list()
    b1obj_2L = list()
    b2obj_2L = list()
    b1obj_3L = list()
    b2obj_3L = list()
    
    for k in range(len(setting2L_2)):
        
        b1obj_1L.append(np.asarray(setting1L_1[k]))
        b2obj_1L.append(np.asarray(setting1L_2[k]))
    
        b1obj_2L.append(np.asarray(setting2L_1[k]))
        b2obj_2L.append(np.asarray(setting2L_2[k]))
        
        b1obj_3L.append(np.asarray(setting3L_1[k]))
        b2obj_3L.append(np.asarray(setting3L_2[k]))
        
    bespooled_1obj['1L'] = [float(i) for i in b1obj_1L]  
    bespooled_1obj['2L'] = [l.tolist() for l in b1obj_2L]
    bespooled_1obj['3L'] = [l.tolist() for l in b1obj_3L]
    bespooled_2obj['1L'] = [float(i) for i in b2obj_1L]  
    bespooled_2obj['2L'] = [l.tolist() for l in b2obj_2L]
    bespooled_2obj['3L'] = [l.tolist() for l in b2obj_3L]
    
    bespooled = dict()
    bespooled['1obj'] = bespooled_1obj
    bespooled['2obj'] = bespooled_2obj
    return(bespooled)

    
def unwind_codes_LP(data_dict, code, subcode):
    result = data_dict['result']
    obj1L_1 = result['obj1']['lev1']['test']
    obj1L_2 = result['obj2']['lev1']['test']
    obj1L_3 = result['obj3']['lev1']['test']
    
    obj2L_1 = result['obj1']['lev2']['test']
    obj2L_2 = result['obj2']['lev2']['test']
    obj2L_3 = result['obj3']['lev2']['test']
    
    obj3L_1 = result['obj1']['lev3']['test']
    obj3L_2 = result['obj2']['lev3']['test']
    obj3L_3 = result['obj3']['lev3']['test']
    
    if len(obj1L_1) != len(obj1L_2):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    
    PI_1L = ((result['obj1']['lev1'][code], result['obj2']['lev1'][code], result['obj3']['lev1'][code]))
    PI_2L = ((result['obj1']['lev2'][code], result['obj2']['lev2'][code], result['obj3']['lev2'][code]))
    PI_3L = ((result['obj1']['lev3'][code], result['obj2']['lev3'][code], result['obj3']['lev3'][code]))
    
    
    # Make a list of participants who coded "O" at the one-objective stage
    names_code = list()
    
    setting1L_1 = list()
    setting1L_2 = list()
    setting1L_3 = list()
    
    setting2L_1 = list()
    setting2L_2 = list()
    setting2L_3 = list()
    
    setting3L_1 = list()
    setting3L_2 = list()
    setting3L_3 = list()
    
        
    b1obj_1L = list()
    b2obj_1L = list()
    b3obj_1L = list()
    
    b1obj_2L = list()
    b2obj_2L = list()
    b3obj_2L = list()
    
    b1obj_3L = list()
    b2obj_3L = list()
    b3obj_3L = list()
    
    def codecheck(data_dict, levlist, objlist, objnum, levnum, code, subcode):
        names_code = list()
        settings = list()
        bespooled = list()
        
        if levnum == 1:
            inds = 4
        elif levnum == 2:
            inds = [4,5]
        elif levnum == 3:
            inds = [4,5,6]
        else:
            print('error')
        
        count = 0
        
        for k in range(len(levlist[objnum])):
            if subcode in levlist[objnum][k]:
                names_code.append(data_dict['intro'][k][0][0])
                if type(objlist[k]) is not np.ndarray: 
                    settings.append(objlist[k].iloc[:,inds].values)
                else: 
                    settings.append(np.nan)
                bespooled.append(np.asarray(settings[count]))
                count = count + 1
            else:
                pass
            
            
            
        return(names_code, settings, bespooled)
        
    (names_code, setting1L_1, b1obj_1L) = codecheck(data_dict, PI_1L, obj1L_1, 0, 1, code, subcode)
    (names_code, setting1L_2, b2obj_1L) = codecheck(data_dict, PI_1L, obj1L_2, 1, 1, code, subcode)
    (names_code, setting1L_3, b3obj_1L) = codecheck(data_dict, PI_1L, obj1L_3, 2, 1, code, subcode)
    
    (names_code, setting2L_1, b1obj_2L) = codecheck(data_dict, PI_2L, obj2L_1, 0, 2, code, subcode)
    (names_code, setting2L_2, b2obj_2L) = codecheck(data_dict, PI_2L, obj2L_2, 1, 2, code, subcode)
    (names_code, setting2L_3, b3obj_2L) = codecheck(data_dict, PI_2L, obj2L_3, 2, 2, code, subcode)
    
    (names_code, setting3L_1, b1obj_3L) = codecheck(data_dict, PI_3L, obj3L_1, 0, 3, code, subcode)
    (names_code, setting3L_2, b2obj_3L) = codecheck(data_dict, PI_3L, obj3L_2, 1, 3, code, subcode)
    (names_code, setting3L_3, b3obj_3L) = codecheck(data_dict, PI_3L, obj3L_3, 2, 3, code, subcode)

    bespooled_1obj = dict()
    bespooled_2obj = dict()
    bespooled_3obj = dict()
        
    bespooled_1obj['1L'] = [float(i) for i in b1obj_1L]  
    bespooled_1obj['2L'] = [l.tolist() for l in b1obj_2L]
    bespooled_1obj['3L'] = [l.tolist() for l in b1obj_3L]
    bespooled_2obj['1L'] = [float(i) for i in b2obj_1L]  
    bespooled_2obj['2L'] = [l.tolist() for l in b2obj_2L]
    bespooled_2obj['3L'] = [l.tolist() for l in b2obj_3L]
    bespooled_3obj['1L'] = [float(i) for i in b3obj_1L]  
    bespooled_3obj['2L'] = [l.tolist() for l in b3obj_2L]
    bespooled_3obj['3L'] = [l.tolist() for l in b3obj_3L]
    
    bespooled = dict()
    bespooled['1obj'] = bespooled_1obj
    bespooled['2obj'] = bespooled_2obj
    bespooled['3obj'] = bespooled_3obj
    return(bespooled)
    
def unwind_codes_NP(data_dict, code, subcode):
    result = data_dict['result']
    obj1L_1 = result['obj1']['lev1']['test']
    obj1L_2 = result['obj2']['lev1']['test']
    obj1L_3 = result['obj3']['lev1']['test']
    
    obj2L_1 = result['obj1']['lev2']['test']
    obj2L_2 = result['obj2']['lev2']['test']
    obj2L_3 = result['obj3']['lev2']['test']
    
    obj3L_1 = result['obj1']['lev3']['test']
    obj3L_2 = result['obj2']['lev3']['test']
    obj3L_3 = result['obj3']['lev3']['test']
    
    if len(obj1L_1) != len(obj1L_2):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    
    PI_1L = ((result['obj1']['lev1'][code], result['obj2']['lev1'][code], result['obj3']['lev1'][code]))
    PI_2L = ((result['obj1']['lev2'][code], result['obj2']['lev2'][code], result['obj3']['lev2'][code]))
    PI_3L = ((result['obj1']['lev3'][code], result['obj2']['lev3'][code], result['obj3']['lev3'][code]))
    
    
    # Make a list of participants who coded "O" at the one-objective stage
    names_code = list()
    
    setting1L_1 = list()
    setting1L_2 = list()
    setting1L_3 = list()
    
    setting2L_1 = list()
    setting2L_2 = list()
    setting2L_3 = list()
    
    setting3L_1 = list()
    setting3L_2 = list()
    setting3L_3 = list()
    
        
    b1obj_1L = list()
    b2obj_1L = list()
    b3obj_1L = list()
    
    b1obj_2L = list()
    b2obj_2L = list()
    b3obj_2L = list()
    
    b1obj_3L = list()
    b2obj_3L = list()
    b3obj_3L = list()
    
    def codecheck(data_dict, levlist, objlist, objnum, levnum, code, subcode):
        names_code = list()
        settings = list()
        bespooled = list()
        
        if levnum == 1:
            inds = 4
        elif levnum == 2:
            inds = [4,5]
        elif levnum == 3:
            inds = [4,5,6]
        else:
            print('error')
        
        count = 0
        
        for k in range(len(levlist[objnum])):
            if subcode in levlist[objnum][k]:
                names_code.append(data_dict['intro'][k][0][0])
                if type(objlist[k]) is not np.ndarray: 
                    settings.append(objlist[k].iloc[:,inds].values)
                else: 
                    settings.append(np.nan)
                bespooled.append(np.asarray(settings[count]/100))
                count = count + 1
            else:
                pass
            
        return(names_code, settings, bespooled)
        
    (names_code, setting1L_1, b1obj_1L) = codecheck(data_dict, PI_1L, obj1L_1, 0, 1, code, subcode)
    (names_code, setting1L_2, b2obj_1L) = codecheck(data_dict, PI_1L, obj1L_2, 1, 1, code, subcode)
    (names_code, setting1L_3, b3obj_1L) = codecheck(data_dict, PI_1L, obj1L_3, 2, 1, code, subcode)
    
    (names_code, setting2L_1, b1obj_2L) = codecheck(data_dict, PI_2L, obj2L_1, 0, 2, code, subcode)
    (names_code, setting2L_2, b2obj_2L) = codecheck(data_dict, PI_2L, obj2L_2, 1, 2, code, subcode)
    (names_code, setting2L_3, b3obj_2L) = codecheck(data_dict, PI_2L, obj2L_3, 2, 2, code, subcode)
    
    (names_code, setting3L_1, b1obj_3L) = codecheck(data_dict, PI_3L, obj3L_1, 0, 3, code, subcode)
    (names_code, setting3L_2, b2obj_3L) = codecheck(data_dict, PI_3L, obj3L_2, 1, 3, code, subcode)
    (names_code, setting3L_3, b3obj_3L) = codecheck(data_dict, PI_3L, obj3L_3, 2, 3, code, subcode)

    bespooled_1obj = dict()
    bespooled_2obj = dict()
    bespooled_3obj = dict()
        
    bespooled_1obj['1L'] = [float(i) for i in b1obj_1L]  
    bespooled_1obj['2L'] = [l.tolist() for l in b1obj_2L]
    bespooled_1obj['3L'] = [l.tolist() for l in b1obj_3L]
    bespooled_2obj['1L'] = [float(i) for i in b2obj_1L]  
    bespooled_2obj['2L'] = [l.tolist() for l in b2obj_2L]
    bespooled_2obj['3L'] = [l.tolist() for l in b2obj_3L]
    bespooled_3obj['1L'] = [float(i) for i in b3obj_1L]  
    bespooled_3obj['2L'] = [l.tolist() for l in b3obj_2L]
    bespooled_3obj['3L'] = [l.tolist() for l in b3obj_3L]
    
    bespooled = dict()
    bespooled['1obj'] = bespooled_1obj
    bespooled['2obj'] = bespooled_2obj
    bespooled['3obj'] = bespooled_3obj
    return(bespooled)
    
def unwind_codes_LP_any(data_dict, code):
    result = data_dict['result']
    obj1L_1 = result['obj1']['lev1']['test']
    obj1L_2 = result['obj2']['lev1']['test']
    obj1L_3 = result['obj3']['lev1']['test']
    
    obj2L_1 = result['obj1']['lev2']['test']
    obj2L_2 = result['obj2']['lev2']['test']
    obj2L_3 = result['obj3']['lev2']['test']
    
    obj3L_1 = result['obj1']['lev3']['test']
    obj3L_2 = result['obj2']['lev3']['test']
    obj3L_3 = result['obj3']['lev3']['test']
    
    if len(obj1L_1) != len(obj1L_2):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    
    PI_1L = ((result['obj1']['lev1'][code], result['obj2']['lev1'][code], result['obj3']['lev1'][code]))
    PI_2L = ((result['obj1']['lev2'][code], result['obj2']['lev2'][code], result['obj3']['lev2'][code]))
    PI_3L = ((result['obj1']['lev3'][code], result['obj2']['lev3'][code], result['obj3']['lev3'][code]))
    
    
    # Make a list of participants who coded "O" at the one-objective stage
    names_code = list()
    
    setting1L_1 = list()
    setting1L_2 = list()
    setting1L_3 = list()
    
    setting2L_1 = list()
    setting2L_2 = list()
    setting2L_3 = list()
    
    setting3L_1 = list()
    setting3L_2 = list()
    setting3L_3 = list()
    
        
    b1obj_1L = list()
    b2obj_1L = list()
    b3obj_1L = list()
    
    b1obj_2L = list()
    b2obj_2L = list()
    b3obj_2L = list()
    
    b1obj_3L = list()
    b2obj_3L = list()
    b3obj_3L = list()
    
    def codecheck(data_dict, levlist, objlist, objnum, levnum):
        names_code = list()
        settings = list()
        bespooled = list()
        
        if levnum == 1:
            inds = 4
        elif levnum == 2:
            inds = [4,5]
        elif levnum == 3:
            inds = [4,5,6]
        else:
            print('error')
        
        count = 0
        
        for k in range(len(levlist[objnum])):
            names_code.append(data_dict['intro'][k][0][0])
            if type(objlist[k]) is not np.ndarray: 
                settings.append(objlist[k].iloc[:,inds].values)
            else: 
                settings.append(np.nan)
            bespooled.append(np.asarray(settings[count]))
            count = count + 1  
            
        return(names_code, settings, bespooled)
        
    (names_code, setting1L_1, b1obj_1L) = codecheck(data_dict, PI_1L, obj1L_1, 0, 1)
    (names_code, setting1L_2, b2obj_1L) = codecheck(data_dict, PI_1L, obj1L_2, 1, 1)
    (names_code, setting1L_3, b3obj_1L) = codecheck(data_dict, PI_1L, obj1L_3, 2, 1)
    
    (names_code, setting2L_1, b1obj_2L) = codecheck(data_dict, PI_2L, obj2L_1, 0, 2)
    (names_code, setting2L_2, b2obj_2L) = codecheck(data_dict, PI_2L, obj2L_2, 1, 2)
    (names_code, setting2L_3, b3obj_2L) = codecheck(data_dict, PI_2L, obj2L_3, 2, 2)
    
    (names_code, setting3L_1, b1obj_3L) = codecheck(data_dict, PI_3L, obj3L_1, 0, 3)
    (names_code, setting3L_2, b2obj_3L) = codecheck(data_dict, PI_3L, obj3L_2, 1, 3)
    (names_code, setting3L_3, b3obj_3L) = codecheck(data_dict, PI_3L, obj3L_3, 2, 3)

    bespooled_1obj = dict()
    bespooled_2obj = dict()
    bespooled_3obj = dict()
        
    bespooled_1obj['1L'] = [float(i) for i in b1obj_1L]  
    bespooled_1obj['2L'] = [l.tolist() for l in b1obj_2L]
    bespooled_1obj['3L'] = [l.tolist() for l in b1obj_3L]
    bespooled_2obj['1L'] = [float(i) for i in b2obj_1L]  
    bespooled_2obj['2L'] = [l.tolist() for l in b2obj_2L]
    bespooled_2obj['3L'] = [l.tolist() for l in b2obj_3L]
    bespooled_3obj['1L'] = [float(i) for i in b3obj_1L]  
    bespooled_3obj['2L'] = [l.tolist() for l in b3obj_2L]
    bespooled_3obj['3L'] = [l.tolist() for l in b3obj_3L]
    
    bespooled = dict()
    bespooled['1obj'] = bespooled_1obj
    bespooled['2obj'] = bespooled_2obj
    bespooled['3obj'] = bespooled_3obj
    return(bespooled)
    
def unwind_codes_NP_any(data_dict, code):
    result = data_dict['result']
    obj1L_1 = result['obj1']['lev1']['test']
    obj1L_2 = result['obj2']['lev1']['test']
    obj1L_3 = result['obj3']['lev1']['test']
    
    obj2L_1 = result['obj1']['lev2']['test']
    obj2L_2 = result['obj2']['lev2']['test']
    obj2L_3 = result['obj3']['lev2']['test']
    
    obj3L_1 = result['obj1']['lev3']['test']
    obj3L_2 = result['obj2']['lev3']['test']
    obj3L_3 = result['obj3']['lev3']['test']
    
    if len(obj1L_1) != len(obj1L_2):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    
    PI_1L = ((result['obj1']['lev1'][code], result['obj2']['lev1'][code], result['obj3']['lev1'][code]))
    PI_2L = ((result['obj1']['lev2'][code], result['obj2']['lev2'][code], result['obj3']['lev2'][code]))
    PI_3L = ((result['obj1']['lev3'][code], result['obj2']['lev3'][code], result['obj3']['lev3'][code]))
    
    
    # Make a list of participants who coded "O" at the one-objective stage
    names_code = list()
    
    setting1L_1 = list()
    setting1L_2 = list()
    setting1L_3 = list()
    
    setting2L_1 = list()
    setting2L_2 = list()
    setting2L_3 = list()
    
    setting3L_1 = list()
    setting3L_2 = list()
    setting3L_3 = list()
    
        
    b1obj_1L = list()
    b2obj_1L = list()
    b3obj_1L = list()
    
    b1obj_2L = list()
    b2obj_2L = list()
    b3obj_2L = list()
    
    b1obj_3L = list()
    b2obj_3L = list()
    b3obj_3L = list()
    
    def codecheck(data_dict, levlist, objlist, objnum, levnum):
        names_code = list()
        settings = list()
        bespooled = list()
        
        if levnum == 1:
            inds = 4
        elif levnum == 2:
            inds = [4,5]
        elif levnum == 3:
            inds = [4,5,6]
        else:
            print('error')
        
        count = 0
        
        for k in range(len(levlist[objnum])):
            names_code.append(data_dict['intro'][k][0][0])
            if type(objlist[k]) is not np.ndarray: 
                settings.append(objlist[k].iloc[:,inds].values)
            else: 
                settings.append(np.nan)
            bespooled.append(np.asarray(settings[count]/100))
            count = count + 1  
            
        return(names_code, settings, bespooled)
        
    (names_code, setting1L_1, b1obj_1L) = codecheck(data_dict, PI_1L, obj1L_1, 0, 1)
    (names_code, setting1L_2, b2obj_1L) = codecheck(data_dict, PI_1L, obj1L_2, 1, 1)
    (names_code, setting1L_3, b3obj_1L) = codecheck(data_dict, PI_1L, obj1L_3, 2, 1)
    
    (names_code, setting2L_1, b1obj_2L) = codecheck(data_dict, PI_2L, obj2L_1, 0, 2)
    (names_code, setting2L_2, b2obj_2L) = codecheck(data_dict, PI_2L, obj2L_2, 1, 2)
    (names_code, setting2L_3, b3obj_2L) = codecheck(data_dict, PI_2L, obj2L_3, 2, 2)
    
    (names_code, setting3L_1, b1obj_3L) = codecheck(data_dict, PI_3L, obj3L_1, 0, 3)
    (names_code, setting3L_2, b2obj_3L) = codecheck(data_dict, PI_3L, obj3L_2, 1, 3)
    (names_code, setting3L_3, b3obj_3L) = codecheck(data_dict, PI_3L, obj3L_3, 2, 3)

    bespooled_1obj = dict()
    bespooled_2obj = dict()
    bespooled_3obj = dict()
        
    bespooled_1obj['1L'] = [float(i) for i in b1obj_1L]  
    bespooled_1obj['2L'] = [l.tolist() for l in b1obj_2L]
    bespooled_1obj['3L'] = [l.tolist() for l in b1obj_3L]
    bespooled_2obj['1L'] = [float(i) for i in b2obj_1L]  
    bespooled_2obj['2L'] = [l.tolist() for l in b2obj_2L]
    bespooled_2obj['3L'] = [l.tolist() for l in b2obj_3L]
    bespooled_3obj['1L'] = [float(i) for i in b3obj_1L]  
    bespooled_3obj['2L'] = [l.tolist() for l in b3obj_2L]
    bespooled_3obj['3L'] = [l.tolist() for l in b3obj_3L]
    
    bespooled = dict()
    bespooled['1obj'] = bespooled_1obj
    bespooled['2obj'] = bespooled_2obj
    bespooled['3obj'] = bespooled_3obj
    return(bespooled)
#    
def check_bespooled_length(bespooled):
    
    len1 = len(bespooled['obj1']['1L'])
    len2 = len(bespooled['obj1']['2L'])
    len3 = len(bespooled['obj1']['3L'])
    
    len4 = len(bespooled['obj2']['1L'])
    len5 = len(bespooled['obj2']['2L'])
    len6 = len(bespooled['obj2']['3L'])

    len7 = len(bespooled['obj3']['1L'])
    len8 = len(bespooled['obj3']['2L'])
    len9 = len(bespooled['obj3']['3L'])
    
    len_bespooled = len1 + len2 + len3 + len4 + len5 + len6 + len7 + len8 + len9
    
    len_1obj = len1 + len2 + len3
    len_2obj = len4 + len5 + len6
    len_3obj = len7 + len8 + len9
    
    return(len_bespooled, len_1obj, len_2obj, len_3obj)
#    
def unwind_OOs_NP(data_dict):
    result = data_dict['result']
    obj1L_1 = result['obj1']['lev1']['test']
    obj1L_2 = result['obj2']['lev1']['test']
    
    obj2L_1 = result['obj1']['lev2']['test']
    obj2L_2 = result['obj2']['lev2']['test']
    
    obj3L_1 = result['obj1']['lev3']['test']
    obj3L_2 = result['obj2']['lev3']['test']
    
    if len(obj1L_1) != len(obj1L_2):
        print(result['obj1']['lev1']['test'][0].iloc[:,1])
    
    PI_1L = result['obj1']['lev1']['ProblemInterpretation']
    PI_2L = result['obj1']['lev2']['ProblemInterpretation']
    PI_3L = result['obj1']['lev3']['ProblemInterpretation']
    
    
    # Make a list of participants who coded "O" at the one-objective stage
    names_OO = list()
    
    setting1L_1 = list()
    setting1L_2 = list()
    
    setting2L_1 = list()
    setting2L_2 = list()
    
    setting3L_1 = list()
    setting3L_2 = list()
    
    for k in range(len(PI_1L)):
        if ('O' in PI_1L[k] or 'O' in PI_2L[k] or 'O' in PI_3L[k]):
            names_OO.append(data_dict['intro'][k][0][0])
            setting1L_1.append(obj1L_1[k].iloc[:,4].values)
            setting1L_2.append(obj1L_2[k].iloc[:,4].values)
            
            setting2L_1.append(obj2L_1[k].iloc[:,4:6].values)
            setting2L_2.append(obj2L_2[k].iloc[:,4:6].values)
            
            setting3L_1.append(obj3L_1[k].iloc[:,4:7].values)
            setting3L_2.append(obj3L_2[k].iloc[:,4:7].values)


    bespooled_1obj = dict()
    bespooled_2obj = dict()

    bespooled_1obj['1L'] = np.asarray(setting1L_1)/100
    bespooled_2obj['1L'] = np.asarray(setting1L_2)/100
    
    b1obj_1L = list()
    b2obj_1L = list()
    b1obj_2L = list()
    b2obj_2L = list()
    b1obj_3L = list()
    b2obj_3L = list()
    
    for k in range(len(setting2L_2)):
        
        b1obj_1L.append(np.asarray(setting1L_1[k])/100)
        b2obj_1L.append(np.asarray(setting1L_2[k])/100)
    
        b1obj_2L.append(np.asarray(setting2L_1[k])/100)
        b2obj_2L.append(np.asarray(setting2L_2[k])/100)
        
        b1obj_3L.append(np.asarray(setting3L_1[k])/100)
        b2obj_3L.append(np.asarray(setting3L_2[k])/100)
        
    bespooled_1obj['1L'] = [float(i) for i in b1obj_1L]  
    bespooled_1obj['2L'] = [l.tolist() for l in b1obj_2L]
    bespooled_1obj['3L'] = [l.tolist() for l in b1obj_3L]
    bespooled_2obj['1L'] = [float(i) for i in b2obj_1L]  
    bespooled_2obj['2L'] = [l.tolist() for l in b2obj_2L]
    bespooled_2obj['3L'] = [l.tolist() for l in b2obj_3L]
    
    bespooled = dict()
    bespooled['1obj'] = bespooled_1obj
    bespooled['2obj'] = bespooled_2obj
    
    return(bespooled)
    
def bespooled_combine_PI(bespooled1, bespooled2):
    
    bespooled = dict()
    
    obj1 = dict()
    obj2 = dict()
    
    bespooled1['1obj']['1L'].extend(bespooled2['1obj']['1L'])
    bespooled1['1obj']['2L'].extend(bespooled2['1obj']['2L'])
    bespooled1['1obj']['3L'].extend(bespooled2['1obj']['3L'])
    
    bespooled1['2obj']['1L'].extend(bespooled2['2obj']['1L'])
    bespooled1['2obj']['2L'].extend(bespooled2['2obj']['2L'])
    bespooled1['2obj']['3L'].extend(bespooled2['2obj']['3L'])
    
    obj1['1L'] = bespooled1['1obj']['1L']
    obj1['2L'] = bespooled1['1obj']['2L']
    obj1['3L'] = bespooled1['1obj']['3L']
    
    obj2['1L'] = bespooled1['2obj']['1L']
    obj2['2L'] = bespooled1['2obj']['2L']
    obj2['3L'] = bespooled1['2obj']['3L']
    
    bespooled['1obj'] = obj1
    bespooled['2obj'] = obj2
    
    return(bespooled)
    
def bespooled_combine(bespooled1, bespooled2):
    
    bespooled = dict()
    
    obj1 = dict()
    obj2 = dict()
    obj3 = dict()
    
    bespooled1['1obj']['1L'].extend(bespooled2['1obj']['1L'])
    bespooled1['1obj']['2L'].extend(bespooled2['1obj']['2L'])
    bespooled1['1obj']['3L'].extend(bespooled2['1obj']['3L'])
    
    bespooled1['2obj']['1L'].extend(bespooled2['2obj']['1L'])
    bespooled1['2obj']['2L'].extend(bespooled2['2obj']['2L'])
    bespooled1['2obj']['3L'].extend(bespooled2['2obj']['3L'])
    
    bespooled1['3obj']['1L'].extend(bespooled2['3obj']['1L'])
    bespooled1['3obj']['2L'].extend(bespooled2['3obj']['2L'])
    bespooled1['3obj']['3L'].extend(bespooled2['3obj']['3L'])
    
    obj1['1L'] = bespooled1['1obj']['1L']
    obj1['2L'] = bespooled1['1obj']['2L']
    obj1['3L'] = bespooled1['1obj']['3L']
    
    obj2['1L'] = bespooled1['2obj']['1L']
    obj2['2L'] = bespooled1['2obj']['2L']
    obj2['3L'] = bespooled1['2obj']['3L']
    
    obj3['1L'] = bespooled1['3obj']['1L']
    obj3['2L'] = bespooled1['3obj']['2L']
    obj3['3L'] = bespooled1['3obj']['3L']
    
    bespooled['obj1'] = obj1
    bespooled['obj2'] = obj2
    bespooled['obj3'] = obj3
    
    return(bespooled)

## one lever one objective
def lake_conc_JDM_1L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100):    # Number of years simulated
    decisions= np.full((100), pollution_limit)

    return (decisions)

def lake_conc_JDM_2L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100):    # Number of years simulated
    decisions = np.empty((100))
    for j in range(2):
        lowind = (j+1)*50 - 50
        hihind = (j+1)*50

        decisions[lowind:hihind] = pollution_limit[j]

    return (decisions)

def lake_conc_JDM_3L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100):    # Number of years simulated
    decisions = np.empty((100))
    for j in range(3):
        lowind = (j+1)*33 - 33
        hihind = (j+1)*33

        decisions[lowind:hihind] = pollution_limit[j]

    return (decisions)
#
#
## Start by defining models that take the five slider bars' phosphorous discharge
## values and evaluate the effects on each objective (separately).
def lake_problem_JDM_uti_1L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100): # monte carlo sampling of natural inflows)
    Pcrit = root(lambda x: x**q/(1+x**q) - b*x, 0.01, 1.5)
    average_daily_P = np.zeros((nsamples,))
    decisions = lake_conc_JDM_1L(pollution_limit)

    nvars = len(decisions)
    X = np.zeros((nvars,))
    reliability = 0.0

    for _ in range(nsamples):
        X[0] = 0.0

        natural_inflows = np.random.lognormal(
                math.log(mean**2 / math.sqrt(stdev**2 + mean**2)),
                math.sqrt(math.log(1.0 + stdev**2 / mean**2)),
                size = nvars)

        for t in range(1,nvars):
            X[t] = (1-b)*X[t-1] + X[t-1]**q/(1+X[t-1]**q) + decisions[t-1] + natural_inflows[t-1]
            average_daily_P[t] += X[t]/float(nsamples)

        reliability += np.sum(X < Pcrit)/float(nsamples*nvars)

    max_P = np.max(average_daily_P)
    utility = np.sum(alpha*decisions*np.power(delta,np.arange(nvars)))
    # intertia = np.sum(np.diff(decisions) > -0.02)/float(nvars-1)

    return (utility)

def lake_problem_JDM_pho_1L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100): # monte carlo sampling of natural inflows)
    Pcrit = root(lambda x: x**q/(1+x**q) - b*x, 0.01, 1.5)
    average_daily_P = np.zeros((nsamples,))
    decisions = lake_conc_JDM_1L(pollution_limit)

    nvars = len(decisions)
    X = np.zeros((nvars,))
    reliability = 0.0

    for _ in range(nsamples):
        X[0] = 0.0

        natural_inflows = np.random.lognormal(
                math.log(mean**2 / math.sqrt(stdev**2 + mean**2)),
                math.sqrt(math.log(1.0 + stdev**2 / mean**2)),
                size = nvars)

        for t in range(1,nvars):
            X[t] = (1-b)*X[t-1] + X[t-1]**q/(1+X[t-1]**q) + decisions[t-1] + natural_inflows[t-1]
            average_daily_P[t] += X[t]/float(nsamples)

        reliability += np.sum(X < Pcrit)/float(nsamples*nvars)

    max_P = np.max(average_daily_P)
    utility = np.sum(alpha*decisions*np.power(delta,np.arange(nvars)))

    return (max_P)

def lake_problem_JDM_rel_1L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100): # monte carlo sampling of natural inflows)
    Pcrit = root(lambda x: x**q/(1+x**q) - b*x, 0.01, 1.5)
    average_daily_P = np.zeros((nsamples,))
    decisions = lake_conc_JDM_1L(pollution_limit)

    nvars = len(decisions)
    X = np.zeros((nvars,))
    reliability = 0.0

    for _ in range(nsamples):
        X[0] = 0.0

        natural_inflows = np.random.lognormal(
                math.log(mean**2 / math.sqrt(stdev**2 + mean**2)),
                math.sqrt(math.log(1.0 + stdev**2 / mean**2)),
                size = nvars)

        for t in range(1,nvars):
            X[t] = (1-b)*X[t-1] + X[t-1]**q/(1+X[t-1]**q) + decisions[t-1] + natural_inflows[t-1]
            average_daily_P[t] += X[t]/float(nsamples)

        reliability += np.sum(X < Pcrit)/float(nsamples*nvars)

    max_P = np.max(average_daily_P)
    utility = np.sum(alpha*decisions*np.power(delta,np.arange(nvars)))

    return (reliability)

def lake_problem_JDM_uti_2L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100): # monte carlo sampling of natural inflows)
    Pcrit = root(lambda x: x**q/(1+x**q) - b*x, 0.01, 1.5)
    average_daily_P = np.zeros((nsamples,))
    decisions = lake_conc_JDM_2L(pollution_limit)

    nvars = len(decisions)
    X = np.zeros((nvars,))
    reliability = 0.0

    for _ in range(nsamples):
        X[0] = 0.0

        natural_inflows = np.random.lognormal(
                math.log(mean**2 / math.sqrt(stdev**2 + mean**2)),
                math.sqrt(math.log(1.0 + stdev**2 / mean**2)),
                size = nvars)

        for t in range(1,nvars):
            X[t] = (1-b)*X[t-1] + X[t-1]**q/(1+X[t-1]**q) + decisions[t-1] + natural_inflows[t-1]
            average_daily_P[t] += X[t]/float(nsamples)

        reliability += np.sum(X < Pcrit)/float(nsamples*nvars)

    max_P = np.max(average_daily_P)
    utility = np.sum(alpha*decisions*np.power(delta,np.arange(nvars)))

    return (utility)

def lake_problem_JDM_pho_2L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100): # monte carlo sampling of natural inflows)
    Pcrit = root(lambda x: x**q/(1+x**q) - b*x, 0.01, 1.5)
    average_daily_P = np.zeros((nsamples,))
    decisions = lake_conc_JDM_2L(pollution_limit)

    nvars = len(decisions)
    X = np.zeros((nvars,))
    reliability = 0.0

    for _ in range(nsamples):
        X[0] = 0.0

        natural_inflows = np.random.lognormal(
                math.log(mean**2 / math.sqrt(stdev**2 + mean**2)),
                math.sqrt(math.log(1.0 + stdev**2 / mean**2)),
                size = nvars)

        for t in range(1,nvars):
            X[t] = (1-b)*X[t-1] + X[t-1]**q/(1+X[t-1]**q) + decisions[t-1] + natural_inflows[t-1]
            average_daily_P[t] += X[t]/float(nsamples)

        reliability += np.sum(X < Pcrit)/float(nsamples*nvars)

    max_P = np.max(average_daily_P)
    utility = np.sum(alpha*decisions*np.power(delta,np.arange(nvars)))

    return (max_P)

def lake_problem_JDM_rel_2L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100): # monte carlo sampling of natural inflows)
    Pcrit = root(lambda x: x**q/(1+x**q) - b*x, 0.01, 1.5)
    average_daily_P = np.zeros((nsamples,))
    decisions = lake_conc_JDM_2L(pollution_limit)

    nvars = len(decisions)
    X = np.zeros((nvars,))
    reliability = 0.0

    for _ in range(nsamples):
        X[0] = 0.0

        natural_inflows = np.random.lognormal(
                math.log(mean**2 / math.sqrt(stdev**2 + mean**2)),
                math.sqrt(math.log(1.0 + stdev**2 / mean**2)),
                size = nvars)

        for t in range(1,nvars):
            X[t] = (1-b)*X[t-1] + X[t-1]**q/(1+X[t-1]**q) + decisions[t-1] + natural_inflows[t-1]
            average_daily_P[t] += X[t]/float(nsamples)

        reliability += np.sum(X < Pcrit)/float(nsamples*nvars)

    max_P = np.max(average_daily_P)
    utility = np.sum(alpha*decisions*np.power(delta,np.arange(nvars)))

    return (reliability)

def lake_problem_JDM_uti_3L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100): # monte carlo sampling of natural inflows)
    Pcrit = root(lambda x: x**q/(1+x**q) - b*x, 0.01, 1.5)
    average_daily_P = np.zeros((nsamples,))
    decisions = lake_conc_JDM_3L(pollution_limit)

    nvars = len(decisions)
    X = np.zeros((nvars,))
    reliability = 0.0

    for _ in range(nsamples):
        X[0] = 0.0

        natural_inflows = np.random.lognormal(
                math.log(mean**2 / math.sqrt(stdev**2 + mean**2)),
                math.sqrt(math.log(1.0 + stdev**2 / mean**2)),
                size = nvars)

        for t in range(1,nvars):
            X[t] = (1-b)*X[t-1] + X[t-1]**q/(1+X[t-1]**q) + decisions[t-1] + natural_inflows[t-1]
            average_daily_P[t] += X[t]/float(nsamples)

        reliability += np.sum(X < Pcrit)/float(nsamples*nvars)

    max_P = np.max(average_daily_P)
    utility = np.sum(alpha*decisions*np.power(delta,np.arange(nvars)))

    return (utility)

def lake_problem_JDM_pho_3L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100): # monte carlo sampling of natural inflows)
    Pcrit = root(lambda x: x**q/(1+x**q) - b*x, 0.01, 1.5)
    average_daily_P = np.zeros((nsamples,))
    decisions = lake_conc_JDM_3L(pollution_limit)

    nvars = len(decisions)
    X = np.zeros((nvars,))
    reliability = 0.0

    for _ in range(nsamples):
        X[0] = 0.0

        natural_inflows = np.random.lognormal(
                math.log(mean**2 / math.sqrt(stdev**2 + mean**2)),
                math.sqrt(math.log(1.0 + stdev**2 / mean**2)),
                size = nvars)

        for t in range(1,nvars):
            X[t] = (1-b)*X[t-1] + X[t-1]**q/(1+X[t-1]**q) + decisions[t-1] + natural_inflows[t-1]
            average_daily_P[t] += X[t]/float(nsamples)

        reliability += np.sum(X < Pcrit)/float(nsamples*nvars)

    max_P = np.max(average_daily_P)
    utility = np.sum(alpha*decisions*np.power(delta,np.arange(nvars)))

    return (max_P)
#
# Start by defining models that take the five slider bars' phosphorous discharge
# values and evaluate the effects on each objective (separately).
def lake_problem_JDM_rel_3L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100): # monte carlo sampling of natural inflows)
    Pcrit = root(lambda x: x**q/(1+x**q) - b*x, 0.01, 1.5)
    average_daily_P = np.zeros((nsamples,))
    decisions = lake_conc_JDM_3L(pollution_limit)

    nvars = len(decisions)
    X = np.zeros((nvars,))
    reliability = 0.0

    for _ in range(nsamples):
        X[0] = 0.0

        natural_inflows = np.random.lognormal(
                math.log(mean**2 / math.sqrt(stdev**2 + mean**2)),
                math.sqrt(math.log(1.0 + stdev**2 / mean**2)),
                size = nvars)

        for t in range(1,nvars):
            X[t] = (1-b)*X[t-1] + X[t-1]**q/(1+X[t-1]**q) + decisions[t-1] + natural_inflows[t-1]
            average_daily_P[t] += X[t]/float(nsamples)

        reliability += np.sum(X < Pcrit)/float(nsamples*nvars)

    max_P = np.max(average_daily_P)
    utility = np.sum(alpha*decisions*np.power(delta,np.arange(nvars)))

    return (reliability)
#
## Measure score with one lever
#    
def score_1D_1L(pollution_lim):
    # This function compares the difference between the distance between a user-
    # selected point from the pareto front and the distance between the origin
    # and the pareto front. it returns a skill score in which "1" is on the Pareto
    # front and "0" is on the origin.
    reference = lake_problem_JDM_uti_1L((0.1))
    score = lake_problem_JDM_uti_1L(pollution_lim)
    naive = lake_problem_JDM_uti_1L((0))

    skillscore = (score-naive)/(reference-naive)
    return skillscore
#
def find_shortest_21(pt1, refset):
    dista = np.empty((1,1))
    distb = np.empty((1,1))
    for k in range(len(refset)):
        # If past the first two
        if (k > 1):
            # Find the euclidean distance between the proposed point and pt in refset
            dist_temp = distance.euclidean(pt1, refset[k,:])
            # Compare the distance to distance a: If less, compare to b
            if dist_temp < dista:
                # Compare the distance to distance b: If also less,
                if dist_temp < distb:
                    # If dista < distb
                    if dista < distb:
                        # Reset distb to dist temp
                        distb = dist_temp
                        # Reset ptb to the point in refset
                        ptb = refset[k,:]
                    # If distb < dista
                    else:
                        # Replace point a
                        dista = dist_temp
                        pta = refset[k,:]
            # if distance not less than distance a, compare to b. If less,
            elif dist_temp < distb:
                # Replace pointb with this point.
                distb = dist_temp
                ptb = refset[k,:]
            # If equal, pass
            elif dist_temp == dista:
                if dist_temp > distb:
                    pass
                else: # dist_temp == distb
                    pass
            # If equal to distb, pass
            elif dist_temp == distb:
                pass
        # If this is the second point
        elif (k == 1):
            # Set pta as the proposed point
            pta = refset[k,:]
            # Calculate the distance between point a and the reference set
            dista = distance.euclidean(pt1, pta)
        else:
            # We are at 0: Set ptb
             ptb = refset[k,:]
             distb = distance.euclidean(pt1, ptb)
    return(pta, ptb)
    
def find_shortest_22(pt1, refset):
    dista = np.empty((1,1))
    distb = np.empty((1,1))
    for k in range(len(refset)):
        # If past the first two
        if (k > 1):
            # Find the euclidean distance between the proposed point and pt in refset
            dist_temp = distance.euclidean(pt1, refset[k,:])
            # Compare the distance to distance a: If less, compare to b
            if dist_temp < dista:
                # Compare the distance to distance b: If also less,
                if dist_temp < distb:
                    # If dista < distb
                    if dista < distb:
                        # Reset distb to dist temp
                        distb = dist_temp
                        # Reset ptb to the point in refset
                        ptb = refset[k,:]
                    # If distb < dista
                    else:
                        # Replace point a
                        dista = dist_temp
                        pta = refset[k,:]
            # if distance not less than distance a, compare to b. If less,
            elif dist_temp < distb:
                # Replace pointb with this point.
                distb = dist_temp
                ptb = refset[k,:]
            # If equal, pass
            elif dist_temp == dista:
                if dist_temp > distb:
                    pass
                else: # dist_temp == distb
                    pass
            # If equal to distb, pass
            elif dist_temp == distb:
                pass
        # If this is the second point
        elif (k == 1):
            # Set pta as the proposed point
            pta = refset[k,:]
            # Calculate the distance between point a and the reference set
            dista = distance.euclidean(pt1, pta)
        else:
            # We are at 0: Set ptb
             ptb = refset[k,:]
             distb = distance.euclidean(pt1, ptb)
    return(pta, ptb)
    
def find_shortest_23(pt1, refset):
    dista = np.empty((1,1))
    distb = np.empty((1,1))
    for k in range(len(refset)):
        # If past the first two
        if (k > 1):
            # Find the euclidean distance between the proposed point and pt in refset
            dist_temp = distance.euclidean(pt1, refset[k,:])
            # Compare the distance to distance a: If less, compare to b
            if dist_temp < dista:
                # Compare the distance to distance b: If also less,
                if dist_temp < distb:
                    # If dista < distb
                    if dista < distb:
                        # Reset distb to dist temp
                        distb = dist_temp
                        # Reset ptb to the point in refset
                        ptb = refset[k,:]
                    # If distb < dista
                    else:
                        # Replace point a
                        dista = dist_temp
                        pta = refset[k,:]
            # if distance not less than distance a, compare to b. If less,
            elif dist_temp < distb:
                # Replace pointb with this point.
                distb = dist_temp
                ptb = refset[k,:]
            # If equal, pass
            elif dist_temp == dista:
                if dist_temp > distb:
                    pass
                else: # dist_temp == distb
                    pass
            # If equal to distb, pass
            elif dist_temp == distb:
                pass
        # If this is the second point
        elif (k == 1):
            # Set pta as the proposed point
            pta = refset[k,:]
            # Calculate the distance between point a and the reference set
            dista = distance.euclidean(pt1, pta)
        else:
            # We are at 0: Set ptb
             ptb = refset[k,:]
             distb = distance.euclidean(pt1, ptb)
    return(pta, ptb)

def find_shortest_31(pt1, refset):
    dista = np.empty((1,1))
    distb = np.empty((1,1))
    for k in range(len(refset)):
        # If past the first two
        if (k > 1):
            # Find the euclidean distance between the proposed point and pt in refset
            dist_temp = distance.euclidean(pt1, refset[k,:])
            # Compare the distance to distance a: If less, compare to b
            if dist_temp < dista:
                # Compare the distance to distance b: If also less,
                if dist_temp < distb:
                    # If dista < distb
                    if dista < distb:
                        # Reset distb to dist temp
                        distb = dist_temp
                        # Reset ptb to the point in refset
                        ptb = refset[k,:]
                    # If distb < dista
                    else:
                        # Replace point a
                        dista = dist_temp
                        pta = refset[k,:]
            # if distance not less than distance a, compare to b. If less,
            elif dist_temp < distb:
                # Replace pointb with this point.
                distb = dist_temp
                ptb = refset[k,:]
            # If equal, pass
            elif dist_temp == dista:
                if dist_temp > distb:
                    pass
                else: # dist_temp == distb
                    pass
            # If equal to distb, pass
            elif dist_temp == distb:
                pass
        # If this is the second point
        elif (k == 1):
            # Set pta as the proposed point
            pta = refset[k,:]
            # Calculate the distance between point a and the reference set
            dista = distance.euclidean(pt1, pta)
        else:
            # We are at 0: Set ptb
             ptb = refset[k,:]
             distb = distance.euclidean(pt1, ptb)
    return(pta, ptb)
    
def find_shortest_32(pt1, refset):
    dista = np.empty((1,1))
    distb = np.empty((1,1))
    for k in range(len(refset)):
        # If past the first two
        if (k > 1):
            # Find the euclidean distance between the proposed point and pt in refset
            dist_temp = distance.euclidean(pt1, refset[k,:])
            # Compare the distance to distance a: If less, compare to b
            if dist_temp < dista:
                # Compare the distance to distance b: If also less,
                if dist_temp < distb:
                    # If dista < distb
                    if dista < distb:
                        # Reset distb to dist temp
                        distb = dist_temp
                        # Reset ptb to the point in refset
                        ptb = refset[k,:]
                    # If distb < dista
                    else:
                        # Replace point a
                        dista = dist_temp
                        pta = refset[k,:]
            # if distance not less than distance a, compare to b. If less,
            elif dist_temp < distb:
                # Replace pointb with this point.
                distb = dist_temp
                ptb = refset[k,:]
            # If equal, pass
            elif dist_temp == dista:
                if dist_temp > distb:
                    pass
                else: # dist_temp == distb
                    pass
            # If equal to distb, pass
            elif dist_temp == distb:
                pass
        # If this is the second point
        elif (k == 1):
            # Set pta as the proposed point
            pta = refset[k,:]
            # Calculate the distance between point a and the reference set
            dista = distance.euclidean(pt1, pta)
        else:
            # We are at 0: Set ptb
             ptb = refset[k,:]
             distb = distance.euclidean(pt1, ptb)
    return(pta, ptb)
    
def find_shortest_33(pt1, refset):
    dista = np.empty((1,1))
    distb = np.empty((1,1))
    for k in range(len(refset)):
        # If past the first two
        if (k > 1):
            # Find the euclidean distance between the proposed point and pt in refset
            dist_temp = distance.euclidean(pt1, refset[k,:])
            # Compare the distance to distance a: If less, compare to b
            if dist_temp < dista:
                # Compare the distance to distance b: If also less,
                if dist_temp < distb:
                    # If dista < distb
                    if dista < distb:
                        # Reset distb to dist temp
                        distb = dist_temp
                        # Reset ptb to the point in refset
                        ptb = refset[k,:]
                    # If distb < dista
                    else:
                        # Replace point a
                        dista = dist_temp
                        pta = refset[k,:]
            # if distance not less than distance a, compare to b. If less,
            elif dist_temp < distb:
                # Replace pointb with this point.
                distb = dist_temp
                ptb = refset[k,:]
            # If equal, pass
            elif dist_temp == dista:
                if dist_temp > distb:
                    pass
                else: # dist_temp == distb
                    pass
            # If equal to distb, pass
            elif dist_temp == distb:
                pass
        # If this is the second point
        elif (k == 1):
            # Set pta as the proposed point
            pta = refset[k,:]
            # Calculate the distance between point a and the reference set
            dista = distance.euclidean(pt1, pta)
        else:
            # We are at 0: Set ptb
             ptb = refset[k,:]
             distb = distance.euclidean(pt1, ptb)
    return(pta, ptb)
    

refpho_2D1L = np.array((2.2838068014018602,
                       0.05493796716984372,
                       1.3705289339348998,
                       1.5219055837591027,
                       1.1163778593457294,
                       0.88998874108676396,
                       0.97861307850928714,
                       0.64442840816826252,
                       1.2747767142259534,
                       1.1914353588682975,
                       0.73063443563219632,
                       1.2124180547185788,
                       1.6416313879480622,
                       0.77470616226193845,
                       1.7744780538234977,
                       1.0549037013141671,
                       0.83047893073879731,
                       2.2726397752319754,
                       1.3147127358289739,
                       1.8101002166594755,
                       0.85197144760514121,
                       1.0027215584999265,
                       0.11540298634419441,
                       1.3489659074489251,
                       1.7326089683100154,
                       0.55814951902543641,
                       0.48320846617375129,
                       0.51340215408501388,
                       0.13763207929007931,
                       1.0387705696082825,
                       1.6885987316942583,
                       1.8527437243491942,
                       1.5684915086285653,
                       2.2668895200072678,
                       1.6056017965004901,
                       1.8919433884354528,
                       1.5313790885100846,
                       0.53564781824570562,
                       1.8411620150781987,
                       2.0592967751903424,
                       2.2021247812447191,
                       2.0047973055437494,
                       2.2610043766064041,
                       1.9771453880050607,
                       0.58992561833003898,
                       0.14667312742433256,
                       0.10918472503917809,
                       2.1370879984561908,
                       0.75196468453013565,
                       2.2639611490319562,
                       1.913472852625163,
                       2.2357722973335834,
                       2.1960095816491001,
                       2.125756461040293,
                       2.2769631870058151,
                       0.12376840766947873,
                       2.249426001574395,
                       0.14908172877524226,
                       0.43432797488153552,
                       0.46083486622891806,
                       2.0494517208156622,
                       2.0979463819337223,
                       0.05850611201856068,
                       0.62837585810810537,
                       2.2279418553670807,
                       2.2817556000727537,
                       1.9650970238888248,
                       2.1803631141363153,
                       2.0564890305836045,
                       0.15692067978485907,
                       2.1232946954166652,
                       2.2055185803627566,
                       2.1006097314274133,
                       2.2524397209847966,
                       2.1545475931323774,
                       0.29146556825061365,
                       1.9389679951491903,
                       0.12831551843225461,
                       0.092043981922079077,
                       2.2793463813242796,
                       2.1938065295256406,
                       2.1775456163914639,
                       2.0958001823569901,
                       2.1588754886796777,
                       2.0458573012501584,
                       2.2474116615854145,
                       2.1067738481793978,
                       0.18458408014682606,
                       0.61069717775638455,
                       2.1819283112682788,
                       2.1037584480885982,
                       0.41191408662704226,
                       2.0854767909993304,
                       2.0909719458117686,
                       2.2093323613856799,
                       2.2433274038080002,
                       2.1884086869525405,
                       2.0626978159282197,
                       0.10796971398476102,
                       2.1512251165559149,
                       0.11985152600447117,
                       2.1452788914688683,
                       2.1429910101582195,
                       2.0830215974331048,
                       2.0882883570458852,
                       0.44832394115761653,
                       2.233533128356171,
                       0.055441642838202229,
                       0.36829502341965653,
                       0.1754269743241163,
                       1.944418523295661,
                       2.1110326095077245,
                       2.1843245791302026,
                       1.7083902790663854,
                       2.2116631742663242,
                       0.35424705133046003,
                       2.0167407610843804,
                       0.12992129455460807,
                       2.1664478467197594,
                       0.38998768690873897,
                       0.096151140745611416,
                       2.0509649389665427,
                       2.1342419499480525,
                       1.5813070939395826,
                       1.7196775489994023,
                       1.5932499584644519,
                       2.2387089076236713,
                       0.30436882084749178,
                       2.1561211803345688,
                       2.1467658035335058,
                       0.10430366033968169,
                       2.1989502342113614,
                       0.3428492130166983,
                       2.2310597044118201,
                       0.098550776640482743,
                       2.1187707855962818,
                       0.3312851582410094,
                       2.0703984857016025,
                       0.40547803467512694,
                       2.1397271620808307,
                       2.175214283661445,
                       2.1643915692898257,
                       0.089084152742354372,
                       0.38030132239305359,
                       2.1910631366349516,
                       1.9011216021798223,
                       2.2660800543133943,
                       2.2584789564728656,
                       2.1026038748906237,
                       2.1092353782955953,
                       0.22926630937115292,
                       0.73559691790237669,
                       0.1037037882062665,
                       2.185696840818566,
                       2.1287110342512339,
                       0.59876584500975982,
                       2.0870572882934626,
                       2.0938195308382141,
                       0.27514162255642183,
                       0.069247456080352141,
                       2.0259806997479402,
                       0.13387910143611723,
                       0.26087058165292404,
                       2.1487042752581678,
                       2.2776156724947874,
                       2.1996991488481785,
                       2.1871355629189146,
                       2.1691678358476194,
                       2.1129861353704444,
                       1.6934647361938326,
                       0.07889712674831241,
                       0.073124051416001798,
                       2.1730479594479508,
                       2.1678636995520408,
                       2.054552558946952,
                       2.0425289565636442,
                       0.081383010292580715,
                       0.12054279560844262,
                       2.2413466592010232,
                       2.2236731810123076,
                       0.064968939831208383,
                       2.1081111839629112,
                       0.32050903667118158,
                       0.10064750960590127,
                       2.2202565981971043,
                       2.1761276448134144,
                       0.074552412729634712,
                       2.117203553893352,
                       2.078411009793725,
                       0.076665502839756774,
                       0.24125255283810923,
                       0.13451562480945231,
                       0.062769104790892677,
                       2.2454544981422457,
                       0.084144315378467394,
                       0.068066426433180241,
                       2.2183431145351062,
                       0.31396184411733141,
                       2.1320138968252649,
                       2.0660064045537041,
                       0.055))  # Insert reference set
refecon_2D1L = np.array((1.7347608882101524,
                        1.7769747529535853e-05,
                        0.48218534543344155,
                        0.48233196511438409,
                        0.48048183768625596,
                        0.47970133529584902,
                        0.48001461646024079,
                        0.47810230573962209,
                        0.48140364609297015,
                        0.48089006557835628,
                        0.47823213086533545,
                        0.48117207716360977,
                        0.48347026977243235,
                        0.47886801228920406,
                        0.48457640307509064,
                        0.48033983996957935,
                        0.47902966834392369,
                        1.6760977222886229,
                        0.48150458326391676,
                        0.48489246872753855,
                        0.47920492594091957,
                        0.48006263358595258,
                        0.26408346245571995,
                        0.4815691212488733,
                        0.48430734889193827,
                        0.47724877491042944,
                        0.47681860320981084,
                        0.47684297907746098,
                        0.33244659821833872,
                        0.48017752689818394,
                        0.48352459798785025,
                        0.48562569602609618,
                        0.48271552337373624,
                        1.646134924048438,
                        0.48330412227619812,
                        0.48566434552105525,
                        0.4825839794345233,
                        0.47712139534513848,
                        0.48522921512179407,
                        0.61883207097898718,
                        1.3136163687013762,
                        0.48892979159319505,
                        1.6154551956702881,
                        0.48798011498534688,
                        0.47727742597740586,
                        0.35509468312812137,
                        0.24297872858328784,
                        0.99069236181189191,
                        0.47840062242022152,
                        1.6311850491984674,
                        0.48622025609794739,
                        1.4860593546527108,
                        1.2839433615824407,
                        0.93576659846427668,
                        1.6978135901881131,
                        0.29119662238683225,
                        1.5559843575915868,
                        0.36116195526409811,
                        0.47564171347565659,
                        0.47621504041517332,
                        0.5722897394087465,
                        0.80208544210873611,
                        0.018309003937567805,
                        0.47763734670535513,
                        1.4457413382662534,
                        1.7232751101305568,
                        0.48766353209705043,
                        1.2046628382074343,
                        0.60595576790381334,
                        0.37801074359840525,
                        0.92402928378283855,
                        1.3315262284876579,
                        0.81492812884353627,
                        1.571213621965512,
                        1.0768208408103339,
                        0.47068555460288708,
                        0.48704909701586047,
                        0.30579046056049308,
                        0.1766188881177716,
                        1.7117537610444666,
                        1.2724291858260128,
                        1.1905741151657312,
                        0.7910472482098706,
                        1.0986796605145313,
                        0.55583217974341614,
                        1.5454955578482419,
                        0.84342751085561707,
                        0.42562582444903957,
                        0.47755281717780301,
                        1.2133681852464628,
                        0.82964636055139118,
                        0.47556617440465609,
                        0.74096078558712919,
                        0.76824832274305055,
                        1.3504672131557833,
                        1.5247676543849433,
                        1.24489469445067,
                        0.63470959498646939,
                        0.23836684195653057,
                        1.0604162047359427,
                        0.27943442276466751,
                        1.031264240466234,
                        1.019572026668595,
                        0.73014728790076899,
                        0.75520237996861872,
                        0.47597149182128401,
                        1.4747105444221069,
                        0.0030688249616983893,
                        0.47456719763770677,
                        0.41278036988737532,
                        0.48719431604436886,
                        0.86444601024467882,
                        1.2247584884046332,
                        0.48371019547097527,
                        1.362355011167609,
                        0.47405707017950227,
                        0.49061916234724512,
                        0.31119331443631648,
                        1.1357823480141114,
                        0.47502043774150676,
                        0.19293010919952186,
                        0.57981253787828646,
                        0.97715936597229935,
                        0.48291862197268776,
                        0.48406386765995407,
                        0.48294226667299345,
                        1.5008698559249325,
                        0.47218315953142065,
                        1.0845760041035859,
                        1.0383857751170966,
                        0.22482229820584368,
                        1.2984375195932958,
                        0.4739667691482225,
                        1.461327025338323,
                        0.20270026357187657,
                        0.90166457374231967,
                        0.47331722515278729,
                        0.67049419514889197,
                        0.475079583156365,
                        1.0039776382409722,
                        1.1779772248118956,
                        1.1256744296407741,
                        0.1644493745994651,
                        0.47482401139194824,
                        1.2581694875712308,
                        0.48606191476573796,
                        1.6423856141461455,
                        1.6028403931467137,
                        0.82364970530483816,
                        0.85600691981307053,
                        0.46041400132511134,
                        0.47828874888008427,
                        0.22295317826051858,
                        1.2312900946010237,
                        0.94977317878195433,
                        0.47744881921502452,
                        0.74993278367863181,
                        0.78118383834921779,
                        0.46985787520615868,
                        0.073553165859438413,
                        0.49280888921593813,
                        0.32147481281549201,
                        0.46806157215150584,
                        1.047678152021831,
                        1.7021443374764467,
                        1.3025794419772325,
                        1.2392222757506894,
                        1.1488855437222081,
                        0.87395347209121199,
                        0.48366047170540349,
                        0.11914148123854749,
                        0.09230384518858703,
                        1.1687471631286679,
                        1.1428530735848277,
                        0.59673826658031137,
                        0.54038475572535083,
                        0.13052749057525204,
                        0.28196375231222792,
                        1.5140312260077036,
                        1.4238397846773421,
                        0.051498910184598214,
                        0.84981180685996238,
                        0.47314383260206,
                        0.21097785972850294,
                        1.4070476433766101,
                        1.1838304760054732,
                        0.098748030663677169,
                        0.89436657996264679,
                        0.70885290474834839,
                        0.10850793253942394,
                        0.46399555138901721,
                        0.32348925308676679,
                        0.040119131086953495,
                        1.5354856244039545,
                        0.14299534909763437,
                        0.067602675803280998,
                        1.3969610400902082,
                        0.4723174295888411,
                        0.96634738182447055,
                        0.64978341469059053,
                        0.0))

refecon_3D1L = np.array((0.0,
                        1.7186344574863024,
                        1.0728223799335575e-05,
                        1.7347608880997518,
                        0.0054369874662749057,
                        0.48153903960415279,
                        0.48058239095164623,
                        0.47826640018107669,
                        0.48129862708947757,
                        0.48057522039930251,
                        0.47829698112110336,
                        0.48393074247269796,
                        0.47789493909856595,
                        0.47916387779078279,
                        0.47939674204731492,
                        0.48187679117213328,
                        0.47902339600122007,
                        0.48385901621867056,
                        0.48222074088626837,
                        0.4795044978634242,
                        0.47968279698284072,
                        0.48289983988294366,
                        0.58059332757330062,
                        0.59279872846732362,
                        0.47974149451558828,
                        0.49736575624647855,
                        0.48079279899997956,
                        0.96014503073433055,
                        1.2668303438749375,
                        0.50259156588376863,
                        0.48266715632438123,
                        0.47833052803885262,
                        0.48224579185338262,
                        1.3795271469480557,
                        0.64298935141465308,
                        0.48427213114056417,
                        0.48299257726207084,
                        0.50928495834496756,
                        0.47136302346797576,
                        0.4855245971564997,
                        1.1896940699435683,
                        0.48599437097663817,
                        1.2844680138807774,
                        0.47716431962660832,
                        0.47574012904099749,
                        0.48251580660784893,
                        0.4792948937027916,
                        0.48960910898646937,
                        0.49316523158989861,
                        1.3629680241531816,
                        0.48578951003389509,
                        1.0639713864566942,
                        0.34636761355324336,
                        1.0181802714767911,
                        0.49897774484202584,
                        0.49605357371716186,
                        0.48115201689938514,
                        0.50520800098263774,
                        0.62905706564113972,
                        0.47447857671980548,
                        1.395034037960851,
                        0.47883775272738544,
                        0.93486630989291675,
                        0.48423228510126687,
                        0.48709677700885645,
                        1.4758019252542647,
                        0.67585475199016487,
                        0.48181681306462376,
                        0.47638981693446436,
                        0.53135238473510238,
                        1.6940279360657382,
                        0.84442600808454538,
                        1.4953150772247905,
                        1.5628868080574769,
                        0.85942545247409907,
                        0.087970438763887215,
                        0.4887125861365067,
                        1.2178333423945797,
                        1.1140562819729949,
                        0.4806140232844559,
                        1.1409837139855203,
                        0.49525041649978541,
                        0.031931998777586304,
                        1.1631724452159768,
                        0.4767942260687591,
                        0.48451588890065522,
                        1.3444264855052344,
                        0.53649315267086062,
                        0.54368755854775341,
                        0.47872972728587637,
                        1.030772050466082,
                        1.175144284021796,
                        0.50074549385808864,
                        0.48451231511591397,
                        0.47722872336755889,
                        0.48663079665419023,
                        0.4875007476159145,
                        1.0856293381590021,
                        0.87220463727865538,
                        1.5854805373721121,
                        0.058361161019705392,
                        0.53017506839794826,
                        0.57086679979386401,
                        0.49419432012385761,
                        0.46862203097366267,
                        0.48803310996689442,
                        1.6072337060077582,
                        0.52343466377556425,
                        0.78470921669304683,
                        0.17840907138005066,
                        0.51136835388599777,
                        0.69211450765649496,
                        0.48268574310582202,
                        0.56634249179151608,
                        0.47611260592390758,
                        0.59438403730275824,
                        0.47530072306368704,
                        0.48319619781658935,
                        0.22594918730024896,
                        0.32533129711133063,
                        0.52567565175612363,
                        0.60088925677959781,
                        0.55290203353708411,
                        0.7012198416598393,
                        0.48460264053977581,
                        0.48078043317007985,
                        1.3095663590712028,
                        0.54648324467320319,
                        0.4727280179353533,
                        1.5399091567172705,
                        0.89807160565281485,
                        0.5573212816353601,
                        0.57262881464251369,
                        0.24584481336929279,
                        0.30057093895838499,
                        1.3306681054396368,
                        0.87884146336538405,
                        0.038557368021228083,
                        0.1287915701460999,
                        0.48536913748172972,
                        0.66611617903117315,
                        0.61822507193643594,
                        0.51415436586040242,
                        0.53861742310256844,
                        0.48373951142364552,
                        0.48512501934095176,
                        1.0905879868681339,
                        0.47510777939257431,
                        0.10970919426813505,
                        0.48022015852757172,
                        0.82367470189591441,
                        1.2297965834843012,
                        0.88567126239108962,
                        0.56066886514077274,
                        0.79183259994181487,
                        0.92664150809409818,
                        0.48179932483032994,
                        1.6237745937185128,
                        0.5777196134891408,
                        0.48336827168714308,
                        0.48721747403946924,
                        0.80886195251480753,
                        0.15635698535163767,
                        0.65878816441187593,
                        0.48719004542375749,
                        0.49093883101239066,
                        0.74063211627454151,
                        1.4171124959303305,
                        0.4905675279369856,
                        0.51931060326679479,
                        0.91106759853983255,
                        1.5501575535695156,
                        1.1660108364021635,
                        0.54842198359508654,
                        0.28389800648153529,
                        0.48853456357877534,
                        0.61236028701095258,
                        0.48802345493062771,
                        1.6440325053950979,
                        0.5000248968999853,
                        0.10436738523652958,
                        1.2488009020162085,
                        0.77583470106876484,
                        0.91812787757594183,
                        1.5936749636716585,
                        0.49224271879250053,
                        0.83730348782340369,
                        0.47581789054039275,
                        0.51267194166229724,
                        0.50211070710379846,
                        0.39819237007380148,
                        1.4580791495410024,
                        0.96938267677540413,
                        0.36138024109612871,
                        0.30889423835102414,
                        0.38438000369138509,
                        0.49109813019481152,
                        0.13708652455889331,
                        1.7128927315323013,
                        0.52562925146240003,
                        0.47410074382190087))
refrel_3D1L = np.array((1.0,
                       0.070000000000000007,
                       1.0000000000000007,
                       0.070000000000000007,
                       1.0000000000000007,
                       0.91030000000000033,
                       0.93040000000000023,
                       0.97830000000000072,
                       0.92049999999999998,
                       0.93830000000000002,
                       0.97240000000000038,
                       0.86520000000000008,
                       0.98530000000000051,
                       0.95810000000000017,
                       0.95340000000000014,
                       0.90159999999999973,
                       0.9628000000000001,
                       0.8733000000000003,
                       0.89669999999999972,
                       0.9484999999999999,
                       0.94570000000000032,
                       0.88329999999999986,
                       0.3523,
                       0.33150000000000035,
                       0.94160000000000044,
                       0.68520000000000025,
                       0.92400000000000038,
                       0.13769999999999996,
                       0.093799999999999967,
                       0.63779999999999948,
                       0.88589999999999991,
                       0.96850000000000025,
                       0.89300000000000002,
                       0.08889999999999991,
                       0.27110000000000006,
                       0.85959999999999992,
                       0.87849999999999995,
                       0.59020000000000017,
                       1.0000000000000007,
                       0.83690000000000009,
                       0.10000000000000007,
                       0.82699999999999996,
                       0.0899999999999999,
                       0.98710000000000064,
                       0.99510000000000065,
                       0.89280000000000015,
                       0.9552000000000006,
                       0.77289999999999981,
                       0.73259999999999958,
                       0.0899999999999999,
                       0.83139999999999992,
                       0.1200000000000003,
                       1.0000000000000007,
                       0.12699999999999995,
                       0.66800000000000026,
                       0.69680000000000031,
                       0.91989999999999994,
                       0.61559999999999959,
                       0.28480000000000022,
                       0.99930000000000063,
                       0.081899999999999931,
                       0.9654000000000007,
                       0.14000000000000001,
                       0.85940000000000039,
                       0.81929999999999992,
                       0.07999999999999996,
                       0.24260000000000054,
                       0.90420000000000011,
                       0.99030000000000074,
                       0.47840000000000021,
                       0.070000000000000007,
                       0.16229999999999989,
                       0.07999999999999996,
                       0.070000000000000007,
                       0.15999999999999992,
                       1.0000000000000007,
                       0.78429999999999989,
                       0.10000000000000007,
                       0.11000000000000008,
                       0.92610000000000015,
                       0.11000000000000008,
                       0.70810000000000006,
                       1.0000000000000007,
                       0.10700000000000007,
                       0.9905000000000006,
                       0.85300000000000009,
                       0.0899999999999999,
                       0.46409999999999979,
                       0.43820000000000042,
                       0.96730000000000038,
                       0.1201000000000003,
                       0.10040000000000009,
                       0.65560000000000018,
                       0.85240000000000005,
                       0.98650000000000082,
                       0.81989999999999941,
                       0.80450000000000021,
                       0.1155000000000002,
                       0.15829999999999994,
                       0.070000000000000007,
                       1.0000000000000007,
                       0.48700000000000077,
                       0.3698999999999999,
                       0.71799999999999986,
                       1.0000000000000007,
                       0.79220000000000013,
                       0.070000000000000007,
                       0.51269999999999982,
                       0.18520000000000006,
                       1.0000000000000007,
                       0.57430000000000014,
                       0.23099999999999982,
                       0.88560000000000039,
                       0.38060000000000044,
                       0.99480000000000068,
                       0.32920000000000005,
                       0.99790000000000068,
                       0.87789999999999979,
                       1.0000000000000007,
                       1.0000000000000007,
                       0.50170000000000015,
                       0.31839999999999991,
                       0.41249999999999987,
                       0.22639999999999991,
                       0.84930000000000017,
                       0.92650000000000032,
                       0.0899999999999999,
                       0.42840000000000039,
                       0.99980000000000069,
                       0.078999999999999973,
                       0.15000000000000011,
                       0.40120000000000011,
                       0.36579999999999968,
                       1.0000000000000007,
                       1.0000000000000007,
                       0.0899999999999999,
                       0.15290000000000006,
                       1.0000000000000007,
                       1.0000000000000007,
                       0.84309999999999996,
                       0.25010000000000016,
                       0.29750000000000032,
                       0.55960000000000021,
                       0.45509999999999989,
                       0.87430000000000008,
                       0.84509999999999963,
                       0.1112000000000001,
                       0.99780000000000069,
                       1.0000000000000007,
                       0.94050000000000011,
                       0.16999999999999993,
                       0.10000000000000007,
                       0.15010000000000009,
                       0.39250000000000029,
                       0.1801999999999998,
                       0.14020000000000002,
                       0.90640000000000021,
                       0.070000000000000007,
                       0.35689999999999983,
                       0.87359999999999982,
                       0.80810000000000004,
                       0.1762999999999999,
                       1.0000000000000007,
                       0.25729999999999981,
                       0.81249999999999956,
                       0.75389999999999979,
                       0.20359999999999998,
                       0.07999999999999996,
                       0.76369999999999993,
                       0.53200000000000025,
                       0.14860000000000009,
                       0.074600000000000055,
                       0.10510000000000005,
                       0.42370000000000013,
                       1.0000000000000007,
                       0.78720000000000001,
                       0.30350000000000005,
                       0.79969999999999986,
                       0.070000000000000007,
                       0.66230000000000022,
                       1.0000000000000007,
                       0.099900000000000072,
                       0.18970000000000037,
                       0.14440000000000008,
                       0.070000000000000007,
                       0.74329999999999985,
                       0.16809999999999986,
                       0.99380000000000068,
                       0.56960000000000033,
                       0.64380000000000004,
                       1.0000000000000007,
                       0.07999999999999996,
                       0.13109999999999983,
                       1.0000000000000007,
                       1.0000000000000007,
                       1.0000000000000007,
                       0.75229999999999975,
                       1.0000000000000007,
                       0.070000000000000007,
                       0.5022000000000002,
                       0.99980000000000069))
refpho_3D1L = np.array((0.055,
                       2.2807600939506401,
                       0.05492031761322029,
                       2.2838129855030949,
                       0.055953805733346032,
                       1.3469127597860788,
                       1.1224553773847108,
                       0.63882091318936096,
                       1.2299446865027972,
                       1.0406590339233615,
                       0.69151947867197772,
                       1.720223781305728,
                       0.57544647919966696,
                       0.84270922117053104,
                       0.89289031039502009,
                       1.4078776496428331,
                       0.79218481482276659,
                       1.6617968518794128,
                       1.4421889858047889,
                       0.94654199243053472,
                       0.95873992187114265,
                       1.5672414807830555,
                       2.0510914064902717,
                       2.0537551597698651,
                       1.0133441266425087,
                       2.0316066683242022,
                       1.1966783154350076,
                       2.1308812214386799,
                       2.1926479160561567,
                       2.0335071888283447,
                       1.529811932910681,
                       0.73059087054886163,
                       1.4873473892983775,
                       2.2150125869139718,
                       2.0644630188758777,
                       1.7599065079160501,
                       1.6023645550230439,
                       2.0355304337422284,
                       0.30197555704360396,
                       1.8685280054678826,
                       2.1772082910186956,
                       1.9053072500574559,
                       2.1962278193376408,
                       0.53371874035517386,
                       0.43692151345661828,
                       1.4723320915052394,
                       0.86913083672853808,
                       2.0094952027995601,
                       2.0264016900814181,
                       2.2117558959138837,
                       1.8867712854321526,
                       2.1519232553813619,
                       0.14333120819974662,
                       2.1425001882049481,
                       2.0325745362316643,
                       2.0307182843127198,
                       1.2256810812262382,
                       2.0345208024289345,
                       2.0615724784633369,
                       0.3705510389612065,
                       2.2180085705124197,
                       0.77011620189984753,
                       2.1255118960809249,
                       1.7324647524185643,
                       1.9321534101834719,
                       2.2338873789117786,
                       2.0717109667364948,
                       1.3671050419866053,
                       0.49442205537498007,
                       2.0405563332915881,
                       2.2759448531282014,
                       2.1069986127801532,
                       2.2375256491170621,
                       2.250667268624833,
                       2.1100476547832399,
                       0.072216053184703491,
                       2.0009797810736387,
                       2.1829020480713952,
                       2.1620947167834172,
                       1.1649887939058543,
                       2.1675668051934833,
                       2.0297170811167144,
                       0.061032745127599472,
                       2.1720596216505892,
                       0.50326393742335818,
                       1.797820354495641,
                       2.2079516704457709,
                       2.0415798264905338,
                       2.0432591986728572,
                       0.74635622722146477,
                       2.1453617950601607,
                       2.1743140280905946,
                       2.0333866159828613,
                       1.7848297161263293,
                       0.55697301897298523,
                       1.9224070586701623,
                       1.9595267938546177,
                       2.1562818235697931,
                       2.1126555889664091,
                       2.2551489867213763,
                       0.066347992560349831,
                       2.0401826287685823,
                       2.0490902249847474,
                       2.028296007083954,
                       0.26394102714170165,
                       1.9875244721243026,
                       2.2593429556569546,
                       2.0388502383647524,
                       2.0944542378231579,
                       0.092577501360909975,
                       2.0359452607368831,
                       2.0748758952360591,
                       1.5394500753844345,
                       2.0480433351916805,
                       0.45774570555966793,
                       2.0540625990026586,
                       0.39955501637929164,
                       1.6197071229305811,
                       0.10465740361966487,
                       0.13509819472239201,
                       2.0393371817905313,
                       2.0554759372925844,
                       2.0451214712911034,
                       2.0769311608991963,
                       1.8164558830070985,
                       1.1660745427957595,
                       2.2011876627087976,
                       2.0437201991838414,
                       0.32359854919269232,
                       2.2462944177750304,
                       2.1180784751559343,
                       2.0460539253431298,
                       2.0494490155265757,
                       0.11013595235285495,
                       0.12651073290818599,
                       2.2052207066038458,
                       2.1139973884319696,
                       0.062368631471121462,
                       0.08098194716696995,
                       1.8348141055006431,
                       2.0693560163732365,
                       2.0593118667725734,
                       2.0366975222185779,
                       2.0418944777019274,
                       1.6513292321130557,
                       1.8505251715234028,
                       2.1572254569103366,
                       0.39796700517950107,
                       0.076919711683641992,
                       1.020844978736112,
                       2.1026664756637645,
                       2.1852728166475215,
                       2.1155092800621422,
                       2.0468343463366359,
                       2.0960362317743866,
                       2.1239073644566382,
                       1.3648207195081279,
                       2.2625036459110426,
                       2.050488914371098,
                       1.6351530437506907,
                       1.966592465112611,
                       2.0994647585923554,
                       0.087278715236057638,
                       2.0679423300204465,
                       1.961851701960267,
                       2.0204863763751906,
                       2.0852295523243054,
                       2.2222839744392342,
                       2.0151341682732951,
                       2.037815607450697,
                       2.120808864252913,
                       2.2482257110461012,
                       2.1724323919437913,
                       2.0442637158689241,
                       0.12113613200400333,
                       1.9948981626316473,
                       2.0580366439578137,
                       1.9807630183486822,
                       2.266576030579889,
                       2.0330731227248591,
                       0.075659511483638933,
                       2.1889345663326631,
                       2.0926528880421715,
                       2.1222847408154575,
                       2.2566763466242499,
                       2.0239097723157653,
                       2.1054086974274808,
                       0.45445097511997862,
                       2.0362818079329514,
                       2.0338234217341773,
                       0.16665556711709631,
                       2.2302907408265291,
                       2.1328357077954223,
                       0.14908074915446107,
                       0.12930699438835366,
                       0.15967138218035043,
                       2.0211423629956222,
                       0.082805917694991168,
                       2.2797300666726428,
                       2.0392286942072864,
                       0.34598080477333171))

refpho_2D2L = np.array((0.055028868664724485,
                        2.2836809640405962,
                        0.9519539319046374,
                        0.72928002255980373,
                        1.379652848277555,
                        1.4793637456578235,
                        1.106425535085324,
                        0.6634269091409476,
                        0.56158481907948765,
                        1.6825078096048032,
                        1.8283683797839776,
                        1.5597162226849235,
                        1.2580174195999638,
                        1.1408198168099535,
                        1.2474506572584041,
                        0.49954875486630562,
                        0.36329214398151144,
                        0.39026717008482886,
                        0.30202865655929162,
                        0.44713683510691105,
                        1.830571515548731,
                        1.6232640688815541,
                        1.8944825514081745,
                        1.6151314135022772,
                        1.6800895141229584,
                        0.4606062076202449,
                        2.1821721886007519,
                        0.12102867590841743,
                        2.2528206300447913,
                        0.11519415751086724,
                        2.0955869037827588,
                        2.1868063214613054,
                        0.15518061618684942,
                        2.1771944905982625,
                        2.1456585752673667,
                        2.1120196048386926,
                        2.1981881394745777,
                        2.0610475581810186,
                        0.073054667807681994,
                        2.0898975024106545,
                        2.104259238996653,
                        2.1729269633865931,
                        1.9443960990802731,
                        2.027681475071581,
                        0.075334910322497381,
                        2.1165083554712716,
                        2.194785550698076,
                        2.1937115727382901,
                        2.2213153673815107,
                        2.1894877311267549,
                        2.2570846294312528,
                        2.0750569971024704,
                        0.14778985927546109,
                        1.9568917222412046,
                        2.0785385393503431,
                        2.2244515543424135,
                        2.2707536177146928,
                        0.26111032036232923,
                        2.1792651983481663,
                        0.24084040642401422,
                        2.0827088964738878,
                        0.05811907376117538,
                        0.12454780334770174,
                        0.1783323728961467,
                        2.0390538004483765,
                        0.069147788288044174,
                        2.2143756369038625,
                        2.1190433669996835,
                        2.2315014375543085,
                        1.1259217952814806,
                        2.1624097672831835,
                        2.08468473475078,
                        2.2601690846660887,
                        0.10939301253780327,
                        2.1558494039621503,
                        2.2656877690407282,
                        0.13752327793227251,
                        2.2077064215516753,
                        2.1087354738387569,
                        2.1321194045413261,
                        0.11158725919423169,
                        2.2675877697840643,
                        2.1249879327572057,
                        0.18724713326532333,
                        2.2761820108144355,
                        2.2409970006723823,
                        0.27114529629851863,
                        2.1136615575577635,
                        1.9988922977866623,
                        2.1348853122955815,
                        0.12781412582630503,
                        2.1491838732330133,
                        2.2351819125758561,
                        0.10302240255776844,
                        1.917027024561484,
                        2.0427447476899658,
                        0.29208248210682947,
                        1.9936838883867485,
                        0.083155843761025056,
                        2.1031509066710363,
                        2.1069781121926643,
                        2.1237813140079611,
                        2.1891149637229668,
                        2.2274128860642533,
                        0.20497765166609247,
                        2.2117914129647454,
                        0.059956223475653152,
                        0.17081641429594732,
                        0.099499888498563061,
                        0.089157062522781882,
                        2.0637755146697718,
                        2.2510621325773186,
                        2.0678531053171132,
                        0.20010024964968212,
                        2.0868232742428718,
                        0.061834971635362196,
                        2.2340590223289545,
                        2.0567045148215626,
                        0.15894486273877964,
                        2.1615418324536528,
                        2.2494948829874337,
                        2.2206009523518233,
                        2.2032546155844672,
                        2.2475793971857487,
                        0.13305250245877018,
                        2.2102876494265216,
                        2.2424600137057649,
                        2.1381109632511608,
                        2.1533984078496591,
                        0.2354824541685841,
                        0.14025374848079705,
                        0.16592033147488069,
                        2.1432509797603174,
                        0.08107187468313494,
                        2.0159448397412438,
                        2.0250628021011567,
                        2.2011233486154165,
                        0.22194349268294683,
                        0.17518431079345309,
                        2.2061773358847736,
                        0.076888034858743001,
                        2.1526250162369571,
                        2.2179009222416743,
                        2.0990495762433401,
                        0.092635979694091791,
                        0.19035332329503624,
                        0.21595005931071085,
                        1.9844248385294008,
                        2.2753182702217294,
                        2.0424238933803109,
                        2.2640869840061502,
                        2.0766470401996866,
                        2.1660610466051891,
                        1.975538674664898,
                        2.0176980596876688,
                        2.1712283264919026,
                        2.0460365997382413,
                        2.1404046515535913,
                        2.121195402924462,
                        2.1364657992437959,
                        2.2724581787371503,
                        2.2828168505897812,
                        0.1320937228907805,
                        2.1279966569660775,
                        2.142507541753226,
                        0.10763530750944608,
                        0.097880398752970277,
                        2.206878583759122,
                        2.2392680133705372,
                        0.086504598876670849,
                        2.0102041039345568,
                        2.2375442715183365,
                        2.0881080694142793,
                        1.9138364564753605,
                        0.1626700926563717,
                        2.2184086373044547,
                        0.07919503075460356,
                        2.0495554748457496,
                        2.0519289638054548,
                        1.976660938992876,
                        2.0675889127094429,
                        2.1700918603832644,
                        2.1581212159748246,
                        2.2582458912826642,
                        2.2803918459932415,
                        0.10608038676664786,
                        2.0028240333982779,
                        2.2322890924055367,
                        0.085067939814674698,
                        2.2779796277217801,
                        2.2475269568264271,
                        1.8944865785637137,
                        2.1302925391188361,
                        0.093871886100716229,
                        2.0983230371397563,
                        2.1291660245665103,
                        0.068531554119694194,
                        2.0775240416328784,
                        0.067602479959175107,
                        2.150333695832519))  # Insert reference set
refecon_2D2L = np.array((0.00022669680252903574,
                         1.7345191271985436,
                         0.48082322391372229,
                         0.48051086295704687,
                         0.48266387820516155,
                         0.48314512239892959,
                         0.48116077090774045,
                         0.47961178890808953,
                         0.47903338897904441,
                         0.4843029896652743,
                         0.48493360384820433,
                         0.48343578082035138,
                         0.48232206711690317,
                         0.48154618036749458,
                         0.48196761456463111,
                         0.47897523012450222,
                         0.47749751493529075,
                         0.4777658343251529,
                         0.4758150545138195,
                         0.47812482861945393,
                         0.48544223920177587,
                         0.48360838027051972,
                         0.4854984104230427,
                         0.48350044148855664,
                         0.48372301269052115,
                         0.47883286891664018,
                         1.2120181943891588,
                         0.28181309262430876,
                         1.5729392391198067,
                         0.26103414293930882,
                         0.78570008485312914,
                         1.2301778503491738,
                         0.36947321465754479,
                         1.1879759855190846,
                         1.032241245079752,
                         0.86705501343702185,
                         1.2941262301697249,
                         0.64545632278251808,
                         0.082236717145034291,
                         0.76428572826726948,
                         0.82665008490803427,
                         1.1664566159270282,
                         0.48681106787630551,
                         0.56710198430440606,
                         0.10009164800358009,
                         0.88837485889108314,
                         1.2775444874031714,
                         1.2675219792255301,
                         1.4127188145817917,
                         1.2521470131174492,
                         1.5959183203748992,
                         0.68151539796322136,
                         0.35728207972135678,
                         0.48736483039842382,
                         0.71428909232583071,
                         1.4269092340973302,
                         1.6613886807957887,
                         0.47461084068780018,
                         1.1962748784996917,
                         0.47107197224080199,
                         0.72513623640823699,
                         0.012343876781533029,
                         0.29240688631715922,
                         0.41810693225684137,
                         0.58054893512699868,
                         0.071090295602874082,
                         1.374119389334499,
                         0.90420749509078313,
                         1.4570420535926407,
                         0.48117660818567454,
                         1.1166413163797937,
                         0.73728213239802809,
                         1.6106318711529028,
                         0.24002161107622447,
                         1.0816145370102064,
                         1.6398074232860722,
                         0.32975820828158586,
                         1.3428533903985347,
                         0.84723844627139699,
                         0.96254746024253723,
                         0.2515992481786406,
                         1.6509738634941056,
                         0.93305121528035906,
                         0.43030054065238521,
                         1.6934289405638896,
                         1.5092987969293696,
                         0.4755380738625104,
                         0.87761286224740498,
                         0.52533833370318095,
                         0.97807547562443642,
                         0.30405625888447235,
                         1.0500297081036585,
                         1.4828909160043497,
                         0.21497885352254112,
                         0.48660417395234462,
                         0.59864809797008434,
                         0.47556171798223901,
                         0.51280267495513809,
                         0.13729348078147874,
                         0.81582607182520217,
                         0.84534429882225215,
                         0.92080590694186915,
                         1.2419403348733358,
                         1.4386082587908093,
                         0.44603613842580414,
                         1.3623084184540448,
                         0.023920928624773848,
                         0.40251440466320709,
                         0.20439036908187638,
                         0.16095158142790403,
                         0.65546343802813078,
                         1.5627551432919109,
                         0.66971083816343124,
                         0.44133602314258441,
                         0.74850460987252743,
                         0.03310286730422235,
                         1.4716005627391862,
                         0.62714132445182857,
                         0.38336240886527595,
                         1.1055619596048281,
                         1.5519922007477218,
                         1.4004050455690378,
                         1.3117464355658401,
                         1.5425809496835754,
                         0.31957750976224775,
                         1.3535588436616741,
                         1.5205652383258292,
                         0.99562542250956054,
                         1.0721011880321012,
                         0.46672122864116999,
                         0.33987798936460506,
                         0.39595335448429753,
                         1.0201914286369902,
                         0.12468242076976226,
                         0.54689086346488835,
                         0.56030694699434558,
                         1.306552779777179,
                         0.4635058215719835,
                         0.41237436239456249,
                         1.3254202574098546,
                         0.11033868385552949,
                         1.0617345439660795,
                         1.3848062128240448,
                         0.80658976162805496,
                         0.16967646144960646,
                         0.43406995860392311,
                         0.45292033110164792,
                         0.50160718834117779,
                         1.6778435666128784,
                         0.58289770961933407,
                         1.6277192407068943,
                         0.69177955757030019,
                         1.1287892009382834,
                         0.49106544294386234,
                         0.55324140871940153,
                         1.1602768191214938,
                         0.60441491566415262,
                         1.0034116100639738,
                         0.91194211997143548,
                         0.98394204296952414,
                         1.675326813537318,
                         1.7270406633191151,
                         0.31122376656687006,
                         0.94288346460981487,
                         1.0125997699888243,
                         0.22820181379254553,
                         0.1953810740024681,
                         1.3303505217129552,
                         1.4978960789889679,
                         0.15086148420701817,
                         0.53711218601329269,
                         1.4933731981917726,
                         0.75794874707595572,
                         0.48621968988967529,
                         0.38665753577911188,
                         1.3921801300470213,
                         0.11833870476260533,
                         0.61376115667489195,
                         0.61740396936850162,
                         0.49255844772721868,
                         0.66390413758817357,
                         1.1481981120737597,
                         1.0948403958921737,
                         1.5976347383576652,
                         1.7060401956775326,
                         0.22372552630376927,
                         0.53047477001544041,
                         1.4619752508048596,
                         0.14577361556326238,
                         1.7010710686747081,
                         1.5307339240549152,
                         0.48603889002153206,
                         0.95604196070138747,
                         0.17832490812574212,
                         0.79506557237389097,
                         0.94925836039953271,
                         0.058494153697185823,
                         0.70073802839865262,
                         0.053179710507255631,
                         1.0532402890064878))
    
refecon_3D2L = np.array((1.5845814047656643,
                         1.7347608882013192,
                         3.9930269653530752e-05,
                         0.1047509609929477,
                         0.48170635560139924,
                         0.48149429319147302,
                         0.48225814162499908,
                         0.48083043163703049,
                         0.48184320479429738,
                         0.48061230147624245,
                         0.47841869699117345,
                         0.48032021762459048,
                         0.28688084935248181,
                         0.31718444676249596,
                         0.47922242392081021,
                         0.48383273121192666,
                         0.48207991154972629,
                         0.54189564336039375,
                         0.4794933213602588,
                         0.47847606909003998,
                         0.48373462751157026,
                         0.4848599695206115,
                         0.48316667507407873,
                         1.4501562558537273,
                         0.4799555746735038,
                         0.51916615743842487,
                         0.47933726100003532,
                         1.4246698004348159,
                         0.56497668650950716,
                         0.48435178825096009,
                         0.48389884938959182,
                         0.48041361913961145,
                         0.47751900918012635,
                         0.73014104025443383,
                         0.47871962891677838,
                         0.48278138642039581,
                         0.99113868446796594,
                         0.49845818627396254,
                         0.4796948026605104,
                         0.48324793172259101,
                         0.48278138642039581,
                         0.48731187420114375,
                         0.48500084307019192,
                         0.4822916816806031,
                         1.4806846057528029,
                         0.39990501103885018,
                         1.4995712520598707,
                         0.88593374284326487,
                         0.48244001539317244,
                         0.13575689894691256,
                         1.5600859510148886,
                         0.25648909909518114,
                         1.129975066967126,
                         1.0278997833915307,
                         0.22430869217975391,
                         0.34379190664761905,
                         0.47989124870580746,
                         0.49391051739749864,
                         0.20681977948255884,
                         0.52511661811513188,
                         0.48258036491517309,
                         0.15538228377151089,
                         0.48513473647357286,
                         0.48275781743105778,
                         0.4839324566638602,
                         0.47805921638279286,
                         0.64519052402081245,
                         0.48553360241205484,
                         0.48107060669206941,
                         0.48251771918674918,
                         0.48609049805658217,
                         0.47735143509871142,
                         1.1583668262577285,
                         0.48652307558417474,
                         0.67811088398955244,
                         0.48536872389500441,
                         0.53695690103995608,
                         0.48608856044186599,
                         1.2270669322638788,
                         1.1192926359592379,
                         0.48785010637827048,
                         0.48472091044753401,
                         1.5216056367402646,
                         0.921397180319102,
                         0.47623763394475888,
                         0.24568773385466552,
                         0.37721690931422153,
                         1.3675095399748214,
                         0.52991052737568844,
                         1.7154383848361447,
                         0.59752373959144367,
                         0.43343739822915545,
                         0.48401020411094142,
                         0.48383525030784058,
                         1.5397502731902817,
                         0.76327504860765827,
                         0.75992247691872072,
                         0.45394840956319549,
                         0.44422339567727565,
                         0.49406750900369112,
                         0.84913213210738592,
                         0.48484570812887395,
                         1.3973093441131137,
                         0.84341276651783514,
                         1.1826236398918439,
                         1.0615669449076561,
                         0.49707888047177645,
                         0.60845186694112197,
                         0.18321435323920554,
                         0.61575983047551774,
                         0.50634951221646018,
                         0.80846960935675072,
                         0.4917193256561565,
                         0.11310638349653183,
                         0.4744174640019283,
                         1.0075865262601589,
                         1.0810566861680719,
                         0.82353643759821282,
                         0.53231040199009383,
                         1.206371452003032,
                         0.48359644947137642,
                         1.3513331447243313,
                         0.95944568871841729,
                         0.49955876212022843,
                         0.48914278054293053,
                         0.62258414179602151,
                         0.083830256824647148,
                         0.48565343914914982,
                         0.48964653525778151,
                         0.97092305852198935,
                         0.57645478845312703,
                         0.48255273880877014,
                         0.78929136946585454,
                         0.49007252503894477,
                         0.48834232597903021,
                         1.1821112902424606,
                         0.17502142484016381,
                         1.6423981475333669,
                         1.3117968756806029,
                         0.48710438954813245,
                         0.84391126263032934,
                         0.65960846712217436,
                         1.045027718434518,
                         1.6887972301636378,
                         0.35151808851526534,
                         1.4041466893421062,
                         1.5962504097353338,
                         0.47366012356214032,
                         0.37050772673073407,
                         0.69275120857268968,
                         0.49535965050877095,
                         0.48703472757122662,
                         0.86314470432820323,
                         0.48085369211572127,
                         1.6146698790093492,
                         0.77004996432440653,
                         0.012881839360707227,
                         0.79505016192204414,
                         0.74989809609048574,
                         0.023443998438666364,
                         0.59469226172220557,
                         0.97575655713497789,
                         0.51089534077375653,
                         0.74503145827230166,
                         0.54846339143957501,
                         1.6956796857771024,
                         0.41348616574504843,
                         1.6252836557453105,
                         1.3425006402951869,
                         0.04852394039538218,
                         0.41222998483628398,
                         0.5503439734313631,
                         0.9272282016901856,
                         1.1066548626730583,
                         0.74017217453201789,
                         1.2973155063628716,
                         0.47191772751965849,
                         0.91632009894336142,
                         0.071863764750595138,
                         0.77698864738630391,
                         0.74356848145775589,
                         1.0185727037284498,
                         0.49378368913618115,
                         1.1660084279943024,
                         0.75150107906091712,
                         0.59276574298746376,
                         0.66480872179399453,
                         1.5761296041293376,
                         0.80419611035200567,
                         0.67536960680821723,
                         1.289656896794539,
                         0.73496613066456384,
                         1.261077242642642,
                         0.46319400033947106,
                         1.6641217781609841,
                         0.62684832522868383,
                         0.49237224091023624,
                         0.4939369675521974,
                         0.90766335022802691,
                         0.64486833414593847))
refrel_3D2L = np.array((0.070000000000000007,
                        0.070000000000000007,
                        1.0000000000000007,
                        1.0000000000000007,
                        0.93440000000000012,
                        0.9448000000000002,
                        0.91410000000000036,
                        0.95500000000000029,
                        0.92440000000000044,
                        0.96020000000000061,
                        0.99410000000000065,
                        0.96670000000000034,
                        1.0000000000000007,
                        1.0000000000000007,
                        0.98390000000000055,
                        0.87890000000000024,
                        0.92410000000000014,
                        0.62159999999999904,
                        0.97610000000000063,
                        0.98170000000000057,
                        0.87880000000000014,
                        0.84749999999999992,
                        0.88680000000000003,
                        0.086599999999999913,
                        0.96840000000000059,
                        0.44680000000000031,
                        0.98010000000000075,
                        0.084099999999999925,
                        0.60130000000000028,
                        0.8660000000000001,
                        0.87360000000000049,
                        0.96210000000000062,
                        0.99270000000000047,
                        0.42820000000000025,
                        0.98720000000000074,
                        0.89430000000000009,
                        0.19140000000000038,
                        0.70659999999999989,
                        0.97460000000000047,
                        0.88390000000000035,
                        0.8929999999999999,
                        0.80879999999999996,
                        0.85109999999999975,
                        0.91020000000000023,
                        0.07999999999999996,
                        1.0000000000000007,
                        0.07999999999999996,
                        0.30949999999999966,
                        0.90790000000000048,
                        1.0000000000000007,
                        0.079799999999999954,
                        1.0000000000000007,
                        0.1116000000000001,
                        0.1872000000000002,
                        1.0000000000000007,
                        1.0000000000000007,
                        0.97220000000000029,
                        0.65789999999999982,
                        1.0000000000000007,
                        0.64259999999999962,
                        0.89799999999999991,
                        1.0000000000000007,
                        0.8425999999999999,
                        0.89870000000000039,
                        0.85930000000000029,
                        0.99400000000000077,
                        0.33230000000000015,
                        0.83770000000000033,
                        0.94940000000000047,
                        0.90440000000000054,
                        0.82289999999999996,
                        0.99860000000000071,
                        0.13299999999999984,
                        0.81950000000000023,
                        0.35170000000000001,
                        0.83999999999999997,
                        0.62979999999999892,
                        0.82779999999999976,
                        0.11800000000000026,
                        0.1473000000000001,
                        0.79490000000000005,
                        0.8639,
                        0.07999999999999996,
                        0.25649999999999984,
                        0.99840000000000073,
                        1.0000000000000007,
                        1.0000000000000007,
                        0.098800000000000054,
                        0.41699999999999976,
                        0.070000000000000007,
                        0.27750000000000002,
                        1.0000000000000007,
                        0.86860000000000026,
                        0.86960000000000026,
                        0.073000000000000023,
                        0.35899999999999971,
                        0.39180000000000026,
                        1.0000000000000007,
                        1.0000000000000007,
                        0.67949999999999999,
                        0.46679999999999994,
                        0.84789999999999976,
                        0.0899999999999999,
                        0.28990000000000066,
                        0.10690000000000009,
                        0.15340000000000004,
                        0.71909999999999918,
                        0.58090000000000142,
                        1.0000000000000007,
                        0.56409999999999993,
                        0.67290000000000039,
                        0.47820000000000035,
                        0.75640000000000041,
                        1.0000000000000007,
                        1.0000000000000007,
                        0.17819999999999983,
                        0.15999999999999992,
                        0.26669999999999999,
                        0.6376999999999996,
                        0.12110000000000025,
                        0.88210000000000011,
                        0.096000000000000016,
                        0.20669999999999986,
                        0.69240000000000013,
                        0.78760000000000041,
                        0.57420000000000038,
                        1.0000000000000007,
                        0.8322999999999996,
                        0.76959999999999995,
                        0.17939999999999978,
                        0.30240000000000006,
                        0.90489999999999982,
                        0.53070000000000106,
                        0.77850000000000041,
                        0.79760000000000042,
                        0.12619999999999998,
                        1.0000000000000007,
                        0.070000000000000007,
                        0.10040000000000007,
                        0.81390000000000029,
                        0.31659999999999983,
                        0.4914000000000005,
                        0.12999999999999984,
                        0.070000000000000007,
                        1.0000000000000007,
                        0.0899999999999999,
                        0.070000000000000007,
                        1.0000000000000007,
                        1.0000000000000007,
                        0.52360000000000029,
                        0.72949999999999915,
                        0.81629999999999969,
                        0.39960000000000012,
                        0.94860000000000033,
                        0.070000000000000007,
                        0.48870000000000047,
                        1.0000000000000007,
                        0.50629999999999986,
                        0.32690000000000019,
                        1.0000000000000007,
                        0.51559999999999973,
                        0.21820000000000009,
                        0.66790000000000027,
                        0.26329999999999981,
                        0.38580000000000042,
                        0.070000000000000007,
                        1.0000000000000007,
                        0.070000000000000007,
                        0.091699999999999934,
                        1.0000000000000007,
                        1.0000000000000007,
                        0.40089999999999998,
                        0.28010000000000007,
                        0.13229999999999983,
                        0.22999999999999976,
                        0.0899999999999999,
                        1.0000000000000007,
                        0.21489999999999992,
                        1.0000000000000007,
                        0.24800000000000028,
                        0.34070000000000006,
                        0.17019999999999993,
                        0.73979999999999924,
                        0.10000000000000007,
                        0.31299999999999972,
                        0.29860000000000025,
                        0.40779999999999983,
                        0.079899999999999971,
                        0.3698999999999999,
                        0.52329999999999999,
                        0.0899999999999999,
                        0.17549999999999988,
                        0.11000000000000008,
                        1.0000000000000007,
                        0.070000000000000007,
                        0.53520000000000045,
                        0.69209999999999994,
                        0.74349999999999961,
                        0.22050000000000011,
                        0.23580000000000012))
refpho_3D2L = np.array((2.2554525694641749,
                        2.2838666763726634,
                        0.054925996890590481,
                        0.076314548218177569,
                        1.0503259086910153,
                        0.93121520474898245,
                        1.2206023609675338,
                        0.86979868823201301,
                        1.1185091930682991,
                        0.77499112017961125,
                        0.40065133595964286,
                        0.71669041934107813,
                        0.1226097473157821,
                        0.13397028831429555,
                        0.52080455640262679,
                        1.577866242622086,
                        1.1117401688226034,
                        2.0778770216318567,
                        0.58620044324932652,
                        0.47102564417336756,
                        1.5119380348148206,
                        1.7444221904091097,
                        1.4472395205468542,
                        2.2636546186807482,
                        0.68585334537364151,
                        2.0252489747261468,
                        0.56288809611419333,
                        2.2425490934415375,
                        2.1232957816307438,
                        1.6946541078838162,
                        1.6572431044990739,
                        0.77335413786449525,
                        0.34633074392717006,
                        2.1860868822018196,
                        0.47897637291070466,
                        1.4141709925350885,
                        2.2608702076927982,
                        2.0353855395007159,
                        0.63876895278632084,
                        1.4789067784529457,
                        1.3876618245763523,
                        1.9717806983057202,
                        1.8097626624770924,
                        1.2580670742955944,
                        2.2376659505804559,
                        0.16933354022919492,
                        2.2387642266121941,
                        2.2671297603983116,
                        1.2720778387906966,
                        0.083331922440030612,
                        2.2637410998943053,
                        0.11310012644278794,
                        2.1863182378632917,
                        2.2776855775966189,
                        0.10484019337641982,
                        0.14738443800936446,
                        0.64465857190670395,
                        2.0258766050002701,
                        0.099367717261491253,
                        2.0613876016423363,
                        1.3440580554719226,
                        0.089957309130704044,
                        1.7842850937729553,
                        1.3646865340694372,
                        1.6160798326973904,
                        0.37651030594846258,
                        2.0953910668186997,
                        1.8235079986349365,
                        0.89819981699750118,
                        1.3092481915626042,
                        1.8869960445815916,
                        0.31999596770645078,
                        2.27405713932913,
                        1.9185766330281619,
                        2.1278013183067594,
                        1.8495666404631355,
                        2.07381517579236,
                        1.8664652613789139,
                        2.2633125012505348,
                        2.2739565567552198,
                        1.9822799060068985,
                        1.6810953688731674,
                        2.248686055524276,
                        2.265724121289038,
                        0.27652136961863605,
                        0.11221061478884023,
                        0.15998970123607256,
                        2.2712721937102462,
                        2.027629660940069,
                        2.2822071925959806,
                        2.0538185329295628,
                        0.18934751821492274,
                        1.6283248469037208,
                        1.6001123300470637,
                        2.2486300944576123,
                        2.1943272756267254,
                        2.2000641889467691,
                        0.21269941289803546,
                        0.19885342540739315,
                        2.0270770854338602,
                        2.2791596704187915,
                        1.7689438263351032,
                        2.2425431820432378,
                        2.2278684160181372,
                        2.1858997832833804,
                        2.2508618325109939,
                        2.0344355852326514,
                        2.1435947149506958,
                        0.096714180107542569,
                        2.1260572668630777,
                        2.0425514153941124,
                        2.2515677028590733,
                        2.0223713587976291,
                        0.080651615170671501,
                        0.29484889443813955,
                        2.2503400606459745,
                        2.2777579440367894,
                        2.2002026084322948,
                        2.0854931614643939,
                        2.2778010336497658,
                        1.5034941410568403,
                        2.2575069705243003,
                        2.2526975582844222,
                        2.0352682051287561,
                        2.0122335696392137,
                        2.1429006156132608,
                        0.074375273422844293,
                        1.8814368806968225,
                        2.0086493543689796,
                        2.2243559639564734,
                        2.0370552948042366,
                        1.3150980669523717,
                        2.2520238987927885,
                        2.0128003356699522,
                        2.0026924966038138,
                        2.2639626029929065,
                        0.092632832271889828,
                        2.2663669793770231,
                        2.2740342183391991,
                        1.942575870090272,
                        2.2396136481067632,
                        2.1430533512605279,
                        2.1814961137570328,
                        2.2790149895352827,
                        0.15259520892333611,
                        2.2451915648125107,
                        2.2576143157499886,
                        0.25643064943489402,
                        0.15441065168481322,
                        2.1741479648033493,
                        2.0313963960835206,
                        1.9543956640986195,
                        2.2775913231645664,
                        0.88922388003837249,
                        2.2612936911733752,
                        2.2253063733257612,
                        0.058241156662966025,
                        2.245937305797967,
                        2.1737959671563041,
                        0.063121872005810417,
                        2.0962650723260379,
                        2.2748483950430525,
                        2.0483315313170083,
                        2.1398987442160782,
                        2.0350965724016912,
                        2.2803362834601781,
                        0.18791069927538745,
                        2.2629262011924229,
                        2.2463254018190426,
                        0.067987118204959202,
                        0.18001015674953602,
                        2.040627834645238,
                        2.2834287206549946,
                        2.2365190848549417,
                        2.1107108804800729,
                        2.2073988031604737,
                        0.23918967741056046,
                        2.2295883344901806,
                        0.069502005192605201,
                        2.1532594236195051,
                        2.1739553735964732,
                        2.2511036365794412,
                        2.0285021269563042,
                        2.180692164701691,
                        2.1692569680956844,
                        2.0405169457577683,
                        2.1324667829478621,
                        2.2754007165397976,
                        2.2280219925875828,
                        2.1610635538044538,
                        2.2048336185135442,
                        2.0992424213011245,
                        2.2559812506147408,
                        0.22422884001824675,
                        2.2748276991495704,
                        2.1258892680217656,
                        2.0256756215901395,
                        2.0378649770431854,
                        2.2296726768087503,
                        2.071023780276561))
            
refpho_2D3L = np.array((2.2839,
                       0.05506,
                       0.060342718481896526,
                       2.2826704822027817,
                       1.0970989633830328,
                       0.92207389817578311,
                       1.3266085265245628,
                       0.79823512224936544,
                       0.99426647652909195,
                       1.7452970415633871,
                       1.4104290290157995,
                       1.5892857865473544,
                       1.2151046729871902,
                       1.2184049887021238,
                       0.64144756185954077,
                       0.48374843813864399,
                       1.4611806694579601,
                       1.8359190755098502,
                       0.71466414376375575,
                       1.6807825449437499,
                       0.73620616127534499,
                       0.60390757661887351,
                       0.53682562940711687,
                       1.5483432647962996,
                       0.55854277096626714,
                       1.6831635493731236,
                       0.4346239247507262,
                       1.9302490319128869,
                       1.5072174995581358,
                       0.35371408318867231,
                       1.8839336634645292,
                       0.39474591276796811,
                       1.9669426076631129,
                       0.16781139801849199,
                       0.25638128343001815,
                       2.2730338523482772,
                       0.15682947963365806,
                       0.13781168602584207,
                       2.2588699795296394,
                       2.2127562596723194,
                       0.29326512495268992,
                       1.8402853061272606,
                       0.12268915890268348,
                       2.217868730958958,
                       2.1857904956884502,
                       0.067333584826844359,
                       2.1627663761740381,
                       2.1567420920457652,
                       2.1223182096510569,
                       2.1262312723942181,
                       2.2514631511889021,
                       2.1981528064533169,
                       2.1787058095141827,
                       2.2387542595806909,
                       2.2335296154153172,
                       2.0988992613380599,
                       0.13492019561199592,
                       2.207336124268898,
                       2.0375646780486876,
                       0.072146203628089392,
                       1.5210586290981913,
                       2.2782607332851925,
                       2.1351526929746703,
                       2.2377455969185251,
                       1.9738522335576199,
                       2.2435556805732051,
                       0.1156549566942336,
                       0.19742329666530503,
                       2.0043091467569827,
                       2.0949144889652267,
                       2.2264921952287633,
                       0.15411666643671285,
                       0.064943231139836688,
                       2.072437452032132,
                       1.9836367755460487,
                       0.095839334416188082,
                       2.1499543915559278,
                       2.2596245719684949,
                       0.10439616682852501,
                       2.1681701445270671,
                       0.21792783289174117,
                       2.2120703706705438,
                       0.30307149983644865,
                       0.20329375945877629,
                       0.32699043077400647,
                       2.2728271237250253,
                       1.9095215902418121,
                       2.1188155892805001,
                       2.0608050055684122,
                       0.085528637792654585,
                       2.0795163163488022,
                       2.26819396422446,
                       2.0588452016598429,
                       2.2476286185439931,
                       2.1081221074906753,
                       0.1719275200288802,
                       0.2440266383596259,
                       2.2024989417499019,
                       0.064817755609519134,
                       2.1151627149946099,
                       2.2445691304203876,
                       2.1872276889455873,
                       2.0439175281232744,
                       2.0073857143169658,
                       2.0468874712838998,
                       2.1532545246756971,
                       2.2239260596457568,
                       2.1550256506766687,
                       0.11133684519437959,
                       0.14739613318020456,
                       2.1960558657711924,
                       2.2063839585600444,
                       2.1731862677849061,
                       0.075495378599680377,
                       0.09416285484691625,
                       0.13433389489701988,
                       2.1862167253552429,
                       0.079891391298265779,
                       2.0873809804098156,
                       0.22940131604096134,
                       2.170893661494175,
                       0.085355292186429094,
                       2.14513630247265,
                       1.9697161811227877,
                       2.1312096813807924,
                       2.1954826105281628,
                       2.0156754866028739,
                       2.0515448352221046,
                       2.023564183531585,
                       0.18886155357114498,
                       2.2652634119719055,
                       2.2787509035340596,
                       0.41011071022947193,
                       0.10815078713948389,
                       0.1892867162134407,
                       2.0118721732980207,
                       2.2797928169163963,
                       0.14870308499096999,
                       2.1947650420191893,
                       1.8961451707612242,
                       2.2484072180658865,
                       0.078546719585268501,
                       2.1896990459337204,
                       2.1127733800470749,
                       2.229254758261459,
                       0.21574812842270594,
                       2.1297017208884959,
                       0.33661297681421914,
                       1.9993027814352118,
                       2.1013746852745299,
                       0.08772193996272655,
                       1.9981787862416815,
                       2.2053514163673,
                       2.1429125866092682,
                       0.076509312816554431,
                       0.091310910716059832,
                       0.1032980045090922,
                       2.2647687769405693,
                       2.0634624436297613,
                       2.2623908919206253,
                       2.1133194493900169,
                       2.0765722581575741,
                       2.0698642447049664,
                       2.1370849881056286,
                       0.4247142144136743,
                       0.10037511259496741,
                       0.1821577982639444,
                       2.2624494963529407,
                       0.10732758620142956,
                       2.2512966100363028,
                       2.2310394111755776,
                       1.99227352276374,
                       2.0928950943674978,
                       2.1396813770995982,
                       2.0222457275635364,
                       2.0346975592952519,
                       2.1418838405172056,
                       0.090172852824247876,
                       1.9857174397210096,
                       2.1383387321182834,
                       0.23319526302225063,
                       0.13036898249980527,
                       2.2193220422782125,
                       2.0278550241954432,
                       0.17788522063890361,
                       2.0679296419434294,
                       2.1518713825987672,
                       2.0226578956203185,
                       2.1073968190782164,
                       2.0874213620514506,
                       2.1634702074494094,
                       2.2215667418213525,
                       2.1777790393615506,
                       2.0766062280686906,
                       1.992444758511702,
                       2.1713203442163391,
                       0.11492598514331996,
                       1.9856601809635774,
                       0.12565216721489969,
                       2.0533397323799014,
                       2.1767843625903063,
                       2.1649931422829982))  # Insert reference set
refecon_2D3L = np.array((1.729889,
                        0.0005413,
                        0.027684352347788606,
                        1.714976598394697,
                        0.49319084784627953,
                        0.49118979809952595,
                        0.49462709576198433,
                        0.49098742715097987,
                        0.49186459943547134,
                        0.49903451830858186,
                        0.49540460720283963,
                        0.49678825502642537,
                        0.49397794515028198,
                        0.49421798101983766,
                        0.48963798109662737,
                        0.48791174824539529,
                        0.49572407136414137,
                        0.50004948042887676,
                        0.48967164506266009,
                        0.49770666536364688,
                        0.49048521168790771,
                        0.48915406809435558,
                        0.48840649612193382,
                        0.49626309018792847,
                        0.48899044265417235,
                        0.49792966664638938,
                        0.48749529369274974,
                        0.50332748688231821,
                        0.49602608957706446,
                        0.48563216623709865,
                        0.50023687634287595,
                        0.48656946067197798,
                        0.50530529139504654,
                        0.39261171439244436,
                        0.48148468405861961,
                        1.6684925529476442,
                        0.37248594060265866,
                        0.33194420333573271,
                        1.5804563678720753,
                        1.361668278728291,
                        0.481752974223011,
                        0.50019447936183981,
                        0.27831906960198322,
                        1.3829132221487681,
                        1.2135839449928147,
                        0.063733252577873878,
                        1.1201478018639401,
                        1.0948038729569809,
                        0.94301775281559419,
                        0.95900200590506557,
                        1.5626179450105815,
                        1.2929058871011114,
                        1.1984480550073799,
                        1.4963494660424406,
                        1.469386830199789,
                        0.85388221336839754,
                        0.31719953315752208,
                        1.3373152194230216,
                        0.67748221198660563,
                        0.080308716920203874,
                        0.49611572041789354,
                        1.6877351811835712,
                        0.99128279301336808,
                        1.4816206320736345,
                        0.52387213876743421,
                        1.5103896179270311,
                        0.25928382491422264,
                        0.4385387032049029,
                        0.5891511465135354,
                        0.83668267445015543,
                        1.4347651329453492,
                        0.3639733687850133,
                        0.050636258496642481,
                        0.76707060939926808,
                        0.5355917547446859,
                        0.18805884304161477,
                        1.0525904560404209,
                        1.5942141693256524,
                        0.21754015935713861,
                        1.1416863796577448,
                        0.45996756928041566,
                        1.3501854839896053,
                        0.48286039622323024,
                        0.44954074002360034,
                        0.48455611602437137,
                        1.6517921899988939,
                        0.50291640655184278,
                        0.93037703763071566,
                        0.73616667987413908,
                        0.14041564165541648,
                        0.79343810381042146,
                        1.6446848184959437,
                        0.71933480239268743,
                        1.5336160184793943,
                        0.89038197011071341,
                        0.40280977478031765,
                        0.47761730018645249,
                        1.3038348531282273,
                        0.035903525761989151,
                        0.92118121176366219,
                        1.5226142909207545,
                        1.2367850523170445,
                        0.69036669219200153,
                        0.6026520649843421,
                        0.69643991901790669,
                        1.0719679964978692,
                        1.419570305746789,
                        1.0914000005318198,
                        0.24719813728874318,
                        0.3466261273640715,
                        1.2754650138304018,
                        1.3217608378714867,
                        1.1756466426605512,
                        0.089420862554144429,
                        0.17552905987398965,
                        0.30179341657488007,
                        1.2286804681813219,
                        0.12087606819369909,
                        0.80268236507821233,
                        0.47116120110885978,
                        1.1619927139772022,
                        0.12665078610923527,
                        1.0420303743122468,
                        0.51541337051618485,
                        0.97672945219600305,
                        1.2699530390041842,
                        0.61898182322641537,
                        0.71049251338266806,
                        0.64083676094587816,
                        0.42236629065225906,
                        1.6304205660779703,
                        1.6953647792410547,
                        0.48667807570390176,
                        0.23351402141028368,
                        0.42990147085814034,
                        0.60942897948966568,
                        1.7095220962529183,
                        0.34883058212288875,
                        1.2528650334325619,
                        0.50183646422338435,
                        1.5464875981044253,
                        0.10765688649074538,
                        1.252202144586485,
                        0.90282917822496445,
                        1.4453703821005179,
                        0.45287200781299164,
                        0.97161572381408523,
                        0.48488669255234668,
                        0.57880746483908019,
                        0.86472980773607411,
                        0.15205380620663014,
                        0.57245243803398593,
                        1.313942135742648,
                        1.0341221642235501,
                        0.10163144401569896,
                        0.16696348340946154,
                        0.2017142894644969,
                        1.6240837753600643,
                        0.74307720701926239,
                        1.6068798317873489,
                        0.90813251457944144,
                        0.77973414694143595,
                        0.75509669934553914,
                        1.0032951439053539,
                        0.48668966316094125,
                        0.20012558207972084,
                        0.41211034168878313,
                        1.6123070853023456,
                        0.22748662747355591,
                        1.5529359197567563,
                        1.4537533198296337,
                        0.56146429294996381,
                        0.82851055869703383,
                        1.0189256807726341,
                        0.6250972646800006,
                        0.66500116303917123,
                        1.0236966838960213,
                        0.15805489952865792,
                        0.549625982472428,
                        1.0083534842513646,
                        0.47245716524912934,
                        0.29634110971137806,
                        1.3929071843685628,
                        0.650962638673377,
                        0.41159649972645279,
                        0.75100286203194644,
                        1.0660669671449139,
                        0.63163401184700185,
                        0.88017568821450287,
                        0.81154364263417222,
                        1.1246805954792316,
                        1.4127332479120851,
                        1.1864707021265388,
                        0.78367298420641529,
                        0.56287843009405458,
                        1.1632626361732317,
                        0.25381751839428007,
                        0.54425321077496724,
                        0.2882062657307311,
                        0.71499018355838617,
                        1.1837830498134114,
                        1.1350540202015169))

refecon_3D3L = np.array((1.7227951617415307,
                         1.3656195894895802,
                         0.038995206726813052,
                         1.7289157779806632,
                         0.16544728502345138,
                         0.49555778616951046,
                         0.49636167542988646,
                         0.49707831459126262,
                         0.39841901116599737,
                         0.48790138044831449,
                         0.49824726673990716,
                         0.48900866935363291,
                         0.36468114203133872,
                         0.50197245605716201,
                         0.49740962936437499,
                         0.49424028954877336,
                         0.49889116590909649,
                         0.84722919352692239,
                         0.49457978020342241,
                         0.48633508354815835,
                         0.91037829327221087,
                         0.53395710670289787,
                         1.5931003149204421,
                         0.9689241535448212,
                         1.0416085383981304,
                         0.49107380849037541,
                         0.071210405437290361,
                         0.23911071562834441,
                         0.48283109009719871,
                         0.53835996964700972,
                         1.2239858535971075,
                         0.77466544334177034,
                         0.50494059504172217,
                         0.31974517786347978,
                         1.1005278220813142,
                         0.51074498940249979,
                         0.51358332320522859,
                         0.49070226543023315,
                         0.49180835940671325,
                         0.80724917665882534,
                         0.50353277548440656,
                         1.6698812009845432,
                         0.52078229213093596,
                         1.5153554757823355,
                         0.49580893837269285,
                         1.1909750967782933,
                         0.49098788637139062,
                         0.34660895945102566,
                         1.6316465806696399,
                         0.49578337734378558,
                         0.55985322363658063,
                         1.4456181070231922,
                         0.49785182269892486,
                         0.4465034388589979,
                         0.49472228504931909,
                         0.52586006091640425,
                         0.48767844709050251,
                         0.72502274108484432,
                         0.20574662990079065,
                         0.50220202385892965,
                         0.95447230014067552,
                         1.4169725753451574,
                         1.0611185938101064,
                         1.7035851689566328,
                         1.0755549777161335,
                         0.56841662010794181,
                         0.50694453866581424,
                         0.48939092847629406,
                         0.82255764665218611,
                         1.3972728871029387,
                         0.49267125469837736,
                         0.46031360886651501,
                         1.1286660418699712,
                         0.66779860781118983,
                         0.94171194542199166,
                         0.49457134824163718,
                         0.48121940991169548,
                         0.49239311922907547,
                         0.49729441272475905,
                         0.47268879104090644,
                         1.0207191994587093,
                         0.25565798108327314,
                         0.86379726207248242,
                         0.71680633559067364,
                         0.49358986580307634,
                         0.49223879887195821,
                         0.49015731869049534,
                         0.49136253536138064,
                         0.5085378943053579,
                         0.90954949487146808,
                         0.87544071401147527,
                         0.52742292898103127,
                         0.48365148348960185,
                         0.42494795529956458,
                         0.88944959205631458,
                         0.49126552874872526,
                         0.49244451489322744,
                         0.4826206082337019,
                         0.49269069933640941,
                         0.49987291422962926,
                         0.61237486189305224,
                         0.56021438950098967,
                         0.4921835921047879,
                         0.49334909181310016,
                         1.1727804219170128,
                         0.78279372445825768,
                         0.41986422940046647,
                         0.50133902674521369,
                         0.49924549444874144,
                         0.49990326211804637,
                         1.6465913437412889,
                         0.50066727396152733,
                         1.0039051987753358,
                         0.70568579953787003,
                         0.92636929669026502,
                         1.3097427589772264,
                         0.27610685276138008,
                         1.5590240277610194,
                         0.81427364916429545,
                         0.98802392681438889,
                         0.59882297742277579,
                         0.49485380503027132,
                         0.50988681101631173,
                         0.68018214181068515,
                         1.3344161162158135,
                         0.5411846465785789,
                         0.90166247681814982,
                         0.50073969824192377,
                         0.60456669652092343,
                         1.4811533468276628,
                         1.1469793037248941,
                         1.343634837101976,
                         1.4636336897547593,
                         0.62864073337623416,
                         0.52906459549182905,
                         0.54025876093425929,
                         0.50403252109433583,
                         0.60484926126966565,
                         0.59303601884442303,
                         0.49484510066457987,
                         0.5169726963910356,
                         0.49957680922185377,
                         0.17758299740949951,
                         0.49753195835205927,
                         0.14552802162730155,
                         0.29481584399765592,
                         1.5423196031012472,
                         0.56694815792201336,
                         1.3120122850379281,
                         1.0840689650691502,
                         0.088472981317427007,
                         0.49337820534477378,
                         1.3869400454851448,
                         0.75442848820150255,
                         0.62990632044989403,
                         0.49379519735980343,
                         0.49314819197124915,
                         1.3748005428522962,
                         0.48948590132544845,
                         1.0193841047833225,
                         0.69122677522409259,
                         0.13740479865618649,
                         0.6201907443027781,
                         0.50389863386152067,
                         0.55093665054464169,
                         1.13363703432935,
                         0.69565235249872948,
                         0.53934703194613354,
                         0.55581435067748453,
                         0.64050352348010409,
                         0.50046027731016085,
                         0.54763934962632965,
                         0.8208690540810667,
                         0.49189961264857807,
                         0.58388719237795839,
                         1.1615995591131338,
                         0.49314819197124915,
                         0.52405463483487125,
                         0.66037335206171821,
                         0.64811635077293328,
                         0.65488811244457623,
                         0.5052055714752447,
                         0.75920281491047503,
                         1.2523452671928099,
                         0.9641943158723042,
                         0.52933577179510549,
                         1.719591749796386,
                         0.85536351005316513,
                         0.6174568468691588,
                         0.11738350955663561,
                         0.48584926317355503,
                         0.57575091958169367,
                         1.5775219824714157,
                         0.74212951099277924,
                         0.4864822796894227,
                         0.5549516509776854,
                         0.51978888975990889,
                         0.60329382850251778,
                         1.2922402790171852,
                         0.48958936189969038))
refrel_3D3L = np.array((7.4136000000010318,
                        11.746799999999732,
                        99.000000000013742,
                        7.4136000000010318,
                        99.000000000013742,
                        91.465100000001854,
                        90.085500000001019,
                        89.690400000005042,
                        99.000000000013742,
                        98.802000000010821,
                        88.423199999996697,
                        98.297100000010659,
                        99.000000000013742,
                        86.11099999999503,
                        88.896499999998525,
                        92.780700000002795,
                        88.301399999993322,
                        12.369500000002168,
                        92.117400000002903,
                        98.99010000001411,
                        28.989000000003045,
                        54.381900000002659,
                        7.7898000000003265,
                        23.301300000005238,
                        20.150999999999488,
                        96.514800000006417,
                        99.000000000013742,
                        99.000000000013742,
                        98.960400000013792,
                        75.885599999988003,
                        15.099600000000814,
                        40.997100000005716,
                        84.403700000003937,
                        99.000000000013742,
                        14.347200000001934,
                        82.194300000002031,
                        80.487800000002977,
                        97.14860000000634,
                        95.465099999994436,
                        21.059999999998929,
                        85.347300000002292,
                        7.4136000000010318,
                        65.11109999999897,
                        8.1164999999997125,
                        90.342900000005059,
                        15.326000000000528,
                        96.782100000003126,
                        99.000000000013742,
                        7.4136000000010318,
                        90.678500000005783,
                        67.567399999998088,
                        9.3922999999982455,
                        88.630200000001366,
                        99.000000000013742,
                        91.752200000002674,
                        78.278100000009118,
                        98.69310000001397,
                        39.034700000008499,
                        99.000000000013742,
                        85.318999999992457,
                        26.749500000004392,
                        9.3922999999982455,
                        34.653299999996207,
                        7.4136000000010318,
                        33.669799999995625,
                        56.202300000000378,
                        83.692499999995505,
                        97.970100000008557,
                        15.563599999999999,
                        9.7090999999986618,
                        94.141200000002826,
                        99.000000000013742,
                        17.766799999996504,
                        61.755000000001615,
                        35.455199999997255,
                        92.257100000003859,
                        99.000000000013742,
                        94.490000000006091,
                        88.98660000000433,
                        99.000000000013742,
                        18.439999999996353,
                        99.000000000013742,
                        21.454099999998604,
                        47.505600000000697,
                        93.057900000004494,
                        94.98989999999776,
                        97.504800000005176,
                        95.989800000001651,
                        83.126599999997424,
                        30.606900000000078,
                        36.075499999993511,
                        68.849000000001766,
                        99.000000000013742,
                        99.000000000013742,
                        13.655400000001267,
                        95.930700000004506,
                        94.424700000001124,
                        99.000000000013742,
                        94.025700000003084,
                        87.628199999992916,
                        63.412800000000694,
                        51.604999999999222,
                        95.09790000000072,
                        93.377600000000584,
                        17.144699999997052,
                        40.997100000005716,
                        99.000000000013742,
                        86.776799999994793,
                        87.925199999992529,
                        87.345599999991038,
                        7.4136000000010318,
                        86.974799999998169,
                        36.709099999995296,
                        41.399000000002026,
                        26.610900000003507,
                        13.300100000001295,
                        99.000000000013742,
                        8.3336999999993324,
                        24.348500000004012,
                        38.038499999989952,
                        57.567300000003577,
                        91.581300000001491,
                        82.720699999999695,
                        48.828000000001175,
                        10.381499999999686,
                        64.528100000002141,
                        30.609800000000064,
                        86.941199999993941,
                        49.95660000000278,
                        8.6596999999990789,
                        17.194199999997043,
                        8.9276999999988842,
                        9.3922999999982455,
                        67.907100000000085,
                        62.976600000005476,
                        52.906799999995144,
                        85.101200000008873,
                        42.305700000001245,
                        72.49950000000652,
                        91.352700000001718,
                        56.660699999998585,
                        88.045099999990157,
                        99.000000000013742,
                        88.865699999998483,
                        99.000000000013742,
                        99.000000000013742,
                        7.9674000000000609,
                        26.103500000002491,
                        11.301299999998374,
                        15.316100000000551,
                        99.000000000013742,
                        93.296599999999671,
                        10.381499999999686,
                        16.284899999998533,
                        60.8223000000025,
                        92.770800000006034,
                        93.544800000001331,
                        10.865699999998977,
                        97.653600000011565,
                        31.494899999998257,
                        48.822900000000374,
                        99.000000000013742,
                        60.273899999999301,
                        83.989499999997093,
                        45.029600000004244,
                        17.510999999996731,
                        46.490400000003056,
                        27.932400000004218,
                        52.575199999999271,
                        71.397799999989331,
                        87.094699999992557,
                        75.27929999998301,
                        37.230299999995651,
                        95.117100000002139,
                        72.957599999998621,
                        17.164499999997108,
                        93.622800000001334,
                        78.630200000002574,
                        43.434299999999354,
                        43.47389999999865,
                        70.533600000002338,
                        84.009299999991086,
                        17.669399999996767,
                        14.337300000001957,
                        10.875599999999148,
                        50.936699999999099,
                        7.4136000000010318,
                        24.447500000003831,
                        32.484899999996429,
                        99.000000000013742,
                        99.000000000013742,
                        24.714800000003819,
                        8.4029999999991976,
                        16.304699999998487,
                        98.910900000012518,
                        74.494699999992264,
                        79.80269999999949,
                        50.471399999999669,
                        13.3485000000012,
                        97.683300000004721))
refpho_3D3L = np.array((2.2836049563737335,
                        2.2838860003653161,
                        0.06304617754601545,
                        2.283708415488281,
                        0.089593960660152266,
                        1.2301081516401506,
                        1.3464234188832325,
                        1.4172731848310511,
                        0.17686630563269792,
                        0.47930260123326818,
                        1.5891163066679381,
                        0.53689480756808183,
                        0.15083214662508923,
                        1.8215883762163712,
                        1.4879145239156175,
                        1.0565431214633505,
                        1.6388318811248861,
                        2.1370981597356864,
                        1.1302188319550632,
                        0.35966305945110855,
                        2.1986714756951407,
                        2.0706059206464378,
                        2.2743368032648545,
                        2.208645822661552,
                        2.2383813729409594,
                        0.69962156177824508,
                        0.068985913889593201,
                        0.11122496317873062,
                        0.30716716660454135,
                        2.1313511193979653,
                        2.2773338981231142,
                        2.2198316412918806,
                        1.9288633394550248,
                        0.13615095364444191,
                        2.2089298092148062,
                        2.0083094472987013,
                        2.0313134475992758,
                        0.64157012716409922,
                        0.7730138500222048,
                        2.1300450511921456,
                        1.8809662651170338,
                        2.2742126878888689,
                        2.0665756935401292,
                        2.2484068302983391,
                        1.3947526597753201,
                        2.2699307008966154,
                        0.66794924109788034,
                        0.1455599334004018,
                        2.2653149038543026,
                        1.3576791450510144,
                        2.1221637832482312,
                        2.2629691640126954,
                        1.545205227326079,
                        0.2050471610644429,
                        1.1753405598697078,
                        2.07787291248082,
                        0.43969989710692337,
                        2.2000367491719279,
                        0.10477711567448826,
                        1.8512627007920928,
                        2.2331037280951254,
                        2.2536566361698025,
                        2.278146288231957,
                        2.2824899207283176,
                        2.2815084895918352,
                        2.1254599302294261,
                        1.9626908684230597,
                        0.56084254657781196,
                        2.1187664221015781,
                        2.2615895019725398,
                        0.91417206916035876,
                        0.21990841402388567,
                        2.2518195044370013,
                        2.2640933556094618,
                        2.2267917848433871,
                        1.1328336694050687,
                        0.25297797197185101,
                        0.8755930413451275,
                        1.5085510587103874,
                        0.23453927283003467,
                        2.2087957588779519,
                        0.11940193902525428,
                        2.1830983595548767,
                        2.2779155782280149,
                        1.0286967364691546,
                        0.82787419103399584,
                        0.6089737037785331,
                        0.74331576428037971,
                        1.9853572263512687,
                        2.2214209151465858,
                        2.2013383892098295,
                        2.0817729975767345,
                        0.3938223266095971,
                        0.19577786985566614,
                        2.1444623358608337,
                        0.7300677271904793,
                        0.86695493783186628,
                        0.28282004359360968,
                        0.92957437459144998,
                        1.7054690037414988,
                        2.1957022893750175,
                        2.1044012659907021,
                        0.80032263847375396,
                        0.99842073211039128,
                        2.2719215630360696,
                        2.2199356010920055,
                        0.18299451878786585,
                        1.7913818823535059,
                        1.6714144317690725,
                        1.7216260835952382,
                        2.2688579005655787,
                        1.7495379772175357,
                        2.2629869055794702,
                        2.2627814917961753,
                        2.1975018308742835,
                        2.2828986193247354,
                        0.12277757872193552,
                        2.2602697321763641,
                        2.1916150747593202,
                        2.27810684981571,
                        2.1694225746622946,
                        1.200661115064301,
                        1.9987244959495774,
                        2.2482659195074133,
                        2.2456639322765763,
                        2.0962675381032687,
                        2.2049007321678102,
                        1.7905296160980422,
                        2.1877801508574146,
                        2.2601972030577522,
                        2.2547425045783727,
                        2.2151441915273491,
                        2.2633660292816842,
                        2.2194700733870847,
                        2.0768003814889195,
                        2.071207261075847,
                        1.9125256635742853,
                        2.1156785583169975,
                        2.2293579603968028,
                        1.1893154470909155,
                        2.0493136085031725,
                        1.6801586946488982,
                        0.094967562977707476,
                        1.5289517787366775,
                        0.085058255323178275,
                        0.13564127423096001,
                        2.2596701234641867,
                        2.045872896612992,
                        2.2675901328405574,
                        2.2086009697478164,
                        0.079387567053986322,
                        0.98080013060254734,
                        2.2597247973200814,
                        2.0790978483072653,
                        2.2175108415771971,
                        1.0442044191629405,
                        0.9569628654040494,
                        2.268068650123404,
                        0.58600579432356559,
                        2.25597844434275,
                        2.2631262379353667,
                        0.08307567882854118,
                        2.2014446246276935,
                        1.9064804877113772,
                        2.0419370638866385,
                        2.2574528925608131,
                        2.2626425889458961,
                        2.017482186328547,
                        2.0955170729032782,
                        2.2624116624009831,
                        1.743575238135449,
                        2.1466224125539957,
                        2.2129076796091192,
                        0.8238569791789474,
                        2.1769846390667018,
                        2.2645418658341572,
                        0.96466951965597736,
                        2.0740322697013567,
                        2.1712047888318184,
                        2.1546268382385407,
                        2.2780518093257918,
                        1.9683632964863054,
                        2.0989664842041025,
                        2.2731533221777962,
                        2.1682804003531819,
                        2.0526097941734016,
                        2.2835270266906256,
                        2.1916522305630539,
                        2.0968299785482691,
                        0.081624999921106459,
                        0.41288801039064538,
                        2.0242504231525889,
                        2.2769394452241194,
                        2.079342299197759,
                        0.4242122571020821,
                        2.1417612432399511,
                        2.0596378411886365,
                        2.1694701922321564,
                        2.2829564239534035,
                        0.59734177481324224))

def model_3L(pollution_limit,
         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
         q = 2.0,         # recycling exponent
         mean = 0.02,     # mean of natural inflows
         stdev = 0.001,   # standard deviation of natural inflows
         alpha = 0.4,     # utility from pollution
         delta = 0.98,    # future utility discount rate
         nsamples = 100): # monte carlo sampling of natural inflows)

    def lake_conc_JDM_3L(pollution_limit,
                         b = 0.42,        # decay rate for P in lake (0.42 = irreversible)
                         q = 2.0,         # recycling exponent
                         mean = 0.02,     # mean of natural inflows
                         stdev = 0.001,   # standard deviation of natural inflows
                         alpha = 0.4,     # utility from pollution
                         delta = 0.98,    # future utility discount rate
                         nsamples = 100):    # Number of years simulated
        decisions = np.empty((100))
        for j in range(3):
            lowind = (j+1)*33 - 33
            hihind = (j+1)*33

            decisions[lowind:hihind] = pollution_limit[j]
    
        return (decisions)
        
    
    Pcrit = root(lambda x: x**q/(1+x**q) - b*x, 0.01, 1.5)
    average_daily_P = np.zeros((nsamples,))
    decisions = lake_conc_JDM_3L(pollution_limit)

    nvars = len(decisions)
    X = np.zeros((nvars,))
    reliability = 0.0

    for _ in range(nsamples):
        X[0] = 0.0

        natural_inflows = np.random.lognormal(
                math.log(mean**2 / math.sqrt(stdev**2 + mean**2)),
                math.sqrt(math.log(1.0 + stdev**2 / mean**2)),
                size = nvars)

        for t in range(1,nvars):
            X[t] = (1-b)*X[t-1] + X[t-1]**q/(1+X[t-1]**q) + decisions[t-1] + natural_inflows[t-1]
            average_daily_P[t] += X[t]/float(nsamples)

        reliability += np.sum(X < Pcrit)/float(nsamples*nvars)

    max_P = np.max(average_daily_P)
    utility = np.sum(alpha*decisions*np.power(delta,np.arange(nvars)))

    return (utility, max_P)

def refgen_2D3L(ngens):
    
    from rhodium.config import RhodiumConfig
    from platypus import MapEvaluator

    model2D = Model(model_3L)

    # define all parameters to the model that we will be studying
    model2D.parameters = [Parameter("pollution_limit"),
                          Parameter("b"),
                          Parameter("q"),
                          Parameter("mean"),
                          Parameter("stdev"),
                          Parameter("delta")]

    # define the model outputs
    model2D.responses = [Response("utility", Response.MAXIMIZE),
                         Response("max_P", Response.MINIMIZE)]
    
    # define any constraints (can reference any parameter or response by name)
    #model3.constraints = [Constraint("reliability >= 0.80")]
    
    # some parameters are levers that we control via our policy
    model2D.levers = [RealLever("pollution_limit", 0.0, 0.1, length=3)]
    
    # some parameters are exogeneous uncertainties, and we want to better
    # understand how these uncertainties impact our model and decision making
    # process
    model2D.uncertainties = [UniformUncertainty("b", 0.1, 0.45),
                             UniformUncertainty("q", 2.0, 4.5),
                             UniformUncertainty("mean", 0.01, 0.05),
                             UniformUncertainty("stdev", 0.001, 0.005),
                             UniformUncertainty("delta", 0.93, 0.99)]

    name_output = optimize(model2D, "NSGAII", ngens)
    
    output_uti = name_output['utility']
    output_pho = name_output['max_P']

    output_uti = np.sort(output_uti)
    output_pho = np.sort(output_pho)
    #output_pho = np.flipud(output_pho)
    
    return(output_uti, output_pho)
            
def measure_2D_1L(pollution_lim, refecon = refecon_2D1L, refpho=refpho_2D1L):
    # This function measures the euclidean distance of the chosen phosphorous
    # discharge sequence (pollution_lim) from a reference Pareto-efficient set
    # that is hard-coded in for the 2D version of the Lake problem.
    refset = np.empty((201,2))
    refset[:,0] = refecon
    refset[:,1] = refpho
    refset = np.asarray(refset)
    econval = lake_problem_JDM_uti_1L(pollution_lim)
    phoval = lake_problem_JDM_pho_1L(pollution_lim)
    pt1 = (econval, phoval)
    (pta, ptb) = find_shortest_21(pt1, refset)
    dist1 = distance.euclidean((econval, phoval), pta)
    dist2 = distance.euclidean((econval, phoval), ptb)
    score = np.min((dist1, dist2))
    return score

def measure_3D_1L(pollution_lim, refecon = refecon_3D1L, refrel = refrel_3D1L, refpho = refpho_3D1L):
    # This function measures the euclidean distance of the chosen phosphorous
    # discharge sequence (pollution_lim) from a reference Pareto-efficient set
    # that is hard-coded in for the 3D version of the Lake problem.
    
    refset = np.empty((201,3))
    refset[:,0] = refecon
    refset[:,1] = refrel
    refset[:,2] = refpho
    refset = np.asarray(refset)
    econval = lake_problem_JDM_uti_1L(pollution_lim)
    relval = lake_problem_JDM_rel_1L(pollution_lim)
    phoval = lake_problem_JDM_pho_1L(pollution_lim)
    pt1 = (econval, relval, phoval)
    (pta, ptb) = find_shortest_31(pt1, refset)
    dist1 = distance.euclidean((econval, relval, phoval), pta)
    dist2 = distance.euclidean((econval, relval, phoval), ptb)
    score = np.min((dist1, dist2))
    return score

# OR just use the euclidean distance
def measure_2D_2L(pollution_lim, refecon = refecon_2D1L, refpho = refpho_2D1L):
    # This function measures the euclidean distance of the chosen phosphorous
    # discharge sequence (pollution_lim) from a reference Pareto-efficient set
    # that is hard-coded in for the 2D version of the Lake problem.
    
    refset = np.empty((201,2))
    refset[:,0] = refecon
    refset[:,1] = refpho
    refset = np.asarray(refset)
    econval = lake_problem_JDM_uti_2L(pollution_lim)
    phoval = lake_problem_JDM_pho_2L(pollution_lim)
    pt1 = (econval, phoval)
    (pta, ptb) = find_shortest_22(pt1, refset)
    dist1 = distance.euclidean((econval, phoval), pta)
    dist2 = distance.euclidean((econval, phoval), ptb)
    score = np.min((dist1, dist2))
    return score

def measure_3D_2L(pollution_lim, refecon=refecon_3D2L, refrel=refrel_3D2L, refpho=refpho_3D2L):
    # This function measures the euclidean distance of the chosen phosphorous
    # discharge sequence (pollution_lim) from a reference Pareto-efficient set
    # that is hard-coded in for the 3D version of the Lake problem.
    
    refset = np.empty((200,3))
    refset[:,0] = refecon
    refset[:,1] = refrel
    refset[:,2] = refpho
    refset = np.asarray(refset)
    econval = lake_problem_JDM_uti_2L(pollution_lim)
    relval = lake_problem_JDM_rel_2L(pollution_lim)
    phoval = lake_problem_JDM_pho_2L(pollution_lim)
    pt1 = (econval, relval, phoval)
    (pta, ptb) = find_shortest_32(pt1, refset)
    dist1 = distance.euclidean((econval, relval, phoval), pta)
    dist2 = distance.euclidean((econval, relval, phoval), ptb)
    score = np.min((dist1, dist2))
    return score

def measure_2D_3L(pollution_lim, refecon=refecon_2D3L, refpho=refpho_2D3L):
    # This function measures the euclidean distance of the chosen phosphorous
    # discharge sequence (pollution_lim) from a reference Pareto-efficient set
    # that is hard-coded in for the 2D version of the Lake problem.
    
    refset = np.empty((202,2))
    refset[:,0] = refecon
    refset[:,1] = refpho
    refset = np.asarray(refset)
    econval = lake_problem_JDM_uti_3L(pollution_lim)
    phoval = lake_problem_JDM_pho_3L(pollution_lim)
    pt1 = (econval, phoval)
    (pta, ptb) = find_shortest_23(pt1, refset)
    dist1 = distance.euclidean((econval, phoval), pta)
    dist2 = distance.euclidean((econval, phoval), ptb)
    score = np.min((dist1, dist2))
    return score

def measure_3D_3L(pollution_lim, refecon=refecon_3D3L, refpho=refpho_3D3L, refrel=refrel_3D3L):
    # This function measures the euclidean distance of the chosen phosphorous
    # discharge sequence (pollution_lim) from a reference Pareto-efficient set
    # that is hard-coded in for the 3D version of the Lake problem.
    refrel = refrel/100
    
    refset = np.empty((200,3))
    refset[:,0] = refecon
    refset[:,1] = refrel
    refset[:,2] = refpho
    refset = np.asarray(refset)
    econval = lake_problem_JDM_uti_3L(pollution_lim)
    relval = lake_problem_JDM_rel_3L(pollution_lim)
    phoval = lake_problem_JDM_pho_3L(pollution_lim)
    pt1 = (econval, relval, phoval)
    (pta, ptb) = find_shortest_33(pt1, refset)
    dist1 = distance.euclidean((econval, relval, phoval), pta)
    dist2 = distance.euclidean((econval, relval, phoval), ptb)
    score = np.min((dist1, dist2))
    return score


def score_2D_1L(pollution_lim):
    # This function compares the difference between the distance between a user-
    # selected point from the pareto front and the distance between the origin
    # and the pareto front. it returns a skill score in which "1" is on the Pareto
    # front and "0" is on the origin.
    yourdist = measure_2D_1L(pollution_lim)
    naivedist = measure_2D_1L((0.03))
    skillscore = 1 - yourdist/naivedist
    return skillscore

def score_3D_1L(pollution_lim):
    # This function compares the difference between the distance between a user-
    # selected point from the pareto front and the distance between the origin
    # and the pareto front. it returns a skill score in which "1" is on the Pareto
    # front and "0" is on the origin.
    yourdist = measure_3D_1L(pollution_lim)
    naivedist = measure_3D_1L(0.012)
    skillscore = 1 - yourdist/naivedist
    return skillscore

def score_1D_2L(pollution_lim):
    # This function compares the difference between the distance between a user-
    # selected point from the pareto front and the distance between the origin
    # and the pareto front. it returns a skill score in which "1" is on the Pareto
    # front and "0" is on the origin.
    reference = lake_problem_JDM_uti_2L((0.1, 0.1))
    score = lake_problem_JDM_uti_2L(pollution_lim)
    naive = lake_problem_JDM_uti_2L((0, 0))

    skillscore = (score-naive)/(reference-naive)
    return skillscore

def score_2D_2L(pollution_lim):
    # This function compares the difference between the distance between a user-
    # selected point from the pareto front and the distance between the origin
    # and the pareto front. it returns a skill score in which "1" is on the Pareto
    # front and "0" is on the origin.
    yourdist = measure_2D_2L(pollution_lim)
    naivedist = measure_2D_2L((0,0.07))
    skillscore = 1 - yourdist/naivedist
    return skillscore

def score_3D_2L(pollution_lim):
    # This function compares the difference between the distance between a user-
    # selected point from the pareto front and the distance between the origin
    # and the pareto front. it returns a skill score in which "1" is on the Pareto
    # front and "0" is on the origin.
    yourdist = measure_3D_2L(pollution_lim)
    naivedist = measure_3D_2L((0.066,0.00))
    skillscore = 1 - yourdist/naivedist
    return skillscore

def score_1D_3L(pollution_lim):
    # This function compares the difference between the distance between a user-
    # selected point from the pareto front and the distance between the origin
    # and the pareto front. it returns a skill score in which "1" is on the Pareto
    # front and "0" is on the origin.
    reference = lake_problem_JDM_uti_3L((0.1, 0.1, 0.1))
    score = lake_problem_JDM_uti_3L(pollution_lim)
    naive = lake_problem_JDM_uti_3L((0, 0, 0))

    skillscore = (score-naive)/(reference-naive)
    return skillscore

def score_2D_3L(pollution_lim):
    # This function compares the difference between the distance between a user-
    # selected point from the pareto front and the distance between the origin
    # and the pareto front. it returns a skill score in which "1" is on the Pareto
    # front and "0" is on the origin.
    yourdist = measure_2D_3L(pollution_lim)
    naivedist = measure_2D_3L((0,0.0,0.1))   # I think this might be the worst you can do
    skillscore = 1 - yourdist/naivedist
    return skillscore

def score_3D_3L(pollution_lim):
    # This function compares the difference between the distance between a user-
    # selected point from the pareto front and the distance between the origin
    # and the pareto front. it returns a skill score in which "1" is on the Pareto
    # front and "0" is on the origin.
    yourdist = measure_3D_3L(pollution_lim)
    naivedist = measure_3D_3L((0,0,0.04))
    skillscore = 1 - yourdist/naivedist
    return skillscore
#
def randomize_preferences(numsettings, seed=None):
    
    if seed is None:
        random_1L = np.random.uniform(low=0.0, high=0.10, size=(numsettings,1))
        random_2L = np.random.uniform(low=0.0, high = 0.10, size=(numsettings,2))
        random_3L = np.random.uniform(low=0.0, high = 0.10, size=(numsettings,3))
    else:
        numpy.random.seed(seed)
        random_1L = np.random.uniform(low=0.0, high=0.10, size=(numsettings,1))
        numpy.random.seed(seed)
        random_2L = np.random.uniform(low=0.0, high = 0.10, size=(numsettings,2))
        numpy.random.seed(seed)
        random_3L = np.random.uniform(low=0.0, high = 0.10, size=(numsettings,3))

    return(random_1L, random_2L, random_3L)

def randomize_score(numsettings, seed=None):
    if seed is None:
        random_1L = np.random.uniform(low=0.0, high=0.10, size=(1,numsettings))
        random_2L = np.random.uniform(low=0.0, high = 0.10, size=(2,numsettings))
        random_3L = np.random.uniform(low=0.0, high = 0.10, size=(3,numsettings))
    else:
        numpy.random.seed(seed)
        random_1L = np.random.uniform(low=0.0, high=0.10, size=(1,numsettings))
        numpy.random.seed(seed)
        random_2L = np.random.uniform(low=0.0, high = 0.10, size=(2,numsettings))
        numpy.random.seed(seed)
        random_3L = np.random.uniform(low=0.0, high = 0.10, size=(3,numsettings))
    
    score_1D1L = list()
    score_1D2L = list()
    score_1D3L = list()
    score_2D1L = list()
    score_2D2L = list()
    score_2D3L = list()
    score_3D1L = list()
    score_3D2L = list()
    score_3D3L = list()
    
    for k in range(numsettings):
        score_1D1L.append(score_1D_1L(random_1L[0][k]))
        score_2D1L.append(score_2D_1L(random_1L[0][k]))
        score_3D1L.append(score_3D_1L(random_1L[0][k]))
        
        score_1D2L.append(score_1D_2L(random_2L[:,k]))
        score_2D2L.append(score_2D_2L(random_2L[:,k]))
        score_3D2L.append(score_3D_2L(random_2L[:,k]))
        
        score_1D3L.append(score_1D_3L(random_3L[:,k]))
        score_2D3L.append(score_2D_3L(random_3L[:,k]))
        score_3D3L.append(score_3D_3L(random_3L[:,k]))
        
    scores = dict()
    
    scores['score_1D'] = dict()
    scores['score_2D'] = dict()
    scores['score_3D'] = dict()
    
    scores['score_1D']['1L'] = score_1D1L
    scores['score_1D']['2L'] = score_1D2L
    scores['score_1D']['3L'] = score_1D3L
    
    scores['score_2D']['1L'] = score_2D1L
    scores['score_2D']['2L'] = score_2D2L
    scores['score_2D']['3L'] = score_2D3L
    
    scores['score_3D']['1L'] = score_3D1L
    scores['score_3D']['2L'] = score_3D2L
    scores['score_3D']['3L'] = score_3D3L

    return(scores)

#''' Figure-generating functions'''
#
def score_track(group):
    
    ''' .'''
    
    nsubjects = len(group['result']['obj1']['lev1']['test'])
    scores = list()
    
    for k in range(nsubjects):
        subscore = list()
        subscore.append(group['result']['obj1']['lev1']['test'][k][8][0])
        subscore.append(group['result']['obj1']['lev2']['test'][k][8][0])
        subscore.append(group['result']['obj1']['lev3']['test'][k][8][0])
        subscore.append(group['result']['obj2']['lev1']['test'][k][8][0])
        if isinstance(group['result']['obj2']['lev2']['test'][k], np.ndarray):
            subscore.append(-99)
        else:
            subscore.append(group['result']['obj2']['lev2']['test'][k][8][0])
        subscore.append(group['result']['obj2']['lev3']['test'][k][8][0])
        subscore.append(group['result']['obj3']['lev1']['test'][k][8][0])
        subscore.append(group['result']['obj3']['lev2']['test'][k][8][0])
        subscore.append(group['result']['obj3']['lev3']['test'][k][8][0])
        
        scores.append(subscore)
        
    return(scores)
#    
def code_track(group, codename):
    
    ''' .'''
    
    nsubjects = len(group['result']['obj1']['lev1'][codename])
    scores = list()
    
    for k in range(nsubjects):
        subscore = list()
        subscore.append(group['result']['obj1']['lev1'][codename][k])
        subscore.append(group['result']['obj1']['lev2'][codename][k])
        subscore.append(group['result']['obj1']['lev3'][codename][k])
        subscore.append(group['result']['obj2']['lev1'][codename][k])
        subscore.append(group['result']['obj2']['lev2'][codename][k])
        subscore.append(group['result']['obj2']['lev3'][codename][k])
        subscore.append(group['result']['obj3']['lev1'][codename][k])
        subscore.append(group['result']['obj3']['lev2'][codename][k])
        subscore.append(group['result']['obj3']['lev3'][codename][k])
        
        scores.append(subscore)
        
    return(scores)
 
def scores_boxplot(group_scoretrack):
    
    scores_1D1L = list()
    scores_1D2L = list()
    scores_1D3L = list()
    
    scores_2D1L = list()
    scores_2D2L = list()
    scores_2D3L = list()
    
    scores_3D1L = list()
    scores_3D2L = list()
    scores_3D3L = list()
    
    for k in range(len(group_scoretrack)):
        scores_1D1L.append(group_scoretrack[k][0])
        scores_1D2L.append(group_scoretrack[k][1])
        scores_1D3L.append(group_scoretrack[k][2])
        scores_2D1L.append(group_scoretrack[k][3])
        scores_2D2L.append(group_scoretrack[k][4])
        scores_2D3L.append(group_scoretrack[k][5])
        scores_3D1L.append(group_scoretrack[k][6])
        scores_3D2L.append(group_scoretrack[k][7])
        scores_3D3L.append(group_scoretrack[k][8])
        
    scores = dict()
    scores['1D1L'] = scores_1D1L
    scores['1D2L'] = scores_1D2L
    scores['1D3L'] = scores_1D3L
    scores['2D1L'] = scores_2D1L
    scores['2D2L'] = scores_2D2L
    scores['2D3L'] = scores_2D3L
    scores['3D1L'] = scores_3D1L
    scores['3D2L'] = scores_3D2L
    scores['3D3L'] = scores_3D3L
    
    return(scores)
#    
def code_boxplot(group_scoretrack):
    
    scores_1D1L = list()
    scores_1D2L = list()
    scores_1D3L = list()
    
    scores_2D1L = list()
    scores_2D2L = list()
    scores_2D3L = list()
    
    scores_3D1L = list()
    scores_3D2L = list()
    scores_3D3L = list()
    
    for k in range(len(group_scoretrack)):
        scores_1D1L.append(group_scoretrack[k][0])
        scores_1D2L.append(group_scoretrack[k][1])
        scores_1D3L.append(group_scoretrack[k][2])
        scores_2D1L.append(group_scoretrack[k][3])
        scores_2D2L.append(group_scoretrack[k][4])
        scores_2D3L.append(group_scoretrack[k][5])
        scores_3D1L.append(group_scoretrack[k][6])
        scores_3D2L.append(group_scoretrack[k][7])
        scores_3D3L.append(group_scoretrack[k][8])
        
    scores = dict()
    scores['1D1L'] = scores_1D1L
    scores['1D2L'] = scores_1D2L
    scores['1D3L'] = scores_1D3L
    scores['2D1L'] = scores_2D1L
    scores['2D2L'] = scores_2D2L
    scores['2D3L'] = scores_2D3L
    scores['3D1L'] = scores_3D1L
    scores['3D2L'] = scores_3D2L
    scores['3D3L'] = scores_3D3L
    
    return(scores)
#    
def naivenorm(scores, scoresrand):
    
    L_scores = len(scores)
    L_naive = len(scoresrand)
    
    score_norm = list()
    
    for k in range(L_scores):
        if scores[k] < 0:
            score_norm.append(-99)
        else:
            score_norm.append(np.sum(scoresrand < scores[k])/L_naive)
        
    return(score_norm)
    
   
def score_uti_1L(strategy):
    
    minuti = lake_problem_JDM_uti_1L(0)
    maxuti = lake_problem_JDM_uti_1L(0.1)
    
    uti = lake_problem_JDM_uti_1L(strategy)
    
    utiscore = (uti - minuti)/(maxuti-minuti)
    
    return(utiscore)
    
def score_pho_1L(strategy):
    
    minpho = lake_problem_JDM_pho_1L(0)
    maxpho = lake_problem_JDM_pho_1L(0.1)
    
    pho = lake_problem_JDM_pho_1L(strategy)
    
    phoscore = 1 - (pho - minpho)/(maxpho-minpho)
    
    return(phoscore)
    
def score_rel_1L(strategy):
    
    minrel = lake_problem_JDM_rel_1L(0.1)
    maxrel = lake_problem_JDM_rel_1L(0)
    
    rel = lake_problem_JDM_rel_1L(strategy)
    
    relscore = (rel - minrel)/(maxrel-minrel)
    
    return(relscore)
       
    
def score_uti_2L(strategy):
    
    minuti = lake_problem_JDM_uti_2L((0,0))
    maxuti = lake_problem_JDM_uti_2L((0.1,0.1))
    
    uti = lake_problem_JDM_uti_2L(strategy)
    
    utiscore = (uti - minuti)/(maxuti-minuti)
    
    return(utiscore)
    
def score_pho_2L(strategy):
    
    minpho = lake_problem_JDM_pho_2L((0,0))
    maxpho = lake_problem_JDM_pho_2L((0.1,0.1))
    
    pho = lake_problem_JDM_pho_2L(strategy)
    
    phoscore = 1 - (pho - minpho)/(maxpho-minpho)
    
    return(phoscore)
    
def score_rel_2L(strategy):
    
    minrel = lake_problem_JDM_rel_2L((0.1,0.1))
    maxrel = lake_problem_JDM_rel_2L((0,0))
    
    rel = lake_problem_JDM_rel_2L(strategy)
    
    relscore = (rel - minrel)/(maxrel-minrel)
    
    return(relscore)
    
def score_uti_3L(strategy):
    
    minuti = lake_problem_JDM_uti_3L((0,0,0))
    maxuti = lake_problem_JDM_uti_3L((0.1,0.1,0.1))
    
    uti = lake_problem_JDM_uti_3L(strategy)
    
    utiscore = (uti - minuti)/(maxuti-minuti)
    
    return(utiscore)
    
def score_pho_3L(strategy):
    
    minpho = lake_problem_JDM_pho_3L((0,0,0))
    maxpho = lake_problem_JDM_pho_3L((0.1,0.1,0.1))
    
    pho = lake_problem_JDM_pho_3L(strategy)
    
    phoscore = 1 - (pho - minpho)/(maxpho-minpho)
    
    return(phoscore)
    
def score_rel_3L(strategy):
    
    minrel = lake_problem_JDM_rel_3L((0.1,0.1,0.1))
    maxrel = lake_problem_JDM_rel_3L((0,0,0))
    
    rel = lake_problem_JDM_rel_3L(strategy)
    
    relscore = (rel - minrel)/(maxrel-minrel)
    
    return(relscore)

def score_utipho_1L(strategy):
    score_pho = score_pho_1L(strategy)
    score_uti = score_uti_1L(strategy)
    
    utipho = score_pho - score_uti
    
    return(utipho)
#    
def score_utirel_1L(strategy):
    score_rel = score_rel_1L(strategy)
    score_uti = score_uti_1L(strategy)
    
    utirel = score_rel - score_uti
    
    return(utirel)
    
def score_utipho_2L(strategy):
    score_pho = score_pho_2L(strategy)
    score_uti = score_uti_2L(strategy)
    
    utipho = score_pho - score_uti
    
    return(utipho)
    
def score_utirel_2L(strategy):
    score_rel = score_rel_2L(strategy)
    score_uti = score_uti_2L(strategy)
    
    utirel = score_rel - score_uti
    
    return(utirel)
    
def score_utipho_3L(strategy):
    score_pho = score_pho_3L(strategy)
    score_uti = score_uti_3L(strategy)
    
    utipho = score_pho - score_uti
    
    return(utipho)
    
def score_utirel_3L(strategy):
    score_rel = score_rel_3L(strategy)
    score_uti = score_uti_3L(strategy)
    
    utirel = score_rel - score_uti
    
    return(utirel)
 
def group_preference(test1lev, test2lev, test3lev, flag):
    
    scores_utirel = dict()
    scores_utipho = dict()
    
    scores_utirel['1D1L'] = list()
    scores_utirel['1D2L'] = list()
    scores_utirel['1D3L'] = list()
    scores_utirel['2D1L'] = list()
    scores_utirel['2D2L'] = list()
    scores_utirel['2D3L'] = list()
    scores_utirel['3D1L'] = list()
    scores_utirel['3D2L'] = list()
    scores_utirel['3D3L'] = list()
    scores_utipho['1D1L'] = list()
    scores_utipho['1D2L'] = list()
    scores_utipho['1D3L'] = list()
    scores_utipho['2D1L'] = list()
    scores_utipho['2D2L'] = list()
    scores_utipho['2D3L'] = list()
    scores_utipho['3D1L'] = list()
    scores_utipho['3D2L'] = list()
    scores_utipho['3D3L'] = list()
    
    if flag == 0:
        for k in range(len(test1lev['obj1'])):
            scores_utirel['1D1L'].append(score_utirel_1L(pd.DataFrame.as_matrix(test1lev['obj1'][k])))

            scores_utirel['1D2L'].append(score_utirel_2L(pd.DataFrame.as_matrix(test2lev['obj1'][k])[0]))
            scores_utirel['1D3L'].append(score_utirel_3L(pd.DataFrame.as_matrix(test3lev['obj1'][k])[0]))
            
            scores_utirel['2D1L'].append(score_utirel_1L(pd.DataFrame.as_matrix(test1lev['obj2'][k])))
            scores_utirel['2D2L'].append(score_utirel_2L(pd.DataFrame.as_matrix(test2lev['obj2'][k])[0]))
            scores_utirel['2D3L'].append(score_utirel_3L(pd.DataFrame.as_matrix(test3lev['obj2'][k])[0]))
            
            scores_utirel['3D1L'].append(score_utirel_1L(pd.DataFrame.as_matrix(test1lev['obj3'][k])))
            scores_utirel['3D2L'].append(score_utirel_2L(pd.DataFrame.as_matrix(test2lev['obj3'][k])[0]))
            scores_utirel['3D3L'].append(score_utirel_3L(pd.DataFrame.as_matrix(test3lev['obj3'][k])[0]))
            
            scores_utipho['1D1L'].append(score_utipho_1L(pd.DataFrame.as_matrix(test1lev['obj1'][k])))
            scores_utipho['1D2L'].append(score_utipho_2L(pd.DataFrame.as_matrix(test2lev['obj1'][k])[0]))
            scores_utipho['1D3L'].append(score_utipho_3L(pd.DataFrame.as_matrix(test3lev['obj1'][k])[0]))
            
            scores_utipho['2D1L'].append(score_utipho_1L(pd.DataFrame.as_matrix(test1lev['obj2'][k])))
            scores_utipho['2D2L'].append(score_utipho_2L(pd.DataFrame.as_matrix(test2lev['obj2'][k])[0]))
            scores_utipho['2D3L'].append(score_utipho_3L(pd.DataFrame.as_matrix(test3lev['obj2'][k])[0]))
            
            scores_utipho['3D1L'].append(score_utipho_1L(pd.DataFrame.as_matrix(test1lev['obj3'][k])))
            scores_utipho['3D2L'].append(score_utipho_2L(pd.DataFrame.as_matrix(test2lev['obj3'][k])[0]))
            scores_utipho['3D3L'].append(score_utipho_3L(pd.DataFrame.as_matrix(test3lev['obj3'][k])[0]))
    else:
        for k in range(len(test1lev['obj1'])):
            # One objective, reliability
            scores_utirel['1D1L'].append(score_utirel_1L(pd.DataFrame.as_matrix(test1lev['obj1'][k]/100)))
            scores_utirel['1D2L'].append(score_utirel_2L(pd.DataFrame.as_matrix(test2lev['obj1'][k])[0]/100))
            scores_utirel['1D3L'].append(score_utirel_3L(pd.DataFrame.as_matrix(test3lev['obj1'][k])[0]/100))
            
            # Two objectives, rel
            scores_utirel['2D1L'].append(score_utirel_1L(pd.DataFrame.as_matrix(test1lev['obj2'][k]/100)))
            if issubclass(type(test2lev['obj2'][k]), np.ndarray):
                scores_utirel['2D2L'].append(-99)
                print(type(test2lev['obj2'][k]))
            else:
                scores_utirel['2D2L'].append(score_utirel_2L(pd.DataFrame.as_matrix(test2lev['obj2'][k])[0]/100))
            scores_utirel['2D3L'].append(score_utirel_3L(pd.DataFrame.as_matrix(test3lev['obj2'][k])[0]/100))
            
            # 3 objectives, reliability
            scores_utirel['3D1L'].append(score_utirel_1L(pd.DataFrame.as_matrix(test1lev['obj3'][k]/100)))
            if issubclass(type(test2lev['obj3'][k]), np.ndarray):
                scores_utirel['3D2L'].append(-99)
                print(type(test2lev['obj3'][k]))
            else:
                scores_utirel['3D2L'].append(score_utirel_2L(pd.DataFrame.as_matrix(test2lev['obj3'][k])[0]/100))
            scores_utirel['3D3L'].append(score_utirel_3L(pd.DataFrame.as_matrix(test3lev['obj3'][k])[0]/100))
            
            # One, objective, pho
            scores_utipho['1D1L'].append(score_utipho_1L(pd.DataFrame.as_matrix(test1lev['obj1'][k]/100)))
            if issubclass(type(test2lev['obj1'][k]), np.ndarray):
                scores_utipho['1D2L'].append(-99)
                print(type(test2lev['obj1'][k]))
            else:
                scores_utipho['1D2L'].append(score_utipho_2L(pd.DataFrame.as_matrix(test2lev['obj1'][k])[0]/100))
            scores_utipho['1D3L'].append(score_utipho_3L(pd.DataFrame.as_matrix(test3lev['obj1'][k])[0]/100))
            
            # Two objectives, pho
            scores_utipho['2D1L'].append(score_utipho_1L(pd.DataFrame.as_matrix(test1lev['obj2'][k]/100)))
            if issubclass(type(test2lev['obj2'][k]), np.ndarray):
                scores_utipho['2D2L'].append(-99)
                print(type(test2lev['obj2'][k]))
            else:
                scores_utipho['2D2L'].append(score_utipho_2L(pd.DataFrame.as_matrix(test2lev['obj2'][k])[0]/100))
            scores_utipho['2D3L'].append(score_utipho_3L(pd.DataFrame.as_matrix(test3lev['obj2'][k])[0]/100))
            
            # Three objectives, pho
            scores_utipho['3D1L'].append(score_utipho_1L(pd.DataFrame.as_matrix(test1lev['obj3'][k]/100)))
            scores_utipho['3D2L'].append(score_utipho_2L(pd.DataFrame.as_matrix(test2lev['obj3'][k])[0]/100))
            scores_utipho['3D3L'].append(score_utipho_3L(pd.DataFrame.as_matrix(test3lev['obj3'][k])[0]/100))
        
    return(scores_utirel, scores_utipho)
#    
def group_prefnorm(utirel, utipho, rand_utirel_1L, rand_utirel_2L, rand_utirel_3L, rand_utipho_1L, rand_utipho_2L, rand_utipho_3L):
    
    utirel_norm = dict()
    utipho_norm = dict()
    
    utirel_norm['1D1L'] = list()
    utirel_norm['1D2L'] = list()
    utirel_norm['1D3L'] = list()
    utirel_norm['2D1L'] = list()
    utirel_norm['2D2L'] = list()
    utirel_norm['2D3L'] = list()
    utirel_norm['3D1L'] = list()
    utirel_norm['3D2L'] = list()
    utirel_norm['3D3L'] = list()
    utipho_norm['1D1L'] = list()
    utipho_norm['1D2L'] = list()
    utipho_norm['1D3L'] = list()
    utipho_norm['2D1L'] = list()
    utipho_norm['2D2L'] = list()
    utipho_norm['2D3L'] = list()
    utipho_norm['3D1L'] = list()
    utipho_norm['3D2L'] = list()
    utipho_norm['3D3L'] = list()
    
    for k in range(len(utirel['1D1L'])):
        utirel_norm['1D1L'].append(np.sum(utirel['1D1L'][k] > rand_utirel_1L)/len(rand_utirel_1L))
        utirel_norm['1D2L'].append(np.sum(utirel['1D2L'][k] > rand_utirel_2L)/len(rand_utirel_2L))
        utirel_norm['1D3L'].append(np.sum(utirel['1D3L'][k] > rand_utirel_3L)/len(rand_utirel_3L))
        
        utirel_norm['2D1L'].append(np.sum(utirel['2D1L'][k] > rand_utirel_1L)/len(rand_utirel_1L))
        if utirel['2D2L'][k] < 0:
            utirel_norm['2D2L'].append(-99)
        else:
            utirel_norm['2D2L'].append(np.sum(utirel['2D2L'][k] > rand_utirel_2L)/len(rand_utirel_2L))
        utirel_norm['2D3L'].append(np.sum(utirel['2D3L'][k] > rand_utirel_3L)/len(rand_utirel_3L))
        
        utirel_norm['3D1L'].append(np.sum(utirel['3D1L'][k] > rand_utirel_1L)/len(rand_utirel_1L))
        utirel_norm['3D2L'].append(np.sum(utirel['3D2L'][k] > rand_utirel_2L)/len(rand_utirel_2L))
        utirel_norm['3D3L'].append(np.sum(utirel['3D3L'][k] > rand_utirel_3L)/len(rand_utirel_3L))
        
        utipho_norm['1D1L'].append(np.sum(utipho['1D1L'][k] > rand_utipho_1L)/len(rand_utipho_1L))
        utipho_norm['1D2L'].append(np.sum(utipho['1D2L'][k] > rand_utipho_2L)/len(rand_utipho_2L))
        utipho_norm['1D3L'].append(np.sum(utipho['1D3L'][k] > rand_utipho_3L)/len(rand_utipho_3L))
        
        utipho_norm['2D1L'].append(np.sum(utipho['2D1L'][k] > rand_utipho_1L)/len(rand_utipho_1L))
        if utipho['2D2L'][k] < 0:
            utipho_norm['2D2L'].append(-99)
        else:
            utipho_norm['2D2L'].append(np.sum(utipho['2D2L'][k] > rand_utipho_2L)/len(rand_utipho_2L))
        utipho_norm['2D3L'].append(np.sum(utipho['2D3L'][k] > rand_utipho_3L)/len(rand_utipho_3L))
        
        utipho_norm['3D1L'].append(np.sum(utipho['3D1L'][k] > rand_utipho_1L)/len(rand_utipho_1L))
        utipho_norm['3D2L'].append(np.sum(utipho['3D2L'][k] > rand_utipho_2L)/len(rand_utipho_2L))
        utipho_norm['3D3L'].append(np.sum(utipho['3D3L'][k] > rand_utipho_3L)/len(rand_utipho_3L))
    
    return(utirel_norm, utipho_norm)
#    
def scores_preference(group1, group2, group3, group4):
    
    (rand_1L, rand_2L, rand_3L) = randomize_preferences(400)
    
    testA_1lev = onelev_unwind(group1)
    testB_1lev = onelev_unwind(group2)
    testC_1lev = onelev_unwind(group3)
    testD_1lev = onelev_unwind(group4)

    testA_2lev = twolev_unwind(group1)
    testB_2lev = twolev_unwind(group2)
    testC_2lev = twolev_unwind(group3)
    testD_2lev = twolev_unwind(group4)

    testA_3lev = threelev_unwind(group1)
    testB_3lev = threelev_unwind(group2)
    testC_3lev = threelev_unwind(group3)
    testD_3lev = threelev_unwind(group4)
    
    (utirel_A, utipho_A) = group_preference(testA_1lev, testA_2lev, testA_3lev, 0)
    (utirel_B, utipho_B) = group_preference(testB_1lev, testB_2lev, testB_3lev, 0)
    (utirel_C, utipho_C) = group_preference(testC_1lev, testC_2lev, testC_3lev, 1)
    (utirel_D, utipho_D) = group_preference(testD_1lev, testD_2lev, testD_3lev, 1)
    
    
    rand_utirel_1L = list()
    rand_utirel_2L = list()
    rand_utirel_3L = list()
    
    rand_utipho_1L = list()
    rand_utipho_2L = list()
    rand_utipho_3L = list()
    
    for k in range(len(rand_1L)):
        rand_utirel_1L.append(score_utirel_1L(rand_1L[k,:]))
        rand_utirel_2L.append(score_utirel_2L(rand_2L[k,:]))
        rand_utirel_3L.append(score_utirel_3L(rand_3L[k,:]))
        
        rand_utipho_1L.append(score_utipho_1L(rand_1L[k,:]))
        rand_utipho_2L.append(score_utipho_2L(rand_2L[k,:]))
        rand_utipho_3L.append(score_utipho_3L(rand_3L[k,:]))
    
    (utirel_normA, utipho_normA) = group_prefnorm(utirel_A, utipho_A, rand_utirel_1L, rand_utirel_2L, rand_utirel_3L, rand_utipho_1L, rand_utipho_2L, rand_utipho_3L)
    (utirel_normB, utipho_normB) = group_prefnorm(utirel_B, utipho_B, rand_utirel_1L, rand_utirel_2L, rand_utirel_3L, rand_utipho_1L, rand_utipho_2L, rand_utipho_3L)
    (utirel_normC, utipho_normC) = group_prefnorm(utirel_C, utipho_C, rand_utirel_1L, rand_utirel_2L, rand_utirel_3L, rand_utipho_1L, rand_utipho_2L, rand_utipho_3L)
    (utirel_normD, utipho_normD) = group_prefnorm(utirel_D, utipho_D, rand_utirel_1L, rand_utirel_2L, rand_utirel_3L, rand_utipho_1L, rand_utipho_2L, rand_utipho_3L)
    
    # Hold number of objectives constant
    

    
    codesA_PI = code_boxplot(code_track(group1, 'ProblemInterpretation'))
    codesB_PI = code_boxplot(code_track(group2, 'ProblemInterpretation'))
    codesC_PI = code_boxplot(code_track(group3, 'ProblemInterpretation'))
    codesD_PI = code_boxplot(code_track(group4, 'ProblemInterpretation'))
    
    codesA_IS = code_boxplot(code_track(group1, 'Issues'))
    codesB_IS = code_boxplot(code_track(group2, 'Issues'))
    codesC_IS = code_boxplot(code_track(group3, 'Issues'))
    codesD_IS = code_boxplot(code_track(group4, 'Issues'))
    
    codesA_CO = code_boxplot(code_track(group1, 'Confidence'))
    codesB_CO = code_boxplot(code_track(group2, 'Confidence'))
    codesC_CO = code_boxplot(code_track(group3, 'Confidence'))
    codesD_CO = code_boxplot(code_track(group4, 'Confidence'))
    
    codesA_MO = code_boxplot(code_track(group1, 'Motivation'))
    codesB_MO = code_boxplot(code_track(group2, 'Motivation'))
    codesC_MO = code_boxplot(code_track(group3, 'Motivation'))
    codesD_MO = code_boxplot(code_track(group4, 'Motivation'))
    
    codesA_PR = code_boxplot(code_track(group1, 'Preference'))
    codesB_PR = code_boxplot(code_track(group2, 'Preference'))
    codesC_PR = code_boxplot(code_track(group3, 'Preference'))
    codesD_PR = code_boxplot(code_track(group4, 'Preference'))
    
    def code_combine_D(codesA, codesB, codesC, codesD):
    
        codes_1D_A = (codesA['1D1L'], codesA['1D2L'], codesA['1D3L'])
        codes_1D_B = (codesB['1D1L'], codesB['1D2L'], codesB['1D3L'])
        codes_1D_C = (codesC['1D1L'], codesC['1D2L'], codesC['1D3L'])
        codes_1D_D = (codesD['1D1L'], codesD['1D2L'], codesD['1D3L'])
        
        codes_2D_A = (codesA['2D1L'], codesA['2D2L'], codesA['2D3L'])
        codes_2D_B = (codesB['2D1L'], codesB['2D2L'], codesB['2D3L'])
        codes_2D_C = (codesC['2D1L'], codesC['2D2L'], codesC['2D3L'])
        codes_2D_D = (codesD['2D1L'], codesD['2D2L'], codesD['2D3L'])
        
        codes_3D_A = (codesA['3D1L'], codesA['3D2L'], codesA['3D3L'])
        codes_3D_B = (codesB['3D1L'], codesB['3D2L'], codesB['3D3L'])
        codes_3D_C = (codesC['3D1L'], codesC['3D2L'], codesC['3D3L'])
        codes_3D_D = (codesD['3D1L'], codesD['3D2L'], codesD['3D3L'])
        
        return(codes_1D_A, codes_1D_B, codes_1D_C, codes_1D_D, codes_2D_A, codes_2D_B, codes_2D_C, codes_2D_D, codes_3D_A, codes_3D_B, codes_3D_C, codes_3D_D)
    
    def code_combine_L(codesA, codesB, codesC, codesD):
    
        codes_1L_A = (codesA['1D1L'], codesA['2D1L'], codesA['3D1L'])
        codes_1L_B = (codesB['1D1L'], codesB['2D1L'], codesB['3D1L'])
        codes_1L_C = (codesC['1D1L'], codesC['2D1L'], codesC['3D1L'])
        codes_1L_D = (codesD['1D1L'], codesD['2D1L'], codesD['3D1L'])
    
        codes_2L_A = (codesA['1D2L'], codesA['2D2L'], codesA['3D2L'])
        codes_2L_B = (codesB['1D2L'], codesB['2D2L'], codesB['3D2L'])
        codes_2L_C = (codesC['1D2L'], codesC['2D2L'], codesC['3D2L'])
        codes_2L_D = (codesD['1D2L'], codesD['2D2L'], codesD['3D2L'])
    
        codes_3L_A = (codesA['1D3L'], codesA['2D3L'], codesA['3D3L'])
        codes_3L_B = (codesB['1D3L'], codesB['2D3L'], codesB['3D3L'])
        codes_3L_C = (codesC['1D3L'], codesC['2D3L'], codesC['3D3L'])
        codes_3L_D = (codesD['1D3L'], codesD['2D3L'], codesD['3D3L'])
        
        return(codes_1L_A, codes_1L_B, codes_1L_C, codes_1L_D, codes_2L_A, codes_2L_B, codes_2L_C, codes_2L_D, codes_3L_A, codes_3L_B, codes_3L_C, codes_3L_D)
        
    (codes_1L_A_PI, codes_1L_B_PI, codes_1L_C_PI, codes_1L_D_PI, codes_2L_A_PI, codes_2L_B_PI, codes_2L_C_PI, codes_2L_D_PI, codes_3L_A_PI, codes_3L_B_PI, codes_3L_C_PI, codes_3L_D_PI) = code_combine_L(codesA_PI, codesB_PI, codesC_PI, codesD_PI)
    (codes_1L_A_IS, codes_1L_B_IS, codes_1L_C_IS, codes_1L_D_IS, codes_2L_A_IS, codes_2L_B_IS, codes_2L_C_IS, codes_2L_D_IS, codes_3L_A_IS, codes_3L_B_IS, codes_3L_C_IS, codes_3L_D_IS) = code_combine_L(codesA_IS, codesB_IS, codesC_IS, codesD_IS)
    (codes_1L_A_CO, codes_1L_B_CO, codes_1L_C_CO, codes_1L_D_CO, codes_2L_A_CO, codes_2L_B_CO, codes_2L_C_CO, codes_2L_D_CO, codes_3L_A_CO, codes_3L_B_CO, codes_3L_C_CO, codes_3L_D_CO) = code_combine_L(codesA_CO, codesB_CO, codesC_CO, codesD_CO)
    (codes_1L_A_MO, codes_1L_B_MO, codes_1L_C_MO, codes_1L_D_MO, codes_2L_A_MO, codes_2L_B_MO, codes_2L_C_MO, codes_2L_D_MO, codes_3L_A_MO, codes_3L_B_MO, codes_3L_C_MO, codes_3L_D_MO) = code_combine_L(codesA_MO, codesB_MO, codesC_MO, codesD_MO)
    (codes_1L_A_PR, codes_1L_B_PR, codes_1L_C_PR, codes_1L_D_PR, codes_2L_A_PR, codes_2L_B_PR, codes_2L_C_PR, codes_2L_D_PR, codes_3L_A_PR, codes_3L_B_PR, codes_3L_C_PR, codes_3L_D_PR) = code_combine_L(codesA_PR, codesB_PR, codesC_PR, codesD_PR)
    
    (codes_1D_A_PI, codes_1D_B_PI, codes_1D_C_PI, codes_1D_D_PI, codes_2D_A_PI, codes_2D_B_PI, codes_2D_C_PI, codes_2D_D_PI, codes_3D_A_PI, codes_3D_B_PI, codes_3D_C_PI, codes_3D_D_PI) = code_combine_D(codesA_PI, codesB_PI, codesC_PI, codesD_PI)
    (codes_1D_A_IS, codes_1D_B_IS, codes_1D_C_IS, codes_1D_D_IS, codes_2D_A_IS, codes_2D_B_IS, codes_2D_C_IS, codes_2D_D_IS, codes_3D_A_IS, codes_3D_B_IS, codes_3D_C_IS, codes_3D_D_IS) = code_combine_D(codesA_IS, codesB_IS, codesC_IS, codesD_IS)
    (codes_1D_A_CO, codes_1D_B_CO, codes_1D_C_CO, codes_1D_D_CO, codes_2D_A_CO, codes_2D_B_CO, codes_2D_C_CO, codes_2D_D_CO, codes_3D_A_CO, codes_3D_B_CO, codes_3D_C_CO, codes_3D_D_CO) = code_combine_D(codesA_CO, codesB_CO, codesC_CO, codesD_CO)
    (codes_1D_A_MO, codes_1D_B_MO, codes_1D_C_MO, codes_1D_D_MO, codes_2D_A_MO, codes_2D_B_MO, codes_2D_C_MO, codes_2D_D_MO, codes_3D_A_MO, codes_3D_B_MO, codes_3D_C_MO, codes_3D_D_MO) = code_combine_D(codesA_MO, codesB_MO, codesC_MO, codesD_MO)
    (codes_1D_A_PR, codes_1D_B_PR, codes_1D_C_PR, codes_1D_D_PR, codes_2D_A_PR, codes_2D_B_PR, codes_2D_C_PR, codes_2D_D_PR, codes_3D_A_PR, codes_3D_B_PR, codes_3D_C_PR, codes_3D_D_PR) = code_combine_D(codesA_PR, codesB_PR, codesC_PR, codesD_PR)
    
    (utirel_1L_A, utirel_1L_B, utirel_1L_C, utirel_1L_D, utirel_2L_A, utirel_2L_B, utirel_2L_C, utirel_2L_D, utirel_3L_A, utirel_3L_B, utirel_3L_C, utirel_3L_D) = code_combine_L(utirel_normA, utirel_normB, utirel_normC, utirel_normD)
    (utipho_1L_A, utipho_1L_B, utipho_1L_C, utipho_1L_D, utipho_2L_A, utipho_2L_B, utipho_2L_C, utipho_2L_D, utipho_3L_A, utipho_3L_B, utipho_3L_C, utipho_3L_D) = code_combine_L(utipho_normA, utipho_normB, utipho_normC, utipho_normD)
    
    (utirel_1D_A, utirel_1D_B, utirel_1D_C, utirel_1D_D, utirel_2D_A, utirel_2D_B, utirel_2D_C, utirel_2D_D, utirel_3D_A, utirel_3D_B, utirel_3D_C, utirel_3D_D) = code_combine_D(utirel_normA, utirel_normB, utirel_normC, utirel_normD)
    (utipho_1D_A, utipho_1D_B, utipho_1D_C, utipho_1D_D, utipho_2D_A, utipho_2D_B, utipho_2D_C, utipho_2D_D, utipho_3D_A, utipho_3D_B, utipho_3D_C, utipho_3D_D) = code_combine_D(utipho_normA, utipho_normB, utipho_normC, utipho_normD)
    
    conditions1D = list()
    probleminterp1D_a = list()
    probleminterp1D_b = list()
    utirel1D = list()
    utipho1D = list()
    levers1D = list()
    probleminterp1D_a = list()
    probleminterp1D_b = list()
    preference1D_a = list()
    preference1D_b = list()
    motivation1D_a = list()
    motivation1D_b = list()
    issues1D_a = list()
    issues1D_b = list()
    confidence1D_a = list()
    confidence1D_b = list()
    
    conditions2D = list()
    probleminterp2D_a = list()
    probleminterp2D_b = list()
    utirel2D = list()
    utipho2D = list()
    levers2D = list()
    probleminterp2D_a = list()
    probleminterp2D_b = list()
    preference2D_a = list()
    preference2D_b = list()
    motivation2D_a = list()
    motivation2D_b = list()
    issues2D_a = list()
    issues2D_b = list()
    confidence2D_a = list()
    confidence2D_b = list()

    conditions3D = list()
    probleminterp3D_a = list()
    probleminterp3D_b = list()
    utirel3D = list()
    utipho3D = list()
    levers3D = list()
    probleminterp3D_a = list()
    probleminterp3D_b = list()
    preference3D_a = list()
    preference3D_b = list()
    motivation3D_a = list()
    motivation3D_b = list()
    issues3D_a = list()
    issues3D_b = list()
    confidence3D_a = list()
    confidence3D_b = list()
    
    conditions1L = list()
    probleminterp1L_a = list()
    probleminterp1L_b = list()
    utirel1L = list()
    utipho1L = list()
    objs1L = list()
    probleminterp1L_a = list()
    probleminterp1L_b = list()
    preference1L_a = list()
    preference1L_b = list()
    motivation1L_a = list()
    motivation1L_b = list()
    issues1L_a = list()
    issues1L_b = list()
    confidence1L_a = list()
    confidence1L_b = list()
    
    conditions2L = list()
    probleminterp2L_a = list()
    probleminterp2L_b = list()
    utirel2L = list()
    utipho2L = list()
    objs2L = list()
    probleminterp2L_a = list()
    probleminterp2L_b = list()
    preference2L_a = list()
    preference2L_b = list()
    motivation2L_a = list()
    motivation2L_b = list()
    issues2L_a = list()
    issues2L_b = list()
    confidence2L_a = list()
    confidence2L_b = list()
    
    conditions3L = list()
    probleminterp3L_a = list()
    probleminterp3L_b = list()
    utirel3L = list()
    utipho3L = list()
    objs3L = list()
    probleminterp3L_a = list()
    probleminterp3L_b = list()
    preference3L_a = list()
    preference3L_b = list()
    motivation3L_a = list()
    motivation3L_b = list()
    issues3L_a = list()
    issues3L_b = list()
    confidence3L_a = list()
    confidence3L_b = list()
    
    
    for k in range(len(utirel_1D_A)):
        for j in range(len(utirel_1D_A[0])):
            conditions1D.append("Lake Problem")
            utirel1D.append(utirel_1D_A[k][j])
            utipho1D.append(utipho_1D_A[k][j])
            levers1D.append(k + 1)
            probleminterp1D_a.append(codes_1D_A_PI[k][j][0])
            probleminterp1D_b.append(codes_1D_A_PI[k][j][1])
            confidence1D_a.append(codes_1D_A_CO[k][j][0])
            confidence1D_b.append(codes_1D_A_CO[k][j][1])
            issues1D_a.append(codes_1D_A_IS[k][j][0])
            issues1D_b.append(codes_1D_A_IS[k][j][1])
            motivation1D_a.append(codes_1D_A_MO[k][j][0])
            motivation1D_b.append(codes_1D_A_MO[k][j][1])
            preference1D_a.append(codes_1D_A_PR[k][j][0])
            preference1D_b.append(codes_1D_A_PR[k][j][1])
    for k in range(len(utirel_1D_B)):
        for j in range(len(utirel_1D_B[0])):
            conditions1D.append("LP-S")
            utirel1D.append(utirel_1D_B[k][j])
            utipho1D.append(utipho_1D_B[k][j])
            levers1D.append(k + 1)
            probleminterp1D_a.append(codes_1D_B_PI[k][j][0])
            probleminterp1D_b.append(codes_1D_B_PI[k][j][1])
            confidence1D_a.append(codes_1D_B_CO[k][j][0])
            confidence1D_b.append(codes_1D_B_CO[k][j][1])
            issues1D_a.append(codes_1D_B_IS[k][j][0])
            issues1D_b.append(codes_1D_B_IS[k][j][1])
            motivation1D_a.append(codes_1D_B_MO[k][j][0])
            motivation1D_b.append(codes_1D_B_MO[k][j][1])
            preference1D_a.append(codes_1D_B_PR[k][j][0])
            preference1D_b.append(codes_1D_B_PR[k][j][1])
    for k in range(len(utirel_1D_C)):
        for j in range(len(utirel_1D_C[0])):
            conditions1D.append("Neutral Problem")
            utirel1D.append(utirel_1D_C[k][j])
            utipho1D.append(utipho_1D_C[k][j])
            levers1D.append(k + 1)
            probleminterp1D_a.append(codes_1D_C_PI[k][j][0])
            probleminterp1D_b.append(codes_1D_C_PI[k][j][1])
            confidence1D_a.append(codes_1D_C_CO[k][j][0])
            confidence1D_b.append(codes_1D_C_CO[k][j][1])
            issues1D_a.append(codes_1D_C_IS[k][j][0])
            issues1D_b.append(codes_1D_C_IS[k][j][1])
            motivation1D_a.append(codes_1D_C_MO[k][j][0])
            motivation1D_b.append(codes_1D_C_MO[k][j][1])
            preference1D_a.append(codes_1D_C_PR[k][j][0])
            preference1D_b.append(codes_1D_C_PR[k][j][1])
    for k in range(len(utirel_1D_D)):
        for j in range(len(utirel_1D_D[0])):
            conditions1D.append("NP-S")
            utirel1D.append(utirel_1D_D[k][j])
            utipho1D.append(utipho_1D_D[k][j])
            levers1D.append(k + 1)
            probleminterp1D_a.append(codes_1D_D_PI[k][j][0])
            probleminterp1D_b.append(codes_1D_D_PI[k][j][1])
            confidence1D_a.append(codes_1D_D_CO[k][j][0])
            confidence1D_b.append(codes_1D_D_CO[k][j][1])
            issues1D_a.append(codes_1D_D_IS[k][j][0])
            issues1D_b.append(codes_1D_D_IS[k][j][1])
            motivation1D_a.append(codes_1D_D_MO[k][j][0])
            motivation1D_b.append(codes_1D_D_MO[k][j][1])
            preference1D_a.append(codes_1D_D_PR[k][j][0])
            preference1D_b.append(codes_1D_D_PR[k][j][1])
    
        
    byobj = {'Condition': conditions1D, 'Uti-Rel': utirel1D, 'Uti-Pho': utipho1D, 'Levers': levers1D, 
             'Problem Interpretation (a)': probleminterp1D_a, 'Problem Interpretation (b)': probleminterp1D_b,
             'Motivation (a)': motivation1D_a, 'Motivation (b)': motivation1D_b,
             'Preference (a)': preference1D_a, 'Preference (b)': preference1D_b,
             'Issues (a)': issues1D_a, 'Issues (b)': issues1D_b,
             'Confidence (a)': confidence1D_a, 'Confidence (b)': confidence1D_b}
    pref1D = pd.DataFrame(data=byobj)
    
    
    for k in range(len(utirel_2D_A)):
        for j in range(len(utirel_2D_A[0])):
            conditions2D.append("Lake Problem")
            utirel2D.append(utirel_2D_A[k][j])
            utipho2D.append(utipho_2D_A[k][j])
            levers2D.append(k + 1)
            probleminterp2D_a.append(codes_2D_A_PI[k][j][0])
            probleminterp2D_b.append(codes_2D_A_PI[k][j][1])
            confidence2D_a.append(codes_2D_A_CO[k][j][0])
            confidence2D_b.append(codes_2D_A_CO[k][j][1])
            issues2D_a.append(codes_2D_A_IS[k][j][0])
            issues2D_b.append(codes_2D_A_IS[k][j][1])
            motivation2D_a.append(codes_2D_A_MO[k][j][0])
            motivation2D_b.append(codes_2D_A_MO[k][j][1])
            preference2D_a.append(codes_2D_A_PR[k][j][0])
            preference2D_b.append(codes_2D_A_PR[k][j][1])
    for k in range(len(utirel_2D_B)):
        for j in range(len(utirel_2D_B[0])):
            conditions2D.append("LP-S")
            utirel2D.append(utirel_2D_B[k][j])
            utipho2D.append(utipho_2D_B[k][j])
            levers2D.append(k + 1)
            probleminterp2D_a.append(codes_2D_B_PI[k][j][0])
            probleminterp2D_b.append(codes_2D_B_PI[k][j][1])
            confidence2D_a.append(codes_2D_B_CO[k][j][0])
            confidence2D_b.append(codes_2D_B_CO[k][j][1])
            issues2D_a.append(codes_2D_B_IS[k][j][0])
            issues2D_b.append(codes_2D_B_IS[k][j][1])
            motivation2D_a.append(codes_2D_B_MO[k][j][0])
            motivation2D_b.append(codes_2D_B_MO[k][j][1])
            preference2D_a.append(codes_2D_B_PR[k][j][0])
            preference2D_b.append(codes_2D_B_PR[k][j][1])
    for k in range(len(utirel_2D_C)):
        for j in range(len(utirel_2D_C[0])):
            conditions2D.append("Neutral Problem")
            utirel2D.append(utirel_2D_C[k][j])
            utipho2D.append(utipho_2D_C[k][j])
            levers2D.append(k + 1)
            probleminterp2D_a.append(codes_2D_C_PI[k][j][0])
            probleminterp2D_b.append(codes_2D_C_PI[k][j][1])
            confidence2D_a.append(codes_2D_C_CO[k][j][0])
            confidence2D_b.append(codes_2D_C_CO[k][j][1])
            issues2D_a.append(codes_2D_C_IS[k][j][0])
            issues2D_b.append(codes_2D_C_IS[k][j][1])
            motivation2D_a.append(codes_2D_C_MO[k][j][0])
            motivation2D_b.append(codes_2D_C_MO[k][j][1])
            preference2D_a.append(codes_2D_C_PR[k][j][0])
            preference2D_b.append(codes_2D_C_PR[k][j][1])
    for k in range(len(utirel_2D_D)):
        for j in range(len(utirel_2D_D[0])):
            conditions2D.append("NP-S")
            utirel2D.append(utirel_2D_D[k][j])
            utipho2D.append(utipho_2D_D[k][j])
            levers2D.append(k + 1)
            probleminterp2D_a.append(codes_2D_D_PI[k][j][0])
            probleminterp2D_b.append(codes_2D_D_PI[k][j][1])
            confidence2D_a.append(codes_2D_D_CO[k][j][0])
            confidence2D_b.append(codes_2D_D_CO[k][j][1])
            issues2D_a.append(codes_2D_D_IS[k][j][0])
            issues2D_b.append(codes_2D_D_IS[k][j][1])
            motivation2D_a.append(codes_2D_D_MO[k][j][0])
            motivation2D_b.append(codes_2D_D_MO[k][j][1])
            preference2D_a.append(codes_2D_D_PR[k][j][0])
            preference2D_b.append(codes_2D_D_PR[k][j][1])
        
    byobj = {'Condition': conditions2D, 'Uti-Rel': utirel2D, 'Uti-Pho': utipho2D, 'Levers': levers2D, 
             'Problem Interpretation (a)': probleminterp2D_a, 'Problem Interpretation (b)': probleminterp2D_b,
             'Motivation (a)': motivation2D_a, 'Motivation (b)': motivation2D_b,
             'Preference (a)': preference2D_a, 'Preference (b)': preference2D_b,
             'Issues (a)': issues2D_a, 'Issues (b)': issues2D_b,
             'Confidence (a)': confidence2D_a, 'Confidence (b)': confidence2D_b}
    pref2D = pd.DataFrame(data=byobj)
    
    
    
    for k in range(len(utirel_3D_A)):
        for j in range(len(utirel_3D_A[0])):
            conditions3D.append("Lake Problem")
            utirel3D.append(utirel_3D_A[k][j])
            utipho3D.append(utipho_3D_A[k][j])
            levers3D.append(k + 1)
            probleminterp3D_a.append(codes_3D_A_PI[k][j][0])
            probleminterp3D_b.append(codes_3D_A_PI[k][j][1])
            confidence3D_a.append(codes_3D_A_CO[k][j][0])
            confidence3D_b.append(codes_3D_A_CO[k][j][1])
            issues3D_a.append(codes_3D_A_IS[k][j][0])
            issues3D_b.append(codes_3D_A_IS[k][j][1])
            motivation3D_a.append(codes_3D_A_MO[k][j][0])
            motivation3D_b.append(codes_3D_A_MO[k][j][1])
            preference3D_a.append(codes_3D_A_PR[k][j][0])
            preference3D_b.append(codes_3D_A_PR[k][j][1])
    for k in range(len(utirel_3D_B)):
        for j in range(len(utirel_3D_B[0])):
            conditions3D.append("LP-S")
            utirel3D.append(utirel_3D_B[k][j])
            utipho3D.append(utipho_3D_B[k][j])
            levers3D.append(k + 1)
            probleminterp3D_a.append(codes_3D_B_PI[k][j][0])
            probleminterp3D_b.append(codes_3D_B_PI[k][j][1])
            confidence3D_a.append(codes_3D_B_CO[k][j][0])
            confidence3D_b.append(codes_3D_B_CO[k][j][1])
            issues3D_a.append(codes_3D_B_IS[k][j][0])
            issues3D_b.append(codes_3D_B_IS[k][j][1])
            motivation3D_a.append(codes_3D_B_MO[k][j][0])
            motivation3D_b.append(codes_3D_B_MO[k][j][1])
            preference3D_a.append(codes_3D_B_PR[k][j][0])
            preference3D_b.append(codes_3D_B_PR[k][j][1])
    for k in range(len(utirel_3D_C)):
        for j in range(len(utirel_3D_C[0])):
            conditions3D.append("Neutral Problem")
            utirel3D.append(utirel_3D_C[k][j])
            utipho3D.append(utipho_3D_C[k][j])
            levers3D.append(k + 1)
            probleminterp3D_a.append(codes_3D_C_PI[k][j][0])
            probleminterp3D_b.append(codes_3D_C_PI[k][j][1])
            confidence3D_a.append(codes_3D_C_CO[k][j][0])
            confidence3D_b.append(codes_3D_C_CO[k][j][1])
            issues3D_a.append(codes_3D_C_IS[k][j][0])
            issues3D_b.append(codes_3D_C_IS[k][j][1])
            motivation3D_a.append(codes_3D_C_MO[k][j][0])
            motivation3D_b.append(codes_3D_C_MO[k][j][1])
            preference3D_a.append(codes_3D_C_PR[k][j][0])
            preference3D_b.append(codes_3D_C_PR[k][j][1])
    for k in range(len(utirel_3D_D)):
        for j in range(len(utirel_3D_D[0])):
            conditions3D.append("NP-S")
            utirel3D.append(utirel_3D_D[k][j])
            utipho3D.append(utipho_3D_D[k][j])
            levers3D.append(k + 1)
            probleminterp3D_a.append(codes_3D_D_PI[k][j][0])
            probleminterp3D_b.append(codes_3D_D_PI[k][j][1])
            confidence3D_a.append(codes_3D_D_CO[k][j][0])
            confidence3D_b.append(codes_3D_D_CO[k][j][1])
            issues3D_a.append(codes_3D_D_IS[k][j][0])
            issues3D_b.append(codes_3D_D_IS[k][j][1])
            motivation3D_a.append(codes_3D_D_MO[k][j][0])
            motivation3D_b.append(codes_3D_D_MO[k][j][1])
            preference3D_a.append(codes_3D_D_PR[k][j][0])
            preference3D_b.append(codes_3D_D_PR[k][j][1])
        
    byobj = {'Condition': conditions3D, 'Uti-Rel': utirel3D, 'Uti-Pho': utipho3D, 'Levers': levers3D, 
             'Problem Interpretation (a)': probleminterp3D_a, 'Problem Interpretation (b)': probleminterp3D_b,
             'Motivation (a)': motivation3D_a, 'Motivation (b)': motivation3D_b,
             'Preference (a)': preference3D_a, 'Preference (b)': preference3D_b,
             'Issues (a)': issues3D_a, 'Issues (b)': issues3D_b,
             'Confidence (a)': confidence3D_a, 'Confidence (b)': confidence3D_b}
    pref3D = pd.DataFrame(data=byobj)
    
    '''                    LEVERS                          '''
    
    for k in range(len(utirel_1L_A)):
        for j in range(len(utirel_1L_A[0])):
            conditions1L.append("Lake Problem")
            utirel1L.append(utirel_1L_A[k][j])
            utipho1L.append(utipho_1L_A[k][j])
            objs1L.append(k + 1)
            probleminterp1L_a.append(codes_1L_A_PI[k][j][0])
            probleminterp1L_b.append(codes_1L_A_PI[k][j][1])
            confidence1L_a.append(codes_1L_A_CO[k][j][0])
            confidence1L_b.append(codes_1L_A_CO[k][j][1])
            issues1L_a.append(codes_1L_A_IS[k][j][0])
            issues1L_b.append(codes_1L_A_IS[k][j][1])
            motivation1L_a.append(codes_1L_A_MO[k][j][0])
            motivation1L_b.append(codes_1L_A_MO[k][j][1])
            preference1L_a.append(codes_1L_A_PR[k][j][0])
            preference1L_b.append(codes_1L_A_PR[k][j][1])
    for k in range(len(utirel_1L_B)):
        for j in range(len(utirel_1L_B[0])):
            conditions1L.append("LP-S")
            utirel1L.append(utirel_1L_B[k][j])
            utipho1L.append(utipho_1L_B[k][j])
            objs1L.append(k + 1)
            probleminterp1L_a.append(codes_1L_B_PI[k][j][0])
            probleminterp1L_b.append(codes_1L_B_PI[k][j][1])
            confidence1L_a.append(codes_1L_B_CO[k][j][0])
            confidence1L_b.append(codes_1L_B_CO[k][j][1])
            issues1L_a.append(codes_1L_B_IS[k][j][0])
            issues1L_b.append(codes_1L_B_IS[k][j][1])
            motivation1L_a.append(codes_1L_B_MO[k][j][0])
            motivation1L_b.append(codes_1L_B_MO[k][j][1])
            preference1L_a.append(codes_1L_B_PR[k][j][0])
            preference1L_b.append(codes_1L_B_PR[k][j][1])
    for k in range(len(utirel_1L_C)):
        for j in range(len(utirel_1L_C[0])):
            conditions1L.append("Neutral Problem")
            utirel1L.append(utirel_1L_C[k][j])
            utipho1L.append(utipho_1L_C[k][j])
            objs1L.append(k + 1)
            probleminterp1L_a.append(codes_1L_C_PI[k][j][0])
            probleminterp1L_b.append(codes_1L_C_PI[k][j][1])
            confidence1L_a.append(codes_1L_C_CO[k][j][0])
            confidence1L_b.append(codes_1L_C_CO[k][j][1])
            issues1L_a.append(codes_1L_C_IS[k][j][0])
            issues1L_b.append(codes_1L_C_IS[k][j][1])
            motivation1L_a.append(codes_1L_C_MO[k][j][0])
            motivation1L_b.append(codes_1L_C_MO[k][j][1])
            preference1L_a.append(codes_1L_C_PR[k][j][0])
            preference1L_b.append(codes_1L_C_PR[k][j][1])
    for k in range(len(utirel_1L_D)):
        for j in range(len(utirel_1L_D[0])):
            conditions1L.append("NP-S")
            utirel1L.append(utirel_1L_D[k][j])
            utipho1L.append(utipho_1L_D[k][j])
            objs1L.append(k + 1)
            probleminterp1L_a.append(codes_1L_D_PI[k][j][0])
            probleminterp1L_b.append(codes_1L_D_PI[k][j][1])
            confidence1L_a.append(codes_1L_D_CO[k][j][0])
            confidence1L_b.append(codes_1L_D_CO[k][j][1])
            issues1L_a.append(codes_1L_D_IS[k][j][0])
            issues1L_b.append(codes_1L_D_IS[k][j][1])
            motivation1L_a.append(codes_1L_D_MO[k][j][0])
            motivation1L_b.append(codes_1L_D_MO[k][j][1])
            preference1L_a.append(codes_1L_D_PR[k][j][0])
            preference1L_b.append(codes_1L_D_PR[k][j][1])
    
        
    byobj = {'Condition': conditions1L, 'Uti-Rel': utirel1L, 'Uti-Pho': utipho1L, 'Objectives': objs1L, 
             'Problem Interpretation (a)': probleminterp1L_a, 'Problem Interpretation (b)': probleminterp1L_b,
             'Motivation (a)': motivation1L_a, 'Motivation (b)': motivation1L_b,
             'Preference (a)': preference1L_a, 'Preference (b)': preference1L_b,
             'Issues (a)': issues1L_a, 'Issues (b)': issues1L_b,
             'Confidence (a)': confidence1L_a, 'Confidence (b)': confidence1L_b}
    pref1L = pd.DataFrame(data=byobj)
    
    
    for k in range(len(utirel_2L_A)):
        for j in range(len(utirel_2L_A[0])):
            conditions2L.append("Lake Problem")
            utirel2L.append(utirel_2L_A[k][j])
            utipho2L.append(utipho_2L_A[k][j])
            objs2L.append(k + 1)
            probleminterp2L_a.append(codes_2L_A_PI[k][j][0])
            probleminterp2L_b.append(codes_2L_A_PI[k][j][1])
            confidence2L_a.append(codes_2L_A_CO[k][j][0])
            confidence2L_b.append(codes_2L_A_CO[k][j][1])
            issues2L_a.append(codes_2L_A_IS[k][j][0])
            issues2L_b.append(codes_2L_A_IS[k][j][1])
            motivation2L_a.append(codes_2L_A_MO[k][j][0])
            motivation2L_b.append(codes_2L_A_MO[k][j][1])
            preference2L_a.append(codes_2L_A_PR[k][j][0])
            preference2L_b.append(codes_2L_A_PR[k][j][1])
    for k in range(len(utirel_2L_B)):
        for j in range(len(utirel_2L_B[0])):
            conditions2L.append("LP-S")
            utirel2L.append(utirel_2L_B[k][j])
            utipho2L.append(utipho_2L_B[k][j])
            objs2L.append(k + 1)
            probleminterp2L_a.append(codes_2L_B_PI[k][j][0])
            probleminterp2L_b.append(codes_2L_B_PI[k][j][1])
            confidence2L_a.append(codes_2L_B_CO[k][j][0])
            confidence2L_b.append(codes_2L_B_CO[k][j][1])
            issues2L_a.append(codes_2L_B_IS[k][j][0])
            issues2L_b.append(codes_2L_B_IS[k][j][1])
            motivation2L_a.append(codes_2L_B_MO[k][j][0])
            motivation2L_b.append(codes_2L_B_MO[k][j][1])
            preference2L_a.append(codes_2L_B_PR[k][j][0])
            preference2L_b.append(codes_2L_B_PR[k][j][1])
    for k in range(len(utirel_2L_C)):
        for j in range(len(utirel_2L_C[0])):
            conditions2L.append("Neutral Problem")
            utirel2L.append(utirel_2L_C[k][j])
            utipho2L.append(utipho_2L_C[k][j])
            objs2L.append(k + 1)
            probleminterp2L_a.append(codes_2L_C_PI[k][j][0])
            probleminterp2L_b.append(codes_2L_C_PI[k][j][1])
            confidence2L_a.append(codes_2L_C_CO[k][j][0])
            confidence2L_b.append(codes_2L_C_CO[k][j][1])
            issues2L_a.append(codes_2L_C_IS[k][j][0])
            issues2L_b.append(codes_2L_C_IS[k][j][1])
            motivation2L_a.append(codes_2L_C_MO[k][j][0])
            motivation2L_b.append(codes_2L_C_MO[k][j][1])
            preference2L_a.append(codes_2L_C_PR[k][j][0])
            preference2L_b.append(codes_2L_C_PR[k][j][1])
    for k in range(len(utirel_2L_D)):
        for j in range(len(utirel_2L_D[0])):
            conditions2L.append("NP-S")
            utirel2L.append(utirel_2L_D[k][j])
            utipho2L.append(utipho_2L_D[k][j])
            objs2L.append(k + 1)
            probleminterp2L_a.append(codes_2L_D_PI[k][j][0])
            probleminterp2L_b.append(codes_2L_D_PI[k][j][1])
            confidence2L_a.append(codes_2L_D_CO[k][j][0])
            confidence2L_b.append(codes_2L_D_CO[k][j][1])
            issues2L_a.append(codes_2L_D_IS[k][j][0])
            issues2L_b.append(codes_2L_D_IS[k][j][1])
            motivation2L_a.append(codes_2L_D_MO[k][j][0])
            motivation2L_b.append(codes_2L_D_MO[k][j][1])
            preference2L_a.append(codes_2L_D_PR[k][j][0])
            preference2L_b.append(codes_2L_D_PR[k][j][1])
        
    byobj = {'Condition': conditions2L, 'Uti-Rel': utirel2L, 'Uti-Pho': utipho2L, 'Objectives': objs2L, 
             'Problem Interpretation (a)': probleminterp2L_a, 'Problem Interpretation (b)': probleminterp2L_b,
             'Motivation (a)': motivation2L_a, 'Motivation (b)': motivation2L_b,
             'Preference (a)': preference2L_a, 'Preference (b)': preference2L_b,
             'Issues (a)': issues2L_a, 'Issues (b)': issues2L_b,
             'Confidence (a)': confidence2L_a, 'Confidence (b)': confidence2L_b}
    pref2L = pd.DataFrame(data=byobj)
    
    
    
    for k in range(len(utirel_3L_A)):
        for j in range(len(utirel_3L_A[0])):
            conditions3L.append("Lake Problem")
            utirel3L.append(utirel_3L_A[k][j])
            utipho3L.append(utipho_3L_A[k][j])
            objs3L.append(k + 1)
            probleminterp3L_a.append(codes_3L_A_PI[k][j][0])
            probleminterp3L_b.append(codes_3L_A_PI[k][j][1])
            confidence3L_a.append(codes_3L_A_CO[k][j][0])
            confidence3L_b.append(codes_3L_A_CO[k][j][1])
            issues3L_a.append(codes_3L_A_IS[k][j][0])
            issues3L_b.append(codes_3L_A_IS[k][j][1])
            motivation3L_a.append(codes_3L_A_MO[k][j][0])
            motivation3L_b.append(codes_3L_A_MO[k][j][1])
            preference3L_a.append(codes_3L_A_PR[k][j][0])
            preference3L_b.append(codes_3L_A_PR[k][j][1])
    for k in range(len(utirel_3L_B)):
        for j in range(len(utirel_3L_B[0])):
            conditions3L.append("LP-S")
            utirel3L.append(utirel_3L_B[k][j])
            utipho3L.append(utipho_3L_B[k][j])
            objs3L.append(k + 1)
            probleminterp3L_a.append(codes_3L_B_PI[k][j][0])
            probleminterp3L_b.append(codes_3L_B_PI[k][j][1])
            confidence3L_a.append(codes_3L_B_CO[k][j][0])
            confidence3L_b.append(codes_3L_B_CO[k][j][1])
            issues3L_a.append(codes_3L_B_IS[k][j][0])
            issues3L_b.append(codes_3L_B_IS[k][j][1])
            motivation3L_a.append(codes_3L_B_MO[k][j][0])
            motivation3L_b.append(codes_3L_B_MO[k][j][1])
            preference3L_a.append(codes_3L_B_PR[k][j][0])
            preference3L_b.append(codes_3L_B_PR[k][j][1])
    for k in range(len(utirel_3L_C)):
        for j in range(len(utirel_3L_C[0])):
            conditions3L.append("Neutral Problem")
            utirel3L.append(utirel_3L_C[k][j])
            utipho3L.append(utipho_3L_C[k][j])
            objs3L.append(k + 1)
            probleminterp3L_a.append(codes_3L_C_PI[k][j][0])
            probleminterp3L_b.append(codes_3L_C_PI[k][j][1])
            confidence3L_a.append(codes_3L_C_CO[k][j][0])
            confidence3L_b.append(codes_3L_C_CO[k][j][1])
            issues3L_a.append(codes_3L_C_IS[k][j][0])
            issues3L_b.append(codes_3L_C_IS[k][j][1])
            motivation3L_a.append(codes_3L_C_MO[k][j][0])
            motivation3L_b.append(codes_3L_C_MO[k][j][1])
            preference3L_a.append(codes_3L_C_PR[k][j][0])
            preference3L_b.append(codes_3L_C_PR[k][j][1])
    for k in range(len(utirel_3L_D)):
        for j in range(len(utirel_3L_D[0])):
            conditions3L.append("NP-S")
            utirel3L.append(utirel_3L_D[k][j])
            utipho3L.append(utipho_3L_D[k][j])
            objs3L.append(k + 1)
            probleminterp3L_a.append(codes_3L_D_PI[k][j][0])
            probleminterp3L_b.append(codes_3L_D_PI[k][j][1])
            confidence3L_a.append(codes_3L_D_CO[k][j][0])
            confidence3L_b.append(codes_3L_D_CO[k][j][1])
            issues3L_a.append(codes_3L_D_IS[k][j][0])
            issues3L_b.append(codes_3L_D_IS[k][j][1])
            motivation3L_a.append(codes_3L_D_MO[k][j][0])
            motivation3L_b.append(codes_3L_D_MO[k][j][1])
            preference3L_a.append(codes_3L_D_PR[k][j][0])
            preference3L_b.append(codes_3L_D_PR[k][j][1])
        
    byobj = {'Condition': conditions3L, 'Uti-Rel': utirel3L, 'Uti-Pho': utipho3L, 'Objectives': objs3L, 
             'Problem Interpretation (a)': probleminterp3L_a, 'Problem Interpretation (b)': probleminterp3L_b,
             'Motivation (a)': motivation3L_a, 'Motivation (b)': motivation3L_b,
             'Preference (a)': preference3L_a, 'Preference (b)': preference3L_b,
             'Issues (a)': issues3L_a, 'Issues (b)': issues3L_b,
             'Confidence (a)': confidence3L_a, 'Confidence (b)': confidence3L_b}
    pref3L = pd.DataFrame(data=byobj)
    
    return(pref1D, pref2D, pref3D, pref1L, pref2L, pref3L)
    
  
def performance_context_1obj(df1D):
    
    df1D = df1D.drop(df1D[df1D['Condition'] == 'NP-S'].index)
    df1D = df1D.drop(df1D[df1D['Condition'] == 'LP-S'].index)
    
    results = np.empty((3,2))
    
    df1D1L_LP = df1D[np.logical_and(df1D['Levers'] ==1, df1D['Condition'] == 'Lake Problem')]
    df1D1L_NP = df1D[np.logical_and(df1D['Levers'] ==1, df1D['Condition'] == 'Neutral Problem')]
    results[0,:] = ks_2samp(df1D1L_LP['Score'], df1D1L_NP['Score'])

    df1D2L_LP = df1D[np.logical_and(df1D['Levers'] ==2, df1D['Condition'] == 'Lake Problem')]
    df1D2L_NP = df1D[np.logical_and(df1D['Levers'] ==2, df1D['Condition'] == 'Neutral Problem')]
    results[1,:] = ks_2samp(df1D2L_LP['Score'], df1D2L_NP['Score'])
    
    df1D3L_LP = df1D[np.logical_and(df1D['Levers'] ==3, df1D['Condition'] == 'Lake Problem')]
    df1D3L_NP = df1D[np.logical_and(df1D['Levers'] ==3, df1D['Condition'] == 'Neutral Problem')]
    results[2,:] = ks_2samp(df1D3L_LP['Score'], df1D3L_NP['Score'])

    return(results)
#    
#    
def performance_interpretation_1obj(df1D):
    
    df1D = df1D.drop(df1D[df1D['Condition'] == 'NP-S'].index)
    df1D = df1D.drop(df1D[df1D['Condition'] == 'LP-S'].index)
    
    OO = list()
    for k in df1D.index:
        if df1D['Problem Interpretation (a)'][k] == 'O' or df1D['Problem Interpretation (b)'][k] == 'O':
            OO.append('Outside Objectives')
        else:
            OO.append('Other')
    df1D = df1D.assign(Problem_Interpretation = OO)
    
    results = np.empty((3,2))
    
    df1D1L_LP = df1D[np.logical_and(df1D['Levers'] ==1, df1D['Problem_Interpretation'] == 'Outside Objectives')]
    df1D1L_NP = df1D[np.logical_and(df1D['Levers'] ==1, df1D['Problem_Interpretation'] == 'Other')]
    results[0,:] = ks_2samp(df1D1L_LP['Score'], df1D1L_NP['Score'])

    df1D2L_LP = df1D[np.logical_and(df1D['Levers'] ==2, df1D['Problem_Interpretation'] == 'Outside Objectives')]
    df1D2L_NP = df1D[np.logical_and(df1D['Levers'] ==2, df1D['Problem_Interpretation'] == 'Other')]
    results[1,:] = ks_2samp(df1D2L_LP['Score'], df1D2L_NP['Score'])
    
    df1D3L_LP = df1D[np.logical_and(df1D['Levers'] ==3, df1D['Problem_Interpretation'] == 'Outside Objectives')]
    df1D3L_NP = df1D[np.logical_and(df1D['Levers'] ==3, df1D['Problem_Interpretation'] == 'Other')]
    results[2,:] = ks_2samp(df1D3L_LP['Score'], df1D3L_NP['Score'])

    return(results)
    
#    
def outerobjectives_context_1obj_notstacked(df1D):
    
    # Remove static conditions
    df1D = df1D.drop(df1D[df1D['Condition'] == 'NP-S'].index)
    df1D = df1D.drop(df1D[df1D['Condition'] == 'LP-S'].index)
    
    width = 0.25
    ind = np.arange(3)
    
    # Create a Lake Problem only dataframe
    LP_interpretations = df1D.drop(df1D[df1D['Condition'] == 'Neutral Problem'].index)
    # Isolate by lever
    LP_interpretations_1L = LP_interpretations[LP_interpretations['Levers'] == 1]
    LP_interpretations_2L = LP_interpretations[LP_interpretations['Levers'] == 2]
    LP_interpretations_3L = LP_interpretations[LP_interpretations['Levers'] == 3]
        
    # Create a neutral problem only dataframe
    NP_interpretations = df1D.drop(df1D[df1D['Condition'] == 'Lake Problem'].index)

    # Isolate by lever
    NP_interpretations_1L = NP_interpretations[NP_interpretations['Levers'] == 1]
    NP_interpretations_2L = NP_interpretations[NP_interpretations['Levers'] == 2]
    NP_interpretations_3L = NP_interpretations[NP_interpretations['Levers'] == 3]
#    
    # Compile participants/decisions in each group that are flagged with "Other Objectives" and calculate fraction
    
    O_LP_1L = list()
    O_LP_2L = list()
    O_LP_3L = list()
    
    O_NP_1L = list()
    O_NP_2L = list()
    O_NP_3L = list()
    
    for k in LP_interpretations_1L.index:
        if LP_interpretations_1L['Problem Interpretation (a)'][k] == 'O' or LP_interpretations_1L['Problem Interpretation (b)'][k] == 'O':
            O_LP_1L.append(1)
        else:
            O_LP_1L.append(0)
            
    for k in LP_interpretations_2L.index:
        if LP_interpretations_2L['Problem Interpretation (a)'][k] == 'O' or LP_interpretations_2L['Problem Interpretation (b)'][k] == 'O':
            O_LP_2L.append(1)
        else:
            O_LP_2L.append(0)
            
    for k in LP_interpretations_3L.index:
        if LP_interpretations_3L['Problem Interpretation (a)'][k] == 'O' or LP_interpretations_3L['Problem Interpretation (b)'][k] == 'O':
            O_LP_3L.append(1)
        else:
            O_LP_3L.append(0)
            
    for k in NP_interpretations_1L.index:
        if NP_interpretations_1L['Problem Interpretation (a)'][k] == 'O' or NP_interpretations_1L['Problem Interpretation (b)'][k] == 'O':
            O_NP_1L.append(1)
        else:
            O_NP_1L.append(0)
            
    for k in NP_interpretations_2L.index:
        if NP_interpretations_2L['Problem Interpretation (a)'][k] == 'O' or NP_interpretations_2L['Problem Interpretation (b)'][k] == 'O':
            O_NP_2L.append(1)
        else:
            O_NP_2L.append(0)
            
    for k in NP_interpretations_3L.index:
        if NP_interpretations_3L['Problem Interpretation (a)'][k] == 'O' or NP_interpretations_3L['Problem Interpretation (b)'][k] == 'O':
            O_NP_3L.append(1)
        else:
            O_NP_3L.append(0)

    OOs_LP = list()
    OOs_LP.append(sum(O_LP_1L)/len(O_LP_1L))
    OOs_LP.append(sum(O_LP_2L)/len(O_LP_2L))
    OOs_LP.append(sum(O_LP_3L)/len(O_LP_3L))
    
    OOs_NP = list()
    OOs_NP.append(sum(O_NP_1L)/len(O_NP_1L))
    OOs_NP.append(sum(O_NP_2L)/len(O_NP_2L))
    OOs_NP.append(sum(O_NP_3L)/len(O_NP_3L))
    
    ind1 = (0.75,1.75,2.75)
    ind2 = (1, 2, 3)

    # Generate figure
    fig = plt.figure(figsize=(5,7), dpi=150)
    p1 = plt.bar(ind1, OOs_LP, width, color = "#1f78b4")
    p2 = plt.bar(ind2, OOs_NP, width, color = "#33a02c")
    
    plt.ylabel('Fraction that described non-assigned objectives')
    plt.xlabel('Number of levers')
    plt.xticks((1,2,3))
    plt.ylim((0,1))
    plt.title('Rates of Alternative Problem Interpretation Among Context Groups')
    plt.legend((p1[0], p2[0]), ('Lake Problem', 'Neutral Problem'))
    
    plt.savefig('fig8.pdf', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    
    plt.savefig('fig8.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    
    
    return(fig, OOs_LP, OOs_NP)
    
    
#def outerobjectives_context_1obj_interp_notstacked(df1D):
#    
#    df1D = df1D.drop(df1D[df1D['Condition'] == 'NP-S'].index)
#    df1D = df1D.drop(df1D[df1D['Condition'] == 'LP-S'].index)
#    
#        # begin fig 8
#    
#
#    width = 0.25
#    ind = np.arange(3)
#    
#    # Create a Lake Problem only dataframe
#    LP_interpretations = df1D.drop(df1D[df1D['Condition'] == 'Neutral Problem'].index)
#    # Isolate by lever
#    LP_interpretations_1L = LP_interpretations[LP_interpretations['Levers'] == 1]
#    LP_interpretations_2L = LP_interpretations[LP_interpretations['Levers'] == 2]
#    LP_interpretations_3L = LP_interpretations[LP_interpretations['Levers'] == 3]
#        
#    # Create a neutral problem only dataframe
#    NP_interpretations = df1D.drop(df1D[df1D['Condition'] == 'Lake Problem'].index)
#
#    # Isolate by lever
#    NP_interpretations_1L = NP_interpretations[NP_interpretations['Levers'] == 1]
#    NP_interpretations_2L = NP_interpretations[NP_interpretations['Levers'] == 2]
#    NP_interpretations_3L = NP_interpretations[NP_interpretations['Levers'] == 3]
##    
#    # Compile participants/decisions in each group that are flagged with "Other Objectives" and calculate fraction
#    
#    O_LP_1L = list()
#    O_LP_2L = list()
#    O_LP_3L = list()
#    
#    O_NP_1L = list()
#    O_NP_2L = list()
#    O_NP_3L = list()
#    
#    for k in LP_interpretations_1L.index:
#        if LP_interpretations_1L['Problem Interpretation (a)'][k] == 'O' or LP_interpretations_1L['Problem Interpretation (b)'][k] == 'O':
#            O_LP_1L.append(1)
#        else:
#            O_LP_1L.append(0)
#            
#    for k in LP_interpretations_2L.index:
#        if LP_interpretations_2L['Problem Interpretation (a)'][k] == 'O' or LP_interpretations_2L['Problem Interpretation (b)'][k] == 'O':
#            O_LP_2L.append(1)
#        else:
#            O_LP_2L.append(0)
#            
#    for k in LP_interpretations_3L.index:
#        if LP_interpretations_3L['Problem Interpretation (a)'][k] == 'O' or LP_interpretations_3L['Problem Interpretation (b)'][k] == 'O':
#            O_LP_3L.append(1)
#        else:
#            O_LP_3L.append(0)
#            
#    for k in NP_interpretations_1L.index:
#        if NP_interpretations_1L['Problem Interpretation (a)'][k] == 'O' or NP_interpretations_1L['Problem Interpretation (b)'][k] == 'O':
#            O_NP_1L.append(1)
#        else:
#            O_NP_1L.append(0)
#            
#    for k in NP_interpretations_2L.index:
#        if NP_interpretations_2L['Problem Interpretation (a)'][k] == 'O' or NP_interpretations_2L['Problem Interpretation (b)'][k] == 'O':
#            O_NP_2L.append(1)
#        else:
#            O_NP_2L.append(0)
#            
#    for k in NP_interpretations_3L.index:
#        if NP_interpretations_3L['Problem Interpretation (a)'][k] == 'O' or NP_interpretations_3L['Problem Interpretation (b)'][k] == 'O':
#            O_NP_3L.append(1)
#        else:
#            O_NP_3L.append(0)
#
#    OOs_LP = list()
#    OOs_LP.append(sum(O_LP_1L)/len(O_LP_1L))
#    OOs_LP.append(sum(O_LP_2L)/len(O_LP_2L))
#    OOs_LP.append(sum(O_LP_3L)/len(O_LP_3L))
#    
#    OOs_NP = list()
#    OOs_NP.append(sum(O_NP_1L)/len(O_NP_1L))
#    OOs_NP.append(sum(O_NP_2L)/len(O_NP_2L))
#    OOs_NP.append(sum(O_NP_3L)/len(O_NP_3L))
#
##    df1D = df1D.reindex(range(len(df1D)))
##    df1D['Levers'] = df1D['Levers'].astype(int)
#    
#    OO = list()
#    for k in df1D.index:
#        if df1D['Problem Interpretation (a)'][k] == 'O' or df1D['Problem Interpretation (b)'][k] == 'O':
#            OO.append('Outside Objectives')
#        else:
#            OO.append('Other')
#    df1D = df1D.assign(Problem_Interpretation = OO)
#    
#    # Lever plot
#    import seaborn as sns
#    sns.set(style="whitegrid", palette="pastel", color_codes=True)
#    
#    f1, ax = plt.subplots(figsize=(12, 8))
#    
#    g = sns.violinplot(x="Levers", y="Score", hue="Problem_Interpretation", data=df1D,
#                   palette={"Outside Objectives": plt.cm.viridis(1.5/2), "Other": plt.cm.viridis(0.25/2)}, cut=0)
#    sns.despine(left=True)
#    
#    f1.suptitle('Maximize Economic Benefits', fontsize=18, fontweight='bold')
#    ax.set_xlabel("Number of Levers",size = 16,alpha=0.7)
#    ax.set_ylabel("Fraction of Economic Benefits Achieved",size = 16,alpha=0.7)
#    ax.set_ylim((0,1))
#    plt.legend(loc='lower right', fontsize=16)
#    
#    plt.savefig('fig9.pdf', dpi=300, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches=None, pad_inches=0.1,
#        frameon=None, metadata=None)
#    
#    #begin fig 8
#    
#    ind1 = (0.75,1.75,2.75)
#    ind2 = (1, 2, 3)
#
#    # Generate figure
#    fig = plt.figure(figsize=(5,7), dpi=150)
#    p1 = plt.bar(ind1, OOs_LP, width, color = "#1f78b4")
#    p2 = plt.bar(ind2, OOs_NP, width, color = "#33a02c")
#    
#    plt.ylabel('Fraction that described non-assigned objectives')
#    plt.xlabel('Number of levers')
#    plt.xticks((1,2,3))
#    plt.ylim((0,1))
#    plt.title('Rates of Alternative Problem Interpretation Among Context Groups')
#    plt.legend((p1[0], p2[0]), ('Lake Problem', 'Neutral Problem'))
#    
#    plt.savefig('fig8.pdf', dpi=300, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches=None, pad_inches=0.1,
#        frameon=None, metadata=None)
#    
#    plt.savefig('fig8.png', dpi=300, facecolor='w', edgecolor='w',
#        orientation='portrait', papertype=None, format=None,
#        transparent=False, bbox_inches=None, pad_inches=0.1,
#        frameon=None, metadata=None)
#    
#    
def outerobjectives_context_1obj(df1D):
    
    # Remove static conditions
    df1D = df1D.drop(df1D[df1D['Condition'] == 'NP-S'].index)
    df1D = df1D.drop(df1D[df1D['Condition'] == 'LP-S'].index)
    
    width = 0.35
    ind = np.arange(3)
    
    # Create a Lake Problem only dataframe
    LP_interpretations = df1D.drop(df1D[df1D['Condition'] == 'Neutral Problem'].index)
    # Isolate by lever
    LP_interpretations_1L = LP_interpretations[LP_interpretations['Levers'] == 1]
    LP_interpretations_2L = LP_interpretations[LP_interpretations['Levers'] == 2]
    LP_interpretations_3L = LP_interpretations[LP_interpretations['Levers'] == 3]
        
    # Create a neutral problem only dataframe
    NP_interpretations = df1D.drop(df1D[df1D['Condition'] == 'Lake Problem'].index)

    # Isolate by lever
    NP_interpretations_1L = NP_interpretations[NP_interpretations['Levers'] == 1]
    NP_interpretations_2L = NP_interpretations[NP_interpretations['Levers'] == 2]
    NP_interpretations_3L = NP_interpretations[NP_interpretations['Levers'] == 3]
#    
    # Compile participants/decisions in each group that are flagged with "Other Objectives" and calculate fraction
    
    O_LP_1L = list()
    O_LP_2L = list()
    O_LP_3L = list()
    
    O_NP_1L = list()
    O_NP_2L = list()
    O_NP_3L = list()
    
    for k in LP_interpretations_1L.index:
        if LP_interpretations_1L['Problem Interpretation (a)'][k] == 'O' or LP_interpretations_1L['Problem Interpretation (b)'][k] == 'O':
            O_LP_1L.append(1)
        else:
            O_LP_1L.append(0)
            
    for k in LP_interpretations_2L.index:
        if LP_interpretations_2L['Problem Interpretation (a)'][k] == 'O' or LP_interpretations_2L['Problem Interpretation (b)'][k] == 'O':
            O_LP_2L.append(1)
        else:
            O_LP_2L.append(0)
            
    for k in LP_interpretations_3L.index:
        if LP_interpretations_3L['Problem Interpretation (a)'][k] == 'O' or LP_interpretations_3L['Problem Interpretation (b)'][k] == 'O':
            O_LP_3L.append(1)
        else:
            O_LP_3L.append(0)
            
    for k in NP_interpretations_1L.index:
        if NP_interpretations_1L['Problem Interpretation (a)'][k] == 'O' or NP_interpretations_1L['Problem Interpretation (b)'][k] == 'O':
            O_NP_1L.append(1)
        else:
            O_NP_1L.append(0)
            
    for k in NP_interpretations_2L.index:
        if NP_interpretations_2L['Problem Interpretation (a)'][k] == 'O' or NP_interpretations_2L['Problem Interpretation (b)'][k] == 'O':
            O_NP_2L.append(1)
        else:
            O_NP_2L.append(0)
            
    for k in NP_interpretations_3L.index:
        if NP_interpretations_3L['Problem Interpretation (a)'][k] == 'O' or NP_interpretations_3L['Problem Interpretation (b)'][k] == 'O':
            O_NP_3L.append(1)
        else:
            O_NP_3L.append(0)

    OOs_LP = list()
    OOs_LP.append(sum(O_LP_1L)/len(O_LP_1L))
    OOs_LP.append(sum(O_LP_2L)/len(O_LP_2L))
    OOs_LP.append(sum(O_LP_3L)/len(O_LP_3L))
    
    OOs_NP = list()
    OOs_NP.append(sum(O_NP_1L)/len(O_NP_1L))
    OOs_NP.append(sum(O_NP_2L)/len(O_NP_2L))
    OOs_NP.append(sum(O_NP_3L)/len(O_NP_3L))
    
    ind = (1,2,3)

    # Generate figure
    fig = plt.figure(figsize=(5,7), dpi=150)
    p1 = plt.bar(ind, OOs_LP, width, color = "#1f78b4")
    p2 = plt.bar(ind, OOs_NP, width, bottom = OOs_LP, color = "#33a02c")
    
    plt.ylabel('Fraction that described non-assigned objectives')
    plt.xlabel('Number of levers')
    plt.xticks((1,2,3))
    plt.title('Rates of Alternative Problem Interpretation Among Context Groups')
    plt.legend((p1[0], p2[0]), ('Lake Problem', 'Neutral Problem'))
    
    plt.savefig('fig6.pdf', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    
    return(fig)
#    
def tradeoffs_1obj_2obj_OO(OOs, refecon, refpho):
    ''' Group 1: Participants flagged "other objectives"'''
    
    participants_1L = len(OOs['1obj']['1L'])
    participants_2L = len(OOs['1obj']['2L'])
    participants_3L = len(OOs['1obj']['3L'])

    
    uti1obj = list()
    uti2obj = list()
    
    pho1obj = list()
    pho2obj = list()
    
    for k in range(participants_1L):
        pollution_lim = OOs['1obj']['1L'][k]
        uti1obj.append(lake_problem_JDM_uti_1L(pollution_lim))
        pho1obj.append(-1*lake_problem_JDM_pho_1L(pollution_lim))
        
    for k in range(participants_2L):
        pollution_lim = OOs['1obj']['2L'][k][0]
        uti1obj.append(lake_problem_JDM_uti_2L(pollution_lim))
        pho1obj.append(-1*lake_problem_JDM_pho_2L(pollution_lim))
        
    for k in range(participants_3L):
        pollution_lim = OOs['1obj']['3L'][k][0]
        uti1obj.append(lake_problem_JDM_uti_3L(pollution_lim))
        pho1obj.append(-1*lake_problem_JDM_pho_3L(pollution_lim))
        
    # Calculate performance of 2-objective strategies
    for k in range(participants_1L):
        pollution_lim = OOs['2obj']['1L'][k]
        uti2obj.append(lake_problem_JDM_uti_1L(pollution_lim))
        pho2obj.append(-1*lake_problem_JDM_pho_1L(pollution_lim))
        
    for k in range(participants_2L):
        pollution_lim = OOs['2obj']['2L'][k][0]
        uti2obj.append(lake_problem_JDM_uti_2L(pollution_lim))
        pho2obj.append(-1*lake_problem_JDM_pho_2L(pollution_lim))
        
    for k in range(participants_3L):
        pollution_lim = OOs['2obj']['3L'][k][0]
#        OOs['2obj']['3L'][k][0]
        uti2obj.append(lake_problem_JDM_uti_3L(pollution_lim))
        pho2obj.append(-1*lake_problem_JDM_pho_3L(pollution_lim))

    utimin = 0
    utimax = 1.1*lake_problem_JDM_uti_1L((0.1))
    phomax = 0
    phomin = -1*(1.1*lake_problem_JDM_pho_1L((0.1)))


    utilims = (utimin, utimax)
    pholims = (phomin, phomax)
    # Show 2D tradeoffs
    fig = plt.figure(dpi=150)

    plt.annotate('',
                 xy=(utimax,phomin),
                 xycoords='data',
                 xytext=(utimin,phomin),
                 arrowprops=dict(facecolor='black', width=3, headwidth=7,headlength=7, connectionstyle='arc3'))
#
    # X axis arrow
    plt.annotate('',
                 xy=(utimin, phomax),
                 xycoords='data',
                 xytext=(utimin,phomin),
                 arrowprops=dict(facecolor='black', width=3, headwidth=7,headlength=7, connectionstyle='arc3'))

    plt.xlabel('Economic Benefits', fontsize=18)
    plt.ylabel('Water Quality',fontsize=18)

    plt.xlim(utilims)
    plt.ylim(pholims)

    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.yticks([])
    plt.xticks([])

    #plt.scatter(2.5,0.05, marker=heart, c='k', s=200, linewidths=4,linestyle='None')
    point_value = 0.75
    plt.plot(refecon, np.multiply(refpho, -1), c='k', lw=2, linestyle = '-')
    plt.scatter(uti1obj, pho1obj, c = plt.cm.plasma(1/4), s=40, lw = 0.2, alpha = point_value)
    plt.scatter(uti2obj, pho2obj, c = plt.cm.plasma(2/4), s=40, lw = 0.2, alpha = point_value)
    
    plt.legend(['Non-dominated set', 'One-objective strategies', 'Two-objective strategies'])
    
    plt.savefig('fig10.pdf', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    
    plt.savefig('fig10.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    
    return(fig)
    
def tradeoffs_example(refecon, refpho):
    ''' Group 1: Participants flagged "other objectives"'''
    
    np.random.seed(3)
    inds = np.random.randint(0, high = len(refecon), size=5)
    
    pts1 = refecon[inds]
    pts2 = -1*refpho[inds]

    pts1 = (1,1.4,0.3) 
    pts2 = (-0.5, -1.65, -0.2)

    pts1a = (0.5,1.2,0.2)
    pts2a = (-1.85, -1.7, -0.5)
    
    utimin = 0
    utimax = 1.1*lake_problem_JDM_uti_1L((0.1))
    phomax = 0
    phomin = -1*(1.1*lake_problem_JDM_pho_1L((0.1)))


    utilims = (utimin, utimax)
    pholims = (phomin, phomax)
    # Show 2D tradeoffs
    fig = plt.figure(dpi=150)

    plt.annotate('',
                 xy=(utimax,phomin),
                 xycoords='data',
                 xytext=(utimin,phomin),
                 arrowprops=dict(facecolor='black', width=3, headwidth=7,headlength=7, connectionstyle='arc3'))
#
    # X axis arrow
    plt.annotate('',
                 xy=(utimin, phomax),
                 xycoords='data',
                 xytext=(utimin,phomin),
                 arrowprops=dict(facecolor='black', width=3, headwidth=7,headlength=7, connectionstyle='arc3'))

    plt.xlabel('A', fontsize=18)
    plt.ylabel('B',fontsize=18)

    plt.xlim(utilims)
    plt.ylim(pholims)

    for spine in plt.gca().spines.values():
        spine.set_visible(False)

    plt.yticks([])
    plt.xticks([])

    #plt.scatter(2.5,0.05, marker=heart, c='k', s=200, linewidths=4,linestyle='None')
    plt.scatter(pts1, pts2, c = 'k', s=200, lw = 0.2)
    plt.scatter(pts1a, pts2a, c = 'k', s=200, lw = 0.2, alpha = 0.25)
    
    plt.legend(['Non-Dominated Alternatives', 'Dominated Alternatives'])
    
    plt.savefig('fig1.pdf', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    
    plt.savefig('fig1.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    
    return(fig)
    
def thresholds_analyze(Ts):
    ''' Group 1: Participants flagged "subcode"'''

    
    uti1obj = list()
    uti2obj = list()
    uti3obj = list()
    
    pho1obj = list()
    pho2obj = list()
    pho3obj = list()
    
    phocrit = 0.422
    uticrit = 0.475
    count_underT = 0
    count_overT = 0
    count_near = 0
    critfrac = 0.1
    
    for k in range(len(Ts['obj1']['1L'])):
        pollution_lim = Ts['obj1']['1L'][k]
        uti1obj.append(lake_problem_JDM_uti_1L(pollution_lim))
        pho1obj.append(lake_problem_JDM_pho_1L(pollution_lim))
        if pho1obj[k] <= phocrit:
            count_underT = count_underT + 1
        else:
            count_overT = count_overT + 1
        if np.abs(pho1obj[k] - phocrit) < (phocrit) and np.abs(uti1obj[k] - uticrit) < (critfrac*uticrit):
            count_near = count_near + 1
            
        
    for k in range(len(Ts['obj1']['2L'])):
        pollution_lim = Ts['obj1']['2L'][k][0]
        uti1obj.append(lake_problem_JDM_uti_2L(pollution_lim))
        pho1obj.append(lake_problem_JDM_pho_2L(pollution_lim))
        if pho1obj[k] <= phocrit:
            count_underT = count_underT + 1
        else:
            count_overT = count_overT + 1
        if np.abs(pho1obj[k] - phocrit) < (phocrit) and np.abs(uti1obj[k] - uticrit) < (critfrac*uticrit):
            count_near = count_near + 1
        
    for k in range(len(Ts['obj1']['3L'])):
        pollution_lim = Ts['obj1']['3L'][k][0]
        uti1obj.append(lake_problem_JDM_uti_3L(pollution_lim))
        pho1obj.append(lake_problem_JDM_pho_3L(pollution_lim))
        if pho1obj[k] <= phocrit:
            count_underT = count_underT + 1
        else:
            count_overT = count_overT + 1
        if np.abs(pho1obj[k] - phocrit) < (phocrit) and np.abs(uti1obj[k] - uticrit) < (critfrac*uticrit):
            count_near = count_near + 1
        
     # Calculate performance of 2-objective strategies
    for k in range(len(Ts['obj2']['1L'])):
        pollution_lim = Ts['obj2']['1L'][k]
        uti2obj.append(lake_problem_JDM_uti_1L(pollution_lim))
        pho2obj.append(lake_problem_JDM_pho_1L(pollution_lim))
        if pho2obj[k] <= phocrit:
            count_underT = count_underT + 1
        else:
            count_overT = count_overT + 1
        if np.abs(pho2obj[k] - phocrit) < (phocrit) and np.abs(uti2obj[k] - uticrit) < (critfrac*uticrit):
            count_near = count_near + 1
        
    for k in range(len(Ts['obj2']['2L'])):
        
        if np.all(~np.isnan(Ts['obj2']['2L'][k])):
            pollution_lim = Ts['obj2']['2L'][k][0]
            uti2obj.append(lake_problem_JDM_uti_2L(pollution_lim))
            pho2obj.append(lake_problem_JDM_pho_2L(pollution_lim))
            if pho2obj[k] <= phocrit:
                count_underT = count_underT + 1
            else:
                count_overT = count_overT + 1
            if np.abs(pho2obj[k] - phocrit) < (phocrit) and np.abs(uti2obj[k] - uticrit) < (critfrac*uticrit):
                count_near = count_near + 1
        else:
            pass
        
    for k in range(len(Ts['obj2']['3L'])):
        pollution_lim = Ts['obj2']['3L'][k][0]
        uti2obj.append(lake_problem_JDM_uti_3L(pollution_lim))
        pho2obj.append(lake_problem_JDM_pho_3L(pollution_lim))
        if pho2obj[k] <= phocrit:
            count_underT = count_underT + 1
        else:
            count_overT = count_overT + 1
        if np.abs(pho2obj[k] - phocrit) < (phocrit) and np.abs(uti2obj[k] - uticrit) < (critfrac*uticrit):
            count_near = count_near + 1
        
     # Calculate performance of 3-objective strategies
    for k in range(len(Ts['obj3']['1L'])):
        pollution_lim = Ts['obj3']['1L'][k]
        uti3obj.append(lake_problem_JDM_uti_1L(pollution_lim))
        pho3obj.append(lake_problem_JDM_pho_1L(pollution_lim))
        if pho3obj[k] <= phocrit:
            count_underT = count_underT + 1
        else:
            count_overT = count_overT + 1
        if np.abs(pho3obj[k] - phocrit) < (phocrit) and np.abs(uti3obj[k] - uticrit) < (critfrac*uticrit):
            count_near = count_near + 1
        
    for k in range(len(Ts['obj3']['2L'])):
        pollution_lim = Ts['obj3']['2L'][k][0]
        uti3obj.append(lake_problem_JDM_uti_2L(pollution_lim))
        pho3obj.append(lake_problem_JDM_pho_2L(pollution_lim))
        if pho3obj[k] <= phocrit:
            count_underT = count_underT + 1
        else:
            count_overT = count_overT + 1
        if np.abs(pho3obj[k] - phocrit) < (phocrit) and np.abs(uti3obj[k] - uticrit) < (critfrac*uticrit):
            count_near = count_near + 1
        
    for k in range(len(Ts['obj3']['3L'])):
        pollution_lim = Ts['obj3']['3L'][k][0]
        uti3obj.append(lake_problem_JDM_uti_3L(pollution_lim))
        pho3obj.append(lake_problem_JDM_pho_3L(pollution_lim))
        if pho3obj[k] <= phocrit:
            count_underT = count_underT + 1
        else:
            count_overT = count_overT + 1
        if np.abs(pho3obj[k] - phocrit) < (phocrit) and np.abs(uti3obj[k] - uticrit) < (critfrac*uticrit):
            count_near = count_near + 1
            
    percent_under = count_underT/(count_underT + count_overT)
    percent_near = count_near/(count_underT + count_overT)

    return(percent_under, percent_near)
   
def visualize_preference_interactive_utipho(pref1L, pref2L, pref3L):

    pref1L = pref1L.drop(pref1L[pref1L['Condition'] == 'NP-S'].index)
    pref1L = pref1L.drop(pref1L[pref1L['Condition'] == 'LP-S'].index)
    
    pref2L = pref2L.drop(pref2L[pref2L['Condition'] == 'NP-S'].index)
    pref2L = pref2L.drop(pref2L[pref2L['Condition'] == 'LP-S'].index)
#    df2L = df2L.reindex(range(len(df2L)))
    
    pref3L = pref3L.drop(pref3L[pref3L['Condition'] == 'NP-S'].index)
    pref3L = pref3L.drop(pref3L[pref3L['Condition'] == 'LP-S'].index)

    # Lever plot
    import seaborn as sns
    sns.set(style="whitegrid", palette="pastel", color_codes=True)
    
    fig = plt.figure(figsize=(8,18), dpi=150)
    
    ax = fig.add_subplot(311)
    
    g = sns.violinplot(y="Objectives", x="Uti-Pho", hue="Condition", data=pref1L,
                   palette={"Lake Problem": "#1f78b4", "Neutral Problem": "#33a02c"}, cut=0, orient="h", legend_out = True)
    sns.despine(left=True)
    g.set(xticklabels=[])
    
    ax.set_title('One-Lever Decisions', fontsize=18, fontweight='bold')
    ax.set_ylabel("Number of Objectives",size = 16,alpha=0.7)
    ax.set_xlabel('')
    #ax.set_xlabel("Prefers Economic Benefits               Prefers Water Quality",size = 16,alpha=0.7)
    ax.set_xlim((0,1))
    #plt.legend(loc='upper right', fontsize=16, labels=["Lake Problem", "Neutral Problem"])
    new_labels = ['Lake Problem', 'Neutral Problem']
    #for t, l in zip(g._legend.texts, new_labels): t.set_text(l)
    
    ax = fig.add_subplot(312)
    
    g = sns.violinplot(y="Objectives", x="Uti-Pho", hue="Condition", data=pref2L,
                   palette={"Lake Problem": "#1f78b4", "Neutral Problem": "#33a02c"}, cut=0, orient="h", legend_out=True)
    sns.despine(left=True)
    g.set(xticklabels=[])
    
    ax.set_title('Two-Lever Decisions', fontsize=18, fontweight='bold')
    ax.set_ylabel("Number of Objectives",size = 16,alpha=0.7)
    ax.set_xlabel('')
    #ax.set_xlabel("Prefers Economic Benefits               Prefers Water Quality",size = 16,alpha=0.7)
    ax.set_xlim((0,1))
    #plt.legend(loc='upper right', fontsize=16)
    new_labels = ['Lake Problem', 'Neutral Problem']
    #for t, l in zip(g._legend.texts, new_labels): t.set_text(l)
    
    ax = fig.add_subplot(313)
    
    
    g = sns.violinplot(y="Objectives", x="Uti-Pho", hue="Condition", data=pref3L,
                   palette={"Lake Problem": "#1f78b4", "Neutral Problem": "#33a02c"}, cut=0, orient="h", legend_out=True)
    sns.despine(left=True)
    g.set(xticklabels=[])
    
    ax.set_title('Three-Lever Decisions', fontsize=18, fontweight='bold')
    ax.set_ylabel("Number of Objectives",size = 16,alpha=0.7)
    ax.set_xlabel("Prefers Economic Benefits                              Prefers Water Quality",size = 16,alpha=0.7)
    ax.set_xlim((0,1))
    #plt.legend(loc='upper right', fontsize=16)
    new_labels = ['Lake Problem', 'Neutral Problem']
    #for t, l in zip(g._legend.texts, new_labels): t.set_text(l)
    
    plt.savefig('fig6.pdf', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    
    plt.savefig('fig6.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)

    return(fig)

def scores_naivenorm(group1, group2, group3, group4):
    ''' This function converts the "normalized score" of each strategy (which 
    is normalized by a problem-specific "worst case" distance from the Pareto
    front) to a large group of randomized strategies, in which each lever 
    is an independently sampled random uniform value '''
    
    scoresA = scores_boxplot(score_track(group1))
    scoresB = scores_boxplot(score_track(group2))
    scoresC = scores_boxplot(score_track(group3))
    scoresD = scores_boxplot(score_track(group4))
    
    codesA_PI = code_boxplot(code_track(group1, 'ProblemInterpretation'))
    codesB_PI = code_boxplot(code_track(group2, 'ProblemInterpretation'))
    codesC_PI = code_boxplot(code_track(group3, 'ProblemInterpretation'))
    codesD_PI = code_boxplot(code_track(group4, 'ProblemInterpretation'))
    
    codesA_IS = code_boxplot(code_track(group1, 'Issues'))
    codesB_IS = code_boxplot(code_track(group2, 'Issues'))
    codesC_IS = code_boxplot(code_track(group3, 'Issues'))
    codesD_IS = code_boxplot(code_track(group4, 'Issues'))
    
    codesA_CO = code_boxplot(code_track(group1, 'Confidence'))
    codesB_CO = code_boxplot(code_track(group2, 'Confidence'))
    codesC_CO = code_boxplot(code_track(group3, 'Confidence'))
    codesD_CO = code_boxplot(code_track(group4, 'Confidence'))
    
    codesA_MO = code_boxplot(code_track(group1, 'Motivation'))
    codesB_MO = code_boxplot(code_track(group2, 'Motivation'))
    codesC_MO = code_boxplot(code_track(group3, 'Motivation'))
    codesD_MO = code_boxplot(code_track(group4, 'Motivation'))
    
    codesA_PR = code_boxplot(code_track(group1, 'Preference'))
    codesB_PR = code_boxplot(code_track(group2, 'Preference'))
    codesC_PR = code_boxplot(code_track(group3, 'Preference'))
    codesD_PR = code_boxplot(code_track(group4, 'Preference'))
      
    scoresrand = randomize_score(400)
    
    scores_1D1L_A = naivenorm(scoresA['1D1L'], scoresrand['score_1D']['1L'])
    scores_1D1L_B = naivenorm(scoresB['1D1L'], scoresrand['score_1D']['1L'])
    scores_1D1L_C = naivenorm(scoresC['1D1L'], scoresrand['score_1D']['1L'])
    scores_1D1L_D = naivenorm(scoresD['1D1L'], scoresrand['score_1D']['1L'])
    
    scores_1D2L_A = naivenorm(scoresA['1D2L'], scoresrand['score_1D']['2L'])
    scores_1D2L_B = naivenorm(scoresB['1D2L'], scoresrand['score_1D']['2L'])
    scores_1D2L_C = naivenorm(scoresC['1D2L'], scoresrand['score_1D']['2L'])
    scores_1D2L_D = naivenorm(scoresD['1D2L'], scoresrand['score_1D']['2L'])
    
    scores_1D3L_A = naivenorm(scoresA['1D3L'], scoresrand['score_1D']['3L'])
    scores_1D3L_B = naivenorm(scoresB['1D3L'], scoresrand['score_1D']['3L'])
    scores_1D3L_C = naivenorm(scoresC['1D3L'], scoresrand['score_1D']['3L'])
    scores_1D3L_D = naivenorm(scoresD['1D3L'], scoresrand['score_1D']['3L'])
       
    scores_2D2L_A = naivenorm(scoresA['2D2L'], scoresrand['score_2D']['2L'])
    scores_2D2L_B = naivenorm(scoresB['2D2L'], scoresrand['score_2D']['2L'])
    scores_2D2L_C = naivenorm(scoresC['2D2L'], scoresrand['score_2D']['2L'])
    scores_2D2L_D = naivenorm(scoresD['2D2L'], scoresrand['score_2D']['2L'])
    
    scores_2D3L_A = naivenorm(scoresA['2D3L'], scoresrand['score_2D']['3L'])
    scores_2D3L_B = naivenorm(scoresB['2D3L'], scoresrand['score_2D']['3L'])
    scores_2D3L_C = naivenorm(scoresC['2D3L'], scoresrand['score_2D']['3L'])
    scores_2D3L_D = naivenorm(scoresD['2D3L'], scoresrand['score_2D']['3L'])

    scores_3D2L_A = naivenorm(scoresA['3D2L'], scoresrand['score_3D']['2L'])
    scores_3D2L_B = naivenorm(scoresB['3D2L'], scoresrand['score_3D']['2L'])
    scores_3D2L_C = naivenorm(scoresC['3D2L'], scoresrand['score_3D']['2L'])
    scores_3D2L_D = naivenorm(scoresD['3D2L'], scoresrand['score_3D']['2L'])
    
    scores_3D3L_A = naivenorm(scoresA['3D3L'], scoresrand['score_3D']['3L'])
    scores_3D3L_B = naivenorm(scoresB['3D3L'], scoresrand['score_3D']['3L'])
    scores_3D3L_C = naivenorm(scoresC['3D3L'], scoresrand['score_3D']['3L'])
    scores_3D3L_D = naivenorm(scoresD['3D3L'], scoresrand['score_3D']['3L'])
    
    # Hold number of objectives constant
    
    scores_1D_A = (scores_1D1L_A, scores_1D2L_A, scores_1D3L_A)
    scores_1D_B = (scores_1D1L_B, scores_1D2L_B, scores_1D3L_B)
    scores_1D_C = (scores_1D1L_C, scores_1D2L_C, scores_1D3L_C)
    scores_1D_D = (scores_1D1L_D, scores_1D2L_D, scores_1D3L_D)
    
    scores_2D_A = (scores_2D2L_A, scores_2D3L_A)
    scores_2D_B = (scores_2D2L_B, scores_2D3L_B)
    scores_2D_C = (scores_2D2L_C, scores_2D3L_C)
    scores_2D_D = (scores_2D2L_D, scores_2D3L_D)
    
    scores_3D_A = (scores_3D2L_A, scores_3D3L_A)
    scores_3D_B = (scores_3D2L_B, scores_3D3L_B)
    scores_3D_C = (scores_3D2L_C, scores_3D3L_C)
    scores_3D_D = (scores_3D2L_D, scores_3D3L_D)
    
    def code_combine_D(codesA, codesB, codesC, codesD):
    
        codes_1D_A = (codesA['1D1L'], codesA['1D2L'], codesA['1D3L'])
        codes_1D_B = (codesB['1D1L'], codesB['1D2L'], codesB['1D3L'])
        codes_1D_C = (codesC['1D1L'], codesC['1D2L'], codesC['1D3L'])
        codes_1D_D = (codesD['1D1L'], codesD['1D2L'], codesD['1D3L'])
        
        codes_2D_A = (codesA['2D2L'], codesA['2D3L'])
        codes_2D_B = (codesB['2D2L'], codesB['2D3L'])
        codes_2D_C = (codesC['2D2L'], codesC['2D3L'])
        codes_2D_D = (codesD['2D2L'], codesD['2D3L'])
        
        codes_3D_A = (codesA['3D2L'], codesA['3D3L'])
        codes_3D_B = (codesB['3D2L'], codesB['3D3L'])
        codes_3D_C = (codesC['3D2L'], codesC['3D3L'])
        codes_3D_D = (codesD['3D2L'], codesD['3D3L'])
        
        return(codes_1D_A, codes_1D_B, codes_1D_C, codes_1D_D, codes_2D_A, codes_2D_B, codes_2D_C, codes_2D_D, codes_3D_A, codes_3D_B, codes_3D_C, codes_3D_D)
    
    def code_combine_L(codesA, codesB, codesC, codesD):
    
        codes_1L_A = (codesA['1D1L'])
        codes_1L_B = (codesB['1D1L'])
        codes_1L_C = (codesC['1D1L'])
        codes_1L_D = (codesD['1D1L'])
    
        codes_2L_A = (codesA['1D2L'], codesA['2D2L'], codesA['3D2L'])
        codes_2L_B = (codesB['1D2L'], codesB['2D2L'], codesB['3D2L'])
        codes_2L_C = (codesC['1D2L'], codesC['2D2L'], codesC['3D2L'])
        codes_2L_D = (codesD['1D2L'], codesD['2D2L'], codesD['3D2L'])
    
        codes_3L_A = (codesA['1D3L'], codesA['2D3L'], codesA['3D3L'])
        codes_3L_B = (codesB['1D3L'], codesB['2D3L'], codesB['3D3L'])
        codes_3L_C = (codesC['1D3L'], codesC['2D3L'], codesC['3D3L'])
        codes_3L_D = (codesD['1D3L'], codesD['2D3L'], codesD['3D3L'])
        
        return(codes_1L_A, codes_1L_B, codes_1L_C, codes_1L_D, codes_2L_A, codes_2L_B, codes_2L_C, codes_2L_D, codes_3L_A, codes_3L_B, codes_3L_C, codes_3L_D)
        
    (codes_1L_A_PI, codes_1L_B_PI, codes_1L_C_PI, codes_1L_D_PI, codes_2L_A_PI, codes_2L_B_PI, codes_2L_C_PI, codes_2L_D_PI, codes_3L_A_PI, codes_3L_B_PI, codes_3L_C_PI, codes_3L_D_PI) = code_combine_L(codesA_PI, codesB_PI, codesC_PI, codesD_PI)
    (codes_1L_A_IS, codes_1L_B_IS, codes_1L_C_IS, codes_1L_D_IS, codes_2L_A_IS, codes_2L_B_IS, codes_2L_C_IS, codes_2L_D_IS, codes_3L_A_IS, codes_3L_B_IS, codes_3L_C_IS, codes_3L_D_IS) = code_combine_L(codesA_IS, codesB_IS, codesC_IS, codesD_IS)
    (codes_1L_A_CO, codes_1L_B_CO, codes_1L_C_CO, codes_1L_D_CO, codes_2L_A_CO, codes_2L_B_CO, codes_2L_C_CO, codes_2L_D_CO, codes_3L_A_CO, codes_3L_B_CO, codes_3L_C_CO, codes_3L_D_CO) = code_combine_L(codesA_CO, codesB_CO, codesC_CO, codesD_CO)
    (codes_1L_A_MO, codes_1L_B_MO, codes_1L_C_MO, codes_1L_D_MO, codes_2L_A_MO, codes_2L_B_MO, codes_2L_C_MO, codes_2L_D_MO, codes_3L_A_MO, codes_3L_B_MO, codes_3L_C_MO, codes_3L_D_MO) = code_combine_L(codesA_MO, codesB_MO, codesC_MO, codesD_MO)
    (codes_1L_A_PR, codes_1L_B_PR, codes_1L_C_PR, codes_1L_D_PR, codes_2L_A_PR, codes_2L_B_PR, codes_2L_C_PR, codes_2L_D_PR, codes_3L_A_PR, codes_3L_B_PR, codes_3L_C_PR, codes_3L_D_PR) = code_combine_L(codesA_PR, codesB_PR, codesC_PR, codesD_PR)
    
    (codes_1D_A_PI, codes_1D_B_PI, codes_1D_C_PI, codes_1D_D_PI, codes_2D_A_PI, codes_2D_B_PI, codes_2D_C_PI, codes_2D_D_PI, codes_3D_A_PI, codes_3D_B_PI, codes_3D_C_PI, codes_3D_D_PI) = code_combine_D(codesA_PI, codesB_PI, codesC_PI, codesD_PI)
    (codes_1D_A_IS, codes_1D_B_IS, codes_1D_C_IS, codes_1D_D_IS, codes_2D_A_IS, codes_2D_B_IS, codes_2D_C_IS, codes_2D_D_IS, codes_3D_A_IS, codes_3D_B_IS, codes_3D_C_IS, codes_3D_D_IS) = code_combine_D(codesA_IS, codesB_IS, codesC_IS, codesD_IS)
    (codes_1D_A_CO, codes_1D_B_CO, codes_1D_C_CO, codes_1D_D_CO, codes_2D_A_CO, codes_2D_B_CO, codes_2D_C_CO, codes_2D_D_CO, codes_3D_A_CO, codes_3D_B_CO, codes_3D_C_CO, codes_3D_D_CO) = code_combine_D(codesA_CO, codesB_CO, codesC_CO, codesD_CO)
    (codes_1D_A_MO, codes_1D_B_MO, codes_1D_C_MO, codes_1D_D_MO, codes_2D_A_MO, codes_2D_B_MO, codes_2D_C_MO, codes_2D_D_MO, codes_3D_A_MO, codes_3D_B_MO, codes_3D_C_MO, codes_3D_D_MO) = code_combine_D(codesA_MO, codesB_MO, codesC_MO, codesD_MO)
    (codes_1D_A_PR, codes_1D_B_PR, codes_1D_C_PR, codes_1D_D_PR, codes_2D_A_PR, codes_2D_B_PR, codes_2D_C_PR, codes_2D_D_PR, codes_3D_A_PR, codes_3D_B_PR, codes_3D_C_PR, codes_3D_D_PR) = code_combine_D(codesA_PR, codesB_PR, codesC_PR, codesD_PR)
    
    # COnvert to numpy array
    def convert_numpy(listofscores):
        scoresarray = np.empty((len(listofscores), len(listofscores[0])))
        
        for k in range(len(listofscores)):
            scoresarray[k,:] = listofscores[k]
            
        return(scoresarray)
        
    scores_1D_A = convert_numpy(scores_1D_A)
    scores_1D_B = convert_numpy(scores_1D_B)
    scores_1D_C = convert_numpy(scores_1D_C)
    scores_1D_D = convert_numpy(scores_1D_D)
    
    scores_2D_A = convert_numpy(scores_2D_A)
    scores_2D_B = convert_numpy(scores_2D_B)
    scores_2D_C = convert_numpy(scores_2D_C)
    scores_2D_D = convert_numpy(scores_2D_D)
    
    scores_3D_A = convert_numpy(scores_3D_A)
    scores_3D_B = convert_numpy(scores_3D_B)
    scores_3D_C = convert_numpy(scores_3D_C)
    scores_3D_D = convert_numpy(scores_3D_D)
    
    # Hold levers constant
    
    scores_1L_A = (scores_1D1L_A)
    scores_1L_B = (scores_1D1L_B)
    scores_1L_C = (scores_1D1L_C)
    scores_1L_D = (scores_1D1L_D)
    
    scores_2L_A = (scores_1D2L_A, scores_2D2L_A, scores_3D2L_A)
    scores_2L_B = (scores_1D2L_B, scores_2D2L_B, scores_3D2L_B)
    scores_2L_C = (scores_1D2L_C, scores_2D2L_C, scores_3D2L_C)
    scores_2L_D = (scores_1D2L_D, scores_2D2L_D, scores_3D2L_D)
    
    scores_3L_A = (scores_1D3L_A, scores_2D3L_A, scores_3D3L_A)
    scores_3L_B = (scores_1D3L_B, scores_2D3L_B, scores_3D3L_B)
    scores_3L_C = (scores_1D3L_C, scores_2D3L_C, scores_3D3L_C)
    scores_3L_D = (scores_1D3L_D, scores_2D3L_D, scores_3D3L_D)
    
    
    scores_2L_A = convert_numpy(scores_2L_A)
    scores_2L_B = convert_numpy(scores_2L_B)
    scores_2L_C = convert_numpy(scores_2L_C)
    scores_2L_D = convert_numpy(scores_2L_D)
    
    scores_3L_A = convert_numpy(scores_3L_A)
    scores_3L_B = convert_numpy(scores_3L_B)
    scores_3L_C = convert_numpy(scores_3L_C)
    scores_3L_D = convert_numpy(scores_3L_D)
    
 
    conditions1D = list()
    scores1D = list()
    levers1D = list()
    probleminterp1D_a = list()
    probleminterp1D_b = list()
    preference1D_a = list()
    preference1D_b = list()
    motivation1D_a = list()
    motivation1D_b = list()
    issues1D_a = list()
    issues1D_b = list()
    confidence1D_a = list()
    confidence1D_b = list()
    
    for k in range(len(scores_1D_A)):
        for j in range(len(scores_1D_A[0])):
            conditions1D.append("Lake Problem")
            scores1D.append(scores_1D_A[k,j])
            levers1D.append(k + 1)
            probleminterp1D_a.append(codes_1D_A_PI[k][j][0])
            probleminterp1D_b.append(codes_1D_A_PI[k][j][1])
            confidence1D_a.append(codes_1D_A_CO[k][j][0])
            confidence1D_b.append(codes_1D_A_CO[k][j][1])
            issues1D_a.append(codes_1D_A_IS[k][j][0])
            issues1D_b.append(codes_1D_A_IS[k][j][1])
            motivation1D_a.append(codes_1D_A_MO[k][j][0])
            motivation1D_b.append(codes_1D_A_MO[k][j][1])
            preference1D_a.append(codes_1D_A_PR[k][j][0])
            preference1D_b.append(codes_1D_A_PR[k][j][1])
    for k in range(len(scores_1D_B)):
        for j in range(len(scores_1D_B[0])):
            conditions1D.append("LP-S")
            scores1D.append(scores_1D_B[k,j])
            levers1D.append(k + 1)
            probleminterp1D_a.append(codes_1D_B_PI[k][j][0])
            probleminterp1D_b.append(codes_1D_B_PI[k][j][1])
            confidence1D_a.append(codes_1D_B_CO[k][j][0])
            confidence1D_b.append(codes_1D_B_CO[k][j][1])
            issues1D_a.append(codes_1D_B_IS[k][j][0])
            issues1D_b.append(codes_1D_B_IS[k][j][1])
            motivation1D_a.append(codes_1D_B_MO[k][j][0])
            motivation1D_b.append(codes_1D_B_MO[k][j][1])
            preference1D_a.append(codes_1D_B_PR[k][j][0])
            preference1D_b.append(codes_1D_B_PR[k][j][1])
    for k in range(len(scores_1D_C)):
        for j in range(len(scores_1D_C[0])):
            conditions1D.append("Neutral Problem")
            scores1D.append(scores_1D_C[k,j])
            levers1D.append(k + 1)
            probleminterp1D_a.append(codes_1D_C_PI[k][j][0])
            probleminterp1D_b.append(codes_1D_C_PI[k][j][1])
            confidence1D_a.append(codes_1D_C_CO[k][j][0])
            confidence1D_b.append(codes_1D_C_CO[k][j][1])
            issues1D_a.append(codes_1D_C_IS[k][j][0])
            issues1D_b.append(codes_1D_C_IS[k][j][1])
            motivation1D_a.append(codes_1D_C_MO[k][j][0])
            motivation1D_b.append(codes_1D_C_MO[k][j][1])
            preference1D_a.append(codes_1D_C_PR[k][j][0])
            preference1D_b.append(codes_1D_C_PR[k][j][1])
    for k in range(len(scores_1D_D)):
        for j in range(len(scores_1D_D[0])):
            conditions1D.append("NP-S")
            scores1D.append(scores_1D_D[k,j])
            levers1D.append(k + 1)
            probleminterp1D_a.append(codes_1D_D_PI[k][j][0])
            probleminterp1D_b.append(codes_1D_D_PI[k][j][1])
            confidence1D_a.append(codes_1D_D_CO[k][j][0])
            confidence1D_b.append(codes_1D_D_CO[k][j][1])
            issues1D_a.append(codes_1D_D_IS[k][j][0])
            issues1D_b.append(codes_1D_D_IS[k][j][1])
            motivation1D_a.append(codes_1D_D_MO[k][j][0])
            motivation1D_b.append(codes_1D_D_MO[k][j][1])
            preference1D_a.append(codes_1D_D_PR[k][j][0])
            preference1D_b.append(codes_1D_D_PR[k][j][1])
            
            
            
    bylever = {'Condition': conditions1D, 'Score': scores1D, 'Levers': levers1D, 
               'Problem Interpretation (a)': probleminterp1D_a, 'Problem Interpretation (b)': probleminterp1D_b,
               'Motivation (a)': motivation1D_a, 'Motivation (b)': motivation1D_b,
               'Preference (a)': preference1D_a, 'Preference (b)': preference1D_b,
               'Issues (a)': issues1D_a, 'Issues (b)': issues1D_b,
               'Confidence (a)': confidence1D_a, 'Confidence (b)': confidence1D_b}
    df1D = pd.DataFrame(data=bylever)
            
    conditions2D = list()
    scores2D = list()
    levers2D = list()
    probleminterp2D_a = list()
    probleminterp2D_b = list()
    preference2D_a = list()
    preference2D_b = list()
    motivation2D_a = list()
    motivation2D_b = list()
    issues2D_a = list()
    issues2D_b = list()
    confidence2D_a = list()
    confidence2D_b = list()
    for k in range(len(scores_2D_A)):
        for j in range(len(scores_2D_A[0])):
            conditions2D.append("Lake Problem")
            scores2D.append(scores_2D_A[k,j])
            levers2D.append(k + 2)
            probleminterp2D_a.append(codes_2D_A_PI[k][j][0])
            probleminterp2D_b.append(codes_2D_A_PI[k][j][1])
            confidence2D_a.append(codes_2D_A_CO[k][j][0])
            confidence2D_b.append(codes_2D_A_CO[k][j][1])
            issues2D_a.append(codes_2D_A_IS[k][j][0])
            issues2D_b.append(codes_2D_A_IS[k][j][1])
            motivation2D_a.append(codes_2D_A_MO[k][j][0])
            motivation2D_b.append(codes_2D_A_MO[k][j][1])
            preference2D_a.append(codes_2D_A_PR[k][j][0])
            preference2D_b.append(codes_2D_A_PR[k][j][1])
    for k in range(len(scores_2D_B)):
        for j in range(len(scores_2D_B[0])):
            conditions2D.append("LP-S")
            scores2D.append(scores_2D_B[k,j])
            levers2D.append(k + 2)
            probleminterp2D_a.append(codes_2D_B_PI[k][j][0])
            probleminterp2D_b.append(codes_2D_B_PI[k][j][1])
            confidence2D_a.append(codes_2D_B_CO[k][j][0])
            confidence2D_b.append(codes_2D_B_CO[k][j][1])
            issues2D_a.append(codes_2D_B_IS[k][j][0])
            issues2D_b.append(codes_2D_B_IS[k][j][1])
            motivation2D_a.append(codes_2D_B_MO[k][j][0])
            motivation2D_b.append(codes_2D_B_MO[k][j][1])
            preference2D_a.append(codes_2D_B_PR[k][j][0])
            preference2D_b.append(codes_2D_B_PR[k][j][1])
    for k in range(len(scores_2D_C)):
        for j in range(len(scores_2D_C[0])):
            conditions2D.append("Neutral Problem")
            scores2D.append(scores_2D_C[k,j])
            levers2D.append(k + 2)
            probleminterp2D_a.append(codes_2D_C_PI[k][j][0])
            probleminterp2D_b.append(codes_2D_C_PI[k][j][1])
            confidence2D_a.append(codes_2D_C_CO[k][j][0])
            confidence2D_b.append(codes_2D_C_CO[k][j][1])
            issues2D_a.append(codes_2D_C_IS[k][j][0])
            issues2D_b.append(codes_2D_C_IS[k][j][1])
            motivation2D_a.append(codes_2D_C_MO[k][j][0])
            motivation2D_b.append(codes_2D_C_MO[k][j][1])
            preference2D_a.append(codes_2D_C_PR[k][j][0])
            preference2D_b.append(codes_2D_C_PR[k][j][1])
    for k in range(len(scores_2D_D)):
        for j in range(len(scores_2D_D[0])):
            conditions2D.append("NP-S")
            scores2D.append(scores_2D_D[k,j])
            levers2D.append(k + 2)
            probleminterp2D_a.append(codes_2D_D_PI[k][j][0])
            probleminterp2D_b.append(codes_2D_D_PI[k][j][1])
            confidence2D_a.append(codes_2D_D_CO[k][j][0])
            confidence2D_b.append(codes_2D_D_CO[k][j][1])
            issues2D_a.append(codes_2D_D_IS[k][j][0])
            issues2D_b.append(codes_2D_D_IS[k][j][1])
            motivation2D_a.append(codes_2D_D_MO[k][j][0])
            motivation2D_b.append(codes_2D_D_MO[k][j][1])
            preference2D_a.append(codes_2D_D_PR[k][j][0])
            preference2D_b.append(codes_2D_D_PR[k][j][1])
            
    bylever = {'Condition': conditions2D, 'Score': scores2D, 'Levers': levers2D, 
               'Problem Interpretation (a)': probleminterp2D_a, 'Problem Interpretation (b)': probleminterp2D_b,
               'Motivation (a)': motivation2D_a, 'Motivation (b)': motivation2D_b,
               'Preference (a)': preference2D_a, 'Preference (b)': preference2D_b,
               'Issues (a)': issues2D_a, 'Issues (b)': issues2D_b,
               'Confidence (a)': confidence2D_a, 'Confidence (b)': confidence2D_b}
    df2D = pd.DataFrame(data=bylever)
            
    conditions3D = list()
    scores3D = list()
    levers3D = list()
    probleminterp3D_a = list()
    probleminterp3D_b = list()
    preference3D_a = list()
    preference3D_b = list()
    motivation3D_a = list()
    motivation3D_b = list()
    issues3D_a = list()
    issues3D_b = list()
    confidence3D_a = list()
    confidence3D_b = list()
    for k in range(len(scores_3D_A)):
        for j in range(len(scores_3D_A[0])):
            conditions3D.append("Lake Problem")
            scores3D.append(scores_3D_A[k,j])
            levers3D.append(k + 2)
            probleminterp3D_a.append(codes_3D_A_PI[k][j][0])
            probleminterp3D_b.append(codes_3D_A_PI[k][j][1])
            confidence3D_a.append(codes_3D_A_CO[k][j][0])
            confidence3D_b.append(codes_3D_A_CO[k][j][1])
            issues3D_a.append(codes_3D_A_IS[k][j][0])
            issues3D_b.append(codes_3D_A_IS[k][j][1])
            motivation3D_a.append(codes_3D_A_MO[k][j][0])
            motivation3D_b.append(codes_3D_A_MO[k][j][1])
            preference3D_a.append(codes_3D_A_PR[k][j][0])
            preference3D_b.append(codes_3D_A_PR[k][j][1])
    for k in range(len(scores_3D_B)):
        for j in range(len(scores_3D_B[0])):
            conditions3D.append("LP-S")
            scores3D.append(scores_3D_B[k,j])
            levers3D.append(k + 2)
            probleminterp3D_a.append(codes_3D_B_PI[k][j][0])
            probleminterp3D_b.append(codes_3D_B_PI[k][j][1])
            confidence3D_a.append(codes_3D_B_CO[k][j][0])
            confidence3D_b.append(codes_3D_B_CO[k][j][1])
            issues3D_a.append(codes_3D_B_IS[k][j][0])
            issues3D_b.append(codes_3D_B_IS[k][j][1])
            motivation3D_a.append(codes_3D_B_MO[k][j][0])
            motivation3D_b.append(codes_3D_B_MO[k][j][1])
            preference3D_a.append(codes_3D_B_PR[k][j][0])
            preference3D_b.append(codes_3D_B_PR[k][j][1])
    for k in range(len(scores_3D_C)):
        for j in range(len(scores_3D_C[0])):
            conditions3D.append("Neutral Problem")
            scores3D.append(scores_3D_C[k,j])
            levers3D.append(k + 2)
            probleminterp3D_a.append(codes_3D_C_PI[k][j][0])
            probleminterp3D_b.append(codes_3D_C_PI[k][j][1])
            confidence3D_a.append(codes_3D_C_CO[k][j][0])
            confidence3D_b.append(codes_3D_C_CO[k][j][1])
            issues3D_a.append(codes_3D_C_IS[k][j][0])
            issues3D_b.append(codes_3D_C_IS[k][j][1])
            motivation3D_a.append(codes_3D_C_MO[k][j][0])
            motivation3D_b.append(codes_3D_C_MO[k][j][1])
            preference3D_a.append(codes_3D_C_PR[k][j][0])
            preference3D_b.append(codes_3D_C_PR[k][j][1])
    for k in range(len(scores_3D_D)):
        for j in range(len(scores_3D_D[0])):
            conditions3D.append("NP-S")
            scores3D.append(scores_3D_D[k,j])
            levers3D.append(k + 2)
            probleminterp3D_a.append(codes_3D_D_PI[k][j][0])
            probleminterp3D_b.append(codes_3D_D_PI[k][j][1])
            confidence3D_a.append(codes_3D_D_CO[k][j][0])
            confidence3D_b.append(codes_3D_D_CO[k][j][1])
            issues3D_a.append(codes_3D_D_IS[k][j][0])
            issues3D_b.append(codes_3D_D_IS[k][j][1])
            motivation3D_a.append(codes_3D_D_MO[k][j][0])
            motivation3D_b.append(codes_3D_D_MO[k][j][1])
            preference3D_a.append(codes_3D_D_PR[k][j][0])
            preference3D_b.append(codes_3D_D_PR[k][j][1])
            
    bylever = {'Condition': conditions3D, 'Score': scores3D, 'Levers': levers3D, 
               'Problem Interpretation (a)': probleminterp3D_a, 'Problem Interpretation (b)': probleminterp3D_b,
               'Motivation (a)': motivation3D_a, 'Motivation (b)': motivation3D_b,
               'Preference (a)': preference3D_a, 'Preference (b)': preference3D_b,
               'Issues (a)': issues3D_a, 'Issues (b)': issues3D_b,
               'Confidence (a)': confidence3D_a, 'Confidence (b)': confidence3D_b}
    df3D = pd.DataFrame(data=bylever)
    
    # Objective plot
    conditions1L = list()
    scores1L = list()
    levers1L = list()
    probleminterp1L_a = list()
    probleminterp1L_b = list()
    preference1L_a = list()
    preference1L_b = list()
    motivation1L_a = list()
    motivation1L_b = list()
    issues1L_a = list()
    issues1L_b = list()
    confidence1L_a = list()
    confidence1L_b = list()
    for k in range(len(scores_1L_A)):
        conditions1L.append("Lake Problem")
        scores1L.append(scores_1L_A[k])
        levers1L.append(k + 1)
        probleminterp1L_a.append(codes_1L_A_PI[k][0])
        probleminterp1L_b.append(codes_1L_A_PI[k][1])
        confidence1L_a.append(codes_1L_A_CO[k][0])
        confidence1L_b.append(codes_1L_A_CO[k][1])
        issues1L_a.append(codes_1L_A_IS[k][0])
        issues1L_b.append(codes_1L_A_IS[k][1])
        motivation1L_a.append(codes_1L_A_MO[k][0])
        motivation1L_b.append(codes_1L_A_MO[k][1])
        preference1L_a.append(codes_1L_A_PR[k][0])
        preference1L_b.append(codes_1L_A_PR[k][1])
    for k in range(len(scores_1L_B)):
        conditions1L.append("LP-S")
        scores1L.append(scores_1L_B[k])
        levers1L.append(k + 1)
        probleminterp1L_a.append(codes_1L_B_PI[k][0])
        probleminterp1L_b.append(codes_1L_B_PI[k][1])
        confidence1L_a.append(codes_1L_B_CO[k][0])
        confidence1L_b.append(codes_1L_B_CO[k][1])
        issues1L_a.append(codes_1L_B_IS[k][0])
        issues1L_b.append(codes_1L_B_IS[k][1])
        motivation1L_a.append(codes_1L_B_MO[k][0])
        motivation1L_b.append(codes_1L_B_MO[k][1])
        preference1L_a.append(codes_1L_B_PR[k][0])
        preference1L_b.append(codes_1L_B_PR[k][1])
    for k in range(len(scores_1L_C)):
        conditions1L.append("Neutral Problem")
        scores1L.append(scores_1L_C[k])
        levers1L.append(k + 1)
        probleminterp1L_a.append(codes_1L_C_PI[k][0])
        probleminterp1L_b.append(codes_1L_C_PI[k][1])
        confidence1L_a.append(codes_1L_C_CO[k][0])
        confidence1L_b.append(codes_1L_C_CO[k][1])
        issues1L_a.append(codes_1L_C_IS[k][0])
        issues1L_b.append(codes_1L_C_IS[k][1])
        motivation1L_a.append(codes_1L_C_MO[k][0])
        motivation1L_b.append(codes_1L_C_MO[k][1])
        preference1L_a.append(codes_1L_C_PR[k][0])
        preference1L_b.append(codes_1L_C_PR[k][1])
    for k in range(len(scores_1L_D)):
        conditions1L.append("NP-S")
        scores1L.append(scores_1L_D[k])
        levers1L.append(k + 1)
        probleminterp1L_a.append(codes_1L_D_PI[k][0])
        probleminterp1L_b.append(codes_1L_D_PI[k][1])
        confidence1L_a.append(codes_1L_D_CO[k][0])
        confidence1L_b.append(codes_1L_D_CO[k][1])
        issues1L_a.append(codes_1L_D_IS[k][0])
        issues1L_b.append(codes_1L_D_IS[k][1])
        motivation1L_a.append(codes_1L_D_MO[k][0])
        motivation1L_b.append(codes_1L_D_MO[k][1])
        preference1L_a.append(codes_1L_D_PR[k][0])
        preference1L_b.append(codes_1L_D_PR[k][1])
            
    bylever = {'Condition': conditions1L, 'Score': scores1L, 'Objectives': levers1L, 
               'Problem Interpretation (a)': probleminterp1L_a, 'Problem Interpretation (b)': probleminterp1L_b,
               'Motivation (a)': motivation1L_a, 'Motivation (b)': motivation1L_b,
               'Preference (a)': preference1L_a, 'Preference (b)': preference1L_b,
               'Issues (a)': issues1L_a, 'Issues (b)': issues1L_b,
               'Confidence (a)': confidence1L_a, 'Confidence (b)': confidence1L_b}
    df1L = pd.DataFrame(data=bylever)
            
    conditions2L = list()
    scores2L = list()
    levers2L = list()
    probleminterp2L_a = list()
    probleminterp2L_b = list()
    preference2L_a = list()
    preference2L_b = list()
    motivation2L_a = list()
    motivation2L_b = list()
    issues2L_a = list()
    issues2L_b = list()
    confidence2L_a = list()
    confidence2L_b = list()
    for k in range(len(scores_2L_A)):
        for j in range(len(scores_2L_A[0])):
            conditions2L.append("Lake Problem")
            scores2L.append(scores_2L_A[k,j])
            levers2L.append(k + 1)
            probleminterp2L_a.append(codes_2L_A_PI[k][j][0])
            probleminterp2L_b.append(codes_2L_A_PI[k][j][1])
            confidence2L_a.append(codes_2L_A_CO[k][j][0])
            confidence2L_b.append(codes_2L_A_CO[k][j][1])
            issues2L_a.append(codes_2L_A_IS[k][j][0])
            issues2L_b.append(codes_2L_A_IS[k][j][1])
            motivation2L_a.append(codes_2L_A_MO[k][j][0])
            motivation2L_b.append(codes_2L_A_MO[k][j][1])
            preference2L_a.append(codes_2L_A_PR[k][j][0])
            preference2L_b.append(codes_2L_A_PR[k][j][1]) 
    for k in range(len(scores_2L_B)):
        for j in range(len(scores_2L_B[0])):
            conditions2L.append("LP-S")
            scores2L.append(scores_2L_B[k,j])
            levers2L.append(k + 1)
            probleminterp2L_a.append(codes_2L_B_PI[k][j][0])
            probleminterp2L_b.append(codes_2L_B_PI[k][j][1])
            confidence2L_a.append(codes_2L_B_CO[k][j][0])
            confidence2L_b.append(codes_2L_B_CO[k][j][1])
            issues2L_a.append(codes_2L_B_IS[k][j][0])
            issues2L_b.append(codes_2L_B_IS[k][j][1])
            motivation2L_a.append(codes_2L_B_MO[k][j][0])
            motivation2L_b.append(codes_2L_B_MO[k][j][1])
            preference2L_a.append(codes_2L_B_PR[k][j][0])
            preference2L_b.append(codes_2L_B_PR[k][j][1]) 
    for k in range(len(scores_2L_C)):
        for j in range(len(scores_2L_C[0])):
            conditions2L.append("Neutral Problem")
            scores2L.append(scores_2L_C[k,j])
            levers2L.append(k + 1)
            probleminterp2L_a.append(codes_2L_C_PI[k][j][0])
            probleminterp2L_b.append(codes_2L_C_PI[k][j][1])
            confidence2L_a.append(codes_2L_C_CO[k][j][0])
            confidence2L_b.append(codes_2L_C_CO[k][j][1])
            issues2L_a.append(codes_2L_C_IS[k][j][0])
            issues2L_b.append(codes_2L_C_IS[k][j][1])
            motivation2L_a.append(codes_2L_C_MO[k][j][0])
            motivation2L_b.append(codes_2L_C_MO[k][j][1])
            preference2L_a.append(codes_2L_C_PR[k][j][0])
            preference2L_b.append(codes_2L_C_PR[k][j][1]) 
    for k in range(len(scores_2L_D)):
        for j in range(len(scores_2L_D[0])):
            conditions2L.append("NP-S")
            scores2L.append(scores_2L_D[k,j])
            levers2L.append(k + 1)
            probleminterp2L_a.append(codes_2L_D_PI[k][j][0])
            probleminterp2L_b.append(codes_2L_D_PI[k][j][1])
            confidence2L_a.append(codes_2L_D_CO[k][j][0])
            confidence2L_b.append(codes_2L_D_CO[k][j][1])
            issues2L_a.append(codes_2L_D_IS[k][j][0])
            issues2L_b.append(codes_2L_D_IS[k][j][1])
            motivation2L_a.append(codes_2L_D_MO[k][j][0])
            motivation2L_b.append(codes_2L_D_MO[k][j][1])
            preference2L_a.append(codes_2L_D_PR[k][j][0])
            preference2L_b.append(codes_2L_D_PR[k][j][1]) 
            
    bylever = {'Condition': conditions2L, 'Score': scores2L, 'Objectives': levers2L,
               'Problem Interpretation (a)': probleminterp2L_a, 'Problem Interpretation (b)': probleminterp2L_b,
               'Motivation (a)': motivation2L_a, 'Motivation (b)': motivation2L_b,
               'Preference (a)': preference2L_a, 'Preference (b)': preference2L_b,
               'Issues (a)': issues2L_a, 'Issues (b)': issues2L_b,
               'Confidence (a)': confidence2L_a, 'Confidence (b)': confidence2L_b}
    df2L = pd.DataFrame(data=bylever)
            
    conditions3L = list()
    scores3L = list()
    levers3L = list()
    probleminterp3L_a = list()
    probleminterp3L_b = list()
    preference3L_a = list()
    preference3L_b = list()
    motivation3L_a = list()
    motivation3L_b = list()
    issues3L_a = list()
    issues3L_b = list()
    confidence3L_a = list()
    confidence3L_b = list()
    for k in range(len(scores_3L_A)):
        for j in range(len(scores_3L_A[0])):
            conditions3L.append("Lake Problem")
            scores3L.append(scores_3L_A[k,j])
            levers3L.append(k + 1)
            probleminterp3L_a.append(codes_3L_A_PI[k][j][0])
            probleminterp3L_b.append(codes_3L_A_PI[k][j][1])
            confidence3L_a.append(codes_3L_A_CO[k][j][0])
            confidence3L_b.append(codes_3L_A_CO[k][j][1])
            issues3L_a.append(codes_3L_A_IS[k][j][0])
            issues3L_b.append(codes_3L_A_IS[k][j][1])
            motivation3L_a.append(codes_3L_A_MO[k][j][0])
            motivation3L_b.append(codes_3L_A_MO[k][j][1])
            preference3L_a.append(codes_3L_A_PR[k][j][0])
            preference3L_b.append(codes_3L_A_PR[k][j][1]) 
    for k in range(len(scores_3L_B)):
        for j in range(len(scores_3L_B[0])):
            conditions3L.append("LP-S")
            scores3L.append(scores_3L_B[k,j])
            levers3L.append(k + 1)
            probleminterp3L_a.append(codes_3L_B_PI[k][j][0])
            probleminterp3L_b.append(codes_3L_B_PI[k][j][1])
            confidence3L_a.append(codes_3L_B_CO[k][j][0])
            confidence3L_b.append(codes_3L_B_CO[k][j][1])
            issues3L_a.append(codes_3L_B_IS[k][j][0])
            issues3L_b.append(codes_3L_B_IS[k][j][1])
            motivation3L_a.append(codes_3L_B_MO[k][j][0])
            motivation3L_b.append(codes_3L_B_MO[k][j][1])
            preference3L_a.append(codes_3L_B_PR[k][j][0])
            preference3L_b.append(codes_3L_B_PR[k][j][1]) 
    for k in range(len(scores_3L_C)):
        for j in range(len(scores_3L_C[0])):
            conditions3L.append("Neutral Problem")
            scores3L.append(scores_3L_C[k,j])
            levers3L.append(k + 1)
            probleminterp3L_a.append(codes_3L_C_PI[k][j][0])
            probleminterp3L_b.append(codes_3L_C_PI[k][j][1])
            confidence3L_a.append(codes_3L_C_CO[k][j][0])
            confidence3L_b.append(codes_3L_C_CO[k][j][1])
            issues3L_a.append(codes_3L_C_IS[k][j][0])
            issues3L_b.append(codes_3L_C_IS[k][j][1])
            motivation3L_a.append(codes_3L_C_MO[k][j][0])
            motivation3L_b.append(codes_3L_C_MO[k][j][1])
            preference3L_a.append(codes_3L_C_PR[k][j][0])
            preference3L_b.append(codes_3L_C_PR[k][j][1])  
    for k in range(len(scores_3L_D)):
        for j in range(len(scores_3L_D[0])):
            conditions3L.append("NP-S")
            scores3L.append(scores_3L_D[k,j])
            levers3L.append(k + 1)
            probleminterp3L_a.append(codes_3L_D_PI[k][j][0])
            probleminterp3L_b.append(codes_3L_D_PI[k][j][1])
            confidence3L_a.append(codes_3L_D_CO[k][j][0])
            confidence3L_b.append(codes_3L_D_CO[k][j][1])
            issues3L_a.append(codes_3L_D_IS[k][j][0])
            issues3L_b.append(codes_3L_D_IS[k][j][1])
            motivation3L_a.append(codes_3L_D_MO[k][j][0])
            motivation3L_b.append(codes_3L_D_MO[k][j][1])
            preference3L_a.append(codes_3L_D_PR[k][j][0])
            preference3L_b.append(codes_3L_D_PR[k][j][1])  
            
    bylever = {'Condition': conditions3L, 'Score': scores3L, 'Objectives': levers3L, 
               'Problem Interpretation (a)': probleminterp3L_a, 'Problem Interpretation (b)': probleminterp3L_b,
               'Motivation (a)': motivation3L_a, 'Motivation (b)': motivation3L_b,
               'Preference (a)': preference3L_a, 'Preference (b)': preference3L_b,
               'Issues (a)': issues3L_a, 'Issues (b)': issues3L_b,
               'Confidence (a)': confidence3L_a, 'Confidence (b)': confidence3L_b}
    df3L = pd.DataFrame(data=bylever)
    
    return(df1D, df2D, df3D, df1L, df2L, df3L)
    
def visualize_skill_interactive_1obj(df1D):
    
    df1D = df1D.drop(df1D[df1D['Condition'] == 'NP-S'].index)
    df1D = df1D.drop(df1D[df1D['Condition'] == 'LP-S'].index)
    
    # Lever plot
    import seaborn as sns
    sns.set(style="whitegrid", palette="pastel", color_codes=True)
    
    f1, ax = plt.subplots(figsize=(12, 8))
    
    g = sns.violinplot(x="Levers", y="Score", hue="Condition", data=df1D,
                   palette={"Lake Problem": "#1f78b4", "Neutral Problem": "#33a02c"}, cut=0, legend_out = True)
    sns.despine(left=True)
    
    f1.suptitle('Maximize Economic Benefits', fontsize=18, fontweight='bold')
    ax.set_xlabel("Number of Levers",size = 16,alpha=0.7)
    ax.set_ylabel("Fraction of Economic Benefits Achieved",size = 16,alpha=0.7)
    ax.set_ylim((0,1))
    plt.legend(loc='lower right', fontsize=16)
#    new_labels = ['Lake Problem', 'Neutral Problem']
#    for t, l in zip(g._legend.texts, new_labels): t.set_text(l)
    
    plt.savefig('fig7.pdf', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    
    plt.savefig('fig7.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)

    return(f1)
#    
def visualize_skill_interpretation_1obj(df1D):
    
    df1D = df1D.drop(df1D[df1D['Condition'] == 'NP-S'].index)
    df1D = df1D.drop(df1D[df1D['Condition'] == 'LP-S'].index)

#    df1D = df1D.reindex(range(len(df1D)))
#    df1D['Levers'] = df1D['Levers'].astype(int)
    
    OO = list()
    for k in df1D.index:
        if df1D['Problem Interpretation (a)'][k] == 'O' or df1D['Problem Interpretation (b)'][k] == 'O':
            OO.append('Outside Objectives')
        else:
            OO.append('Other')
    df1D = df1D.assign(Problem_Interpretation = OO)
    
    # Lever plot
    import seaborn as sns
    sns.set(style="whitegrid", palette="pastel", color_codes=True)
    
    f1, ax = plt.subplots(figsize=(12, 8))
    
    g = sns.violinplot(x="Levers", y="Score", hue="Problem_Interpretation", data=df1D,
                   palette={"Outside Objectives": plt.cm.viridis(1.5/2), "Other": plt.cm.viridis(0.25/2)}, cut=0)
    sns.despine(left=True)
    
    f1.suptitle('Maximize Economic Benefits', fontsize=18, fontweight='bold')
    ax.set_xlabel("Number of Levers",size = 16,alpha=0.7)
    ax.set_ylabel("Fraction of Economic Benefits Achieved",size = 16,alpha=0.7)
    ax.set_ylim((0,1))
    plt.legend(loc='lower right', fontsize=16)
    
    plt.savefig('fig9.pdf', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    
    plt.savefig('fig9.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)

    return(f1)
    

def visualize_skill_interactive_byobj(df2L, df3L):
    
    df2L = df2L.drop(df2L[df2L['Condition'] == 'NP-S'].index)
    df2L = df2L.drop(df2L[df2L['Condition'] == 'LP-S'].index)
#    df2L = df2L.reindex(range(len(df2L)))
    
    df3L = df3L.drop(df3L[df3L['Condition'] == 'NP-S'].index)
    df3L = df3L.drop(df3L[df3L['Condition'] == 'LP-S'].index)
#    df3L = df3L.reindex(range(len(df3L)))
        
    # Lever plot
    import seaborn as sns
    sns.set(style="whitegrid", palette="pastel", color_codes=True)
    
    fig = plt.figure(figsize=(8,12), dpi=150)
    ax = fig.add_subplot(211)
    
    g = sns.violinplot(x="Objectives", y="Score", hue="Condition", data=df2L,
                   palette={"Lake Problem": "#1f78b4", "Neutral Problem": "#33a02c"}, cut=0)
    sns.despine(left=True)
    
    ax.set_title('Two-Lever Decisions', fontsize=18, fontweight='bold')
    ax.set_xlabel("Number of Objectives",size = 16,alpha=0.7)
    ax.set_ylabel("Pareto score",size = 16,alpha=0.7)
    ax.set_ylim((0,1))
    plt.legend(loc='lower left', fontsize=16)
    
    ax = fig.add_subplot(212)
    
    g = sns.violinplot(x="Objectives", y="Score", hue="Condition", data=df3L,
                   palette={"Lake Problem": "#1f78b4", "Neutral Problem": "#33a02c"}, cut=0)
    sns.despine(left=True)
    
    ax.set_title('Three-Lever Decisions', fontsize=18, fontweight='bold')
    ax.set_xlabel("Number of Objectives",size = 16,alpha=0.7)
    ax.set_ylabel("Pareto score", size = 16, alpha=0.7)
    ax.set_ylim((0,1))
    plt.legend(loc='lower left', fontsize=16)
    
    plt.savefig('fig3.pdf', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
    
    plt.savefig('fig3.png', dpi=300, facecolor='w', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches=0.1,
        frameon=None, metadata=None)
        
    
    return(fig)
