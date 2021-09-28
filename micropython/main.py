import machine
import neopixel
np = neopixel.NeoPixel(machine.Pin(4), 150, timing=True)

# Turn off LEDS
np.write();

import mcp

buttons = mcp.MCP(0x20, np)

import random
import time   # time.sleep_ms() und time.ticks_ms()



# Hack to get ticks_ms() method in Tigerjython working
if not hasattr(time, 'ticks_ms'):
    from types import MethodType
    def ticks_ms(self):
        return int(round(self.time() * 1000))
    time.ticks_ms = MethodType(ticks_ms, time)
    
    def sleep_ms(self,a):
        time.sleep(a/1000.0)
    time.sleep_ms = MethodType(sleep_ms, time)
# END of Hack



colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255),(255,255,255)]

bricks = list(map(lambda x:list(map(lambda y: [y%4,y//4],x)), [(0,1,2,3),(0,1,2,5), (0,1,4,5), (0,1,5,6), (4,5,1,2), (0,1,2,6), (4,0,1,2)]))

led = 0
num = 20
h = 1
dh=1

feld = [[-1 for i in range(0,15)] for j in range(0,10)]


import letters

ledcycle=0
def ledcyclefun():
    global buttons
    global ledcycle
    buttons.setLeds(1 << ledcycle)
    ledcycle=(ledcycle+1)%8

lt = letters.Letters(np)
lt.animateString(4,"TETRIS TABLE",(100,255,100), 100, callback=ledcyclefun)


def rotate(brick, angle=1):
    res = [[0,0] for i in range(0,4)]
    xmin = 10
    ymin = 10
    for i in range(0,4):
        res[i][0] = brick[i][1]*angle
        res[i][1] = -brick[i][0]*angle
        if (res[i][0]<xmin):
            xmin=res[i][0]
        if (res[i][1]<ymin):
            ymin = res[i][1]
    for i in range(0,4):
        res[i][0]-=xmin
        res[i][1]-=ymin    
    return res

#Nullpunkt unten links, x nach rechs, y nach oben.
def setPixel(x,y,what):
    global np
    x=9-x
    if x%2==1:
        y=14-y
    np[x*15+y] = what


def showBrick(brick, col, x, y):
    global colors,np
    for i in range(0,4):
        a=x+brick[i][0]
        b=y+brick[i][1]
        if (a<10 and b<15):
            setPixel(a,b,colors[col])
    np.write()

def clearBrick(brick, x, y):
    global np
    for i in range(0,4):
        a=x+brick[i][0]
        b=y+brick[i][1]
        if (a<10 and b<15):
            setPixel(a,b,(0,0,0))
    np.write()

def setBrick(brick,col, x,y):
    global feld
    for i in range(0,4):
        a = brick[i][0]+x
        b = brick[i][1]+y
        if (b>14):
            return False
        feld[a][b]=col
    return True


def canMove(brick, x, y, dx, dy):
    global feld
    for i in range(0,4):
        a = brick[i][0]+x+dx
        b = brick[i][1]+y+dy
        if (a<0 or a>9 or b<0):
            return False
        if (b<15 and feld[a][b]!=-1):
            return False
    return True

def canTurn(brick, x, y, angle):
    global feld
    turned = rotate(brick)
    for i in range(0,4):
        a = turned[i][0]+x
        b = turned[i][1]+y
        if (a<0 or a>9 or b<0):
            return False
        if (b<15 and feld[a][b]!=-1):
            return False
    return True   

def checkLines():
    global feld,np
    blink=[]
    for y in range(0,15):
        full = True
        for x in range(0,10):
            if feld[x][y]==-1:
                full = False
                break
        if full:
            blink.append(y)
    if len(blink)>0:
        for i in range(0,13):
            for y in blink:
                for x in range(0,10):
                    setPixel(x,y, ((0,0,0) if i%2==0 else colors[feld[x][y]]))
            np.write()
            time.sleep_ms(50)
        blink.reverse()
        for y in blink:
            for yy in (range(y,15)):
                for x in range(0,10):
                    feld[x][yy] = feld[x][yy+1] if (yy+1<15) else -1
                    setPixel(x,yy, (colors[feld[x][yy]] if feld[x][yy]!=-1 else (0,0,0)))
            np.write()
            time.sleep_ms(100);
            
            

curbrick=-1  # no current brick
shape=None
bx=-1  # Coordinates of brick
by=-1  #

dropTime = 1000
nextDrop=time.ticks_ms()+dropTime
buttonRepe=300
buttonRepeFast=100
waitButtons = 0
lastButton = 0

while True:
    # print("now: "+str(time.ticks_ms())+"  next:"+str(nextDrop))
    if (curbrick==-1):
        curbrick=random.randint(0,len(bricks)-1)
        shape = bricks[curbrick]
        bx=4;
        by=14;    
        showBrick(shape, curbrick, bx,by);
        nextDrop=time.ticks_ms()+dropTime
    if (time.ticks_ms()>nextDrop):
        if canMove(shape,bx,by,0,-1):
            clearBrick(shape,bx,by)
            by-=1
            showBrick(shape,curbrick, bx, by)
            nextDrop = time.ticks_ms()+dropTime
        else:
            if not setBrick(shape,curbrick,bx,by):
                while True:
                    lt.animateString(random.randint(0,9),"GAME OVER",(100+random.randint(0,155),random.randint(0,255),100+random.randint(0,155)), 100, callback=ledcyclefun)
            checkLines()
            curbrick=random.randint(0,len(bricks)-1)
            shape = bricks[curbrick]
            bx=4;
            by=14;    
            showBrick(shape, curbrick, bx,by);
            nextDrop=time.ticks_ms()+dropTime
    b = buttons.getButtons() ^ 255 # Invert buttons
    buttons.setLeds(b)
    if (b==0):
        waitButtons=0
        lastButton=0
    if ((b&10!=0) and (lastButton!=b or waitButtons<time.ticks_ms())): #right or left
        if lastButton==b:
            waitButtons=time.ticks_ms()+buttonRepeFast
        else:
            waitButtons=time.ticks_ms()+buttonRepe
        lastButton=b
        d = 1 if b&8!=0 else -1
        if canMove(shape,bx,by,d,0):
            clearBrick(shape,bx,by)
            bx+=d
            showBrick(shape,curbrick, bx, by)
    if (b&4!=0 and (lastButton!=b or waitButtons<time.ticks_ms())): # rotate
        if lastButton==b:
            waitButtons=time.ticks_ms()+buttonRepeFast
        else:
            waitButtons=time.ticks_ms()+buttonRepe        
        lastButton=b
        angle = -1 
        if canTurn(shape,bx,by,angle):
            clearBrick(shape,bx,by)
            shape = rotate(shape,angle)
            showBrick(shape,curbrick, bx, by)
    if (b&1!=0 and (lastButton!=b or waitButtons<time.ticks_ms())): # drop
        if lastButton==b:
            waitButtons=time.ticks_ms()+buttonRepeFast
        else:
            waitButtons=time.ticks_ms()+buttonRepe
        lastButton=b     
        nextDrop = time.ticks_ms()-1
        
