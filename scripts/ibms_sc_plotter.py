# ibms_sc_client.py

import zmq
import time
import sys
from datetime import date, datetime, tzinfo, timedelta
import random
from multiprocessing import Process
import json
import numpy as np
import matplotlib.pyplot as plt


string = './data/IBMSSC_{}.log'
filename = string.format(self.get_day())

readout = np.loadtxt(filename, usecols=(1, 2, 3, 4),
		converters={1: strpdate2num('%H:%M:%S')},
		unpack=True)
time, temp, gain1, gain2 = readout
plt.figure(1)
plt.plot(time[-5000:], temp[-5000:], lw=2)
plt.title("Temperature")
plt.ylabel("T [C]")
plt.xlabel("time [hh:mm]")
plt.draw()
#xfmt = mdates.DateFormatter('%H:%M')
#self.axes3.xaxis.set_major_formatter(xfmt)
#self.axes3.grid(True, linewidth=1)
#self.canvas3.draw()
