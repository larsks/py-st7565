import struct


class SpiDev (object):
    '''This is a simple wrapper for accessing SPI devices using the Linux
    spidev kernel driver.'''

    def __init__(self, bus, dev):
        self.bus = bus
        self.dev = dev
        self.fd = -1

        self.open()

    def open(self):
        assert(self.fd == -1)
        self.fd = open(
            '/dev/spidev%d.%d' % (self.bus, self.dev),
            'w')

    def write(self, bytes):
        assert(self.fd != -1)
        self.fd.write(
            struct.pack('%ds' % len(bytes),
                        ''.join(chr(x) for x in bytes)))
        self.fd.flush()

    # compatability with spidev module
    writebytes = write

    def close(self):
        self.fd.close()
        self.fd = -1

    def fileno(self):
        return self.fd
