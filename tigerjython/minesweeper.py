# Code by Dang Khiem

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

class Minesweeper:
    
    def __init__(self,helper):
        self.helper = helper
        self.colour = [(0,0,0),(0,191,255),(255,0,0),(0,139,69),(0,0,139),(139,0,0),(102,205,170),(200,240,233),(255,255,0), (139,90,43)]
  # CountMinen:(         0,      1,          2,          3,         4,        5,          6,    )   7:verdeckt    8:Flag        Mine
        self.feld = [[0 for i in range(0,15)] for j in range(0,10)]
        self.visible = [[False for i in range(0,15)] for j in range(0,10)]
        self.flag = [[False for i in range(0,15)] for j in range(0,10)]
        self.x =  4
        self.y = 7
        self.m = 15 #anzahl Minen
        self.w = 0 #anzahl richtige Flaggen
        ledcycle={'v':0}
        this = self
        def ledcyclefun():
            this.helper.setLeds(1 << ledcycle['v'])
            ledcycle['v']=(ledcycle['v']+1)%8
        self.ledcyclefun=ledcyclefun
        self.letters = letters.Letters(self.helper)
        self.reset()
        
    
        
    def reset(self):
        for y in range(0,15):
            for x in range(0,10):
                self.feld[x][y]=0
                self.flag[x][y]=False
                self.visible[x][y]=False
        for i in range(0,150):
            self.helper.np[i]=(200,240,233);
        self.helper.np.write()
        
    def mine(self):
        self.mine_austeilen()
        self.number()
        return self.feld
    
    def mine_austeilen (self):
        for i in range (0,self.m):
                bomb=False
                while not bomb:
                    a=random.randint(0,9)
                    b=random.randint(0,14)
                    if self.feld[a][b] != 9:
                        self.feld[a][b] = 9 #9 heisst, da gibt es eine Mine
                        bomb = True #falls hier schon eine Mine ist, muss es nochmal diese Schleife durchlaufen
            
        
    def number(self):#zaehlt die Anzahl Minen in angrenzenden Felder
        for x in range (0,10):
            for y in range(0,15):
                if self.feld[x][y] == 9:
                    self.count_down_left(x,y)
                    self.count_down_right(x,y)
                    self.count_down(x,y)
                    self.count_left(x,y)
                    self.count_right(x,y)
                    self.count_up_left(x,y)
                    self.count_up_right(x,y)
                    self.count_up(x,y)
            
    def count_down_left(self,x,y):
        a=x-1
        b=y-1
        if a>=0 and b>=0: #pruefen, ob diese Koordinaten aussehrhalb von Feld ist
            if self.feld[a][b] != 9: #nichts machen, wenn auf dieser Feld eine Mine ist
                self.feld[a][b] += 1 #Wert von Feld +1
    #Das Gleiche mit jede anliegenden Feldern machen
    def count_down_right(self,x,y):
        a=x+1
        b=y-1
        if a<10 and b>=0:
            if self.feld[a][b] != 9:
                self.feld[a][b] += 1
    
    def count_down(self,x,y):
        a=x
        b=y-1
        if b>=0:
            if self.feld[a][b] != 9:
                self.feld[a][b] += 1
                    
    def count_left(self,x,y):
        a=x-1
        b=y
        if a>=0:
            if self.feld[a][b] != 9:
                self.feld[a][b] += 1
    
    def count_right(self,x,y):
        a=x+1
        b=y
        if a<10:
            if self.feld[a][b] != 9:
                self.feld[a][b] += 1
    
    def count_up_left(self,x,y):
        a=x-1
        b=y+1
        if a>=0 and b<15:
            if self.feld[a][b] != 9:
                self.feld[a][b] += 1
    
    def count_up_right(self,x,y):
        a=x+1
        b=y+1
        if a<10 and b<15:
            if self.feld[a][b] != 9:
                self.feld[a][b] += 1
    
    def count_up(self,x,y):
        a=x
        b=y+1
        if b<15:
            if self.feld[a][b] != 9:
                self.feld[a][b] += 1
                
    def led(self,x,y): #Teilt die einzelne Zahlen, Flagge, Minen, ect in ihren Farben ein
        if self.flag[x][y] == True:
            self.helper.setPixel(x,y, self.colour[8])
        elif self.visible[x][y] == False:
            self.helper.setPixel(x,y, self.colour[7])
        elif self.feld[x][y] == 0:
            self.helper.setPixel(x,y, self.colour[0])
        elif self.feld[x][y] == 1:
            self.helper.setPixel(x,y, self.colour[1])
        elif self.feld[x][y] == 2:
            self.helper.setPixel(x,y, self.colour[2])
        elif self.feld[x][y] == 3:
            self.helper.setPixel(x,y, self.colour[3])
        elif self.feld[x][y] == 4:
            self.helper.setPixel(x,y, self.colour[4])
        elif self.feld[x][y] == 5:
            self.helper.setPixel(x,y, self.colour[5])
        elif self.feld[x][y] == 6:
            self.helper.setPixel(x,y, self.colour[6])
        elif self.feld[x][y] == 9:
            self.helper.setPixel(x,y, self.colour[9])
        
    def reveal(self,x,y):# Hier wird das Aufdecken programmiert
        self.visible[x][y] = True #Es wird sichtbar
        self.led(x,y)
        if self.feld[x][y] == 0: #Falls es eine 0 ist, dann alle umliegende Felder aufdecken
            if x+1 < 10: #Prueft das anliegende Fwld ob es aussesrhalbe ist
                if self.visible[x+1][y] == False and self.flag[x+1][y] == False:  #Es wird nicht weitergemacht, wenn es schon sichtbar oder durch eine Flagge markiert ist.
                    self.visible[x+1][y] = True #das nebenliegende Feld wird sichtbar
                    self.led(x+1,y)
                    if self.feld[x+1][y] == 0: #falls diese nebenliegende Feld 0 ist, dann nochmals von vorner beginnen und dessen umliegende Feld aufdecken, pruefen ob diese Felder eine 0 ist ect.
                        self.reveal(x+1,y) #es wird durch Rekursion ermoeglicht
            #das Ganze fuer restliche Felder
            if x-1 >= 0:
                if self.visible[x-1][y] == False and self.flag[x-1][y] == False:
                    self.visible[x-1][y] = True
                    self.led(x-1,y)
                    if self.feld[x-1][y] == 0:
                        self.reveal(x-1,y)
            if x+1 < 10 and y+1 < 15:
                if self.visible[x+1][y+1] == False and self.flag[x+1][y+1] == False:
                    self.visible[x+1][y+1] = True
                    self.led(x+1,y+1)
                    if self.feld[x+1][y+1] == 0:
                        self.reveal(x+1,y+1)
            if y+1 < 15:
                if self.visible[x][y+1] == False and self.flag[x][y+1] == False:
                    self.visible[x][y+1] = True
                    self.led(x,y+1)
                    if self.feld[x][y+1] == 0:
                        self.reveal(x,y+1)
            if x-1 >=0 and y+1 < 15:
                if self.visible[x-1][y+1] == False and self.flag[x-1][y+1] == False:
                    self.visible[x-1][y+1] = True
                    self.led(x-1,y+1)
                    if self.feld[x-1][y+1] == 0:
                        self.reveal(x-1,y+1)
            if x+1 < 10 and y-1 >= 0:
                if self.visible[x+1][y-1] == False and self.flag[x+1][y-1] == False:
                    self.visible[x+1][y-1] = True
                    self.led(x+1,y-1)
                    if self.feld[x+1][y-1] == 0:
                        self.reveal(x+1,y-1)
            if y-1 >= 0:
                if self.visible[x][y-1] == False and self.flag[x][y-1] == False:
                    self.visible[x][y-1] = True
                    self.led(x,y-1)
                    if self.feld[x][y-1] == 0:
                        self.reveal(x,y-1)
            if x-1 >= 0 and y-1 >=0:
                if self.visible[x-1][y-1] == False and self.flag[x-1][y-1] == False:
                    self.visible[x-1][y-1] = True
                    self.led(x-1,y-1)
                    if self.feld[x-1][y-1] == 0:
                        self.reveal(x-1,y-1)

    def win(self): #pruefen ob man gewonnen hat
        w1 = self.win1()
        w2 = self.win2()
        if w1 and w2:
            return True
        else:
            return False
        
    def win1(self): #1. Gewinnbedingung: alle Felder sollten aufgedeckt oder durch Flaggen markiert werden
        for x in range (0,10):
            for y in range (0,15):
                if self.visible[x][y] == False and self.flag[x][y] == False:
                    return False
        return True
    
    def win2(self): # 2. Gewinnbedingung: Flagge und Minen sollten uebereistimmen und alle Minen muessen markiert sein
        if self.w == self.m:
            for x in range (0,10):
                for y in range (0,15):
                    if self.flag[x][y] == True and self.feld[x][y] !=9:
                        return False
        return True
               
    def mov_lim(self): #laesst nicht zu, dass Cursor ausserhalb vom Feld ist und stoppt einen Absturz.
        if self.x < 0:
            self.x = 0
        if self.x > 9:
            self.x = 9
        if self.y < 0:
            self.y = 0
        if self.y > 14:
            self.y = 14
            
    def play(self):
        x=0
        y=0
        self.reset()
        waitButtons = 0
        lastButton = 0
        self.mine()
        run = True
        while True:
            c = 255
            j = self.helper.getJoyStick(0) # -> [x,y,b]
            b = self.helper.getButtons() ^ 255 # Invert buttons
            self.helper.setLeds(b)
            self.led(self.x,self.y)
            self.x = int(10*j [0]//4096)
            self.y = int(15*j [1]//4096)
            x=self.x
            y=self.y
            self.mov_lim()
            if b&1 == 1:  #DIe erste Taste wird gedrueckt, um es mit einer Flagge zu markieren
                if self.flag[self.x][self.y] == False and self.visible[self.x][self.y] == False: #es passiert nur etwas, wenn das Feld nicht markiert und nicht sichtbar ist.
                    self.flag[self.x][self.y] = True #Das Feld wird markiert
                    if self.feld[self.x][self.y] ==9: #wenn Flagge auf mine ist, + 1 richtige Entdeckung
                        self.w += 1
                else:
                    self.flag[self.x][self.y] = False
                    if self.feld[self.x][self.y] ==9: #wenn Flagge weggenommen wird und es eine Mine hat, dann -1 rechnen
                        self.w -= 1
            if b&2 == 2:#zweite Taste wird gedrueckt, um es aufzudecken
                if self.flag[self.x][self.y] == False and self.visible[self.x][self.y] == False: #nur wenn das Feld nicht sichtbar und markiert ist.
                    self.reveal(self.x,self.y) #es wird aufgedeckt
                    if self.feld[self.x][self.y] == 9: #Falls es eine Mine ist, verliert man
                        self.visible[self.x][self.y] = True
                        self.led(self.x,self.y)
                        self.helper.np.write()
                        time.sleep_ms(500)
                        self.letters.animateString(5," You Lose", "inv", 100, callback=self.ledcyclefun)
                        return
            self.helper.setPixel(self.x,self.y, (100,c,100))
            self.helper.np.write()
            if self.win(): #wenn man gewonnen hat, eine Nachricht zeigen
                time.sleep_ms(500)
                self.letters.animateString(5," You Win", "inv", 100, callback=self.ledcyclefun)
                return
                    

if __name__=="__main__":
    from helper import Helper  # Import der Klasse
    helper = Helper()   # Erzeugen der Instanz
    ms = Minesweeper(helper)
    ms.play()
                   
            