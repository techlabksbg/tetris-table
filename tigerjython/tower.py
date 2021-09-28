#TOWER game
from helper import Helper
import time

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


class Tower:
    def __init__(self,helper):
        self.helper=helper
        
    #erstellt eine horizontale linie    
    def line(self):
        for i in range(0,self.w):
            helper.setPixel(self.x+i,self.y,self.colors[self.c])
        for i in range(0,self.x):
            helper.setPixel(i,14,(0,0,0))
        for i in range(self.x+self.w,10):
            helper.setPixel(i,14,(0,0,0))
        if self.y<14:
            for i in range(0,10):
                helper.setPixel(i,self.y+1,(0,0,0))
        
        helper.np.write()
        
    #bewegt linie hin und her
    def move(self):
        if self.nextevent<time.ticks_ms():
            self.x+=self.hd
            self.line()
            if self.x+self.w==10:
                self.hd=-1
            elif self.x==0:
                self.hd=+1
            self.nextevent=time.ticks_ms()+100
            
                
    #lässt linie fallen
    def drop(self):
            if self.nextevent<time.ticks_ms():
                self.y+=self.vd
                self.line()
                self.nextevent=time.ticks_ms()+100
            if self.y==5:
                self.state=0
                self.y=14
            for i in range(0,6):
                i=self.y
                i-=1
            

    #zählt stockwerke    
    def score(self):
        if self.state==0:
            self.floors+=1
        
    def setup(self):
        self.colors=[(255,255,0),(0,255,255)]
        self.nextevent=time.ticks_ms()
        self.x=2
        self.y=14
        self.c=0
        self.w=5
        self.hd=+1
        self.vd=-1
        self.state=0
        self.wt=5
        self.xt=2
        self.floors=0
        
        for i in range(0,150):
            helper.np[i]=(0,0,0)
        helper.np.write()
        #grundtower von 0-5 generieren
        for i in range(0,5):
            self.y=i
            for i in range(0,self.wt+1):
                helper.setPixel(self.xt+i,self.y,self.colors[self.c])
        self.y=14
        
    
    def play(self):
        self.setup()
        while True:
            btn=self.helper.getButtons()^255
            if self.state==0:
                self.move()
            elif self.state==1:
                self.drop()
                
            if btn==1:
                self.state=1



from helper import Helper #import der Klasse
helper = Helper() #erzeugen der Instanz
tower=Tower(helper)
tower.play()