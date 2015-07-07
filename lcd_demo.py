#!/usr/bin/python

import time

import st7565.backlight
import st7565.lcd
import st7565.logo

l = st7565.lcd.LCD(adafruit=True, flipped=True)
b = st7565.backlight.Backlight()

l.pos(3)
l.puts('Hello')
l.pos(4)
l.puts('world!')

for i in range(2):
    for j in range(100):
        b.red = j/100.0
        time.sleep(0.01)
    for j in range(100):
        b.red = 1-(j/100.0)
        time.sleep(0.01)

b.all_leds_on()
l.write_buffer(st7565.logo.logo)

for p in range(8):
    l.pos(p)
    l.puts('%d ' % p)

