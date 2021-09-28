import letters

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


class Tetris:
    
    def __init__(self,helper):
        self.helper = helper
        self.colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255),(255,255,255)]
        self.bricks = list(map(lambda x:list(map(lambda y: [y%4,y//4],x)), [(0,1,2,3),(0,1,2,5), (0,1,4,5), (0,1,5,6), (4,5,1,2), (0,1,2,6), (4,0,1,2)]))
        self.feld = [[-1 for i in range(0,15)] for j in range(0,10)]
        ledcycle={'v':0}
        this = self
        def ledcyclefun():
            this.helper.setLeds(1 << ledcycle['v'])
            ledcycle['v']=(ledcycle['v']+1)%8
        self.ledcyclefun=ledcyclefun
        self.letters = letters.Letters(self.helper)
        self.reset()
#        self.startAnim()
        

    def reset(self):
        for y in range(0,15):
            for x in range(0,10):
                self.feld[x][y]=-1
        for i in range(0,150):
            self.helper.np[i]=(0,0,0);
        self.helper.np.write()
        random.seed(time.ticks_ms());
                
    def startAnim(self):
        self.letters.animateString(4,"TETRIS TABLE",(100,255,100), 100, callback=self.ledcyclefun)


    def rotate(self,brick, angle=1):
        res = [[0,0] for i in range(0,4)]
        xmin = 100
        ymin = 100
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


    def showBrick(self,brick, col, x, y):
        for i in range(0,4):
            a=x+brick[i][0]
            b=y+brick[i][1]
            if (a<10 and b<15):
                self.helper.setPixel(a,b,self.colors[col])
        self.helper.np.write()

    def clearBrick(self,brick, x, y):
        for i in range(0,4):
            a=x+brick[i][0]
            b=y+brick[i][1]
            if (a<10 and b<15):
                self.helper.setPixel(a,b,(0,0,0))
        self.helper.np.write()
    
    def setBrick(self,brick,col, x,y):
        for i in range(0,4):
            a = brick[i][0]+x
            b = brick[i][1]+y
            if (b>14):
                return False
            self.feld[a][b]=col
        return True

    def canMove(self, brick, x, y, dx, dy):
        for i in range(0,4):
            a = brick[i][0]+x+dx
            b = brick[i][1]+y+dy
            if (a<0 or a>9 or b<0):
                return False
            if (b<15 and self.feld[a][b]!=-1):
                return False
        return True

    def canTurn(self,brick, x, y, angle):
        turned = self.rotate(brick)
        for i in range(0,4):
            a = turned[i][0]+x
            b = turned[i][1]+y
            if (a<0 or a>9 or b<0):
                return False
            if (b<15 and self.feld[a][b]!=-1):
                return False
        return True   

    def checkLines(self):
        blink=[]
        for y in range(0,15):
            full = True
            for x in range(0,10):
                if self.feld[x][y]==-1:
                    full = False
                    break
            if full:
                blink.append(y)
        if len(blink)>0:
            for i in range(0,13):
                for y in blink:
                    for x in range(0,10):
                        self.helper.setPixel(x,y, ((0,0,0) if i%2==0 else self.colors[self.feld[x][y]]))
                self.helper.np.write()
                time.sleep_ms(50)
            blink.reverse()
            for y in blink:
                for yy in (range(y,15)):
                    for x in range(0,10):
                        self.feld[x][yy] = self.feld[x][yy+1] if (yy+1<15) else -1
                        self.helper.setPixel(x,yy, (self.colors[self.feld[x][yy]] if self.feld[x][yy]!=-1 else (0,0,0)))
                self.helper.np.write()
                time.sleep_ms(100);
        return len(blink)
                
    def play(self):
        self.reset()
        curbrick=-1  # no current brick
        shape=None
        bx=-1  # Coordinates of brick
        by=-1  #
        
        dropTime = 1500
        nextDrop=time.ticks_ms()+dropTime
        buttonRepe=300
        buttonRepeFast=100
        waitButtons = 0
        lastButton = 0
        debounce = time.ticks_ms()+2
        deButton = 0
        
        points = 0
        reward = (1,5,20,100,500)
        
        while True:
            # print("now: "+str(time.ticks_ms())+"  next:"+str(nextDrop))
            if (curbrick==-1):
                curbrick=random.randint(0,len(self.bricks)-1)
                shape = self.bricks[curbrick]
                bx=4;
                by=14;    
                self.showBrick(shape, curbrick, bx,by);
                nextDrop=time.ticks_ms()+dropTime
            if (time.ticks_ms()>nextDrop):
                if self.canMove(shape,bx,by,0,-1):
                    self.clearBrick(shape,bx,by)
                    by-=1
                    self.showBrick(shape,curbrick, bx, by)
                    nextDrop = time.ticks_ms()+dropTime
                else:
                    if not self.setBrick(shape,curbrick,bx,by):
                        for i in (9,6,3,0):
                            self.letters.animateString(i,str(points),(100+random.randint(0,155),random.randint(0,255),100+random.randint(0,155)), 100, callback=self.ledcyclefun)
                        self.helper.setLeds(0)
                        return
                    points+=reward[self.checkLines()]
                    curbrick=random.randint(0,len(self.bricks)-1)
                    shape = self.bricks[curbrick]
                    bx=4;
                    by=14;    
                    self.showBrick(shape, curbrick, bx,by);
                    if dropTime>100:
                        dropTime-=10
                    nextDrop=time.ticks_ms()+dropTime
            b = self.helper.getButtons() ^ 255 # Invert buttons
            print("--> b=%d, deButton=%d, lastButton=%d, debounce=%d" % (b,deButton,lastButton,debounce-time.ticks_ms()))
            #if (b!=deButton):
            #    debounce = time.ticks_ms()+2
            #    deButton = b
            #    b = lastButton
            #if debounce<=time.ticks_ms():
            #    b = deButton
            #print("    b=%d, deButton=%d, lastButton=%d, debounce=%d" % (b,deButton,lastButton,debounce-time.ticks_ms()))
            self.helper.setLeds(b)
            if (debounce<time.ticks_ms()):
                if (b==0):
                    debounce = time.ticks_ms()+5
                    waitButtons=0
                    lastButton=0
                if ((b&10!=0) and (lastButton!=b or waitButtons<time.ticks_ms())): #right or left
                    if lastButton==b:
                        waitButtons=time.ticks_ms()+buttonRepeFast
                    else:
                        waitButtons=time.ticks_ms()+buttonRepe
                    debounce = time.ticks_ms()+5
                    lastButton=b
                    d = 1 if b&8!=0 else -1
                    if self.canMove(shape,bx,by,d,0):
                        self.clearBrick(shape,bx,by)
                        bx+=d
                        self.showBrick(shape,curbrick, bx, by)
                if (b&4!=0 and (lastButton!=b or waitButtons<time.ticks_ms())): # rotate
                    if lastButton==b:
                        waitButtons=time.ticks_ms()+buttonRepeFast
                    else:
                        waitButtons=time.ticks_ms()+buttonRepe        
                    debounce = time.ticks_ms()+5
                    lastButton=b
                    angle = -1 
                    if self.canTurn(shape,bx,by,angle):
                        self.clearBrick(shape,bx,by)
                        shape = self.rotate(shape,angle)
                        self.showBrick(shape,curbrick, bx, by)
                if (b&1!=0 and (lastButton!=b or waitButtons<time.ticks_ms())): # drop
                    if lastButton==b:
                        waitButtons=time.ticks_ms()+buttonRepeFast
                    else:
                        waitButtons=time.ticks_ms()+buttonRepe
                    debounce = time.ticks_ms()+5
                    lastButton=b     
                    nextDrop = time.ticks_ms()-1
                    


# Nur wenn Datei direkt ausgefuehrt wird:    
if __name__== "__main__":
    from helper import Helper
    t=Tetris(Helper())
    t.play()
    
    
