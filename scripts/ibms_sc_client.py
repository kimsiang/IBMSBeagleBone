import Adafruit_BBIO.GPIO as GPIO
from spidev import SpiDev
import time
import datetime

spi = SpiDev(1, 0)
spi.mode = 3
spi.max_speed_hz = 1000000

GPIO.setup("P9_11", GPIO.OUT) # PGA1 chip select
GPIO.setup("P9_12", GPIO.OUT) # PGA2 chip select
GPIO.setup("P9_13", GPIO.OUT) # TEMP chip select

GPIO.output("P9_11", GPIO.HIGH)
GPIO.output("P9_12", GPIO.HIGH)
GPIO.output("P9_13", GPIO.HIGH)

time.sleep(0.2)

chip_map = { "pga1": "P9_11", "pga2" : "P9_12", "temp": "P9_13" }

gain_map = {0:'18dB, 7.94', 1:'15dB, 5.63', 2:'12dB, 3.98', 3:'9dB, 2.82', 4:'6dB, 2.00', 5:'3dB, 1.41', 6:'0dB, 1'}

def chip_select(key):
	for k, pin_name in chip_map.iteritems():
		GPIO.output(pin_name, GPIO.HIGH)

	time.sleep(0.1)

	if chip_map.get(key):
		GPIO.output(chip_map[key], GPIO.LOW)

	time.sleep(0.1)

def read_temperature():
	chip_select("temp")
	res = spi.xfer2([0x50, 0x00, 0x00])
	temp = (res[1] << 8 | res[2]) / 128.0
	print "[bb<-temp] %f deg C" % temp
	return temp

def reset_pga(key):
	chip_select(key)
	res = spi.xfer2([0x00, 0x00, 0x01])
	chip_select("none")

def set_gain(key,gain_value):
	chip_select(key)
	print "[bb->%s] set gain = %d" % (key, gain_value)
        res = spi.xfer2([0x3b, 0x00, gain_value << 4])
	chip_select("none")

def read_gain(key):
	#set read bit
	chip_select(key)
        res = spi.xfer2([0x00, 0x00, 0x02])
	chip_select("none")
	time.sleep(0.1)

	#read gain register
	chip_select(key)
        res = spi.xfer2([0x3b, 0x00, 0x00])
	chip_select("none")
	gainReg = res[2] >> 4
	print "[bb<-%s] res = %s, gain = %d (%s)" % (key, res, gainReg, gain_map[gainReg])

	#unset read bit
	chip_select(key)
        res = spi.xfer2([0x00, 0x00, 0x00])
	chip_select("none")

if __name__ == "__main__":

	gain=raw_input('please insert gain (<0 = stop): ')
	gain=int(gain)
	try:
		while (gain >= 0):	
			# this order is important
			reset_pga("pga1")
			set_gain("pga1",gain)
			read_gain("pga1")
			reset_pga("pga2")
			set_gain("pga2",gain)
			read_gain("pga2")
			read_temperature()	
			gain=raw_input('please insert gain (0-6, <0 = stop, -100= T & gain loop): ')
			gain=int(gain) 

	except KeyboardInterrupt:
		GPIO.cleanup()       
		spi.close()

	if (gain == -100):
		for step in range(1000):
			read_gain("pga1")
			read_gain("pga2")
			read_temperature()
			time.sleep(1.0)
