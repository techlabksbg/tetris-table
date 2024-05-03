import letters

import random

class Werbung:
    def __init__(self,np, buttons):
        self.np = np
        self.buttons = buttons
        self.letters = letters.Letters(np)
         
    def setPixel(self,x,y,what):
        x=9-x
        if x%2==1:
            y=14-y
        self.np[x*15+y] = what
       
    def play(self):
        self.buttons.setLeds(1)
        self.np.fill((0,0,0))
        
        self.setPixel(1, 0, (0, 0, 255))
        self.np.write()

        for y in range(15):
            if 4>y or y>10:
                for x in range (10):
                    self.setPixel(x, y, (0, 0, (y*y)))
                    print(x, y)
        self.np.write()
        
        self.letters.animateString(4,"WILLKOMMEN IM TECH LAB",(10,0, 255), 100)
        
        while True:
            b = self.buttons.getButtons() ^ 255
            if b&1==1:
                print("Zurück")
                self.buttons.setLeds(0)
                return            
       
