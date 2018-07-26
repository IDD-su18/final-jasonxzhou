from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import time
from datetime import datetime

#user set variables:
PORT = "COM3"
BAUD_RATE = 9600
REMOTE_NODE_IDS = ["REMOTE"]
ANALOG_LINES = [IOLine.DIO1_AD1]
IO_SAMPLING_RATE = 0.1 #10hz sampling rate

#non-user variables
REMOTE_DEVICES = []

#outputs samples received
def io_samples_callback(sample, remote, time):
    index = find_remote_index(remote)
    print("--------------------------------")
    print("TIMESTAMP: " + datetime.now().strftime("%H:%M:%S.%f"))
    print("REMOTE ID: " + str(remote.get_64bit_addr()))
    print("REMOTE NAME: " + REMOTE_NODE_IDS[index])
    print("SAMPLE VALUE: " + str(sample.get_analog_value(ANALOG_LINES[index])))

#utility function for outputting remote index in lists such as REMOTE_NODE_IDS and ANALOG_LINES
def find_remote_index(remote):
    i = 0
    for rem in REMOTE_DEVICES:
        if rem.get_64bit_addr() == remote.get_64bit_addr():
            return i
        else:
            i += 1
    return -1

#main function
def main():
    print(" | Launching MyoCarta V2 07/25/18 |")
    all_connected = True
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        print("Launching home receiver module...")
        device.open()

        print("Connecting to remote devices...")
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

        print("Configuring remote device parameters...")

        i = 0
        for rem in REMOTE_DEVICES:
            rem.set_dest_address(device.get_64bit_addr())
            rem.set_io_configuration(ANALOG_LINES[i], IOMode.ADC)
            rem.set_io_sampling_rate(IO_SAMPLING_RATE)
            i += 1
        
        print("Home module " + str(device.get_64bit_addr()) + " is connected to the following addresses:")
        for rem in REMOTE_DEVICES:
            print(str(rem.get_64bit_addr()) + " ")
    
        response = input(" | Launch successful. Press any key to start data collection. |")

        device.add_io_sample_received_callback(io_samples_callback)
        input()
        print(" | Closing MyoCarta V2 07/25/18 |")

    finally:
        if device is not None and device.is_open():
            device.close()

if __name__ == '__main__':
    main()