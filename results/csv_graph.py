import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import sys

'''
def read_datafile(file_name):
    # the skiprows keyword is for heading, but I don't know if trailing lines
    # can be specified
    data = np.loadtxt(file_name, delimiter=',', skiprows=10)
    return data
'''
#data = read_datafile('e:\dir1\datafile.csv')
data = np.genfromtxt('./'+sys.argv[1], delimiter=' ', skip_header=10, skip_footer=25, names=['Time', 'Window', 'ACK'])


fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.plot(data['ACK'], data['Window'], color='r', label='the data')
ax1.set_title("Window Size vs ACK Number")
ax1.set_xlabel('ACK Number')
ax1.set_ylabel('Window Size')

#ax1.plot(x,y, c='r', label='the data')

leg = ax1.legend()

plt.show()
