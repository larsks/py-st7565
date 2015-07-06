import time
import itertools
import ctypes
import logging

try:
    import spidev
except ImportError:
    import stub_spidev as spidev

try:
    import RPIO
except ImportError:
    import stub_rpio as RPIO

LOG = logging.getLogger(__name__)

font5x7 = [
    [0x00, 0x00, 0x00, 0x00, 0x00,],
    [0x00, 0x00, 0x5F, 0x00, 0x00,],
    [0x00, 0x07, 0x00, 0x07, 0x00,],
    [0x14, 0x7F, 0x14, 0x7F, 0x14,],
    [0x24, 0x2A, 0x7F, 0x2A, 0x12,],
    [0x23, 0x13, 0x08, 0x64, 0x62,],
    [0x36, 0x49, 0x55, 0x22, 0x50,],
    [0x00, 0x05, 0x03, 0x00, 0x00,],
    [0x00, 0x1C, 0x22, 0x41, 0x00,],
    [0x00, 0x41, 0x22, 0x1C, 0x00,],
    [0x08, 0x2A, 0x1C, 0x2A, 0x08,],
    [0x08, 0x08, 0x3E, 0x08, 0x08,],
    [0x00, 0x50, 0x30, 0x00, 0x00,],
    [0x08, 0x08, 0x08, 0x08, 0x08,],
    [0x00, 0x30, 0x30, 0x00, 0x00,],
    [0x20, 0x10, 0x08, 0x04, 0x02,],
    [0x3E, 0x51, 0x49, 0x45, 0x3E,],
    [0x00, 0x42, 0x7F, 0x40, 0x00,],
    [0x42, 0x61, 0x51, 0x49, 0x46,],
    [0x21, 0x41, 0x45, 0x4B, 0x31,],
    [0x18, 0x14, 0x12, 0x7F, 0x10,],
    [0x27, 0x45, 0x45, 0x45, 0x39,],
    [0x3C, 0x4A, 0x49, 0x49, 0x30,],
    [0x01, 0x71, 0x09, 0x05, 0x03,],
    [0x36, 0x49, 0x49, 0x49, 0x36,],
    [0x06, 0x49, 0x49, 0x29, 0x1E,],
    [0x00, 0x36, 0x36, 0x00, 0x00,],
    [0x00, 0x56, 0x36, 0x00, 0x00,],
    [0x00, 0x08, 0x14, 0x22, 0x41,],
    [0x14, 0x14, 0x14, 0x14, 0x14,],
    [0x41, 0x22, 0x14, 0x08, 0x00,],
    [0x02, 0x01, 0x51, 0x09, 0x06,],
    [0x32, 0x49, 0x79, 0x41, 0x3E,],
    [0x7E, 0x11, 0x11, 0x11, 0x7E,],
    [0x7F, 0x49, 0x49, 0x49, 0x36,],
    [0x3E, 0x41, 0x41, 0x41, 0x22,],
    [0x7F, 0x41, 0x41, 0x22, 0x1C,],
    [0x7F, 0x49, 0x49, 0x49, 0x41,],
    [0x7F, 0x09, 0x09, 0x01, 0x01,],
    [0x3E, 0x41, 0x41, 0x51, 0x32,],
    [0x7F, 0x08, 0x08, 0x08, 0x7F,],
    [0x00, 0x41, 0x7F, 0x41, 0x00,],
    [0x20, 0x40, 0x41, 0x3F, 0x01,],
    [0x7F, 0x08, 0x14, 0x22, 0x41,],
    [0x7F, 0x40, 0x40, 0x40, 0x40,],
    [0x7F, 0x02, 0x04, 0x02, 0x7F,],
    [0x7F, 0x04, 0x08, 0x10, 0x7F,],
    [0x3E, 0x41, 0x41, 0x41, 0x3E,],
    [0x7F, 0x09, 0x09, 0x09, 0x06,],
    [0x3E, 0x41, 0x51, 0x21, 0x5E,],
    [0x7F, 0x09, 0x19, 0x29, 0x46,],
    [0x46, 0x49, 0x49, 0x49, 0x31,],
    [0x01, 0x01, 0x7F, 0x01, 0x01,],
    [0x3F, 0x40, 0x40, 0x40, 0x3F,],
    [0x1F, 0x20, 0x40, 0x20, 0x1F,],
    [0x7F, 0x20, 0x18, 0x20, 0x7F,],
    [0x63, 0x14, 0x08, 0x14, 0x63,],
    [0x03, 0x04, 0x78, 0x04, 0x03,],
    [0x61, 0x51, 0x49, 0x45, 0x43,],
    [0x00, 0x00, 0x7F, 0x41, 0x41,],
    [0x02, 0x04, 0x08, 0x10, 0x20,],
    [0x41, 0x41, 0x7F, 0x00, 0x00,],
    [0x04, 0x02, 0x01, 0x02, 0x04,],
    [0x40, 0x40, 0x40, 0x40, 0x40,],
    [0x00, 0x01, 0x02, 0x04, 0x00,],
    [0x20, 0x54, 0x54, 0x54, 0x78,],
    [0x7F, 0x48, 0x44, 0x44, 0x38,],
    [0x38, 0x44, 0x44, 0x44, 0x20,],
    [0x38, 0x44, 0x44, 0x48, 0x7F,],
    [0x38, 0x54, 0x54, 0x54, 0x18,],
    [0x08, 0x7E, 0x09, 0x01, 0x02,],
    [0x08, 0x14, 0x54, 0x54, 0x3C,],
    [0x7F, 0x08, 0x04, 0x04, 0x78,],
    [0x00, 0x44, 0x7D, 0x40, 0x00,],
    [0x20, 0x40, 0x44, 0x3D, 0x00,],
    [0x00, 0x7F, 0x10, 0x28, 0x44,],
    [0x00, 0x41, 0x7F, 0x40, 0x00,],
    [0x7C, 0x04, 0x18, 0x04, 0x78,],
    [0x7C, 0x08, 0x04, 0x04, 0x78,],
    [0x38, 0x44, 0x44, 0x44, 0x38,],
    [0x7C, 0x14, 0x14, 0x14, 0x08,],
    [0x08, 0x14, 0x14, 0x18, 0x7C,],
    [0x7C, 0x08, 0x04, 0x04, 0x08,],
    [0x48, 0x54, 0x54, 0x54, 0x20,],
    [0x04, 0x3F, 0x44, 0x40, 0x20,],
    [0x3C, 0x40, 0x40, 0x20, 0x7C,],
    [0x1C, 0x20, 0x40, 0x20, 0x1C,],
    [0x3C, 0x40, 0x30, 0x40, 0x3C,],
    [0x44, 0x28, 0x10, 0x28, 0x44,],
    [0x0C, 0x50, 0x50, 0x50, 0x3C,],
    [0x44, 0x64, 0x54, 0x4C, 0x44,],
    [0x00, 0x08, 0x36, 0x41, 0x00,],
    [0x00, 0x00, 0x7F, 0x00, 0x00,],
    [0x00, 0x41, 0x36, 0x08, 0x00,],
    [0x08, 0x08, 0x2A, 0x1C, 0x08,],
    [0x08, 0x1C, 0x2A, 0x08, 0x08 ],
]

libc = ctypes.CDLL('libc.so.6')


def delayus(us):
    """ Delay microseconds with libc usleep() using ctypes. """
    libc.usleep(int(us))


def delayms(ms):
    """ Delay microseconds with libc usleep() using ctypes. """
    libc.usleep(int(ms) * 1000)


class LCD (object):

    LCD_RST = 25
    LCD_A0 = 24
    LCD_RED = 18
    LCD_GREEN = 22
    LCD_BLUE = 23

    BIAS_1_9 = 0
    BIAS_1_7 = 1

    RESISTOR_RATIO = {
            3.0: 0b000,
            3.5: 0b001,
            4.0: 0b010,
            4.5: 0b011,
            5.0: 0b100,
            5.5: 0b101,
            6.0: 0b110,
            6.4: 0b111,
            }

    def __init__(self,
                 lcd_rst=LCD_RST,
                 lcd_a0=LCD_A0,
                 lcd_red=LCD_RED,
                 lcd_green=LCD_GREEN,
                 lcd_blue=LCD_BLUE,
                 spi_bus=0,
                 spi_dev=0,
                 adafruit=False,
                 flipped=False):

        self.lcd_rst = lcd_rst
        self.lcd_a0 = lcd_a0
        self.lcd_red = lcd_red
        self.lcd_green = lcd_green
        self.lcd_blue = lcd_blue
        self.spi_bus = spi_bus
        self.spi_dev = spi_dev
        self.adafruit = adafruit
        self.flipped = flipped

        if adafruit:
            self.pagemap = [3, 2, 1, 0, 7, 6, 5, 4]
        else:
            self.pagemap = None


        self.init_gpio()
        self.init_spi()
        self.init_lcd()

#    # XXX: This doesn't actually work as intended.
#    def __del__(self):
#        self.all_leds_off()

    def all_leds_off(self):
        self.rgb(1, 1, 1)

    def all_leds_on(self):
        self.rgb(0, 0, 0)

    def rgb(self, red, green, blue):
        RPIO.output(self.lcd_red, red)
        RPIO.output(self.lcd_green, green)
        RPIO.output(self.lcd_blue, blue)

    def init_gpio(self):
        RPIO.setmode(RPIO.BCM)
        for pin in [self.lcd_rst, self.lcd_a0]:
            RPIO.setup(pin, RPIO.OUT, initial=1)

        for pin in [self.lcd_red, self.lcd_green, self.lcd_blue]:
            RPIO.setup(pin, RPIO.OUT, initial=0)

    def init_spi(self):
        self.spi = spidev.SpiDev()
        self.spi.open(self.spi_bus, self.spi_dev)

    def init_lcd(self):
        self.reset()
        self.soft_reset()
        self.bias_set(bias=self.BIAS_1_7)
        self.adc_select()
        self.common_output_mode_select()
        self.display_start_address_set()

        LOG.debug('power on')
        self.power_control_set(True, False, False)
        delayms(50)
        self.power_control_set(True, True, False)
        delayms(50)
        self.power_control_set(True, True, True)
        delayms(10)

        self.regulator_resistor_select(ratio=6.0)
        self.electronic_volume_mode_set(0x20)

        LOG.debug('display on')
        self.display_on()
        self.display_points_normal()

        LOG.debug('clear')
        self.clear()

    def clear(self):
        for page in range(8):
            LOG.debug('clear page %d', page)
            self.page_address_set(page)
            self.column_set(0)
            self.send_data([0x00] * 128)

        self.page_address_set(0)
        self.column_set(0)

    def page_address_set(self, page):
        if self.pagemap:
            page = self.pagemap[page]

        op = 0b10110000
        op = op | page
        self.send_command([op])

    def column_set(self, col):
        if self.adafruit:
            col += 1

        # set column lsb
        lsb = (col & 0x0f)
        op = 0b00000000
        op = op | lsb
        self.send_command([op])

        # set column msb
        msb = (col & 0xf0) >> 4
        op = 0b00010000
        op = op | msb
        self.send_command([op])

    def pos(self, page, col=0):
        self.page_address_set(page)
        self.column_set(col)

    def set_pin(self, pin):
        RPIO.output(pin, 1)

    def reset_pin(self, pin):
        RPIO.output(pin, 0)

    def reset(self):
        LOG.debug('hard reset start')
        self.reset_pin(self.lcd_rst)
        delayms(500)
        self.set_pin(self.lcd_rst)
        delayms(1)
        LOG.debug('hard reset finished')

    def send_command(self, bytes):
        LOG.debug('sending command: %s',
                  ' '.join(hex(x) for x in bytes))
        self.reset_pin(self.lcd_a0)
        self.send(bytes)

    def send_data(self, bytes):
        LOG.debug('sending data: %s',
                  ' '.join(hex(x) for x in bytes))
        self.set_pin(self.lcd_a0)
        self.send(bytes)

    def send(self, bytes):
        self.spi.writebytes(bytes)

    def soft_reset(self):
        self.send_command([0b11100010])

    def display_on(self):
        self.send_command([0b10101111])

    def display_off(self):
        self.send_command([0b10101110])

    def display_points_on(self):
        self.send_command([0b10100101])

    def display_points_normal(self):
        self.send_command([0b10100100])

    def display_reverse(self):
        self.send_command([0b10100111])

    def display_normal(self):
        self.send_command([0b10100110])

    def adc_select(self, reverse=False):
        op = 0b10100000
        op = op | int(reverse)
        self.send_command([op])

    def common_output_mode_select(self, reverse=False):
        op = 0b11000000
        op = op | (int(reverse) << 3)
        self.send_command([op])

    def bias_set(self, bias=BIAS_1_9):
        if bias not in [self.BIAS_1_9, self.BIAS_1_7]:
            raise ValueError(bias)

        op = 0b10100010
        op = op | (int(bias))
        self.send_command([op])

    def power_control_set(self,
            converter=False,
            regulator=False,
            follower=False):

        op = 0b00101000
        op = op | (int(converter) << 2)
        op = op | (int(regulator) << 1)
        op = op | (int(follower))
        self.send_command([op])

    def regulator_resistor_select(self, ratio=5.0):
        op = 0b00100000
        op = op | self.RESISTOR_RATIO[ratio]
        self.send_command([op])

    def display_start_address_set(self, line=0):
        if line > 64:
            raise ValueError(line)

        op = 0b01000000
        op = op | line
        self.send_command([op])

    def brightness_set(self, val):
        op = 0b10000001
        self.send_command([op, val])

    def putc(self, c):
        bytes = font5x7[ord(c) - 32]

        if self.flipped:
            bytes = [int('{:08b}'.format(x)[::-1], 2)
                     for x in bytes]

        self.send_data(bytes + [0x00])

    def puts(self, s):
        for c in s:
            self.putc(c)


if __name__ == '__main__':
    logging.basicConfig(
        level='DEBUG')
    l = LCD(adafruit=True, flipped=True)
