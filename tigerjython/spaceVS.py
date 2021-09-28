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

class spaceVS:
    
    def __init__(self, helper):
        self.helper = helper
        self.colors = [(173,255,47), (226,61,40), (0,0,255), (255,255,0), (255,0,255), (0,255,255),(255,255,255)]
        self.schiff = list(map(lambda x:list(map(lambda y: [y%4,y//4],x)), [(4,4,1,6), (0,0,5,2), (0,0,0,0)]))
        self.feld = [[-1 for i in range(0,15)] for j in range(0,10)]
        
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
        
    def canMove(self, brick, x, y, dx, dy):
        for i in range(0,4):
            a = brick[i][0]+x+dx
            b = brick[i][1]+y+dy
            if (a<0 or a>9 or b<0):
                return False
            if (b<15 and self.feld[a][b]!=-1):
                return False
        return True  
    
    def play(self):
        shape2 = self.schiff[0]
        shape1 = self.schiff[1]
        shot = self.schiff[2]
        curgame=0
        print(shape1)
        buttonRepe=300
        buttonRepeFast=100
        
        while True:
            if curgame==0:
                curgame=1
                x1 = 3
                y1 = 1
                x2 = 3
                y2 = 12
                self.showBrick(shape1, 0, x1,y1);
                self.showBrick(shape2, 1, x2,y2);
            b=self.helper.getButtons() ^ 255
            if (b==0):
                waitButtons=0
                lastButton=0
            if ((b&9!=0) and (lastButton!=b or waitButtons<time.ticks_ms())):
                if lastButton==b:
                    waitButtons=time.ticks_ms()+buttonRepeFast
                else:
                    waitButtons=time.ticks_ms()+buttonRepe
                lastButton=b
                d = 1 if b&8!=0 else -1
                if self.canMove(shape1, x1, y1, d, 1):
                    self.clearBrick(shape1, x1, y1)
                    x1+=d
                    self.showBrick(shape1, 0, x1, y1)
            if ((b&2!=0) and (lastButton!=b or waitButtons<time.ticks_ms())):
                if lastButton==b:
                    waitButtons=time.ticks_ms()+buttonRepeFast
                else:
                    waitButtons=time.ticks_ms()+buttonRepe
                lastButton=b
                x3 = x1+1
                y3 = y1+2
                z = 1
                self.showBrick(shot, 2, x3, y3)
                while z==1:
                    if self.canMove(shot, x3, y3, 0, 1):
                        self.clearBrick(shot, x3, y3)
                        y3 += 1
                        self.showBrick(shot, 2, x3, y3)
                    else:
                        z = 0





# Nur wenn Datei direkt ausgefuehrt wird:    
if __name__== "__main__":
    from helper import Helper
    p=spaceVS(Helper())
    p.play()