from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import time

PORT = "COM3"
BAUD_RATE = 9600
REMOTE_NODE_ID = "REMOTE"
IOLINE_IN = IOLine.DIO1_AD1
samples = []

def io_sample_callback(io_sample, remote_xbee, send_time):
	if send_time not in samples:
		print("IO sample received at time %s." % str(send_time))
		print("IO sample:")
		print(str(io_sample))
		samples.append(send_time)

def main():
    print(" | MyoCarta V1.0 07/18/18 |")
    print("S1: Configuring local receiver")

    local_device = XBeeDevice(PORT, BAUD_RATE)
    local_device.open()

    print("S1: SUCCESS")
    print("S2: Initiating all wireless sensor connections")
    xbee_network = local_device.get_network()
    
    remote_device = None
    while (remote_device == None):
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
    print("S2: SUCCESS")
    
    remote_device.set_io_configuration(IOLINE_IN, IOMode.ADC)
    
    while True:
        value = remote_device.get_adc_value(IOLINE_IN)
        print(value)
        time.sleep(0.2)

    local_device.close()

main()

