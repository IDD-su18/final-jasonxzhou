from digi.xbee.devices import XBeeDevice
from digi.xbee.io import IOLine, IOMode

PORT = "COM3"
BAUD_RATE = 9600
REMOTE_NODE_ID = "REMOTE"
ANALOG_LINE = IOLine.DIO1_AD1

IO_SAMPLING_RATE = 0.1 #10hz

def main():
    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)

        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        remote_device.set_dest_address(device.get_64bit_addr())
        remote_device.set_io_configuration(ANALOG_LINE, IOMode.ADC)
        remote_device.set_io_sampling_rate(IO_SAMPLING_RATE)

        def io_samples_callback(sample, remote, time):
            print("New sample received from %s - %s" % (remote.get_64bit_addr(), sample))

        device.add_io_sample_received_callback(io_samples_callback)
        input()

    finally:
        if device is not None and device.is_open():
            device.close()

if __name__ == '__main__':
    main()