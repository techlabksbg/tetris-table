
import time
import random

class FabiosFarbenSpiel:
    def __init__(self, helper):
        self.helper = helper
        
    def play(self):
        r1=0
        r2=255
        g1=0
        g2=255
        b1=0
        b2=255
        
        helper = self.helper
        np = helper.np
        while True:
            i=random.randint(0,149)
            r=random.randint(int(r1),int(r2))
            g=random.randint(int(g1),int(g2))
            b=random.randint(int(b1),int(b2))
            np[i] = (r,g,b)
            #np[(i+149)%150] = (0,0,0)
            np.write()
            
            btn=helper.getButtons() ^ 255
            helper.setLeds(btn)
            
            if btn&0xf==0xf or btn&0xf0==0xf0:
                while helper.getButtons()!=255:
                    pass
                break
            
            if (btn==1 or btn==16 or btn==17):
                if g2 > g1+1:
                    g2-=0.25
                if b2 > b1+1:
                    b2-=0.25
                
            elif (btn==2 or btn==32 or btn==34):
                if r2 > r1+1: 
                    r2-=0.25
                if b2 > b1+1:
                    b2-=0.25
            elif (btn==4 or btn==64 or btn==68):
                if r2 > r1+1: 
                    r2-=0.25
                if g2 > g1+1:
                    g2-=0.25
            elif (btn==8 or btn==128 or btn==136):
                if r2 < 255:
                    r2+=0.25
                if g2 < 255:
                    g2+=0.25
                if b2 < 255:
                    b2+=0.25
            #rg
            elif (btn==3 or btn==33 or btn==18 or btn==19 or btn==35 or btn==48 or btn==49 or btn==50 or btn==51):
                if r2 < 255: 
                    r2+=0.25
                if g2 < 255:
                    g2+=0.25
                if b2 > b1+1:
                    b2-=0.25
            #rb
            elif (btn==5 or btn==65 or btn==20 or btn==21 or btn==69 or btn==80 or btn==81 or btn==84 or btn==85):
                if r2 < 255: 
                    r2+=0.25
                if g2 > g1+1:
                    g2-=0.25
                if b2 < 255:
                    b2+=0.25
            #gb
            elif (btn==6 or btn==66 or btn==36 or btn==38 or btn==70 or btn==100 or btn==98 or btn==96 or btn==102):
                if r2 > r1+1: 
                    r2-=0.25
                if g2 < 255:
                    g2+=0.25
                if b2 < 255:
                    b2+=0.25
            
            
            #print (btn)
        