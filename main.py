################### imports

#print("Starting imports")

from pyscan import Pyscan
from MFRC630 import MFRC630
import time
import pycom
from machine import SD, Pin, I2C, RTC
import _thread
import os 

#print("imports successful")

################# Functions start

def chiplog(tap): #local recording of taps as csv on sd card
    f = open("/sd/taplog.csv", "a")
    f.write(tap)
    f.write("\n")
    f.close()

def errorlog(error): #local recording of errors as csv on sd card - needs some improvement
    error = str(error)
    time = rtc.now()
    errortime = str(time)
    errortext = errortime + "-" + error
    f = open("/sd/errorlog.csv", "a")
    f.write(errortext)
    f.write("\n")
    f.close()


def time_calc(): #due to change with new RTC component coming in
    time_now = rtc.now()
    #year = str(time_now[0])
    #month = str(time_now[1])
    #day = str(time_now[2])
    #hour = str(time_now[4])
    #minute = str(time_now[5])
    #second = str(time_now[6])
    #millisecond = str(time_now[7])
    time_stamp = str(time_now[0]) + "-" + str(time_now[1]) + "-" + str(time_now[2]) + " " + str(time_now[3]) + ":" + str(time_now[4]) + ":" + str(time_now[5]) + "." + str(time_now[6])
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
    while True:
        global taps_pending
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
            #tap = '"{' + '"uid" : "' + uid_send + '" , ' + '"timestamp" : ' + '"' + time_send + '"}"'
            tap = ("uid"+uid_send+"timestamp"+time_send)
            taps_pending.append(tap)
            chiplog(tap)
            print(tap)
            posindication()

def checkpending(): #checks the unsent list and sends and unsent taps
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

def posindication(): #beep and flash for successful scan
    global count
    buzzer(True)
    led(True)
    time.sleep(0.5)
    buzzer(False)
    led(False)
    count = 0

def negindication(): #periodic flash
    global count
    if count == 300:
        led(True)
        time.sleep(0.2)
        led(False)
        count = 0
    else:
        count = count + 1

def setexternalrtc():
    buzzer(True)
    led(True)
    time.sleep(0.5)
    buzzer(False)
    time.sleep(0.5)
    buzzer(True)
    time.sleep(0.5)
    buzzer(False)
    #do something
    led(False)

################# Functions end

#setup SD card
sd = SD()
os.mount(sd, "/sd")
#print("SD card setup")

#setup LEDs and buzzer
#scanled = Pin('P3', mode=Pin.OUT) pin3 is the only other free GPIO pin found
buzzer = Pin('P19', mode=Pin.OUT)
led = Pin('P10', mode=Pin.OUT)

#tests LED and buzzer
buzzer(True)
led(True)
time.sleep(1)
buzzer(False)
led(False)

#setup real rtc
#i2c = I2C(0, I2C.MASTER) #intiate I2C bus as master
#rtc = pcf8563.PCF8563(i2c)

#setup network rtc - dropping soon
print("Getting time from NTP")
time.sleep(5)
rtc = RTC()
rtc.ntp_sync("0.uk.pool.ntp.org",update_period=3600)
time.sleep(2)
print(rtc.synced())

if rtc.synced() == True:
    print("Time synced")
    #and log
else:
    print("Time not synced - using default 1.1.00")
    rtc.init((2000, 1, 1, 0, 0, 0, 0, 0))
    errorlog("Time not synced - using default 1.1.00") #and log

print(rtc.now())


#setup taps pending list and counter
taps_pending = []
#print("variables set")
count = 0

#setup scan
py = Pyscan()
nfc = MFRC630(py)
#print("Scan setup")
nfc.mfrc630_cmd_init() # Initialise the MFRC630 with some settings

#RGB LED setuo
pycom.heartbeat(False)
RGB_BRIGHTNESS = 0x8
RGB_RED = (RGB_BRIGHTNESS << 16)
RGB_GREEN = (RGB_BRIGHTNESS << 8)
RGB_BLUE = (RGB_BRIGHTNESS)
#print("LED setup")

#thread start
#print("Starting threads")
_thread.start_new_thread(mainloop,())
_thread.start_new_thread(checkpending,())
