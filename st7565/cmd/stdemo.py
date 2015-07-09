#!/usr/bin/python

import time
import argparse
import threading
import math

from pkg_resources import Requirement, resource_filename

from itertools import cycle
from PIL import Image

import st7565.backlight
import st7565.lcd
import st7565.bitmap

args = None
leds = None
lcd = None
screen = None


def pulse():
    for angle in cycle(range(0, 361)):
        r = (math.sin(math.radians(angle)) + 1)/2
        g = (math.sin(math.radians((angle + 90) % 360)) + 1)/2
        b = (math.sin(math.radians((angle + 180) % 360)) + 1)/2

        leds.backlight(r, g, b)
        time.sleep(0.01)


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument('--spin', action='store_true')
    p.add_argument('--step', default=5, type=int)
    p.add_argument('--delay', default=0.001, type=float)
    p.add_argument('--adafruit', '-a',
                   action='store_true', default=False)
    p.add_argument('--loop', action='store_true')
    p.add_argument('--pulse', action='store_true')
    p.add_argument('image',
                   nargs='?',
                   default=resource_filename(
                       'st7565', "images/adafruit-logo.pbm"))

    return p.parse_args()


def display_image(img):
    screen.drawbitmap(img, centerx=True, centery=True)
    lcd.write_buffer(screen)


def spin_image(img):
    lcd.pos(4, 24)
    lcd.puts('Generating frames...')

    frames = []
    for angle in range(0, 360, args.step):
        lcd.pos(4)
        lcd.puts('%3s' % (int((angle/360.0) * 100)))
        lcd.send_data([0xff] * int(angle/360.0 * (128-24)))
        screen.clear()

        x = img.rotate(angle, expand=True)
        x = x.crop(box=(x.size[0]/2 - img.size[0]/2,
                   x.size[1]/2 - img.size[1]/2,
                   x.size[0]/2 + img.size[0]/2,
                   x.size[1]/2 + img.size[1]/2))
        screen.drawbitmap(x, centerx=True, centery=True)
        frames.append(screen[:])

    if args.pulse:
        t = threading.Thread(target=pulse)
        t.start()

    while True:
        for frame in frames:
            lcd.write_buffer(frame)
            time.sleep(args.delay)

        if not args.loop:
            break


def main():
    global args, lcd, leds, screen

    args = parse_args()

    lcd = st7565.lcd.LCD(adafruit=args.adafruit)
    leds = st7565.backlight.Backlight()
    screen = st7565.bitmap.Bitmap()

    img = Image.open(args.image)

    leds.all_leds_on()

    if args.spin:
        spin_image(img)
    else:
        display_image(img)


if __name__ == '__main__':
    main()
