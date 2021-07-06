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


def makeHist(data, title, xlabel, ylabel, bins = 20):
    plt.hist(data, bins = bins)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

def getHighs():
    inFile = open('temperatures.csv')
    population = []
    for l in inFile:
        try:
            tempC = float(l.split(',')[1])
            population.append(tempC)
        except:
            continue
    return population

def getMeansAndSDs(population, sample, verbose = False):
    popMean = sum(population)/len(population)
    sampleMean = sum(sample)/len(sample)
    if verbose:
        makeHist(population,
                 'Daily High 1961-2015, Population\n' +\
                 '(mean = '  + str(round(popMean, 2)) + ')',
                 'Degrees C', 'Number Days')
        plt.figure()
        makeHist(sample, 'Daily High 1961-2015, Sample\n' +\
                 '(mean = ' + str(round(sampleMean, 2)) + ')',
                 'Degrees C', 'Number Days')   
        print('Population mean =', popMean)
        print('Standard deviation of population =',
              numpy.std(population))
        print('Sample mean =', sampleMean)
        print('Standard deviation of sample =',
              numpy.std(sample))
    return popMean, sampleMean,\
           numpy.std(population), numpy.std(sample)

# random.seed(0)         
# population = getHighs()
# sample = random.sample(population, 100)
# getMeansAndSDs(population, sample, True)

# random.seed(0) 
# population = getHighs()
# sampleSize = 200
# numSamples = 1000
# sampleMeans = []
# for i in range(numSamples):
#    sample = random.sample(population, sampleSize)
#    popMean, sampleMean, popSD, sampleSD =\
#       getMeansAndSDs(population, sample, verbose = False)
#    sampleMeans.append(sampleMean)
# print('Mean of sample Means =',
#      round(sum(sampleMeans)/len(sampleMeans), 3))
# print('Standard deviation of sample means =',
#      round(numpy.std(sampleMeans), 3))
# makeHist(sampleMeans, 'Means of Samples', 'Mean', 'Frequency')
# plt.axvline(x = popMean, color = 'r')
# plt.show()


def showErrorBars(population, sizes, numTrials):
    xVals = []
    sizeMeans, sizeSDs = [], []
    for sampleSize in sizes:
        xVals.append(sampleSize)
        trialMeans = []
        for t in range(numTrials):
            sample = random.sample(population, sampleSize)
            popMean, sampleMean, popSD, sampleSD =\
               getMeansAndSDs(population, sample)
            trialMeans.append(sampleMean)
        sizeMeans.append(sum(trialMeans)/len(trialMeans))
        sizeSDs.append(numpy.std(trialMeans))
    print(sizeSDs)
    plt.errorbar(xVals, sizeMeans,
                   yerr = 1.96*numpy.array(sizeSDs), fmt = 'o',
                   label = '95% Confidence Interval')
    plt.title('Mean Temperature ('
                + str(numTrials) + ' trials)')
    plt.xlabel('Sample Size')
    plt.ylabel('Mean')
    plt.axhline(y = popMean, color ='r', label = 'Population Mean')
    plt.xlim(0, sizes[-1] + 10)
    plt.legend()

# random.seed(0)
# population = getHighs()   
# showErrorBars(population,
#              (50, 100, 200, 300, 400, 500, 600), 100)
# plt.show()

def sem(popSD, sampleSize):
    return popSD/sampleSize**0.5

# sampleSizes = (25, 50, 100, 200, 300, 400, 500, 600)
# numTrials = 50
# population = getHighs()
# popSD = numpy.std(population)
# sems = []
# sampleSDs = []
# for size in sampleSizes:
#    sems.append(sem(popSD, size))
#    means = []
#    for t in range(numTrials):
#        sample = random.sample(population, size)
#        means.append(sum(sample)/len(sample))
#    sampleSDs.append(numpy.std(means))
# plt.plot(sampleSizes, sampleSDs,
#           label = 'Std of ' + str(numTrials) + ' means')
# plt.plot(sampleSizes, sems, 'r--', label = 'SEM')
# plt.xlabel('Sample Size')
# plt.ylabel('Std and SEM')
# plt.title('SD for ' + str(numTrials) + ' Means and SEM')
# plt.legend()
# plt.show()

def getDiffs(population, sampleSizes):
    popStd = numpy.std(population)
    diffsFracs = []
    for sampleSize in sampleSizes:
        diffs = []
        for t in range(100):
            sample = random.sample(population, sampleSize)
            diffs.append(abs(popStd - numpy.std(sample)))
        diffMean = sum(diffs)/len(diffs)
        diffsFracs.append(diffMean/popStd)
    return numpy.array(diffsFracs)*100
    
def plotDiffs(sampleSizes, diffs, title, label, color = 'b'):
    plt.plot(sampleSizes, diffs, label = label,
               color = color)
    plt.xlabel('Sample Size')
    plt.ylabel('% Difference in SD')
    plt.title(title)
    plt.legend()

# sampleSizes = range(20, 600, 1)
# diffs = getDiffs(getHighs(), sampleSizes)
# plotDiffs(sampleSizes, diffs,
#          'Sample SD vs Population SD, Temperatures',
#          label = 'High temps')


def plotDistributions():
    uniform, normal, exp = [], [], []
    for i in range(100000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    makeHist(uniform, 'Uniform', 'Value', 'Frequency')
    plt.figure()
    makeHist(normal, 'Gaussian', 'Value', 'Frequency')
    plt.figure()
    makeHist(exp, 'Exponential', 'Value', 'Frequency')
    plt.show()

# plotDistributions()


def compareDists():
    uniform, normal, exp = [], [], []
    for i in range(100000):
        uniform.append(random.random())
        normal.append(random.gauss(0, 1))
        exp.append(random.expovariate(0.5))
    sampleSizes = range(20, 600, 1)
    udiffs = getDiffs(uniform, sampleSizes)
    ndiffs = getDiffs(normal, sampleSizes)
    ediffs = getDiffs(exp, sampleSizes)
    plotDiffs(sampleSizes, udiffs,
              'Sample SD vs Population SD',
              'Uniform population', 'm')
    plotDiffs(sampleSizes, ndiffs,
              'Sample SD vs Population SD',
              'Normal population', 'b')
    plotDiffs(sampleSizes, ediffs,
              'Sample SD vs Population SD',
              'Exponential population', 'r')

# compareDists()  
# plt.show()

#
# popSizes = (10000, 100000, 1000000)
# colors = ('g', 'b', 'r')
# sampleSizes = range(20, 600, 1)
# for n in range(len(popSizes)):
#    population = []
#    for i in range(popSizes[n]):
#        population.append(random.expovariate(0.5))
#    ediffs = getDiffs(population, sampleSizes)
#    plotDiffs(sampleSizes, ediffs,
#              'Sample SD vs Population SD, Uniform',
#              'Population size = ' + str(popSizes[n]),
#              colors[n])
# plt.show()

temps = getHighs()
popMean = sum(temps)/len(temps)
sampleSize = 200
numTrials = 10000

random.seed(0)
numBad = 0
for t in range(numTrials):
   posStartingPts = range(0, len(temps) - sampleSize)
   start = random.choice(posStartingPts)
   sample = temps[start:start+sampleSize]
   sampleMean = sum(sample)/sampleSize
   se = numpy.std(sample)/sampleSize**0.5
   if abs(popMean - sampleMean) > 1.96*se:
       numBad += 1
print('Fraction outside 95% confidence interval =',
     numBad/numTrials)
#
random.seed(0)      
numBad = 0
for t in range(numTrials):
   sample = random.sample(temps, sampleSize)
   sampleMean = sum(sample)/sampleSize
   se = numpy.std(sample)/sampleSize**0.5
   if abs(popMean - sampleMean) > 1.96*se:
       numBad += 1
print('Fraction outside 95% confidence interval =',
     numBad/numTrials)