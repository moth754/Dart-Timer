# boot.py -- run on boot-up
#RGB LED setup
import pycom
#from network import WLAN
from machine import Pin

pycom.heartbeat(False) #turn off RGB LED - need that pin

p=Pin('P12', mode=Pin.OUT)(True)
#wlan = WLAN()
#wlan.antenna(WLAN.EXT_ANTENNA)