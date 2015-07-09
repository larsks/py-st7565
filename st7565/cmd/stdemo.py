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

    g = p.add_argument_group('GPIO Configuration')
    g.add_argument('--pin-a0', default=-1, type=int)
    g.add_argument('--pin-rst', default=-1, type=int)
    g.add_argument('--pin-red', default=-1, type=int)
    g.add_argument('--pin-green', default=-1, type=int)
    g.add_argument('--pin-blue', default=-1, type=int)

    g = p.add_argument_group('Animation options')
    g.add_argument('--spin',
                   action='store_const',
                   const='spin',
                   dest='animation')
    g.add_argument('--hscroll',
                   action='store_const',
                   const='hscroll',
                   dest='animation')
    g.add_argument('--vscroll',
                   action='store_const',
                   const='vscroll',
                   dest='animation')

    p.add_argument('--step', default=5, type=int)
    p.add_argument('--delay', default=0.001, type=float)
    p.add_argument('--adafruit', '-a',
                   action='store_true', default=False)
    p.add_argument('--pulse', action='store_true')
    p.add_argument('--wild', action='store_true')
    p.add_argument('image',
                   nargs='?',
                   default=resource_filename(
                       'st7565', "images/adafruit-logo.pbm"))

    return p.parse_args()


def display_image(img):
    screen.drawbitmap(img, centerx=True, centery=True)
    lcd.write_buffer(screen)


def vscroll_image(img):
    screen.drawbitmap(img)

    while True:
        screen.vscroll(args.step)
        lcd.write_buffer(screen)
        time.sleep(args.delay)


def hscroll_image(img):
    screen.drawbitmap(img)

    while True:
        screen.hscroll(args.step)
        lcd.write_buffer(screen)
        time.sleep(args.delay)


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


def main():
    global args, lcd, leds, screen

    args = parse_args()

    if args.wild:
        args.spin = args.pulse = True

    lcd_kwargs = {}
    backlight_kwargs = {}

    if args.pin_a0 != -1:
        lcd_kwargs['pin_a0'] = args.pin_a0
    if args.pin_rst != -1:
        lcd_kwargs['pin_rst'] = args.pin_rst
    if args.pin_red != -1:
        backlight_kwargs['pin_red'] = args.pin_red
    if args.pin_green != -1:
        backlight_kwargs['pin_green'] = args.pin_green
    if args.pin_blue != -1:
        backlight_kwargs['pin_blue'] = args.pin_blue

    lcd = st7565.lcd.LCD(adafruit=args.adafruit, **lcd_kwargs)
    leds = st7565.backlight.Backlight(**backlight_kwargs)
    screen = st7565.bitmap.Bitmap()

    img = Image.open(args.image)

    leds.all_leds_on()

    if args.animation == 'spin':
        spin_image(img)
    elif args.animation == 'hscroll':
        hscroll_image(img)
    elif args.animation == 'vscroll':
        vscroll_image(img)
    else:
        display_image(img)


if __name__ == '__main__':
    main()
