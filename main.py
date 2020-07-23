################### imports

print("Starting imports")

from pyscan import Pyscan
from MFRC630 import MFRC630
import time
import pycom
from machine import SD, Pin, I2C
import _thread
import os
#from mqtt import MQTTClient
import network
#import _pybytes as pybytes
import pcf8563

print("imports successful")

################# Functions start

def chiplog(tap):
    f = open("/sd/taplog.csv", "a")
    f.write(tap)
    f.write("\n")
    f.close()

def errorlog(error):
    error = str(error)
    time = rtc.datetime()
    errortime = str(time)
    errortext = errortime + "-" + error
    f = open("/sd/errorlog.csv", "a")
    f.write(errortext)
    f.write("\n")
    f.close()


def time_calc():
    time_now = rtc.datetime()
    #year = str(time_now[0])
    #month = str(time_now[1])
    #day = str(time_now[2])
    #hour = str(time_now[4])
    #minute = str(time_now[5])
    #second = str(time_now[6])
    #millisecond = str(time_now[7])
    time_stamp = str(time_now[0]) + "-" + str(time_now[1]) + "-" + str(time_now[2]) + " " + str(time_now[4]) + ":" + str(time_now[5]) + ":" + str(time_now[6]) + "." + str(time_now[7])
    return(time_stamp)

def chipscan():
    global counter
    # Send REQA for ISO14443A card type
    atqa = nfc.mfrc630_iso14443a_WUPA_REQA(nfc.MFRC630_ISO14443_CMD_REQA)
    if (atqa != 0):
        # A card has been detected, read UID
        uid = bytearray(10)
        uid_len = nfc.mfrc630_iso14443a_select(uid)
        #print("Detected")
        if (uid_len > 0):
            # A valid UID has been detected, print details
            counter += 1
            #print("%d\tUID [%d]: %s" % (counter, uid_len, nfc.format_block(uid, uid_len)))
            #print("UID Detected")
            # If we're not trying to authenticate, show green when a UID > 0 has been detected
            pycom.rgbled(RGB_GREEN)
            uid_str=map(str,uid)
            uid_str=''.join(uid_str)
            #print(uid_str)
            #print(rtc.now())
            return(uid_str)
            
        else:
            pycom.rgbled(RGB_RED)
            return("misread")
    else:
        pycom.rgbled(RGB_BLUE)
        return("no_chip")
    #reset for next time
    nfc.mfrc630_cmd_reset()
    time.sleep(0.01)
    # Re-Initialise the MFRC630 with settings as these got wiped during reset
    nfc.mfrc630_cmd_init()

def mainloop():
    while True:
        global taps_pending
        uid_send = chipscan()
        if uid_send == "misread":
            time.sleep(0.01)
        elif uid_send == "no_chip":
            time.sleep(0.01)
        else:
            time_send = time_calc()
            #tap = '"{' + '"uid" : "' + uid_send + '" , ' + '"timestamp" : ' + '"' + time_send + '"}"'
            tap = ("uid"+uid_send+"timestamp"+time_send)
            taps_pending.append(tap)
            chiplog(tap)
            print(tap)

def checkpending():
    global taps_pending
    while True:
        if len(taps_pending) > 0:
            if pybytes.is_connected() == True:
                print("Sending " + taps_pending[0])
                pybytes.send_signal(1,taps_pending[0])
                del taps_pending[0]
            else:
                time.sleep(0.5)
        else:
            time.sleep(0.5)



################# Functions end

#setup SD card
sd = SD()
os.mount(sd, "/sd")
print("SD card setup")

#setup rtc
#i2c = I2C(0, I2C.MASTER) #intiate I2C bus as master
rtc = pcf8563.PCF8563(i2c)


#print("Getting time from NTP")
#time.sleep(5)
#rtc = RTC()
#rtc.ntp_sync("0.uk.pool.ntp.org",update_period=3600)
#time.sleep(2)
#print(rtc.synced())

#if rtc.synced() == True:
#    print("Time synced")
#    #and log
#else:
#    print("Time not synced - using default 1.1.00")
#    rtc.init((2000, 1, 1, 0, 0, 0, 0, 0))
#    errorlog("Time not synced - using default 1.1.00")
#    #and log

print(rtc.now())


#setup taps pending list and counter
taps_pending = []
counter = 0
print("variables set")

#setup scan
py = Pyscan()
nfc = MFRC630(py)
print("Scan setup")
nfc.mfrc630_cmd_init() # Initialise the MFRC630 with some settings

# Make sure heartbeat is disabled before setting RGB LED
pycom.heartbeat(False)

#setup LED
RGB_BRIGHTNESS = 0x8

RGB_RED = (RGB_BRIGHTNESS << 16)
RGB_GREEN = (RGB_BRIGHTNESS << 8)
RGB_BLUE = (RGB_BRIGHTNESS)

print("LED setup")

#thread start
print("Starting threads")
_thread.start_new_thread(mainloop,())
_thread.start_new_thread(checkpending,())