import st7565.bitops as bitops


class Bitmap (list):

    def __init__(self, rows=8, columns=128):
        self.rows = rows
        self.columns = columns
        self.width = columns
        self.height = 8 * rows

        super(Bitmap, self).__init__([0] * rows * columns)

    def clear(self):
        self[:] = [0] * self.rows * self.columns

    def set_pixel(self, x, y, pen=True):
        if x < 0 or x > self.width:
            raise ValueError(x)
        if y < 0 or y > self.height:
            raise ValueError(y)

        col = x
        row = y/8

        i = (row * self.columns) + col

        if pen:
            self[i] |= 1 << (7-(y % 8))
        else:
            self[i] &= ~(1 << (7-(y % 8)))

    def vline(self, x, y, len, pen=True):
        for l in range(len):
            self.set_pixel(x, y+l, pen)

    def hline(self, x, y, len, pen=True):
        for l in range(len):
            self.set_pixel(x+l, y, pen)

    def box(self, x1, y1, x2, y2, pen=True):
        self.hline(x1, y1, (x2-x1), pen)
        self.hline(x1, y2, (x2-x1), pen)
        self.vline(x1, y1, (y2-y1), pen)
        self.vline(x2, y1, (y2-y1), pen)

    def drawbitmap(self, img, tx=0, ty=0, centerx=False, centery=False):
        # convert to black and white
        img = img.convert('1')
        img_x, img_y = img.size

        if centerx:
            tx = self.width/2 - img_x/2

        if centery:
            ty = self.height/2 - img_y/2

        if img_x > self.width or img_y > self.height:
            raise ValueError('image is too large: (%d,%d) '
                             'is larger than (%d, %d)' % (
                                 img_x, img_y,
                                 self.width, self.height))

        imgdata = list(img.getdata())
        for x in range(img_x):
            for y in range(img_y):
                pen = imgdata[(y*img_x) + x]
                self.set_pixel(tx+x, ty+y, pen == 0)

    def vscroll(self, steps=1):
        for col in range(self.columns):
            bits = self[col::self.columns]
            if steps > 0:
                self[col::self.columns] = bitops.rotater(bits, steps)
            elif steps < 0:
                self[col::self.columns] = bitops.rotatel(bits, abs(steps))

    def hscroll(self, steps=1):
        steps = 0-steps
        for row in range(self.rows):
            t = self[row * self.columns:(row * self.columns) + self.columns]
            t = t[steps:] + t[:steps]
            self[row * self.columns:(row * self.columns) + self.columns] = t

    def dump(self):
        lines = []
        for row in range(self.rows):
            t = self[row * self.columns:(row * self.columns) + self.columns]
#            print 'ROW %d:' % row, t
            for bit in range(8):
                line = []
                for col in t:
                    val = int(((col) & (1 << (8-(bit+1)))) != 0)
                    line.append(val)

#                print 'BIT %d:' % bit, line
                lines.append(''.join((str(x) for x in line)))

        return '\n'.join(lines)


if __name__ == '__main__':
    b = Bitmap(2,32)
    b.set_pixel(0,0)
    b.vscroll(1)
    print b.dump()
