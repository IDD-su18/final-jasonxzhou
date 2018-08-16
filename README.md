# final-jasonxzhou

Useful files in this repo:  
test2.py -> final myocarta code  
test4.py -> mock data stream generator
profile_4060.xpro -> xbee configuration file for sensor zigbee
need to add profile for coordinator/dongle zigbee  
other files can be safely ignored

To run:  
Install digi xbee python library  
Install pubnub python library  
Set up user variables in test2.py:  
PORT: the port for usb dongle  
BAUD_RATE: usually 9600  
REMOTE_NODE_IDS: a list of the names of the myocarta dongles  
ANALOG_LINES: add one line for every sensor  
IO_SAMPLING_RATE: 0.1hz is usually sufficient  

Execute test2.py  
View data stream on freeboard  
