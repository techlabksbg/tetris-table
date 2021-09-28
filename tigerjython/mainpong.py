from helper import Helper
hp = Helper()

singlePlayer=False
computerPlayer=False
computerPlayerReaction=450


import random
import math
import time
import machine
import neopixel

np = neopixel.NeoPixel(machine.Pin(4), 150, timing=True)

if not hasattr(time, 'ticks_ms'):
    from types import MethodType
    def ticks_ms(self):
        return int(round(self.time() * 1000))
    time.ticks_ms = MethodType(ticks_ms, time)
    
    def sleep_ms(self,a):
        time.sleep(a/1000.0)
    time.sleep_ms = MethodType(sleep_ms, time)


p1=[0,29,30,59,60,89,90,119,120,149]
p2=[14,15,44,45,74,75,104,105,134,135]

cPTicker=0

#Anfang Bloecke anzeigen

np[p1[3]] = (255,255,0)
np[p1[4]] = (255,255,0)
np[p1[5]] = (255,255,0)
np[p1[6]] = (255,255,0)
    
np[p2[3]] = (100,200,255)
np[p2[4]] = (100,200,255)
np[p2[5]] = (100,200,255)
np[p2[6]] = (100,200,255)
np.write()    

q=hp.pixelNumber(5,6)


i=3;
j=3
#Ballsteuerung
x=4.5
y=7
ball=hp.pixelNumber(int(x),int(y))
np[ball]=(255,255,255)
np.write()

#ballvor -> debug
ballvor=-1

ballupdater=0
stepticker=0
velocityvar=0

wandstopper=0
balkenstopper=0

modeblock=0

P1=0
P2=0
SP=0
SPP=0

hp.setLeds(153)
while True:
    joyst=hp.getJoyStick(0)
    if joyst[2]==0 and singlePlayer==False and computerPlayer==False and modeblock==0:
        singlePlayer=True
        modeblock=1
        hp.setLeds(9)
    elif joyst[2]==0 and singlePlayer==True and computerPlayer==False and modeblock==0:
        singlePlayer=False
        computerPlayer=True
        hp.setLeds(249)
        modeblock=1
    elif joyst[2]==0 and singlePlayer==False and computerPlayer==True and modeblock==0:
        computerPlayer=False
        hp.setLeds(153)
        modeblock=1
    elif joyst[2]==1:
        modeblock=0
    
    if joyst[0]<1500 and computerPlayerReaction>0 and computerPlayer==True:
        computerPlayerReaction-=10
        time.sleep_ms(25)
    elif joyst[0]>2500 and computerPlayerReaction<900 and computerPlayer==True:
        computerPlayerReaction+=10
        time.sleep_ms(25)
    if computerPlayer==True:
        for nmr in range(int(computerPlayerReaction/100)+1):
            print(computerPlayerReaction)  
            np[hp.pixelNumber(nmr,11)]=(int(255-computerPlayerReaction/3.53),int(computerPlayerReaction/3.53),0)
            if computerPlayerReaction<900:
                np[hp.pixelNumber(9-(int((900-computerPlayerReaction)/100)),11)]=(0,0,0)
        np.write()
    
    btn=hp.getButtons() ^ 255
    if btn&0b11111111>0:
        break
        
hp.setLeds(0)
for clearcpdif in range(10):        
    np[hp.pixelNumber(clearcpdif,11)]=(0,0,0)


xd=(time.ticks_ms()%11)/10-0.5
firstdirection=time.ticks_ms()%2
if firstdirection==0:
    np[ball]=(0,0,255)
    np.write()
    yd=1
else:
    np[ball]=(255,0,0)
    np.write()
    yd=-1

time.sleep_ms(1000)

for rah in range(7):
    np[rah]=(50+rah*34,10,10)
    np[149-rah]=(50+rah*34,10,10)
    np[14-rah]=(10,10,50+rah*34)
    np[135+rah]=(10,10,50+rah*34)
    np.write()
    time.sleep_ms(100)
np[7]=(255,100,255)
np[142]=(255,100,255)
np.write()
time.sleep_ms(100)

for loeschen in range(15):
    np[loeschen]=(0,0,0)
    np[149-loeschen]=(0,0,0)
np.write()


stepticker=time.ticks_ms()

#Spiel

while True:
    #Balken
    if i!=0:
        np[p1[i-1]] = (0,0,0)
    np[p1[i]] = (255,255,0)
    np[p1[i+1]] = (255,255,0)
    np[p1[i+2]] = (255,255,0)
    np[p1[i+3]] = (255,255,0)
    if i<6:
        np[p1[i+4]] = (0,0,0)
        
    if j!=0:
        np[p2[j-1]] = (0,0,0)
    np[p2[j]] = (100,200,255)
    np[p2[j+1]] = (100,200,255)
    np[p2[j+2]] = (100,200,255)
    np[p2[j+3]] = (100,200,255)
    if j<6:
        np[p2[j+4]] = (0,0,0)
    np.write()
    
    
    #Buttons
    btn=hp.getButtons() ^ 255
            

    if btn&0b00001111==0:
        stopper1=0
        stopper2=0
        
    if btn&0b11110000==0:
        stopper3=0
        stopper4=0
        
        
    if btn&0b00001111==1 and i<6 and stopper1==0:
        i+=1
        stopper1=1
        if singlePlayer==True:
            j+=1
            stopper3=1
        
    
    if btn&0b00001111==8 and i>0 and stopper2==0:
        i-=1
        stopper2=1
        if singlePlayer==True:
            j-=1
            stopper4=1
        
        
    
    if btn&0b11110000==128 and j<6 and stopper3==0 and computerPlayer==False:
        j+=1
        stopper3=1

    if btn&0b11110000==16 and j>0 and stopper4==0 and computerPlayer==False:
        j-=1
        stopper4=1

#Multiplayer/computerPlayer Punktzahl
    if singlePlayer==False:
        hp.setLeds(0)


#SinglePlayer Punktzahl

    if singlePlayer==True:
        if SP==256:
            SPP+=1
            SP=0

    if singlePlayer==True:
        hp.setLeds(SP)
        

#API-PLAYER

    if computerPlayer==True:
        if time.ticks_ms()-cPTicker>int(computerPlayerReaction/3):
            if 7-j>round(x-0.5,0) and j<6:
                j+=1
            elif 8-j<round(x-0.5,0) and j>0:
                j-=1
            cPTicker=time.ticks_ms()
              


    #Ball
    
#Abprallen an Waenden
    if (int(x)==9 or int(x)==0):
        if wandstopper==0:
            xd=0-xd
            wandstopper=1
    else:
        wandstopper=0

#Abprallen an Balken
    #on P1-Side
    if int(y)==1:
        if balkenstopper==0:
            if (9-int(x))==i:
                xd+=0.1
                yd=0-yd
                balkenstopper=1
                if singlePlayer==True:
                    SP+=1
            elif (9-int(x))==i+1:
                xd+=0.05
                yd=0-yd
                balkenstopper=1
                if singlePlayer==True:
                    SP+=1
            elif (9-int(x))==i+2:
                xd-=0.05
                yd=0-yd
                balkenstopper=1
                if singlePlayer==True:
                    SP+=1
            elif (9-int(x))==i+3:
                xd-=0.1
                yd=0-yd
                balkenstopper=1
                if singlePlayer==True:
                    SP+=1
        
    #on P2-Side
    elif int(y)==13:
        if balkenstopper==0:
            if (9-int(x))==j:
                xd+=0.1
                yd=0-yd
                balkenstopper=1
                if singlePlayer==True:
                    SP+=1
            elif (9-int(x))==j+1:
                xd+=0.05
                yd=0-yd
                balkenstopper=1
                if singlePlayer==True:
                    SP+=1
            elif (9-int(x))==j+2:
                xd-=0.05
                yd=0-yd
                balkenstopper=1
                if singlePlayer==True:
                    SP+=1
            elif (9-int(x))==j+3:
                xd-=0.1
                yd=0-yd
                balkenstopper=1
                if singlePlayer==True:
                    SP+=1
            
    else:
        balkenstopper=0
        
#Punkte und Reset
    if int(y)==14:
        if singlePlayer==False:
            P1+=1
            if P1==16:
                time.sleep_ms(1000)
                for win in range(75):
                    np[win]=(255,255,0)
                    np[149-win]=(255,255,0)
                    np.write()
                    time.sleep_ms(10)
                for win1 in range(85):
                    for win2 in range(150):
                        np[win2]=(252-3*win1,252-3*win1,0)
                    np.write()
                break
            hp.setLeds(P1+P2*16)
        for qi in range(255):
            np[ball]= (255-qi,255-qi,255-qi)
            np.write()
            time.sleep_ms(2)
        np[ball]=(0,0,0)
        btn=0
        if singlePlayer==True:
            hp.setLeds(SP)
            time.sleep_ms(1000)
            while btn&0b11111111==0:
                btn=hp.getButtons() ^ 255
                if time.ticks_ms()%1000>500:
                    hp.setLeds(SP)
                elif SPP<256:
                    hp.setLeds(SPP)
            SP=0
        x=4.5
        y=7
        xd=(time.ticks_ms()%11)/10-0.5
        yd=-1
        x=4.5
        y=7
        velocityvar=0
        ball=hp.pixelNumber(int(x),int(y))
        for qi in range(128):
            np[ball]= (255,254-2*qi,254-2*qi)
            np.write()
            time.sleep_ms(1)
        btn=0
        if singlePlayer==False and computerPlayer==False:
            while btn&0b01100000==0:
                btn=hp.getButtons() ^ 255
                if time.ticks_ms()%1000<=400:
                    hp.setLeds(P1+96)
                elif 400<time.ticks_ms()%1000<=500 or 900<time.ticks_ms()%1000<=1000:
                    hp.setLeds(P1)
                else:
                    hp.setLeds(P1+P2*16)
        if singlePlayer==True or computerPlayer==True:
            while btn&0b00000110==0:
                btn=hp.getButtons() ^ 255
                if time.ticks_ms()%1000<=400:
                    hp.setLeds(6+P2*16)
                elif 400<time.ticks_ms()%1000<=500 or 900<time.ticks_ms()%1000<=1000:
                    hp.setLeds(P2*16)
                else:
                    hp.setLeds(P1+P2*16)
        velocityvar=0
        stepticker=time.ticks_ms()
        np[ball]=(0,0,0)
        
    elif int(y)==0:
        if singlePlayer==False:
            P2+=1
            if P2==16:
                time.sleep_ms(1000)
                for win in range(75):
                    np[win]=(100,200,255)
                    np[149-win]=(100,200,255)
                    np.write()
                    time.sleep_ms(10)
                for win1 in range(85):
                    for win2 in range(150):
                        np[win2]=(84-win1,168-3*win1,252-3*win1)
                break
            hp.setLeds(P1+P2*16)
        btn=0
        if singlePlayer==True:
            hp.setLeds(SP)
            time.sleep_ms(1000)
            while btn&0b11111111==0:
                btn=hp.getButtons() ^ 255
                if time.ticks_ms()%1000>500:
                    hp.setLeds(SP)
                elif SPP<256:
                    hp.setLeds(SPP)
            SP=0   
        for qi in range(255):
            np[ball]= (255-qi,255-qi,255-qi)
            np.write()
            time.sleep_ms(2)
        np[ball]=(0,0,0)
        x=4.5
        y=7
        xd=(time.ticks_ms()%11)/10-0.5
        yd=1
        x=4.5
        y=7
        ball=hp.pixelNumber(int(x),int(y))
        for qi in range(128):
            np[ball]= (100-(int((200*qi+1)/255)),200-(int((400*qi+1)/255)),255)
            np.write()
            time.sleep_ms(1)
        btn=0
        while btn&0b00000110==0:
            btn=hp.getButtons() ^ 255
            if time.ticks_ms()%1000<=400:
                hp.setLeds(6+P2*16)
            elif 400<time.ticks_ms()%1000<=500 or 900<time.ticks_ms()%1000<=1000:
                hp.setLeds(P2*16)
            else:
                hp.setLeds(P1+P2*16)
        velocityvar=0
        stepticker=time.ticks_ms()
        np[ball]=(0,0,0)
#Bewegung Ball
    
    if time.ticks_ms()-stepticker>25:
        ballupdater=1
        velocityvar+=(time.ticks_ms()-stepticker)/12
        stepticker=time.ticks_ms()
        
    timevar=math.log(velocityvar+1,100)+0.1
        
    if ballupdater==1:
        x+=xd*timevar*0.35
        y+=yd*timevar*0.35
        ballupdater=0
    
#Anzeige Ball

    ball=hp.pixelNumber(int(x),int(y))
    if ballvor!=ball:
        np[ballvor]=(0,0,0)
        #print("x=", int(x))
        #print("y=", int(y))
        print(yd*timevar*0.7)
        print(y)
    ballvor=ball
    np[ball]= (255,255,255)
    

    
    
    