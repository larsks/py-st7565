This is a Python module for driving an [ST7565 Positive LCD (128x64) with RGB backlight][lcd], as available from [Adafruit][] and other vendors.

It uses the Linux kernel [spidev][] module to handle communication
with the LCD, and the [RPIO.PWM][] module for accurate software PWM to
control the RGB backlight.

[lcd]: http://www.adafruit.com/products/250
[adafruit]: http://www.adafruit.com/
[spidev]: https://www.kernel.org/doc/Documentation/spi/spidev
[rpio.pwm]: https://pythonhosted.org/RPIO/pwm_py.html

## Requirements

You must have the Linux `spidev` module loaded. You should see at
least the file `/dev/spidev0.0` on your system (and entries in
`/sys/bus/spi`).

## Pins

You can configure this library to use whatever pins suit your fancy,
but the defaults are:

- spi bus 0
- spi dev 0
- lcd A0 is GPIO 24
- lcd RST is GPIO 25
- red led is GPIO 18
- green led is GPIO 22
- blue led is GPIO 23

## Installation

This is a standard Python package:

    python setup.py install

## Demo

This package includes a simple demo.  After installing the library as
above,  you can run the `stdemo` command to display an image on your
LCD. If you are not using the default pin layout you will need to
configure things using `--pin-a0`, `--pin-rst`,
`--pin-red`, `--pin-green`, and `--pin-blue`.

Display a simple image like this:

    stdemo

Go wild like this:

    stdemo --wild

Note that if you are using an Adafruit ST7565 you will need to pass
the `--adafruit` (`-a`) option or you will end up with garbled images.
