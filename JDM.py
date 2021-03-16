#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 09:12:03 2018

@author: cms793
"""


import pandas as pd
import numpy as np
from jdmtools import *
import pickle
import os


''' 
Begin with initial data processing into nice dictionaries.
'''

# Make a list with the names of the folders and check number of folders
dir = os.getcwd()
#folders = os.listdir('/Users/caitl/Documents/SCRiM/JDM/download-3')
folders = os.listdir(dir + "\\download-3")
#C:\Users\caitl\Documents\SCRiM\JDM

names_A = list()
names_B = list()
names_C = list()
names_D = list()

# Break folders into groups
for names in folders:
    if names.endswith("a") or names.endswith("A") or names.endswith("a-2"):
        names_A.append(names)
    elif names.endswith("b"):
        names_B.append(names)
    elif names.endswith("c"):
        names_C.append(names)
    elif names.endswith("d") or names.endswith("D"):
        names_D.append(names)
    else:
        pass
        
A = Condition(names_A)
B = Condition(names_B)
C = Condition(names_C)
D = Condition(names_D)

A_data = A.setup()
B_data = B.setup()
C_data = C.setup()
D_data = D.setup()

'''
Point 1: Oversimplification leads to poorly-executed attempts to solve what is
perceived to be the real problem.

Analyze economic benefits achieved by different groups at the 1-objective stage.


a. Violin plot comparing A/Economic benefits in the one-objective stage at 
different lever settings between LP and NP, interactive only
b. Violin plot comparing A/Economic benefits achieved at the one-lever setting 
between groups flagged "Problem Interpretation- Other Objectives" versus not, 
regardless of context group (interactive only)
c. Stacked bar chart comparing percentage of participants flagged with 
different problem interpretation codes (including no code) in LP vs. NP at some
any lever setting
d. K-S test comparing distribution among context/context-neutral groups, OO-no 
OO 
e. Show 2-D A/B Economic Benefits/Water Quality tradeoff diagram with points at 
1-objective stage in one color, 2-objective stage in another color
'''

# # If not already done, perform the following analysis"
# (pref1D, pref2D, pref3D, pref1L, pref2L, pref3L) = scores_preference(A_data, B_data, C_data, D_data)
# pref1D.to_pickle('pref1D.pkl')
# pref2D.to_pickle('pref2D.pkl')
# pref3D.to_pickle('pref3D.pkl')
# pref1L.to_pickle('pref1L.pkl')
# pref2L.to_pickle('pref2L.pkl')
# pref3L.to_pickle('pref3L.pkl')

# (df1D, df2D, df3D, df1L, df2L, df3L) = scores_naivenorm(A_data, B_data, C_data, D_data)
# df1D.to_pickle('df1D.pkl')
# df2D.to_pickle('df2D.pkl')
# df3D.to_pickle('df3D.pkl')
# df1L.to_pickle('df1L.pkl')
# df2L.to_pickle('df2L.pkl')
# df3L.to_pickle('df3L.pkl')
    
# Otherwise, read the files in

# Preference scores
pref1D = pd.read_pickle('pref1D.pkl')
pref2D = pd.read_pickle('pref2D.pkl')
pref3D = pd.read_pickle('pref3D.pkl')
pref1L = pd.read_pickle('pref1L.pkl')
pref2L = pd.read_pickle('pref2L.pkl')
pref3L = pd.read_pickle('pref3L.pkl')

# Pareto scores
df1D = pd.read_pickle('df1D.pkl')
df2D = pd.read_pickle('df2D.pkl')
df3D = pd.read_pickle('df3D.pkl')
df1L = pd.read_pickle('df1L.pkl')
df2L = pd.read_pickle('df2L.pkl')
df3L = pd.read_pickle('df3L.pkl')

# Remove rows with flagged (empty) values
# Only do this for the 2D and 2L arrays since C-2D2L has the only empty value
pref2D = pref2D.drop(pref2D.index[254])
pref2L = pref2L.drop(pref2L.index[254])

# Remove rows with flagged (empty) values
# Only do this for the 2D and 2L arrays since C-2D2L has the only empty value
df2D = df2D.drop(df2D.index[151])
df2L = df2L.drop(df2L.index[254])
    
''' A. Violin plot comparing A/Economic Benefits at one-objective stage '''

visualize_skill_interactive_1obj(df1D)

# KS test
KS_scores_1obj = performance_context_1obj(df1D)

# ''' B. Violin plot comparing A/Economic benefits achieved among other objectives/
# no problem interpretation flag group at one objective stage '''
# visualize_skill_interpretation_1obj(df1D)

# KS test
performance_interpretation_1obj(df1D)


# ''' C. Compare problem interpretation codes between lake problem, neutral 
# problem as stacked bar chart'''

# (fig, ooslp, oosnp) = outerobjectives_context_1obj_notstacked(df1D)


''' D. Compare strategies with "Other Objectives" flag in one-objective stage
with same participants' 2-objective strategies in 2-D space'''

(refecon, refpho) = refgen_2D3L(10000)

OOs_LP = unwind_OOs_LP(A_data)
OOs_NP = unwind_OOs_NP(C_data)

OOs = bespooled_combine_PI(OOs_LP, OOs_NP)

#tradeoffs_1obj_2obj_OO(OOs,refecon_2D3L, refpho_2D3L)
tradeoffs_1obj_2obj_OO(OOs_LP,refecon, refpho)
tradeoffs_example(refecon_2D3L, refpho_2D3L)

''' 
2. Are participants able to navigate the ecological threshold?
'''

# What percentage of T participants avoid ecological threshold?
Ts_LP = unwind_codes_LP(A_data, 'Preference', 'T')
Ts_NP = unwind_codes_NP(C_data, 'Preference', 'T')
Ts = bespooled_combine(Ts_LP, Ts_NP)
len_Ts = check_bespooled_length(Ts)

(percent_under_T, percent_near_T) = thresholds_analyze(Ts)

# What percentage coded as T?
n_T_2D = len(df2D.loc[(df2D['Preference (a)'] == 'T') | (df2D['Preference (b)'] == 'T')])
n_2D = len(df2D)
p_T_2D = float(n_T_2D)/float(n_2D)

n_T_3D = len(df3D.loc[(df3D['Preference (a)'] == 'T') | (df3D['Preference (b)'] == 'T')])
n_3D = len(df3D)
p_T_3D = float(n_T_2D)/float(n_3D)

# What percentage of C participants avoid ecological threshold?
Cs_LP = unwind_codes_LP(A_data, 'Preference', 'C')
Cs_NP = unwind_codes_NP(C_data, 'Preference', 'C')
Cs = bespooled_combine(Cs_LP, Cs_NP)
len_Cs = check_bespooled_length(Cs)

(percent_under_C, percent_near_C) = thresholds_analyze(Cs)

# What percentage of S participants avoid ecological threshold?
Ss_LP = unwind_codes_LP(A_data, 'Preference', 'S')
Ss_NP = unwind_codes_NP(C_data, 'Preference', 'S')
Ss = bespooled_combine(Ss_LP, Ss_NP)
len_Ss = check_bespooled_length(Ss)

(percent_under_S, percent_near_S) = thresholds_analyze(Ss)

# What percentage of no flag participants avoid ecological threshold?
nans_LP = unwind_codes_LP(A_data, 'Preference', np.nan)
nans_NP = unwind_codes_NP(C_data, 'Preference', np.nan)
nans = bespooled_combine(nans_LP, nans_NP)
len_nans = check_bespooled_length(nans)

(percent_under_nan, percent_near_nan) = thresholds_analyze(nans)

any_LP = unwind_codes_LP_any(B_data, 'Preference')
any_NP = unwind_codes_NP_any(D_data, 'Preference')
anys = bespooled_combine(any_LP, any_NP)
len_anys = check_bespooled_length(anys)
(percent_under_any, percent_near_any) = thresholds_analyze(anys)

''' 
3. How does the number of objectives influence Pareto score?
'''

visualize_skill_interactive_byobj(df2L, df3L)

visualize_preference_interactive_utipho(pref1L, pref2L, pref3L)

# How does self-reported confusion vary among objective number?

Confused_LP = unwind_codes_LP(A_data, 'Confidence', 'C')
Confused_NP = unwind_codes_NP(C_data, 'Confidence', 'C')
confused = bespooled_combine(Confused_LP, Confused_NP)

(len_confused, len1obj, len2obj, len3obj) = check_bespooled_length(confused)


Straightforward_LP = unwind_codes_LP(A_data, 'Confidence', 'S')
Straightforward_NP = unwind_codes_NP(C_data, 'Confidence', 'S')
straightforward = bespooled_combine(Straightforward_LP, Straightforward_NP)

(len_straightforward, len1obj, len2obj, len3obj) = check_bespooled_length(straightforward)








