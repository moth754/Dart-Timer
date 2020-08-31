################### imports

#print("Starting imports")

from pyscan import Pyscan
from MFRC630 import MFRC630
import time
import pycom
from machine import SD, I2C, RTC, Pin
from PCA9554 import PCA9554 #for io expander
import _thread
import os
import DS3231 #for RTC
import gc

#imports for pybytes
from _pybytes_config import PybytesConfig
pybytes_config = PybytesConfig().read_config()
from _pybytes import Pybytes
pybytes = Pybytes(pybytes_config)

#setup for watchdog
from machine import WDT
wdt = WDT(timeout=10000)  # enable it with a timeout of 10 seconds
wdt.feed()

#print("imports successful")

################# Functions start

def chiplog(tap): #local recording of taps as csv on sd card
    f = open("/sd/taplog.csv", "a")
    f.write(tap)
    f.write("\n")
    f.close()

def errorlog(error): #local recording of errors as csv on sd card - needs some improvement
    error = str(error)
    time = time_calc()
    errortime = str(time)
    errortext = errortime + "-" + error
    f = open("/sd/errorlog.csv", "a")
    f.write(errortext)
    f.write("\n")
    f.close()

def minute_check(): #get last digit
    time_now = ds.DateTime()
    minute = str(time_now[5])
    if len(minute) > 1:
        minute = minute[1:2]
    return(minute)

def time_calc(): #get time from external RTC
    time_now = ds.DateTime()
    year = str(time_now[0])
    month = str(time_now[1])
    day = str(time_now[2])
    weekday =str(time_now[3])
    hour = str(time_now[4])
    minute = str(time_now[5])
    second = str(time_now[6])
    if len(second) == 1:
        second = "0" + second
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    if len(hour) == 1:
        hour = "0" + hour
    if len(minute) == 1:
        minute = "0" + minute

    #millisecond = str(time_now[7])
    time_stamp = year + "-" + month + "-" + day + " " + hour + ":" + minute + ":" + second
    return(time_stamp)

def chipscan(): #picking up the NFC chips
    # Send REQA for ISO14443A card type
    atqa = nfc.mfrc630_iso14443a_WUPA_REQA(nfc.MFRC630_ISO14443_CMD_REQA)
    if (atqa != 0):
        # A card has been detected, read UID
        uid = bytearray(10)
        uid_len = nfc.mfrc630_iso14443a_select(uid)
        #print("Detected")
        if (uid_len > 0): # A valid UID has been detected, print details
            #print("UID Detected")
            uid_str=map(str,uid)
            uid_str=''.join(uid_str)
            #print(uid_str)
            return(uid_str)
            
        else:
            return("misread")
    else:
        return("no_chip")
    #reset for next time
    nfc.mfrc630_cmd_reset()
    time.sleep(0.01)
    # Re-Initialise the MFRC630 with settings as these got wiped during reset
    nfc.mfrc630_cmd_init()

def mainloop(): #main loop looking for and handling UIDs from chips
    global taps_pending
    taps_pending.append("POWERED ON")
    while True:
        uid_send = chipscan()
        if uid_send == "misread":
            time.sleep(0.01)
            negindication()
        elif uid_send == "no_chip":
            time.sleep(0.01)
            negindication()
        elif uid_send == "115771133000000":
            time.sleep(0.01)
            setexternalrtc()
        else:
            time_send = time_calc()
            #tap = '{' + '"UID":' + uid_send + ', ' + '"TIMESTAMP":' + time_send + '}'
            tap = ("uid"+uid_send+"timestamp"+time_send)
            taps_pending.append(tap)
            chiplog(tap)
            print(tap)
            posindication()
        wdt.feed()

def checkpending(): #checks the unsent list and sends and unsent taps
    global taps_pending
    try:
        pybytes.connect()
        minuteend = minute_check()
        while True:
            if len(taps_pending) > 0 and pybytes.isconnected() == True:
                print("Sending " + taps_pending[0])
                pybytes.send_signal(1,taps_pending[0])
                del taps_pending[0]
                time.sleep(1)
                gc.collect()
            elif pybytes.isconnected() == False and minuteend == "5":
                pybytes.connect()
                time.sleep(300)
                gc.collect()
            elif len(taps_pending) == 0 and pybytes.isconnected() == True:
                pybytes.send_ping_message()
            else:
                time.sleep(0.5)
    except:
        print("Check pending error")
        errorlog("checkpending thread")

def posindication(): #beep and flash for successful scan
    global count
    #buzzer.set()
    buzzer(True)
    led.set()
    time.sleep(0.3)
    #buzzer.reset()
    buzzer(False)
    led.reset()
    count = 0

def negindication(): #periodic flash
    global count
    if count == 50:
        led.set()
        time.sleep(0.2)
        led.reset()
        count = 0
    else:
        count = count + 1

def setexternalrtc():
    buzzer(True)
    led.set()
    time.sleep(0.5)
    buzzer(False)
    time.sleep(0.5)
    buzzer(True)
    time.sleep(0.5)
    buzzer(False)
    
    #start ntp sync
    rtc.ntp_sync("0.uk.pool.ntp.org",update_period=3600)
    time.sleep(5)
    
    if rtc.synced() == True:
        print("Time synced")
        time_now = rtc.now()
        #set date
        ds.Year(time_now[0])
        ds.Month(time_now[1])
        ds.Day(time_now[2])
        #set time
        ds.Hour(time_now[3])
        ds.Minute(time_now[4])
        ds.Second(time_now[5])
        #indicate
        buzzer(True)
        time.sleep(0.5)
        buzzer(False)


    else:
        print("Time not synced")
        errorlog("Time not synced") #and log

    led.reset()

################# Functions end

#setup automatic garbage collection
gc.enable()

#setup SD card
sd = SD()
os.mount(sd, "/sd")
#print("SD card setup")


#setup LEDs and buzzer using Pin
#led = Pin('P2', mode=Pin.OUT) 
buzzer = Pin('P10', mode=Pin.OUT)

#tests LED and buzzer using pin
buzzer(True)
#led(True)
time.sleep(1)
buzzer(False)
#led(False)

#setup LEDs and buzzer using IO expander
led = PCA9554(line=1, direction=0)
#buzzer = PCA9554(line=3, direction=0)

#tests LED and buzzer using IO expander
#buzzer.set()
led.set()
time.sleep(1)
#buzzer.reset()
led.reset()

wdt.feed() #feed timeout

#clock setup
rtc = RTC() #internal RTC module
i2c = I2C(0, pins=('P22','P21')) #setup i2c interface
ds = DS3231.DS3231(i2c) #establish connection to i2c clock

#setup taps pending list and counter
taps_pending = []
#print("variables set")
count = 0

#setup scan
py = Pyscan()
nfc = MFRC630(py)
#print("Scan setup")
nfc.mfrc630_cmd_init() # Initialise the MFRC630 with some settings

wdt.feed() #feed timeout

#thread start
#print("Starting threads")
_thread.start_new_thread(mainloop,())
_thread.start_new_thread(checkpending,())
