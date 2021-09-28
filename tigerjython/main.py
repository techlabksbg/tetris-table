
from helper import Helper  # Import der Klasse
helper = Helper()   # Erzeugen der Instanz

import random
import math


from fire import Fire
from letters import Letters
letters = Letters(helper)

from rickrolling import Rickroll
rickroll = Rickroll(helper)

from tetris import Tetris
tetris = Tetris(helper)

from fabiosfarbenspiel import FabiosFarbenSpiel
fabiosfarbenspiel = FabiosFarbenSpiel(helper)

from painter import Painter
painter = Painter(helper)


def getdist(a,b,x,y):
    dx = (x-a)%10
    if (dx>5):
        dx=10-dx
    dy = (y-b)%15
    if (dy>7.5):
        dy = 15-dy
    return dx*dx+dy*dy


def showmenu():
    while helper.getButtons()!=255:
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
                helper.setPixel(x,y,c)
                
        helper.np.write()
        b=helper.getButtons() ^ 255
        bold = b
        
        if b!=0:
            while b!=0:  # Warten bis losgelassen
                bold = b
                b = helper.getButtons()^255
                helper.setLeds(b^255)
            return bold
        

def runprog(b):
    if b&1==1:
        Fire(helper).play()
    elif b&2==2:
        letters.play()
    elif b&4==4:
        rickroll.play()
    elif b&8==8:
        tetris.play()
    elif b&16==16:
        fabiosfarbenspiel.play()
    elif b&32==32:
        painter.play()


while True:
    b = showmenu()
    runprog(b)

            
