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


class AutoTetris:
    
    def __init__(self,helper):
        self.helper = helper
        self.colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255), (0,255,255),(255,255,255)]
        self.bricks = list(map(lambda x:list(map(lambda y: [y%4,y//4],x)), [(0,1,2,3),(0,1,2,5), (0,1,4,5), (0,1,5,6), (4,5,1,2), (0,1,2,6), (4,0,1,2)]))
        self.rotations = [2,4,1,4,4,4,4]
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
    
    # Minimize this
    def objectiveFunction(self):
        maxh=0
        minh=14
        holecolumns=0
        holes=0
        heights=[0 for i in range(10)]
        for x in range(10):
            h=0
            for y in range(15):
                if self.feld[x][14-y]!=-1:
                    h=14-y
                    break
            heights[x]=h
            if h>maxh:
                maxh=h
            if h<minh:
                minh=h
            for y in range(h):
                f = 1
                if self.feld[x][y]==-1:
                    holes+=1
                    if f==1:
                        f=0
                        holecolumns+=1
        goodConfig=0
        for x in range(9):
            if heights[x]==heights[x+1]:
                goodConfig+=1
                break
        for x in range(8):
            if heights[x]==heights[x+1]+1 and heights[x+1]+1==heights[x+2]:
                goodConfig+=1
                break
            
        # print("maxh=%d, minh=%d, holecolumns=%d, holes=%d" %(maxh, minh, holecolumns, holes))
        return 3*maxh - minh + 3*holecolumns + holes*holes*10 - 3*goodConfig
    
    def bestMove(self, brick, color, x,y):
        fcopy = [[self.feld[i][j] for j in range(15)] for i in range(10)]
        a = x
        b = y
        tile = [[brick[i][j] for j in range(2)] for i in range(4)]
        trans = 0
        bestSoFar = 1000000
        best = None
        for rot in range(self.rotations[color]):
            while self.canMove(tile,x,y,-1,0):
                x-=1
                trans-=1
            #print("Testing rot %d at x=%d, y=%d" % (rot,x,y))
            while True:
                ydown = y
                while self.canMove(tile,x,ydown,0,-1):
                    ydown-=1
                self.setBrick(tile,color,x,ydown)
                #print("Setteled tile at x=%d, y=%d" % (x,ydown))
                l=self.checkLines(False)
                l=self.objectiveFunction()-0*l*l*l + ydown*5
                #print("  with score %d" % l);
                if (l<bestSoFar):
                    bestSoFar = l
                    best = [rot,trans]
                for i in range(10):
                    for j in range(15):
                        self.feld[i][j] = fcopy[i][j]
                
                if self.canMove(tile,x,y,1,0):
                    x+=1
                    trans+=1
                else:
                    break
            tile=self.rotate(tile, -1)
        return best

    def checkLines(self, animate=True):
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
            if animate:
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
                        if animate:
                            self.helper.setPixel(x,yy, (self.colors[self.feld[x][yy]] if self.feld[x][yy]!=-1 else (0,0,0)))
                if animate:
                    self.helper.np.write()
                    time.sleep_ms(100);
        return len(blink)
                
    def play(self):
        self.reset()
        curbrick=-1  # no current brick
        shape=None
        bx=-1  # Coordinates of brick
        by=-1  #
        
        dropTime = 200
        nextDrop=time.ticks_ms()+dropTime
        buttonRepe=300
        buttonRepeFast=100
        waitButtons = 0
        lastButton = 0
        
        points = 0
        reward = (1,5,20,100,500)
        bestmove = (0,0)
        
        while True:
            # print("now: "+str(time.ticks_ms())+"  next:"+str(nextDrop))
            if (curbrick==-1):
                curbrick=random.randint(0,len(self.bricks)-1)
                shape = self.bricks[curbrick]
                bx=4;
                by=14;    
                self.showBrick(shape, curbrick, bx,by);
                bestmove = self.bestMove(shape,curbrick,bx,by)
                # print(bestmove)
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
                    bestmove = self.bestMove(shape,curbrick,bx,by)
                    # print(bestmove)
                    if dropTime>100:
                        dropTime-=10
                    nextDrop=time.ticks_ms()+dropTime
            if lastButton==0 and bestmove!=[0,0]:
                if bestmove[0]>0:
                    b=4  # Rotate
                    bestmove[0]-=1
                else:
                    if bestmove[1]>0:
                        b=8
                        bestmove[1]-=1
                    else:
                        b=2
                        bestmove[1]+=1
            else:
                if lastButton!=0:
                    b=0
                    time.sleep_ms(80)
                elif bestmove==[0,0]:
                    b = 0
                else:
                    b = 1
                
            # b = self.helper.getButtons() ^ 255 # Invert buttons
            self.helper.setLeds(b)
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
                if self.canMove(shape,bx,by,d,0):
                    self.clearBrick(shape,bx,by)
                    bx+=d
                    self.showBrick(shape,curbrick, bx, by)
            if (b&4!=0 and (lastButton!=b or waitButtons<time.ticks_ms())): # rotate
                if lastButton==b:
                    waitButtons=time.ticks_ms()+buttonRepeFast
                else:
                    waitButtons=time.ticks_ms()+buttonRepe        
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
                lastButton=b     
                nextDrop = time.ticks_ms()-1
                



# Nur wenn Datei direkt ausgefuehrt wird:    
if __name__== "__main__":
    from helper import Helper
    t=AutoTetris(Helper())
    t.play()
    
    
