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


class Fire:
    def __init__(self,np, buttons):
        self.np = np
        self.buttons = buttons
       
       
    def setPixel(self,x,y,what):
        x=9-x
        if x%2==1:
            y=14-y
        self.np[x*15+y] = what

    def fcol(self,h):
        palette = [[0.0,(0,0,0)],[0.3,(40,10,0)],[0.4,(200,20,0)], [0.5,(255,200,0)], [0.9,(100,80,0)],[1.0, (200,180,80)]]
        i=1
        while palette[i][0]<h:
            i+=1
        l = (h-palette[i-1][0])/(palette[i][0]-palette[i-1][0])
        return (int(l*palette[i][1][0]+(1-l)*palette[i-1][1][0]), int(l*palette[i][1][1]+(1-l)*palette[i-1][1][1]), int(l*palette[i][1][2]+(1-l)*palette[i-1][1][2]))
       
    def play(self):
        heat = [[0.0 for y in range(0,15)] for x in range(0,10)]
        self.buttons.setLeds(0)
        color = [50,50,50]
        first = True
        while True:
            r = self.buttons.getButtons() ^ 255
            if r>0:
                return
            for x in range(0,10):
                heat[x][0]=0.3+random.random()*0.7
            for yy in range(1,15):
                y = 15-yy
                for x in range(0,10):
                    l = 0.7+random.random()*0.2
                    l2 = random.random()*0.6+0.2
                    heat[x][y] = heat[x][y-1]*l + (heat[(x-1)%10][y-1]*l2+heat[(x+1)%10][y-1]*(1-l2))*0.5*(0.92-l)
            for y in range(0,15):
                for x in range(0,10):
                    self.setPixel(x,y,self.fcol(heat[x][y]))
            self.np.write()
            
       
