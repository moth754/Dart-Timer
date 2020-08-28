# Dart-Timer
This is a timing system built using micropython and based on a [Pycom](https://pycom.io/) FiPy board (will work with some other pycom boards).

The system records taps via NFC chips and relays the chip ID and the time of the tap to a Google Sheet. This can then be analysed to produce timing results.

The system makes use of Pycom's [Pybytes](https://pycom.io/products/software/pybytes-3/) as an easy way to manage the devices and recieve the data. The Pybytes software then sends the data on to the Google Sheet via HTTP post.

Obviously you will need a stock of NFC chips to make this work, but these are freely available - just check it's compatible with a MFRC630. 

Why is this different to other timing systems?
- Others can build, use and develop for free
- Uses Google Sheets so no additional specialist software is required and permissions can be managed easily (so a cut down view can shared with the public live during the race, marshals can see how many are on the course at a glance etc)
- Low running costs (no ongoing license fee for the software or hardware)
- Uses technology such as LoRa and NB-IOT to provide live data even in areas with poor mobile connectivity
- Relatively low cost per checkpoint in comparison to other live data feed systems
- Low cost and re-usable competitor devices (a simple wrist worn NFC tag)

##### Go Fund Me link for the next stage of development - https://gf.me/u/yiimtw

## Important code information
You need to run the following code via REPL to disable pybytes autostart. If you don't do this you will experience slowdowns due to mutliple threads connecting to the network. It will survive reboots.

```python
import pycom
pycom.pybytes_on_boot(False)
```


## Features
### Working and tested
* Records taps by NFC chips to local SD and send to Google Sheet
* Competitor numbers, names distances etc are all held in Google Sheets, so permissions and changes are straight-forward
* Visual and audible indication of successful tap by competitor
* Can use wifi, LoRa ([The Things Network](https://www.thethingsnetwork.org/)) and NB-IOT (a low power, long range cellular network) to connect to the internet
* Device design encloses the entire project in a small waterproof case
* Real time clock which can be updated via NTP via using a particular NFC card (set in code)

### Probably working but needs more testing
* 24 hour battery life
* Devices can mesh network to reduce the chances of connectivity outage - see [Pycom's](https://pycom.io/launching-mesh-networks/) page on mesh networking for more info

### Upcoming
The "to do" list can be found [here](https://trello.com/b/PtuwPh5d/timing-system) on Trello

## Instructions
Build instructions can be found in the instructions folder [here](https://github.com/moth754/Dart-Timer/blob/master/Instructions/INSTRUCTIONS.md).

# The Story
For a couple of years I have marshalled and timed various events. These have mostly been trail running, with a bit of swim running added in for good measure. On the higher risk ultra events timing was done by GPS trackers, but for the rest either NFC (webscorer or SiE) or RFID timing was used.

The most commonly asked question by far when I've been timing events has been by friends and family of the competitors "can you see where they are?" The answer is usually no. Interim timing points require additional kit and extra personnel, both f which are a luxery not normally available for the small to medium scale events. When splits timing is required we often hire the superb SiE system forn another local organiser. Several of our events do have a few splits!

Water safety teams would ask how many in and out the water for different swimrun stages, which the marshals on those checkpoints can usually provide. until they get distracted from counting to deal with first aid issues etc. 

To answer both the issue of people wanting to know where thier loved ones are on a route, and the safety issues, this timing system has come about. On the surface it is a very simple concept. Record who scans it at what time. However, it have taken a year of experimentation (on and off), and near giving up to get this far.

It's available to all (see license) as although it is a fairly technical know how heavy solution, for some race organisers and race timers it may prove useful.

## Thanks
Thanks the the following sources whom I have used thier code (in accordance with licenses) to make this project possible. 

* DS3231 code from the [MicroPython Chinese Community](https://github.com/micropython-Chinese-Community/mpy-lib/tree/master/misc/DS3231)
* This [post](https://railsrescue.com/blog/2015-05-28-step-by-step-setup-to-send-form-data-to-google-sheets/) by Scott Olmsted on posting to Google Sheets
* Pycom support who have been amazing solving problems (largely created by me)
* The PCA9554 library by akael "ported" by theshade
* Everyone elses various posts on forums etc I read in the making of this!

Special thanks to-
 * Laura (https://www.runventureonline.com/)
 * Ceri (https://www.wildrunning.co.uk/)
 * Ben (https://www.lasportiva.com/en)

All three are runners (with running related buisnesses) and have spurred me on to complete this project, even when I was ready to give up.