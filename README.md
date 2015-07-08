This is a Python module for driving an [ST7565 Positive LCD (128x64) with RGB backlight][lcd], as available from [Adafruit][] and other vendors.

It uses the Linux kernel [spidev][] module to handle communication
with the LCD, and the [RPIO.PWM][] module for accurate software PWM to
control the RGB backlight.

[lcd]: http://www.adafruit.com/products/250
[adafruit]: http://www.adafruit.com/
[spidev]: https://www.kernel.org/doc/Documentation/spi/spidev
[rpio.pwm]: https://pythonhosted.org/RPIO/pwm_py.html

