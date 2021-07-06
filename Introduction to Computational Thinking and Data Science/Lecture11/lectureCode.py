import random, matplotlib, numpy
import matplotlib.pyplot as plt
#from test_hypothesis import *

#set line width
matplotlib.rcParams['lines.linewidth'] = 4
#set font size for titles 
matplotlib.rcParams['axes.titlesize'] = 18
#set font size for labels on axes
matplotlib.rcParams['axes.labelsize'] = 18
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

def variance(X):
    mean = float(sum(X))/len(X)
    diffs = 0.0
    for x in X:
        diffs += (x - mean)**2
    return diffs/len(X)

def stdDev(X):
    return variance(X)**0.5
 
def minkowskiDist(v1, v2, p):
    """Assumes v1 and v2 are equal-length arrays of numbers
       Returns Minkowski distance of order p between v1 and v2"""
    dist = 0.0
    for i in range(len(v1)):
        dist += abs(v1[i] - v2[i])**p
    return dist**(1.0/p)

class Animal(object):
    def __init__(self, name, features):
        """Assumes name a string; features a list of numbers"""
        self.name = name
        self.features = numpy.array(features)
        
    def getName(self):
        return self.name
    
    def getFeatures(self):
        return self.features
    
    def distance(self, other):
        """Assumes other an Animal
           Returns the Euclidean distance between feature vectors
              of self and other"""
        return minkowskiDist(self.getFeatures(),
                             other.getFeatures(), 2)

def compareAnimals(animals, precision):
    """Assumes animals is a list of animals, precision an int >= 0
       Builds a table of Euclidean distance between each animal"""
    #Get labels for columns and rows
    columnLabels = []
    for a in animals:
        columnLabels.append(a.getName())
    rowLabels = columnLabels[:]
    tableVals = []
    #Get distances between pairs of animals
    #For each row
    for a1 in animals:
        row = []
        #For each column
        for a2 in animals:
            if a1 == a2:
                row.append('--')
            else:
                distance = a1.distance(a2)
                row.append(str(round(distance, precision)))
        tableVals.append(row)
    #Produce table
    table = plt.table(rowLabels = rowLabels,
                        colLabels = columnLabels,
                        cellText = tableVals,
                        cellLoc = 'center',
                        loc = 'center',
                        colWidths = [0.2]*len(animals))
    table.scale(1, 2.5)
    plt.title('Eucliedan Distance Between Animals')

rattlesnake = Animal('rattlesnake', [1,1,1,1,0])
boa = Animal('boa\nconstrictor', [0,1,0,1,0])
dartFrog = Animal('dart frog', [1,0,1,0,4])
animals = [rattlesnake, boa, dartFrog]
compareAnimals(animals, 3)
#
alligator = Animal('alligator', [1,1,0,1,4])
animals.append(alligator)
compareAnimals(animals, 3)
plt.show()

rattlesnake = Animal('rattlesnake', [1,1,1,1,0])
boa = Animal('boa\nconstrictor', [0,1,0,1,0])
dartFrog = Animal('dart frog', [1,0,1,0,1])
alligator = Animal('alligator', [1,1,0,1,1])
animals = [rattlesnake, boa, dartFrog, alligator]
compareAnimals(animals, 3)
