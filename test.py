from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode
import time
import threading

PORT = "COM3"
BAUD_RATE = 9600

REMOTE_NODE_ID = "REMOTE"

IOLINE_IN = IOLine.DIO1_AD1


def main():
    print(" | MyoCarta V1.0 07/18/18 |")
    print("S1: Configuring local receiver")
    stop = False
    th = None

    local_device = XBeeDevice(PORT, BAUD_RATE)

    try:
        local_device.open()
        print("S1: SUCCESS")
        print("S2: Initiating all wireless sensor connections")

        # Obtain the remote XBee device from the XBee network.
        xbee_network = local_device.get_network()
        
        remote_device = None
        while (remote_device == None):
            remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        print("S2: SUCCESS")
        remote_device.set_io_configuration(IOLINE_IN, IOMode.ADC)

        def read_adc_task():
            i = 0
            while not stop:
                # Read the analog value from the remote input line.
                value = remote_device.get_adc_value(IOLINE_IN)
                print("Data Point " + str(i) + " " + str(value))
                i += 1
                time.sleep(0.2)

        th = threading.Thread(target=read_adc_task)

        time.sleep(0.5)
        th.start()

        input()

    finally:
        stop = True
        if th is not None and th.isAlive():
            th.join()
        if local_device is not None and local_device.is_open():
            local_device.close()


if __name__ == '__main__':
    main()