# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:45:20 2016

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


def rSquared(observed, predicted):
    error = ((predicted - observed)**2).sum()
    meanError = error/len(observed)
    return 1 - (meanError/numpy.var(observed))

def genFits(xVals, yVals, degrees):
    models = []
    for d in degrees:
        model = numpy.polyfit(xVals, yVals, d)
        models.append(model)
    return models

def testFits(models, degrees, xVals, yVals, title):
    plt.plot(xVals, yVals, 'o', label = 'Data')
    for i in range(len(models)):
        estYVals = numpy.polyval(models[i], xVals)
        error = rSquared(yVals, estYVals)
        plt.plot(xVals, estYVals,
                   label = 'Fit of degree '\
                   + str(degrees[i])\
                   + ', R2 = ' + str(round(error, 5)))
    plt.legend(loc = 'best')
    plt.title(title)

def getData(fileName):
    dataFile = open(fileName, 'r')
    distances = []
    masses = []
    dataFile.readline() #discard header
    for line in dataFile:
        d, m = line.split()
        distances.append(float(d))
        masses.append(float(m))
    dataFile.close()
    return (masses, distances)
    
def labelPlot():
    plt.title('Measured Displacement of Spring')
    plt.xlabel('|Force| (Newtons)')
    plt.ylabel('Distance (meters)')

def plotData(fileName):
    xVals, yVals = getData(fileName)
    xVals = numpy.array(xVals)
    yVals = numpy.array(yVals)
    xVals = xVals*9.81  #acc. due to gravity
    plt.plot(xVals, yVals, 'bo',
               label = 'Measured displacements')
    labelPlot()
    
def fitData(fileName):
    xVals, yVals = getData(fileName)
    xVals = numpy.array(xVals)
    yVals = numpy.array(yVals)
    xVals = xVals*9.81 #get force
    plt.plot(xVals, yVals, 'bo',
               label = 'Measured points')                 
    model = numpy.polyfit(xVals, yVals, 1)
    xVals = xVals + [2]
    yVals = yVals + []
    estYVals = numpy.polyval(model, xVals)
    plt.plot(xVals, estYVals, 'r',
               label = 'Linear fit, r**2 = '
               + str(round(rSquared(yVals, estYVals), 5)))                
    model = numpy.polyfit(xVals, yVals, 2)
    estYVals = numpy.polyval(model, xVals)
    plt.plot(xVals, estYVals, 'g--',
               label = 'Quadratic fit, r**2 = '
               + str(round(rSquared(yVals, estYVals), 5)))
    plt.title('A Linear Spring')
    labelPlot()
    plt.legend(loc = 'best')
    
random.seed(0)

class tempDatum(object):
    def __init__(self, s):
        info = s.split(',')
        self.high = float(info[1])
        self.year = int(info[2][0:4])
    def getHigh(self):
        return self.high
    def getYear(self):
        return self.year
    
def getTempData():
    inFile = open('temperatures.csv')
    data = []
    for l in inFile:
        data.append(tempDatum(l))
    return data
    
def getYearlyMeans(data):
    years = {}
    for d in data:
        try:
            years[d.getYear()].append(d.getHigh())
        except:
            years[d.getYear()] = [d.getHigh()]
    for y in years:
        years[y] = sum(years[y])/len(years[y])
    return years
    
data = getTempData()
years = getYearlyMeans(data)
xVals, yVals = [], []
for e in years:
    xVals.append(e)
    yVals.append(years[e])
plt.plot(xVals, yVals)
plt.xlabel('Year')
plt.ylabel('Mean Daily High (C)')
plt.title('Select U.S. Cities')
# plt.show()

def splitData(xVals, yVals):
    toTrain = random.sample(range(len(xVals)),
                            len(xVals)//2)
    trainX, trainY, testX, testY = [],[],[],[]
    for i in range(len(xVals)):
        if i in toTrain:
            trainX.append(xVals[i])
            trainY.append(yVals[i])
        else:
            testX.append(xVals[i])
            testY.append(yVals[i])
    return trainX, trainY, testX, testY
    
##UNCOVER FOR SECOND DEMO    
numSubsets = 10
dimensions = (1, 2, 3, 4)
rSquares = {}
for d in dimensions:
   rSquares[d] = []
       
for f in range(numSubsets):
   trainX, trainY, testX, testY = splitData(xVals, yVals)
   for d in dimensions:
       model = numpy.polyfit(trainX, trainY, d)
    #    estYVals = numpy.polyval(model, trainX)
       estYVals = numpy.polyval(model, testX)
       rSquares[d].append(rSquared(testY, estYVals))
print('Mean R-squares for test data')
for d in dimensions:
   mean = round(sum(rSquares[d])/len(rSquares[d]), 4)
   sd = round(numpy.std(rSquares[d]), 4)
   print('For dimensionality', d, 'mean =', mean,
         'Std =', sd)
print(rSquares[1])
