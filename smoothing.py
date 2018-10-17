import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
import peakutils.peak
from math import factorial

def savitzky_golay(y, window_size, order, deriv=0, rate=1):

   window_size = np.abs(np.int(window_size))
   order = np.abs(np.int(order))

   if window_size % 2 != 1 or window_size < 1:
       raise TypeError("window_size size must be a positive odd number")
   if window_size < order + 2:
       raise TypeError("window_size is too small for the polynomials order")
   order_range = range(order+1)
   half_window = (window_size -1) // 2
   # precompute coefficients
   b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
   m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
   # pad the signal at the extremes with
   # values taken from the signal itself
   firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
   lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
   y = np.concatenate((firstvals, y, lastvals))
   return np.convolve( m[::-1], y, mode='valid')


def isconsecutive(A,i,j,min,max):
    if max - min != j - i:
        return False
    visited = [None] * (j - i + 1)
    k = i
    while k <= j:
        if visited[A[k] - min]:
            return False
        visited[A[k] - min] = True
        k = k+1
    return True


def findMaxSubArray(A):
    len=1
    start=0
    end=0
    i = 0
    while i <A.__len__()-1:
        min_val=A[i]
        max_val = A[i]

        j=i+1
        while j<A.__len__():
            min_val = min(min_val,A[j])
            max_val = max(max_val,A[j])

            if isconsecutive(A,i,j,min_val,max_val):
                if len < max_val -min_val -1:
                    len = max_val - min_val + 1
                    start = i
                    end = j

            j = j+1

        i=i+1

    i=start
    ret= []
    while i<=end :
        ret.append(A[i])
        i = i+1
    return ret


path = "keck_vels_binned/"

choice = "y"

while choice == "y":
    print("Enter filename:")
    filename = input()
    # filename = "HD221354_sample.vels"
    print("\nEnter window size for curve smoothing function\nPress Enter for accepting default(21):")
    window_size = input()

    if window_size == "":
        window_size = 21

    # open the data file and initialize arrays
    f = open(path + filename)
    time = []
    velocities = []

    # read from file, the radial velocity values and timestamps
    line = f.readline()
    min = float(line.split()[0].strip())

    while line != "":
        tokens = line.split()
        time.append(float(tokens[0].strip())-min)
        velocities.append(float(tokens[1].strip()))
        line = f.readline()
    f.close()

    # get the largest subset of consecutive timestamps
    # New_time = findMaxSubArray(time)
    # print(New_time)

    # apply linear interpolation
    f = interp1d(time, velocities)
    length = time.__len__()

    # calculate new timespace for interpolated data
    t_new = np.linspace(time[0], time[length-1], length*5)

    # perform a curve fitting function
    yhat = savitzky_golay(f(t_new), window_size, 3)


    # plot data points against timestamps
    plt.plot(time, velocities, 'x', label="data point")

    # plt.plot(t_new, f(t_new), '--', label="interpolation", color='green')

    # plot curve fitted values
    line2d = plt.plot(t_new,yhat, color='red', label="smoothing curve")
    plt.title(filename)
    plt.xlabel("days")
    plt.ylabel("velocity")
    plt.legend()

    # find peaks in the plotted graph
    peaks = peakutils.peak.indexes(np.array(yhat),thres=1.0/max(yhat), min_dist=1)


    xvalues = line2d[0].get_xdata()
    yvalues = line2d[0].get_ydata()

    period = 0
    i =1

    # calculate the max period between two peaks in the graph
    while i < peaks.__len__():
        temp = xvalues[np.where(yvalues == yvalues[peaks[i]])] - xvalues[np.where(yvalues == yvalues[peaks[i-1]])]
        if temp > period:
            period = temp
        i = i + 1

    print("period estimate is: ", period)
    print("\nPass a value greater than this period to the next program to confirm the orbital period.\n")
    plt.show()

    print("Run again?(y/n):")
    choice = input()
