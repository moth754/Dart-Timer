##This is all going to change - I am switching hardware to use a custom PCB for interconnecting the modules and a Adafruit PN532 NFC reader for increased range. The end product should be significantly more robust.


# Instructions
These are the instructions to build the device how I did. It is possible to modify / change components and still end up with a working result.

## Google Sheets Instuctions
These are based on the instructions found [here](https://railsrescue.com/blog/2015-05-28-step-by-step-setup-to-send-form-data-to-google-sheets/).

1. Start a new sheet and save it in Google Docs. Add the columns names "device" and "payload"
2. Click on Tools - Script Editor
3. Click on File - New Script File
4. Paste in the code from GoogleIntegrations.gs (top level in this repository)
5. Click "Run"
6. Click on Publish - Deploy as web app
7. Make a note of the URL
8. Integration should be set to "Me"
9. Who has access should be set to "Anyone, even anonymous"
10. Click Deploy / Update


## Webhook Instructions
1. Setup a signal as "SIG 1", "taps" in the pybytes signals section
2. Setup a webhook integration under Pybytes integrations section. The correct configuration is shown in the Pybytes Webhook image
3. The URL is the "current web app URL" from the Google Sheets setup

