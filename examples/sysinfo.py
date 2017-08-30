#!/usr/bin/python
import os
import time
from random import randint

import unicornhathd

try:
    import psutil
except ImportError:
    exit("This script requires the psutil module.\nInstall with: pip install psutils")

try:
    import vcgencmd
except ImportError:
    exit("This script requires the vcgencmd module.\nInstall with: pip install git+https://github.com/nicmcd/vcgencmd.git")

class stats:
    def getStats(self):
        self.users = len(psutil.users())
        self.cpuClock = vcgencmd.measure_clock('arm')
        self.rpiTemp = vcgencmd.measure_temp()
        self.cpuPct = psutil.cpu_percent()
        self.ramPct = psutil.virtual_memory().percent
        self.swapPct = psutil.swap_memory().percent
        self.diskPct = psutil.disk_usage('/').percent

    def __init__(self):
        self.getStats()

class bar(object):

    def linear_gradient(self,s, f=[255,255,255], n=16):
        rgbList = [s]
        for t in range(1, n):
           rgbList.append([int(s[j] + (float(t)/(n-1))*(f[j]-s[j])) for j in range(3)])
        return rgbList

    def update(self,v):
        self.val = v

    def __init__(self,w,h,v,m,a,cs=[0,0,0],ce=None):
        self.width = w
        self.height = h
        self.colour = cs
        self.val = v
        self.max = m
        self.alert = a
        self.gradient = None
	if ce is not  None:
            self.gradient = self.linear_gradient(cs,ce)
        
class playfield(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clear()
        unicornhathd.rotation(0)

    def set_pixel(self,x,y,r,g,b):
        self.pixels[x][y] = [r,g,b]

    def show(self):
        for y in xrange(self.height):
            for x in xrange(self.width):
                unicornhathd.set_pixel(x,y,self.pixels[x][y][0],self.pixels[x][y][1],self.pixels[x][y][2])
        unicornhathd.show()

    def clear(self):
        self.pixels = [[[0 for i in xrange(3)] for x in xrange(self.width)] for y in xrange(self.height) ]

def main(args):
    field = playfield(16,16)
    wrk = stats()
    bars = []
    bars.append(bar(2,16,16,16,4,[0,0,255]))
    bars.append(bar(2,16,600000000,1200000000,1200000000,[0,0,255],[255,0,0]))
    bars.append(bar(3,16,89,100,90,[255,0,128],[255,0,0]))
    bars.append(bar(3,16,79,100,80,[0,255,0],[255,0,0]))
    bars.append(bar(2,16,94,100,95,[255,0,255],[255,0,0]))
    bars.append(bar(2,16,94,100,95,[255,255,255],[255,0,0]))
    bars.append(bar(2,16,89,100,90,[255,128,125],[255,0,0]))
    flashing = False   
    try:
        while True:
            if not args.sim:
                wrk.getStats()
                bars[0].update(wrk.users)
                bars[1].update(wrk.cpuClock)
                bars[2].update(wrk.cpuPct)
                bars[3].update(wrk.rpiTemp)
                bars[4].update(wrk.ramPct)
                bars[5].update(wrk.swapPct)
                bars[6].update(wrk.diskPct)
            else:
                i = randint(0,6)
                #bars[i].update(randint(bars[i].max/bars[i].height,bars[i].max))
                inc = randint(-2,2)
                if inc < 0 and bars[i].val < 1:
                    inc = inc + randint(0,2)
                newv = bars[i].val + (bars[i].max/bars[i].height)*inc
		if newv < 0:
                    newv = 0
                if newv > bars[i].max:
                    newv = bars[i].max
                bars[i].update(newv)
            xoff = 0
            for b in bars:
                scale = 1
                if b.max > b.height:
                    scale = (b.max/b.height)
                for y in xrange(0,b.height):
                    for x in xrange(0,b.width):
                        if y <  (b.val / scale) and (not flashing or  b.val <= b.alert):
                           if b.gradient is None:
                               field.set_pixel(xoff+x,y,b.colour[0],b.colour[1], b.colour[2])
                           else:
                               field.set_pixel(xoff+x,y,b.gradient[y][0],b.gradient[y][1],b.gradient[y][2])
                xoff += b.width
            flashing = not flashing
            field.show()
            if args.sim:
                time.sleep(.5)
            else:
                time.sleep(1)
            field.clear()
    except KeyboardInterrupt:
        pass
    field.clear()
    field.show()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='''\
        Raspberry Pi System Monitor for UHHD.

        Displays various system performance metrics as a series of bars.
        Each bar has an alert value which will cause the bar to flash if
        this value is exceeded.

        The bars are:
          Number of logged in users
          CPU Clock Speed
          CPU Usage %
          ARM Core Temperature
          Memory Used %
          Swap Used %
          Disk (/) Used %
        ''',formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--demo', dest='sim', action='store_true', help='Simulate system performance data.')
    parser.set_defaults(sim=False)
    args = parser.parse_args()
    print parser.description
    main(args)
