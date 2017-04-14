import zmq
import time
from datetime import date, datetime, tzinfo, timedelta
import zmq
from ibmssipmspi import IBMSSiPMSPI


class IBMSSCServer():

	def __init__(self):
		print 'IBMS Slow Control initiated!'
		self.ibmsspi = IBMSSiPMSPI()

		self.temp=0
		self.pga1=0
		self.pga2=0

	def get_time(self):
		return datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")

	def get_day(self):
        	return datetime.strftime(datetime.now(), "%Y%m%d")

	def publishe(self):
        # define socket numbers for push and publish ports
        lj_port_push = "5556"
        lj_port_pub = "5566"

        # create pull socket for receiving commands from GUI
        context = zmq.Context()
        socket_pull = context.socket(zmq.PULL)
        socket_pull.connect("tcp://localhost:%s" % lj_port_push)
        print "Connected to server with port %s" % lj_port_push

        # initialize poll set
        poller = zmq.Poller()
        poller.register(socket_pull, zmq.POLLIN)

        # initialize labjack publisher
        socket_pub = context.socket(zmq.PUB)
        socket_pub.bind("tcp://*:%s" % lj_port_pub)
        print "Publish info with port %s" % lj_port_pub

   	# work on requests from any client
        while True:
            socks = dict(poller.poll(1000))

            if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
                msg = socket_pull.recv()
                print '{0} Received control command: {1}'.format(
                        self.get_time(), msg)

                # interpret the GUI messages here
                if msg == "read temp":
                    print self.lj.read_temp()
                elif msg == "read gain":
                    print self.lj.read_gain()
                elif msg == "read pga":
                    print self.lj.read_pga()
                elif msg == "read eeprom":
                    print self.lj.read_eeprom()
                elif msg == "read led":
                    print self.lj.read_led()
                elif msg[0:10] == "set eeprom":
                    print self.lj.write_eeprom(int(msg[11:12]), msg[13:29])
                elif msg[0:7] == "set led":
                    print self.lj.set_led(int(msg[8:]))
                elif msg[0:8] == "set gain":
                    print self.lj.set_gain(int(msg[9:]))
                else:
                    print "Unknown command! Try again."

            else:
                self.temp = self.lj.read_temp()
                self.gain = self.lj.read_gain()
                eeprom1 = self.lj.read_eeprom(1)
                eeprom2 = self.lj.read_eeprom(2)
                eeprom3 = self.lj.read_eeprom(3)
                eeprom4 = self.lj.read_eeprom(4)
                eeprom5 = self.lj.read_eeprom(5)
                eeprom6 = self.lj.read_eeprom(6)
                eeprom7 = self.lj.read_eeprom(7)
                eeprom8 = self.lj.read_eeprom(8)
                self.serial = self.lj.read_serial()
                self.led_no = self.lj.read_led()

                lj_data = {
                        'time': self.get_time(),
                        'temp': self.temp,
                        'gain': self.gain,
                        'eeprom1': eeprom1,
                        'eeprom2': eeprom2,
                        'eeprom3': eeprom3,
                        'eeprom4': eeprom4,
                        'eeprom5': eeprom5,
                        'eeprom6': eeprom6,
                        'eeprom7': eeprom7,
                        'eeprom8': eeprom8,
                        'serial': self.serial,
                        'ledno': self.led_no
                        }

                socket_pub.send_json(lj_data)

if __name__ == "__main__":

	gain=raw_input('please insert gain (<0 = stop): ')
	gain=int(gain)
	try:
		while (gain >= 0):	
			# this order is important
			spi.reset_pga("pga1")
			spi.set_gain("pga1",gain)
			spi.read_gain("pga1")
			spi.reset_pga("pga2")
			spi.set_gain("pga2",gain)
			spi.read_gain("pga2")
			spi.read_temperature()	
			gain=raw_input('please insert gain (0-6, <0 = stop, -100= T & gain loop): ')
			gain=int(gain) 

	except KeyboardInterrupt:
		spi.clean_up()
