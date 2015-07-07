import RPi.GPIO as GPIO
import logging

LCD_RED = 18
LCD_GREEN = 22
LCD_BLUE = 23

LOG = logging.getLogger(__name__)


class Backlight (object):
    def __init__(self,
                 pin_red=LCD_RED,
                 pin_green=LCD_GREEN,
                 pin_blue=LCD_BLUE,
                 freq=100):
        self.pin_red = pin_red
        self.pin_blue = pin_blue
        self.pin_green = pin_green
        self.freq = freq

        self.init_gpio()
        self.init_pwm()
        self.all_leds_off()

    def init_gpio(self):
        GPIO.setmode(GPIO.BCM)
        for pin in [self.pin_red, self.pin_green, self.pin_blue]:
            GPIO.setup(pin, GPIO.OUT, initial=0)

    def init_pwm(self):
        self.pwm_red = GPIO.PWM(self.pin_red, self.freq)
        self.pwm_green = GPIO.PWM(self.pin_green, self.freq)
        self.pwm_blue = GPIO.PWM(self.pin_blue, self.freq)

    def all_leds_off(self):
        self.backlight(0, 0, 0)

    def all_leds_on(self):
        self.backlight(1, 1, 1)

    def _set_led(self, pin, pwm, val):
        LOG.debug('set LED on pin %d to %s', pin, val)
        if val == 0 or val == 1:
            pwm.stop()
            GPIO.output(pin, 1-int(val))
        else:
            pwm.start(int((1-val)*100))

    @property
    def red(self):
        return self._red

    @red.setter
    def red(self, val):
        self._red = val
        self._set_led(self.pin_red,
                      self.pwm_red,
                      val)

    @property
    def green(self):
        return self._green

    @green.setter
    def green(self, val):
        self._green = val
        self._set_led(self.pin_green,
                      self.pwm_green,
                      val)

    @property
    def blue(self):
        return self._blue

    @blue.setter
    def blue(self, val):
        self._blue = val
        self._set_led(self.pin_blue,
                      self.pwm_blue,
                      val)

    def backlight(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

if __name__ == '__main__':

    b = Backlight()
