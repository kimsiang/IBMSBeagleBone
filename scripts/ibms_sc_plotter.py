# ibms_sc_plotter.py

import zmq
import time
import sys
from datetime import date, datetime, tzinfo, timedelta
import random
from multiprocessing import Process
import json
import numpy as np
import matplotlib.pyplot as plt

context = zmq.Context()
socket_sub = context.socket(zmq.SUB)
socket_sub.connect("tcp://localhost:%s" % 5566)
socket_sub.setsockopt(zmq.SUBSCRIBE, "")

json_data = socket_sub.recv_json()
time = json_data['time']
temp = json_data['temp']
plt.plot(time, temp)
plt.show()
