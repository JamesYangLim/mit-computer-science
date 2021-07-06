# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 11:45:20 2016

@author: johnguttag

Modified: egrimson
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
    
# plotData('springData.txt')
# plt.show()

def fitData(fileName):
    xVals, yVals = getData(fileName)
    xVals = numpy.array(xVals)
    yVals = numpy.array(yVals)
    xVals = xVals*9.81 #get force
    plt.plot(xVals, yVals, 'bo',
               label = 'Measured points')
    labelPlot()                 
    a,b = numpy.polyfit(xVals, yVals, 1)
    estYVals = a*numpy.array(xVals) + b
    print('a =', a, 'b =', b)
    plt.plot(xVals, estYVals, 'r',
               label = 'Linear fit, k = '
               + str(round(1/a, 5)))
    plt.legend(loc = 'best')
    
# fitData('springData.txt')
# plt.show()

   
def fitData1(fileName):
    xVals, yVals = getData(fileName)
    xVals = numpy.array(xVals)
    yVals = numpy.array(yVals)
    xVals = xVals*9.81 #get force
    plt.plot(xVals, yVals, 'bo',
               label = 'Measured points')
    labelPlot()                 
    model = numpy.polyfit(xVals, yVals, 1)
    estYVals = numpy.polyval(model, xVals)
    plt.plot(xVals, estYVals, 'r',
               label = 'Linear fit, k = '
               + str(round(1/model[0], 5)))
    plt.legend(loc = 'best')

# fitData1('springData.txt')
# plt.show()

#Demonstration using mystery data

# xVals, yVals = getData('mysteryData.txt')
# plt.plot(xVals, yVals, 'o', label = 'Data Points')
# plt.title('Mystery Data')

# #Try linear model
# model1 = numpy.polyfit(xVals, yVals, 1)
# plt.plot(xVals, numpy.polyval(model1, xVals),
#           label = 'Linear Model')

# #Try a quadratic model
# model2 = numpy.polyfit(xVals, yVals, 2)
# plt.plot(xVals, numpy.polyval(model2, xVals),
#           'r--', label = 'Quadratic Model')
# plt.legend()

# plt.show()


##Compare models
def aveMeanSquareError(data, predicted):
    error = 0.0
    for i in range(len(data)):
        error += (data[i] - predicted[i])**2
    return error/len(data)

#code to compare fits for mystery data
# estYVals = numpy.polyval(model1, xVals)  
# print('Ave. mean square error for linear model =',
#      aveMeanSquareError(yVals, estYVals))
# estYVals = numpy.polyval(model2, xVals)
# print('Ave. mean square error for quadratic model =',
#      aveMeanSquareError(yVals, estYVals))

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

#code for testing goodness of fit to parabolic data

xVals, yVals = getData('mysteryData.txt')
degrees = (1, 2)
models = genFits(xVals, yVals, degrees)
testFits(models, degrees, xVals, yVals, 'Mystery Data')
plt.show()

##Compare higher-order fits
degrees = (2, 4, 8, 16)
models = genFits(xVals, yVals, degrees)
testFits(models, degrees, xVals, yVals, 'Mystery Data')
plt.show()

def genNoisyParabolicData(a, b, c, xVals, fName):
    yVals = []
    for x in xVals:
        theoreticalVal = a*x**2 + b*x + c
        yVals.append(theoreticalVal\
        + random.gauss(0, 35))
    f = open(fName,'w')
    f.write('x        y\n')
    for i in range(len(yVals)):
        f.write(str(yVals[i]) + ' ' + str(xVals[i]) + '\n')
    f.close()
    
