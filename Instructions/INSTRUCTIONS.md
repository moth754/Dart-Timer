# Instructions
These are the instructions to build the device how I did. It is possible to modify / change components and still end up with a working result.

## Bill of materials
The prices were correct at time of completing. Some of the prices / links are a guide only as some of the products (eg the buzzers) are sold in quantity only from the links provided, howerver the specs are correct. Cheaper alternatives can be found via eBay etc for some items.

***Please bear in mind I am still building prototypes!!! These instructions will continue to evolve for the next month or so.***

Item | Price | Quantity | Total |
-----|-------|----------|-------|
[Pycom FiPy](https://pycom.io/product/fipy/) | £49.21 | 1 | £49.21
[Pycom PyScan](https://pycom.io/product/pyscan/) | £29.07 | 1 | £29.07
[Pycom IP67 Antenna Kit](https://pycom.io/product/ip67-antenna-cable/) | £3.60 | 2 | £7.20
[Pycom Wifi Antenna](https://pycom.io/product/external-wifi-antenna/) | £7.29 | 1 | £7.29
[Pycom LoRa Antenna](https://pycom.io/product/lora-868mhz-915mhz-sigfox-antenna-kit/) | £8.20 | 1 | £8.20
[Pycom NB-IOT Antenna](https://pycom.io/product/lte-m-antenna-kit/) | £8.20 | 1 | £8.20
[Vodaphone NB-IOT SIM](https://pycom.io/product/vodafone-nb-iot-prepaid-subscription/) | £18.90 | 1 | £18.90
[10,000mAh USB Power Bank](https://www.amazon.co.uk/gp/product/B019GJLER8/ref=ppx_yo_dt_b_asin_title_o00_s01?ie=UTF8&psc=1) | £19.99 | 1 | £19.99
[MAX001 Case](https://www.trifibre.co.uk/product/max001/) | £7.08 | 1 | £7.08
[5v LED](https://uk.rs-online.com/web/p/leds/2285039/) | £0.48 | 1 | £0.48
[330 Ohm Resistor](https://uk.rs-online.com/web/p/through-hole-fixed-resistors/7077622/) | £0.12 | 1 | £0.12
[PN2222 Transistor](https://uk.rs-online.com/web/p/bjt-bipolar-transistors/7390381/) | £0.13 | 1 | £0.13
[3V Buzzer](https://uk.rs-online.com/web/p/magnetic-buzzer-components/1118176) | £1.76 | 1 | £1.76
[Molex RFID Antenna](https://uk.rs-online.com/web/p/rfid-antennas/1445000/) | £2.33 | 1 | £2.33
[UFL to Coax Cable](https://uk.rs-online.com/web/p/coaxial-cable/1360915/?relevancy-data=636F3D3126696E3D4931384E53656172636847656E65726963266C753D656E266D6D3D6D61746368616C6C7061727469616C26706D3D5E5B5C707B4C7D5C707B4E647D2D2C2F255C2E5D2B2426706F3D31333326736E3D592673723D2673743D4B4559574F52445F53494E474C455F414C5048415F4E554D455249432673633D592677633D4E4F4E45267573743D552E464C2D4C502D3038384B32542D412D2831353029267374613D552E464C2D4C502D3038384B32542D412D31353026&searchHistory=%7B%22enabled%22%3Atrue%7D) | £2.22 | 1 | £2.22
[Stripboard](https://uk.rs-online.com/web/p/stripboards/1004328/) | £8.44 | 1 | £8.44
[Slide Switch](https://uk.rs-online.com/web/p/slide-switches/1759703/) | £3.39 | 1 | £3.39
[Small Lipo](https://hobbyking.com/en_us/turnigy-2000mah-1s-1c-lipoly-w-2-pin-jst-ph-connector.html?countrycode=GB&gclsrc=aw.ds&gclid=CjwKCAjw0_T4BRBlEiwAwoEiAXOBCYp3YtZUUMW9XV4XLosNStAgU3ULHpf67hqPqKB2GIlB7fNIcRoCs5sQAvD_BwE&___store=en_us) | £3.62 | 1 | £3.62
[Battery Connectors](https://www.ebay.co.uk/itm/10x-2-0mm-Mini-Micro-JST-connector-PH-2-Pin-Male-Female-Plug-UK/154015839438?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649) | £2.99 | 1 | £1.49
[PCB Headers](https://www.ebay.co.uk/itm/2-to-40-Way-2-54mm-0-1-Male-Pin-Header-Single-Double-Row-PCB-Connector/262500789187?hash=item3d1e442bc3:g:MLsAAOSwjRpZVj4w) | £1.89 | 1 | £1.89
[DS3231 RTC Unit](https://www.ebay.co.uk/itm/DS3231-AT24C32-IIC-I2C-Module-Precision-RTC-Real-Time-Clock-Memory-Battery/274283810907?ssPageName=STRK%3AMEBIDX%3AIT&_trksid=p2057872.m2749.l2649) | £3.75 | 1 | £3.75
Low capacity good quaity microSD | £3 | 1 | £3
Wire (cut up alarm cable works well) | £2 | 1 | £2

This all brings the total cost to £190 (give or take a few pence). I would love to get it lower without compormising quality or function. Wire and standoffs are also required.

Reflective tape is also helpful for marking the location of the NFC antenna so competitors know where to scan. I#m planning on repurposing a reflective sticker.

Dependant on further testing, the NFC antenna maybe swapped for the molex one with shielding to the reverse. The reason for buying an additional antenna rather than using the one that comes with the Pyscan is sensitivity. The molex antenna with the wire soldered to it is way more sensitive than the antenna which is provided as standard.

## Wiring Diagram
See the image below, also available as a Fritzing sketch in the repository.

![Wiring Schematic](https://github.com/moth754/Dart-Timer/blob/master/Instructions/Images/Wiring%20diagram_schem.jpg)


## Hardware Instructions
Please look in the images folder to see images of each part of the construction.

***Making video coming soon***

1. Decide how you want your case laid out
2. Solder the switch to the battery with a trailing battery connector cable to attach to the Pyscan. Just connect the +ve wires to the switch.
3. Cut the USB A to micro B (incl. with the power bank normally) in half. Adjust the length as required. Connect the power to the other throw on the switch. Solder the data lines from each side together to ensure connectivity. Run a flying lead from the +ve and -ve connections for the buzzer and LED.
4. Solder the wires to the RTC
5. Cut the stripboard to leave a length at least 20 holes long by 3 wide, with the connections running horizonatly accross 3 holes
6. Solder male headers to one side of the stipboard (20 pin length). Solder wires for connecting to the RTC.
7. Another piece of stripboard needs wiring per the diagram to connect the buzzer and LED via the transistors and resistors as shown on the wiring diagram.
8. Drill holes for your antenna mounts (wifi and LoRa).
9. Drill holes for the LED and the buzzer and epoxy resin into position
10. Attach the NB-IOT antenna
11. Attach the stand offs to the pyscan and position. Use epoxy resin to attach the stand offs to the case. Repeat for the DS3231 RTC unit
12. Insert the SIM card and the SD card
13. Connect up antennas as per FiPy and Pyscan diagrams
14. Attach the FiPy
15. Connect up the battery
16. Attach the NFC antenna to the inside of the case (if shielded ensure shielding is inward facing)
17. Setup the device on PyBytes - see below

## Pybytes Instructions
1. Create an account at https://pybytes.pycom.io/
2. Essentially follow the instructions at [Pycom's website](https://docs.pycom.io/pybytes/) to setup the FiPy
2. Click on "devices" and add via USB or App
3. When the Pybytes setup is complete - uplaod the code

## Google Sheets Instuctions
These are based on the instructions found [here](https://railsrescue.com/blog/2015-05-28-step-by-step-setup-to-send-form-data-to-google-sheets/).

1. Start a new sheet and save it in Google Docs. Add the columns names "device" and "payload"
2. Click on Tools - Script Editor
3. Click on File - New Script File
4. Paste in the code from GoogleIntegrations.gs (top level in this repository)
5. Click on Publish - Deploy as web app
6. Make a note of the URL
7. Integration should be set to "Me"
8. Who has access should be set to "Anyone, even anonymous"
9. Click Deploy / Update


## Webhook Instructions
1. Setup a signal as "SIG 1", "taps" in the pybytes signals section
2. Setup a webhook integration under Pybytes integrations section. The correct configuration is shown in the Pybytes Webhook image
3. The URL is the "current web app URL" from the Google Sheets setup

