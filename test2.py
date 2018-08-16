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
    if not status.is_error():
        pass
    else:
        pass
 
 
class MySubscribeCallback(SubscribeCallback):
    def presence(self, pubnub, presence):
        pass
 
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
            pass
        elif status.category == PNStatusCategory.PNConnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNReconnectedCategory:
            pass
        elif status.category == PNStatusCategory.PNDecryptionErrorCategory:
            pass
    def message(self, pubnub, message):
        pass

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

#outputs samples received
def io_samples_callback(sample, remote, time):
    index = find_remote_index(remote)
    print("--------------------------------")
    print("TIMESTAMP: " + datetime.now().strftime("%H:%M:%S.%f"))
    print("REMOTE ID: " + str(remote.get_64bit_addr()))
    print("REMOTE NAME: " + REMOTE_NODE_IDS[index])
    print("SAMPLE VALUE: " + str(sample.get_analog_value(ANALOG_LINES[index])))
    value = round(sample.get_analog_value(ANALOG_LINES[index]) / 1023 * 100, 1)
    MOVING_AVERAGES[index].append(value)
    average = sum(MOVING_AVERAGES[index])/len(MOVING_AVERAGES[index])

    def publish_callback(result, status):
        pass
    if index == 0:
        pubnub.publish().channel('myocarta').message([value]).async(publish_callback)
        pubnub.publish().channel('myocarta2').message([average]).async(publish_callback)
    elif index == 1:
        pubnub.publish().channel('myocarta3').message([value]).async(publish_callback)
        pubnub.publish().channel('myocarta4').message([average]).async(publish_callback)
    else:
        pubnub.publish().channel('myocarta5').message([value]).async(publish_callback)
        pubnub.publish().channel('myocarta6').message([average]).async(publish_callback)

    
#utility function for outputting remote index in lists such as REMOTE_NODE_IDS and ANALOG_LINES
def find_remote_index(remote):
    i = 0
    for rem in REMOTE_DEVICES:
        if rem.get_64bit_addr() == remote.get_64bit_addr():
            return i
        else:
            i += 1
    return -1

#main
def main():
    def publish_callback(result, status):
        pass

    pubnub.publish().channel('myocarta_ui').message(["> Launching myocarta Beta Version"]).async(publish_callback)
    time.sleep(0.7)
    all_connected = True
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        pubnub.publish().channel('myocarta_ui').message([">> Launching home receiver module..."]).async(publish_callback)
        time.sleep(0.7)
        device.open()

        pubnub.publish().channel('myocarta_ui').message([">>> Connecting to sensors..."]).async(publish_callback)
        time.sleep(0.7)
        xbee_network = device.get_network()

        for device_id in REMOTE_NODE_IDS:
            remote_device = xbee_network.discover_device(device_id)
            if remote_device is None:
                print("ERROR: Could not find remote devices with ID " + device_id)
                all_connected = False
            else:
                REMOTE_DEVICES.append(remote_device)

        while (not all_connected):
            response_1 = input("Not all selected remote devices were connected; enter 'proceed' or 'abort' to continue.")
            if response_1 == "proceed":
                print("Proceeding with connected devices.")
                all_connected = True
            if response_1 == "abort":
                print("ERROR: Aborting")
                exit(1)
            else:
                print("Input unrecognized. Please enter proceed or abort.")

        pubnub.publish().channel('myocarta_ui').message([">>>> Configuring remote sensors..."]).async(publish_callback)

        i = 0
        for rem in REMOTE_DEVICES:
            rem.set_dest_address(device.get_64bit_addr())
            rem.set_io_configuration(ANALOG_LINES[i], IOMode.ADC)
            rem.set_io_sampling_rate(IO_SAMPLING_RATE)
            i += 1
            MOVING_AVERAGES.append([])
        
        print("Home module " + str(device.get_64bit_addr()) + " is connected to the following addresses:")
        for rem in REMOTE_DEVICES:
            print(str(rem.get_64bit_addr()) + " ")
    
        pubnub.publish().channel('myocarta_ui').message([">>>>> Launch successful. Starting data collection."]).async(publish_callback)
        time.sleep(0.7)
        pubnub.publish().channel('myocarta_ui').message(["| myocarta |"]).async(publish_callback)
        device.add_io_sample_received_callback(io_samples_callback)
        input()
        print(" | Closing MyoCarta V2 07/25/18 |")
        
    finally:
        if device is not None and device.is_open():
            device.close()

if __name__ == '__main__':
    main()