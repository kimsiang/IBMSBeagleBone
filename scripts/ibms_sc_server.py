# ibms_sc_server.py

import zmq
import time
import sys
from datetime import date, datetime, tzinfo, timedelta
import random
from multiprocessing import Process
from ibms_sipm_spi import IBMSSiPMSPI
import json
import procname

class IBMSSCServer():

	def __init__(self):
		print 'IBMS Slow Control initiated!'
		self.ibmsspi = IBMSSiPMSPI()

		self.temp=0
		self.gain1=0
		self.gain2=0

	def get_time(self):
		return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

	def get_day(self):
        	return datetime.strftime(datetime.now(), "%Y%m%d")

	def publisher(self):
  
		# define socket numbers for push and publish ports
	        bb_port_push = "5556"
       		bb_port_pub = "5566"

	        # create pull socket for receiving commands from GUI
	        context = zmq.Context()
	        socket_pull = context.socket(zmq.PULL)
	        socket_pull.connect("tcp://localhost:%s" % bb_port_push)
	        print "Connected to server with port %s" % bb_port_push
	
	        # initialize poll set
	        poller = zmq.Poller()
	        poller.register(socket_pull, zmq.POLLIN)
	
	        # initialize labjack publisher
	        socket_pub = context.socket(zmq.PUB)
	        socket_pub.bind("tcp://*:%s" % bb_port_pub)
	        print "Publish info with port %s" % bb_port_pub
	
	   	# work on requests from any client
	        while True:
	            socks = dict(poller.poll(1000))
	
	            if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
	                msg = socket_pull.recv()
	                print '{0} Received control command: {1}'.format(
	                        self.get_time(), msg)
	
	                # interpret the GUI messages here
	                if msg == "read temp":
	                    print self.ibmsspi.read_temp()
	                elif msg == "read pga1":
	                    print self.ibmsspi.read_gain("pga1")
	                elif msg == "read pga2":
	                    print self.ibmsspi.read_gain("pga2")
	                elif msg[0:9] == "set gain1":
	                    print self.ibmsspi.set_gain("pga1", int(msg[9:]))
	                elif msg[0:9] == "set gain2":
	                    print self.ibmsspi.set_gain("pga2", int(msg[9:]))
	                else:
	                    print "Unknown command! Try again."
	
	            else:
	                self.temp = self.ibmsspi.read_temp()
        	        #self.gain = self.ibmsspi.read_gain("pga1")
	                #self.gain = self.ibmsspi.read_gain("pga2")
	
	                bb_data = {
	                        'time': self.get_time(),
	                        'temp': self.temp,
	                        'gain1': self.gain1,
	                        'gain2': self.gain2,
	                        }

        	        socket_pub.send_json(bb_data)


# main function
def main():
	server = IBMSSCServer()
	procname.setprocname("ibmsServer")
	Process(target=server.publisher, args=()).start()

if __name__ == '__main__':
	main()
