import ctypes
import logging

try:
    import spidev
except ImportError:
    spidev = None

try:
    import RPi.GPIO as GPIO
except ImportError:
    GPIO = None

from st7565.fonts.font5x7 import glyphs as font5x7

LOG = logging.getLogger(__name__)

commands = {
}

libc = ctypes.CDLL('libc.so.6')


def delayus(us):
    """ Delay microseconds with libc usleep() using ctypes. """
    libc.usleep(int(us))


def delayms(ms):
    """ Delay microseconds with libc usleep() using ctypes. """
    libc.usleep(int(ms) * 1000)


class LCD (object):

    BRIGHTNESS=0x20

    LCD_RST = 25
    LCD_A0 = 24

    BIAS_1_9 = 0
    BIAS_1_7 = 1

    STATIC_OFF = 0
    STATIC_ON_LONG = 1
    STATIC_ON_SHORT = 2
    STATIC_ALWAYS_ON = 3

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
                 spi_bus=0,
                 spi_dev=0,
                 brightness=BRIGHTNESS,
                 adafruit=False,
                 flipped=False):

        self.lcd_rst = lcd_rst
        self.lcd_a0 = lcd_a0
        self.spi_bus = spi_bus
        self.spi_dev = spi_dev
        self.brightness = brightness
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
        self.backlight(1, 1, 1)

    def all_leds_on(self):
        self.backlight(0, 0, 0)

    def init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        for pin in [self.lcd_rst, self.lcd_a0]:
            GPIO.setup(pin, GPIO.OUT, initial=1)

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
        self.brightness_set(self.brightness)

        LOG.debug('display on')
        self.display_on()
        self.display_points_normal()

        LOG.debug('clear')
        self.clear()

    def clear(self):
        for page in range(8):
            LOG.debug('clear page %d', page)
            self.page_set(page)
            self.column_set(0)
            self.send_data([0x00] * 128)

        self.page_set(0)
        self.column_set(0)

    def page_set(self, page):
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
        self.page_set(page)
        self.column_set(col)

    def set_pin(self, pin):
        GPIO.output(pin, 1)

    def reset_pin(self, pin):
        GPIO.output(pin, 0)

    def reset(self):
        LOG.debug('hard reset')
        self.reset_pin(self.lcd_rst)
        delayms(500)
        self.set_pin(self.lcd_rst)
        delayms(1)

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

    def set_static_indicator(self, on=True, mode=STATIC_ALWAYS_ON):
        if mode not in range(0, 4):
            raise ValueError(mode)

        op = 0b10101100
        op = op | int(on)
        self.send_command([op, mode])

    def sleep(self):
        self.set_static_indicator(False, mode=self.STATIC_OFF)
        self.display_off()
        self.display_points_on()

    def wake(self):
        self.soft_reset()
        self.brightness_set(self.brightness)
        self.display_points_normal()
        self.display_on()
        self.set_static_indicator(True)

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
