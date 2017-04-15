# ibms_sc_client.py

import zmq
import time
import sys
from datetime import date, datetime, tzinfo, timedelta
import random
from multiprocessing import Process
import json

context = zmq.Context()
print("Connecting IBMS SC Server")
socket = context.socket(zmq.PUSH)
socket.bind("tcp://*:5556")
print("Sending request")

socket.send ("set pga1 3")
socket.send ("set pga2 3")
while True:
	socket.send ("read temp")
#	socket.send ("read pga1")
	time.sleep(1)

context = zmq.Context()
socket_sub = context.socket(zmq.SUB)

socket_sub.connect("tcp://localhost:%s" % 5566)

socket_sub.setsockopt(zmq.SUBSCRIBE, "")


#while True:
#	json_data = socket_sub.recv_json()
#	print('{0}'.format(json_data))
#	#print json_data['temp']
