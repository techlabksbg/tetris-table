import random
import time

class JumpRun:
    def __init__(self,helper):
        self.helper = helper
        
        
    def play(self):
        jump = False
        duck = False
        t = 0
        a = 0
        b = 0
        u = 29
        o = 59
        oben = False
        unten = False
        
        for l in range(0,150,1): #macht das Spielfeld schwarz
            self.helper.np[l] = (0,0,0)
            self.helper.np.write()
            
        
        for i in range(0,15,1): #zeichnet die Bodenlinie
            self.helper.np[i] = (0,255,0)
            self.helper.np.write()
                    
        self.helper.np[19] = (0,0,255) #zeichnet die Spielfigur
        self.helper.np[40] = (0,0,255)
        self.helper.np[49] = (0,0,255)
        self.helper.np.write()
            
        while True:
            btn=self.helper.getButtons()^255
            self.helper.setLeds(btn)
            

            
            if t+250 < time.ticks_ms() and jump == True: #vollendet die Sprungbewegung
                self.helper.np[70] = (0,0,0)
                self.helper.np[79] = (0,0,0)
                self.helper.np.write()
                jump = False
                
                
            if t+250 < time.ticks_ms() and duck ==True: #vollendet die Duckbewegung
                self.helper.np[39] = (0,0,0)
                self.helper.np[49] = (0,0,255)
                self.helper.np.write()
                duck = False
                
        
            if btn == 1 and not jump: #startet die Sprungbewegung beim Knopfdruck 1
                t = time.ticks_ms()
                self.helper.np[19] = (0,0,0)
                self.helper.np[40] = (0,0,0)
                self.helper.np[70] = (0,0,255)
                self.helper.np[79] = (0,0,255)
                self.helper.np.write()
                jump = True

            
            if btn == 2 and not duck:  #startet die Duckbewegung
                t = time.ticks_ms()
                self.helper.np[39] = (0,0,255)
                self.helper.np[49] = (0,0,0)
                self.helper.np.write()
                duck = True
                
                
            if v+1000 == time.ticks_ms():  #generiert alle Sekunden ein x zufälliges x zwischen 0-1
                v = time.ticks_ms()
                x = random.random()
                      
            if x < 0.5 and stopunten == False:  #wertet x aus und bestimmt, ob das Hinderniss von oben oder unten kommt
                u = 29   #falls x kleiner als 0.5, wird die untere Hinternisbewegung gestartet
                a = time.ticks_ms()
                self.helper.np[u] = (255,0,0)
                self.helper.np.write()
                unten = True
                stopunten = True
            elif x > 0.5 and stopoben == False:
                o = 59  #falls x grösser als 0.5, wird die obere Hindernisbewegung gestartet
                b = time.ticks_ms()
                self.helper.np[o] = (255,0,0)
                self.helper.np.write()
                oben = True
                
                
            if unten == True and a+250 < time.ticks_ms() and u >14 : #sorgt dafür, dass das Hindernis bis zum Rand durchläuft
                a = time.ticks_ms()
                u = u-1
                self.helper.np[u] = (255,0,0)
                self.helper.np[u+1] = (0,0,0)
                self.helper.np.write()
                unten = True
                
                
                if u ==14:
                    stopunten = False
                
                
            if oben == True and b+250 < time.ticks_ms() and o > 44: #sorgt dafür, dass das obere Hindernis bis zum Rand durchläuft
                a = time.ticks_ms()
                o = o-1
                self.helper.np[o]
                self.helper.np[o+1]
                self.helper.np.write()
                oben = True
                
                if o == 44:
                    stopoben =False
                
                
                

from helper import Helper #import der Klasse
helper = Helper() #erzeugen der Instanz
jr=JumpRun(helper)
jr.play()               
            