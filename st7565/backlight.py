import RPi.GPIO as GPIO

LCD_RED = 18
LCD_GREEN = 22
LCD_BLUE = 23

CH_RED = 0
CH_GREEN = 1
CH_BLUE = 2


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
        if val in [0, 1]:
            pwm.stop()
            GPIO.output(pin, 1-val)
        else:
            pwm.start(int((1-val)*100))

    def backlight(self, red, green, blue):
        self._set_led(self.pin_red,
                      self.pwm_red,
                      red)
        self.set_led(self.pin_green,
                     self.pwm_green,
                     green)
        self.set_led(self.pin_blue,
                     self.pwm_blue,
                     blue)


if __name__ == '__main__':

    b = Backlight()
