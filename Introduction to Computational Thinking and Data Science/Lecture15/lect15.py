# -*- coding: utf-8 -*-
"""
Created on Wed May 11 14:29:43 2016

@author: johnguttag
"""

import random, matplotlib, numpy
import matplotlib.pyplot as plt

#set line width
matplotlib.rcParams['lines.linewidth'] = 4
#set font size for titles 
matplotlib.rcParams['axes.titlesize'] = 20
#set font size for labels on axes
matplotlib.rcParams['axes.labelsize'] = 20
#set size of numbers on x-axis
matplotlib.rcParams['xtick.labelsize'] = 16
#set size of numbers on y-axis
matplotlib.rcParams['ytick.labelsize'] = 16
#set size of ticks on x-axis
matplotlib.rcParams['xtick.major.size'] = 7
#set size of ticks on y-axis
matplotlib.rcParams['ytick.major.size'] = 7
#set size of markers
matplotlib.rcParams['lines.markersize'] = 10
#set number of examples shown in legends
matplotlib.rcParams['legend.numpoints'] = 1

# temps = [98.6, 99, 99.5, 99.3, 100, 99.9, 100.5]
# times = range(3,10)
# plt.plot(times, temps)
# plt.xlabel('Time')
# plt.ylabel('Oral Temperature')
# plt.title('A Bout with the Flu')
# plt.ylim(97,102)
# plt.show()

random.seed(0)
numCasesPerYear = 36000
numYears = 3
stateSize = 10000
communitySize = 10
numCommunities = stateSize//communitySize

# numTrials = 100
# numGreater = 0
# for t in range(numTrials):
#     locs = [0]*numCommunities
#     for i in range(numYears*numCasesPerYear):
#         locs[random.choice(range(numCommunities))] += 1
#     if locs[111] >= 143:
#         numGreater += 1
# prob = round(numGreater/numTrials, 4)
# print('Est. probability of region 111 having\
#  at least 143 cases =', prob)


numTrials = 100
anyRegion = 0
for trial in range(numTrials):
   locs = [0]*numCommunities
   for i in range(numYears*numCasesPerYear):
       locs[random.choice(range(numCommunities))] += 1
   if max(locs) >= 143:
       anyRegion += 1
print(anyRegion)
aProb = round(float(anyRegion)/numTrials, 4)
print('Est. probability of some region having \
at least 143 cases =', aProb)

