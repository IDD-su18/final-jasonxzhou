from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import time
from datetime import datetime
from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNStatusCategory
from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
 
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-0c657844-94fd-11e8-8ad6-9a5d6aeb6012'
pnconfig.publish_key = 'pub-c-b8f45a35-bcb2-4c5c-b307-34278cefbc9a'
pubnub = PubNub(pnconfig)

def my_publish_callback(envelope, status):
    # Check whether request successfully completed or not
    if not status.is_error():
        pass  # Message successfully published to specified channel.
    else:
        pass  # Handle message publish error. Check 'category' property to find out possible issue
        # because of which request did fail.
        # Request can be resent using: [status retry];
 
 
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass  # handle incoming presence data
 
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass  # This event happens when radio / connectivity is lost
 
        elif status.category == PNStatusCategory.PNConnectedCategory:
            # Connect event. You can do stuff like publish, and know you'll get it.
            # Or just use the connected event to confirm you are subscribed for
            # UI / internal notifications, etc
            pubnub.publish().channel("awesomeChannel").message("hello!!").async(my_publish_callback)
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
            # Happens as part of our regular operation. This event happens when
            # radio / connectivity is lost, then regained.
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
            # Handle message decryption error. Probably client configured to
            # encrypt messages and on live data feed it received plain text.
 
    def message(self, pubnub, message):
        pass  # Handle new message stored in message.message
 
 
pubnub.add_listener(MySubscribeCallback())
pubnub.subscribe().channels('myocarta').execute()

#user set variables:
PORT = "COM3"
BAUD_RATE = 9600
REMOTE_NODE_IDS = ["REMOTE", "REMOTE2", "REMOTE3"]
ANALOG_LINES = [IOLine.DIO1_AD1, IOLine.DIO1_AD1, IOLine.DIO1_AD1]
IO_SAMPLING_RATE = 0.1 #10hz sampling rate

#non-user variables
REMOTE_DEVICES = []
MOVING_AVERAGES = []

#main
def main():
    def publish_callback(result, status):
        pass
    # Handle PNPublishResult and PNStatus
    print("| Dummy Data Launching |")

    while True:
        for i in range(60):
            pubnub.publish().channel('myodum4').message([i]).async(publish_callback)
            pubnub.publish().channel('myodum5').message([i+10]).async(publish_callback)
            pubnub.publish().channel('myodum6').message([i+20]).async(publish_callback)
            pubnub.publish().channel('myodum7').message([i+30]).async(publish_callback)
            pubnub.publish().channel('myodum8').message([i+40]).async(publish_callback)
            time.sleep(0.1)

  
if __name__ == '__main__':
    main()