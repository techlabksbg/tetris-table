import machine
import neopixel
np = neopixel.NeoPixel(machine.Pin(4), 150)

# Turn off LEDS
np.write()

import mcp
from config import Config
import random
import math

buttons = mcp.MCP(Config.mcp_addr, np)
buttons.setLeds(0)

from tetris import Tetris
from letters import Letters
from light import light
from fire import Fire
from webserver import WebServer

def setPixel(x,y,what):
    x=9-x
    if x%2==1:
        y=14-y
    np[x*15+y] = what

def invertPixel(x,y):
    x=9-x
    if x%2==1:
        y=14-y
    c = np[x*15+y]    
    np[x*15+y] = (255-c[0], 255-c[1], 255-c[2])


l = Letters(np)

def getdist(a,b,x,y):
    dx = (x-a)%10
    if (dx>5):
        dx=10-dx
    dy = (y-b)%15
    if (dy>7.5):
        dy = 15-dy
    return dx*dx+dy*dy


def showmenu():
    while buttons.getButtons()!=255:
        pass
    numpoints = 3
    r=0.2
    points = [[random.random()*9,random.random()*15] for i in range(0,numpoints)]
    angles = [random.random()*2*math.pi for i in range(0,numpoints)]
    omegas = [random.random()*0.004+0.004 for i in range(0,numpoints)]
    firstitem = 0
    while True:
        vecs = [[math.cos(a)*r,math.sin(a)*r] for a in angles]            
        # Update points and angles
        for i in range(0,numpoints):
            angles[i]+=omegas[i]
            points[i][0]=(points[i][0]+vecs[i][0])%10
            points[i][1]=(points[i][1]+vecs[i][1])%15
        # Compute background
        for x in range(0,10):
            for y in range(0,15):
                c = [0,0,0]
                for i in range(0,numpoints):
                    d = 1/(1+2*getdist(x,y,points[i][0],points[i][1]))
                    c[i] = int(d*254)
                setPixel(x,y,c)
        # Show Strings
#        for i in range(firstitem, firstitem+2):
#            l.paintChar(2,3+(i%2)*6,65+i,"inv")
        np.write()
        b=buttons.getButtons() ^ 255
        bold = b
        
        if b!=0:
            bold = b
            while b!=0:
                b = buttons.getButtons()^255
                buttons.setLeds(b)
            return bold
        

def runprog(b):
    if b&8==8:
        print("Tetris")
        Tetris(np,buttons).play()
    elif b&4==4:
        print("Light")
        light(np,buttons).play()
    elif b&2==2:
        print("Fire")
        Fire(np,buttons).play()
    elif b&128==128:
        print("Webserver")
        WebServer(np,buttons).play()

while True:
    b = showmenu()
    print(b)
    runprog(b)

            
