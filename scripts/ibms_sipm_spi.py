import Adafruit_BBIO.GPIO as GPIO
from spidev import SpiDev
import time

# chip select map
# 11: pga1
# 12: pga2
# 13: temp

chip_map = { "pga1": "11", "pga2" : "12", "temp": "13" }
gain_map = { 0:'18dB, 7.94', 1:'15dB, 5.63', 2:'12dB, 3.98', 3:'9dB, 2.82', 4:'6dB, 2.00', 5:'3dB, 1.41', 6:'0dB, 1'}

class IBMSSiPMSPI:
	def __init__(self):
		self.spi = SpiDev(1, 0)
		self.spi.mode = 3
		self.spi.max_speed_hz = 1000000

		for k, pin in chip_map.iteritems():
			GPIO.setup(pin, GPIO.OUT) 
			GPIO.output(pin, GPIO.HIGH) 

	def chip_select(self, key):
		for k, pin in chip_map.iteritems():
			GPIO.output(pin, GPIO.HIGH)

		time.sleep(0.1)

		if chip_map.get(key):
			GPIO.output(chip_map[key], GPIO.LOW)

		time.sleep(0.1)

	def read_temperature(self):
		self.chip_select("temp")
		res = self.spi.xfer2([0x50, 0x00, 0x00])
		temp = (res[1] << 8 | res[2]) / 128.0
		print "[bb<-temp] %f deg C" % temp
		return temp

	def reset_pga(self, key):
		self.chip_select(key)
		res = self.spi.xfer2([0x00, 0x00, 0x01])
		self.chip_select("none")

	def set_gain(self, key,gain_value):
		self.chip_select(key)
		print "[bb->%s] set gain = %d" % (key, gain_value)
	        res = self.spi.xfer2([0x3b, 0x00, gain_value << 4])
		self.chip_select("none")

	def read_gain(self, key):
		#set read bit
		self.chip_select(key)
       		res = self.spi.xfer2([0x00, 0x00, 0x02])
		self.chip_select("none")
		time.sleep(0.1)

		#read gain register
		self.chip_select(key)
	        res = self.spi.xfer2([0x3b, 0x00, 0x00])
		self.chip_select("none")
		gainReg = res[2] >> 4
		print "[bb<-%s] res = %s, gain = %d (%s)" % (key, res, gainReg, gain_map[gainReg])

		#unset read bit
		self.chip_select(key)
	        res = self.spi.xfer2([0x00, 0x00, 0x00])
		self.chip_select("none")

	def clean_up(self):
		GPIO.cleanup()       
		self.spi.close()
