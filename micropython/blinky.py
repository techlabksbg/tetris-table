
import machine
import neopixel
np = neopixel.NeoPixel(machine.Pin(4), 150, timing=True)

# Turn off LEDS
np.write();

import mcp

buttons = mcp.MCP()

import random

colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255),(255,255,255)]

#bricks = [(0,1,2,3),(0,1,2,5), (0,1,4,5), (0,1,5,6), (4,5,1,2), (0,1,2,6), (4,0,1,2)]

led = 0
num = 20
h = 1
dh=1

#feld = [[-1 for i in xrange(0,20)] for j in xrange(0,10)]

#Nullpunkt unten links, x nach rechs, y nach oben.
def setPixel(x,y,what):
    global np
    x=9-x
    if x%2==1:
        y=14-y
    np[x*15+y] = what

while True:
    for i in range(0,150):
        np[i]=(0,0,0)


    if (num==200):
        for y in range(0,h):
            for x in range(0,10):
                setPixel(x,y,colors[random.randint(0,len(colors)-1)])
        h=h+dh
        if (h>15):
            h=15
            dh=-1
        if (h<1):
            h=1
            dh=1
            
    else:
        for i in range(0,num):
            np[random.randint(0,149)] = colors[random.randint(0,len(colors)-1)]

    np.write();

    buttons.setLeds(buttons.getButtons() ^ 255)
    led=(led+1)%8

    s=buttons.getButtons()
    if (s & 0x1 == 0) and (num>1):
        num=num-1
    if (s & 0x8 == 0) and (num<200):
        num=num+1
    
    if (s & 0x4 == 0):
        num=200

    if (s & 0x2 == 0):
        num=1
