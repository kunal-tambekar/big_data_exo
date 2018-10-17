import numpy as np
import sys
import string
from numpy import arange, random, ones
import matplotlib.pylab as mpl
import operator


''' Function to get the equally spaced intervals for iteration
    start: Max Value
    end: Min value
    multiplier: value of intervals 
        1 => 0.1 (No. of iterations = Max value)
        10 => 0.01 (No. of iterations = Max value X10)
        100 => 0.001 (No. of iterations = Max value X100)
        1/K => 1 (one iteration)
'''
def getValuesForIterations(start, end, multiplier):
    return  np.linspace(end, start, num=start*multiplier)


'''Function to calculate fairly close enough value of K '''
def estimateBestGuessValueForK(guessK,guessP,time,vels,verr):
    print("Inside estimateBestGuessValueForK() \n",
          "Initial Guess of K = ",guessK,"\n"
          " Initial Max Guess of P = ",guessP,"\n")

    minXsqr = []
    ''' Initializing variables for calculations and iterations'''

    ''' Generating array of guess/test values for iterating to get the best time period : 
        Iterating over : initial guess (guessP) and 1.5 days [lower value = 1.5 days because 1 observation is taken
        per day for most of the datasets so planets and also exoplanets with time period close to 1 day are rare ]'''
    pArr = getValuesForIterations(guessP, 1.5, 10)
    ''' Variable to enforce break condition when Chi square value starts increasing again
        This indicates that a good esimated value of K is found '''
    prevChi = sys.maxsize
    ''' FOR LOOP: iterating over for specified range to find good estimate value of K '''
    for x in getValuesForIterations(guessK, 0.00000001, 10):
        #Array to store the values of Chi square to get the best value of K for least value of Chi square
        Xsqr = []
        for y in pArr:
            # Variable to store value of Chi square sum
            chi2Sum = 0
            for t, vobs, err in zip(time, vels, verr):
                if not y == 0:
                    vexp = x * np.sin(2 * np.pi * t / y)
                    if not err == 0:
                        chi2Sum += ((vobs - vexp) ** 2) / err ** 2 #calculating and adding Chi square value
                    else:
                        chi2Sum += ((vobs - vexp) ** 2) # handling if error (denominator) is ZERO
            Xsqr.append(chi2Sum)
        minXsqr.append((min(Xsqr), pArr[Xsqr.index(min(Xsqr))], x))
        print("MIN", min(Xsqr), " ", pArr[Xsqr.index(min(Xsqr))], " ", x)
        '''CHECKING: if lowest value of Chi square has been found '''
        if(prevChi<min(Xsqr)):
            break
        prevChi=min(Xsqr)
    # FOUND the best Estimate of K :- print and return it to calling function
    bestKEstimate = min(minXsqr, key=operator.itemgetter(0)).__getitem__(2)

    print("In estimateBestGuessValueForK() Min Chi^2 values = ", min(minXsqr, key=operator.itemgetter(0)))
    print("bestKEstimate K = ",bestKEstimate)
    return bestKEstimate

def calculateFinerValueOfK(bestKEst,guessP,time,vels,verr):
    print("Inside estimateBestGuessValueForK() ",
          "Best Estimate of K = ", bestKEst,
          " Initial Max Guess of P = ", guessP)

    minXsqr = []
    pArr = getValuesForIterations(guessP, 1.5, 10)
    prevChi = sys.maxsize
    for x in getValuesForIterations(bestKEst*1.10, bestKEst*0.995, 100):
        Xsqr = []
        for y in pArr:
            chi2Sum = 0
            for t, vobs, err in zip(time, vels, verr):
                if not y == 0:
                    vexp = x * np.sin(2 * np.pi * t / y)
                    if not err == 0:
                        chi2Sum += ((vobs - vexp) ** 2) / err ** 2
                    else:
                        chi2Sum += ((vobs - vexp) ** 2)
            Xsqr.append(chi2Sum)
        minXsqr.append((min(Xsqr), pArr[Xsqr.index(min(Xsqr))], x))
        print("MIN", min(Xsqr), " ", pArr[Xsqr.index(min(Xsqr))], " ", x)
        if (prevChi < min(Xsqr)):
            break
        prevChi = min(Xsqr)

    bestK = min(minXsqr, key=operator.itemgetter(0)).__getitem__(2)

    print("In calculateFinerValueOfK() Min Chi^2 Entry = ", min(minXsqr, key=operator.itemgetter(0)))
    print("bestK found to be K = ", bestK)
    return bestK

def estimateBestTimePeriod(bestK,guessP,time,vels,verr,starName):
    print("Inside estimateBestTimePeriod() ",
          "Best value of K = ", bestK,
          " Initial Max Guess of P = ", guessP)

    minXsqr = []
    pArr = getValuesForIterations(guessP, 1.5, 1000)
    Xsqr = []
    for y in pArr:
        chi2Sum = 0
        for t, vobs, err in zip(time, vels, verr):
            if not y == 0:
                vexp = bestK * np.sin(2 * np.pi * t / y)
                if not err == 0:
                    chi2Sum += ((vobs - vexp) ** 2) / err ** 2
                else:
                    chi2Sum += ((vobs - vexp) ** 2)
        Xsqr.append(chi2Sum)
        print("Reached ",y, " out of ",guessP)
    minXsqr.append((min(Xsqr), pArr[Xsqr.index(min(Xsqr))], bestK))

    bestP = min(minXsqr, key=operator.itemgetter(0)).__getitem__(1)

    print("In estimateBestTimePeriod() Min Chi^2 Entry = ", min(minXsqr, key=operator.itemgetter(0)))
    print("Time Period of possible exoplanet = ", bestP ," days")

    # Let's see the results...
    mpl.ylabel("Chi sqr")
    mpl.xlabel("P")
    mpl.plot(pArr, Xsqr, 'r-')
    mpl.figtext(0.1, 0.15,starName,
                backgroundcolor='darkkhaki', color='black', weight='roman',
                size='small')
    mpl.figtext(0.05, 0.10, str('P='+str(bestP)+" days"),
                backgroundcolor='royalblue',
                color='black', weight='roman', size='x-small')

    mpl.savefig(str(starName+".png"))
    mpl.show()
    return bestP



'''########## STARTING POINT OF PROGRAM ##########
Setting initial guess to be some value based on looking at the curve '''
starName = raw_input("Enter the name of the star system you want to search eg. HIP74995 >>> Star name:")
P = int(raw_input("Enter the best guess for the time period : "))
'''#######################################'''

inputFileName = str("opdir_binned/"+starName+".csv")
outputImageName= str(starName+".png")

print(inputFileName)
print(outputImageName)

''' Loading data from the csv files we created from the binned data recorded from the observatory '''
data = np.genfromtxt(inputFileName, delimiter=',')

''' Array in which timestamps are stored '''
time = data[:, ][:, 0]

''' Adjusting time to start it from 0 , where 0 is day1 of observation '''
time = time - time[0]

''' Array containing radial velocities that were recorded'''
vels = data[:, ][:, 1]

''' Array containing the error value for the radial velocity values recorded '''
verr = data[:, ][:, 2]

''' Not using this to reduce additional calculations : same results were seen even if V0 is set to 0 since,
        V0 = abs(max(abs(vels))-(abs(max(vels))+abs(min(vels)))/2)
    and
        K = max(abs(vels)) - V0
    Later, during calculations we end up adding the V0 value again while calculating the Expected Velocity for Chi^2
    with FORMULA 
        >> vexp = x*np.sin(2*np.pi*t/y) + V0 

Therefore,
    Making initial guess for the Semi amplitude value as Max value of Radial velocity in any direction +ve or -ve '''
K = max(abs(vels))


print('Starting...\n K = ', K, '\n P = ', P)

bestKest = estimateBestGuessValueForK(guessK=K,guessP=P,time=time,vels=vels,verr=verr)
bestK = calculateFinerValueOfK(bestKEst=bestKest,guessP=P,time=time,vels=vels,verr=verr)
mostProbableP= estimateBestTimePeriod(bestK=bestK,guessP=P,time=time,vels=vels,verr=verr,starName=starName)


