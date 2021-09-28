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


class light:
    def __init__(self,np, buttons):
        self.np = np
        self.buttons = buttons
       
       
    def play(self):
        color = [50,50,50]
        first = True
        while True:
            r = self.buttons.getButtons() ^ 255
            change = False
            for i in range(0,3):
                if r & (1<<i):
                    color[i]+=1+color[i]//10
                    change = True
                if r & (1<< (i+4)):
                    color[i]-=1+color[i]//10
                    change = True
                if color[i]<0:
                    color[i]=0
                if color[i]>255:
                    color[i] = 255
                if (r & 8):
                    color[i]=255
                    change=True
                if (r & 128):
                    color[i]=0
                    change=True
            if change or first:
                first=False
                for i in range(0,150):
                    self.np[i]=color
                self.np.write()
            if r & 15 == 15 or r & 0xf0 == 0xf0:
                return
            
            