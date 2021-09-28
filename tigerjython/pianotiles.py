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

class Pianotiles:
    
    def __init__(self,helper):
        self.helper = helper
        self.colors = [(255,255,255), (255,255,0), (0,255,0), (0,0,255)]#farben der knoepfe
        self.tiles = list(map(lambda x:list(map(lambda y: [y%8,y//8],x)), [(0,1,8,9),(2,3,10,11),(4,5,12,13),(6,7,14,15)]))#tiles in 2x8 raster
        self.feld = [[-1 for i in range(0,15)] for j in range(0,10)]
        ledcycle={'v':0}
        this = self
        def ledcyclefun():
            this.helper.setLeds(1 << ledcycle['v'])
            ledcycle['v']=(ledcycle['v']+1)%8
        self.ledcyclefun=ledcyclefun
        self.letters = letters.Letters(self.helper)
        self.reset()
        #self.startAnim()
        

    def reset(self):
        for y in range(0,15):
            for x in range(0,10):
                self.feld[x][y]=-1
        for i in range(0,150):
            self.helper.np[i]=(0,0,0);
        self.helper.np.write()
                
    def startAnim(self):
        self.letters.animateString(4,"PIANO TILES",(100,255,100), 100, callback=self.ledcyclefun)
        
    def showTiles(self,tiles, col, x, y):#tile setzen
        for i in range(0,4):
            a=x+tiles[i][0]
            b=y+tiles[i][1]
            if (a<10 and b<15):
                self.helper.setPixel(a,b,self.colors[col])
        self.helper.np.write()
    
    def clearTiles(self,tiles, x, y):#tile loeschen
        for i in range(0,4):
            a=x+tiles[i][0]
            b=y+tiles[i][1]
            if (a<10 and b<15):
                self.helper.setPixel(a,b,(0,0,0))
        self.helper.np.write()
        
    def canMove(self, tiles, x, y, dx, dy):#wenn sich tile bewegen kann
        for i in range(4):
            a = tiles[i][0]+x+dx
            b = tiles[i][1]+y+dy
            if (a<0 or a>9 or b<0):
                return False
            if (b<15 and self.feld[a][b]!=-1):
                return False
        return True

    def play(self):
        self.reset()
        curtile=-1  # keinen tile
        pos=None
        bx=-1  # koordinaten tile
        by=-1  #
        
        dropTime = 200
        nextDrop=1000
        buttonRepe=300
        buttonRepeFast=100
        waitButtons = 0
        lastButton = 0
        
        points = 0 #punkte auf 0 setzten
        reward = (1) #belohnung
        while True:
            b = self.helper.getButtons() ^ 255 # Invert buttons
            self.helper.setLeds(b)
            pos = self.tiles[curtile]
            if (curtile==-1):
                curtile=random.randint(0,len(self.tiles)-1)
                pos = self.tiles[curtile]
                bx=1; #tile mitte oben generieren
                by=14;    
                self.showTiles(pos, curtile, bx,by);
                nextDrop=time.ticks_ms()+dropTime
                
                
                
            if (time.ticks_ms()>nextDrop):
                if curtile==0:
                    if b&1==1:#wenn richtiger konpf gedrueckt
                        points+=reward #punkte werden erhoeht, tile verschwindet und neuer random tile wird gesetzt
                        self.clearTiles(pos,bx,by)
                        curtile=random.randint(0,len(self.tiles)-1)
                        pos = self.tiles[curtile]
                        bx=1;
                        by=14;    
                        self.showTiles(pos, curtile, bx,by);
                        if dropTime>100: #naechster tile wird schneller
                            dropTime-=50
                        nextDrop=time.ticks_ms()+dropTime
                    if self.canMove(pos,bx,by,0,-1):#wenn sich tile bewegen kann faellt er herunter
                        self.clearTiles(pos,bx,by)
                        by-=1
                        self.showTiles(pos,curtile, bx, by)
                        nextDrop = time.ticks_ms()+dropTime
                    else: #kann er sich nicht bewegen also unten angekommen resultiert in einem game over wo punktzahl angezeigt wird
                        for i in (9,6,3,0):
                            self.letters.animateString(i,str(points),(100+random.randint(0,155),random.randint(0,255),100+random.randint(0,155)), 100, callback=self.ledcyclefun)
                            self.helper.setLeds(0)
                        return
                    if b&8==8 or b&2==2 or b%4==4:#wird der falsche knopf gedruekt ebenfalls game over
                        for i in (9,6,3,0):
                            self.letters.animateString(i,str(points),(100+random.randint(0,155),random.randint(0,255),100+random.randint(0,155)), 100, callback=self.ledcyclefun)
                            self.helper.setLeds(0)
                        return
                        
                if curtile==1:#wiederholung fuer alle buttons
                    if b&2==2:
                        points+=reward
                        self.clearTiles(pos,bx,by)
                        curtile=random.randint(0,len(self.tiles)-1)
                        pos = self.tiles[curtile]
                        bx=1;
                        by=14;    
                        self.showTiles(pos, curtile, bx,by);
                        if dropTime>100:
                            dropTime-=50
                        nextDrop=time.ticks_ms()+dropTime
                   
                    if self.canMove(pos,bx,by,0,-1):
                        self.clearTiles(pos,bx,by)
                        by-=1
                        self.showTiles(pos,curtile, bx, by)
                        nextDrop = time.ticks_ms()+dropTime
                    else: 
                        for i in (9,6,3,0):
                            self.letters.animateString(i,str(points),(100+random.randint(0,155),random.randint(0,255),100+random.randint(0,155)), 100, callback=self.ledcyclefun)
                            self.helper.setLeds(0)
                        return
                    
                    if b&8==8 or b&1==1 or b%4==4:
                        for i in (9,6,3,0):
                            self.letters.animateString(i,str(points),(100+random.randint(0,155),random.randint(0,255),100+random.randint(0,155)), 100, callback=self.ledcyclefun)
                            self.helper.setLeds(0)
                        return
                        
                if curtile==2:
                    if b&4==4:
                        points+=reward
                        self.clearTiles(pos,bx,by)
                        curtile=random.randint(0,len(self.tiles)-1)
                        pos = self.tiles[curtile]
                        bx=1;
                        by=14;    
                        self.showTiles(pos, curtile, bx,by);
                        if dropTime>100:
                            dropTime-=50
                        nextDrop=time.ticks_ms()+dropTime
                  
                    if self.canMove(pos,bx,by,0,-1):
                        self.clearTiles(pos,bx,by)
                        by-=1
                        self.showTiles(pos,curtile, bx, by)
                        nextDrop = time.ticks_ms()+dropTime
                    else: 
                        for i in (9,6,3,0):
                            self.letters.animateString(i,str(points),(100+random.randint(0,155),random.randint(0,255),100+random.randint(0,155)), 100, callback=self.ledcyclefun)
                            self.helper.setLeds(0)
                        return
                    if b&8==8 or b&2==2 or b%1==1:
                        for i in (9,6,3,0):
                            self.letters.animateString(i,str(points),(100+random.randint(0,155),random.randint(0,255),100+random.randint(0,155)), 100, callback=self.ledcyclefun)
                            self.helper.setLeds(0)
                        return
                        
                if curtile==3:
                    if b&8==8:
                        points+=reward
                        self.clearTiles(pos,bx,by)
                        curtile=random.randint(0,len(self.tiles)-1)
                        pos = self.tiles[curtile]
                        bx=1;
                        by=14; 
                        self.showTiles(pos, curtile, bx,by);
                        if dropTime>100:
                            dropTime-=50
                        nextDrop=time.ticks_ms()+dropTime
           
                    if self.canMove(pos,bx,by,0,-1):
                        self.clearTiles(pos,bx,by)
                        by-=1
                        self.showTiles(pos,curtile, bx, by)
                        nextDrop = time.ticks_ms()+dropTime
                    else: 
                        for i in (9,6,3,0):
                            self.letters.animateString(i,str(points),(100+random.randint(0,155),random.randint(0,255),100+random.randint(0,155)), 100, callback=self.ledcyclefun)
                            self.helper.setLeds(0)
                        return
                    
                    if b&1==1 or b&2==2 or b%4==4:
                        for i in (9,6,3,0):
                            self.letters.animateString(i,str(points),(100+random.randint(0,155),random.randint(0,255),100+random.randint(0,155)), 100, callback=self.ledcyclefun)
                            self.helper.setLeds(0)
                        return
                        
                        

                    
                        

from helper import Helper #import der Klasse
helper = Helper() #erzeugen der Instanz
pt=Pianotiles(helper)
pt.play()