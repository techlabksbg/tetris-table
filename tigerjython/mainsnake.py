#snake
from helper import Helper
hp=Helper()

import time
import machine
import neopixel

np = neopixel.NeoPixel(machine.Pin(4), 150, timing=True)

introdot=0
introlist=[143,126,127,128,129,110,99,98,97,96,95,94,85,64,65,54,53,52,51,38,21,22,23,6]
for i in range(len(introlist)):
    np[introlist[i]]=(0,255,0)
    np.write()

#Startwerte

updatetime=700
speedbonus=1
  
points=0

snakelength=4
snakelist=[(4,7)]
applespawner=0
place_apple=-1
speedamp=0.5
slowmo=0
speedbonustype=0

slowmoled=0

left=False
right=False
up=True
down=False

leftmove=False
rightmove=False
upmove=True
downmove=False

btnblocker=0
timetickerbutton=0
snakedead=False
no_apple=True

x=4
y=7

timeticker=0
timetickerfix=0
move_updater=0

#Game

def playsnake():
    #Startwerte für Restart des Spiels
    global points
    updatetime=700
    speedbonus=1
    
    points=0    

    snakelength=4
    snakelist=[(4,7)]
    applespawner=0
    place_apple=-1
    speedamp=0.5
    slowmo=0
    speedbonustype=0
    
    slowmoled=0    

    left=False
    right=False
    up=True
    down=False
    
    leftmove=False
    rightmove=False
    upmove=True
    downmove=False
    
    btnblocker=0
    timetickerbutton=0
    snakedead=False
    no_apple=True
    
    x=4
    y=7
    
    timeticker=0
    timetickerfix=0
    move_updater=0
    
    
    while True:
        btn=hp.getButtons() ^ 255
        joyst=hp.getJoyStick(0)
    
        #Snake Bewegung
        if left==True and move_updater==1:
            x-=1
            move_updater=0
            leftmove=True
            rightmove=False
            upmove=False
            downmove=False
            print("left")
        elif right==True and move_updater==1:
            x+=1
            move_updater=0
            leftmove=False
            rightmove=True
            upmove=False
            downmove=False
            print("right")
        elif up==True and move_updater==1:
            y+=1
            move_updater=0
            leftmove=False
            rightmove=False
            upmove=True
            downmove=False
            print("up")
        elif down==True and move_updater==1:
            y-=1
            move_updater=0
            leftmove=False
            rightmove=False
            upmove=False
            downmove=True
            print("down")
            
        #put position in list
        if snakelist[0]!=((x%10),(y%15)):
            snakelist.insert(0,(x%10,y%15))
        #erase end of snake
        if len(snakelist)>snakelength:
            delx=snakelist[snakelength][0]
            dely=snakelist[snakelength][1]
            del snakelist[snakelength]
            np[hp.pixelNumber(delx,dely)]=(0,0,0)
        
        #check for dead snake
        for check in range(len(snakelist)-1):
            if snakelist[0] == snakelist[check+1]:
                np[hp.pixelNumber(snakelist[0][0],snakelist[0][1])]=(255,0,0)
                np.write()
                time.sleep_ms(1500)
                snakedead=True
    
        #Snake Tod Ausführen
        if snakedead==True:
            break
                
        #draw snake
        fadein=int((time.ticks_ms()-timeticker)/(updatetime*speedbonus)*255)
        np[hp.pixelNumber(snakelist[0][0],snakelist[0][1])]=(0,fadein,0)
        if len(snakelist)==snakelength:
            fadeout=int(255-((time.ticks_ms()-timeticker)/(updatetime*speedbonus)*255))
            np[hp.pixelNumber(snakelist[snakelength-1][0],snakelist[snakelength-1][1])]=(0,fadeout,0)
        for i in range(len(snakelist)-2):
            position=hp.pixelNumber(snakelist[i+1][0],snakelist[i+1][1])
            np[position]=(0,255,0)
        np.write()
        
        #Speedbonus
        
        if btn&0b00000011==1 and speedamp<0.9 and btnblocker==0:
            speedamp=round(speedamp+0.1,1)
            btnblocker=1
        elif btn&0b00000011==2 and speedamp>0.3 and btnblocker==0:
            speedamp=round(speedamp-0.1,1)
            btnblocker=1
        elif btn&0b00001100==4:
            speedbonus=(1-(updatetime/1000))*speedamp
            speedbonustype=1
        elif btn&0b00001100==8 and slowmo>0:
            speedbonus=2
            speedbonustype=2
        else:
            speedbonus=1
            speedbonustype=0
        
        
        if speedamp>0.8:
            ampled=0
        elif 0.9>speedamp>=0.7:
            ampled=1
        elif 0.7>speedamp>=0.5:
            ampled=3
        elif 0.5>speedamp:
            ampled=7
        
        
        #Ticker
        
        if time.ticks_ms()-timeticker>(updatetime*speedbonus):
            move_updater=1
            if no_apple==True:
                if speedbonustype==0:
                    applespawner+=1
                elif speedbonustype==1:
                    applespawner+=(1-(updatetime/1000))*speedamp
                elif speedbonustype==2:
                    applespawner+=2
                    slowmo-=18
                    
            timeticker=time.ticks_ms()
            if slowmo<99 and btn!=8:
                slowmo+=1
                smpopup=5
            if slowmo==99:
                if time.ticks_ms()%500>250 and smpopup>0:
                    slowmoled=8
                else:
                    slowmoled=0
                smpopup-=1
        
        if time.ticks_ms()-timetickerfix>700:
            updatetime=round(updatetime**0.999,0)
            print("Updatetime=",updatetime)
            timetickerfix=time.ticks_ms()
            
        if time.ticks_ms()-timetickerbutton>300:
            btnblocker=0
            timetickerbutton=time.ticks_ms()
            print("Speedamp:",speedamp)
                    
            
        #Slowmo Leiste
        if 0<slowmo<=30:
            hp.setLeds(ampled+slowmoled+128)
        elif 30<slowmo<=60:
            hp.setLeds(ampled+slowmoled+192)
        elif 60<slowmo<=90:
            hp.setLeds(ampled+slowmoled+224)
        elif 90<slowmo<=99:
            hp.setLeds(ampled+slowmoled+240)
        else:
            hp.setLeds(ampled+slowmoled+0)
        
        
    
        
        #Apple Spawner
        if applespawner>5:
            applespawner=0
            while no_apple==True:
                place_apple=time.ticks_ms()%150
                if np[place_apple]==(0,0,0):
                    np[place_apple]=(255,255,255)
                    np.write()
                    no_apple=False
                else:
                    print("replace apple")
        
        #Eat Apple
        if hp.pixelNumber(snakelist[0][0],snakelist[0][1])==place_apple:
            place_apple=-1
            snakelength+=1
            points+=1
            no_apple=True
                        
                        
                        
        
    
        #Joystick Richtung Detector
        if joyst[0]<1500 and joyst[0]<joyst[1] and joyst[0]<(4095-joyst[1]) and rightmove==False:
            left=True
            right=False
            up=False
            down=False
        elif joyst[0]>2500 and joyst[0]>joyst[1] and joyst[0]>(4095-joyst[1]) and leftmove==False:
            left=False
            right=True
            up=False
            down=False
        elif joyst[1]>2500 and joyst[1]>joyst[0] and joyst[1]>(4095-joyst[0]) and downmove==False:
            left=False
            right=False
            up=True
            down=False
        elif joyst[1]<1500 and joyst[1]<joyst[0] and joyst[1]<(4095-joyst[0]) and upmove==False:
            left=False
            right=False
            up=False
            down=True
    
#Ende des Spiels

        
while True:
    btn=hp.getButtons() ^ 255
    if points==0:
        if time.ticks_ms()%1000>500:
            hp.setLeds(15)
        else:
            hp.setLeds(0)
    else:
        if time.ticks_ms()%1000>500:
            hp.setLeds(points)
        else:
            hp.setLeds(0)
    
    
    if time.ticks_ms()-timeticker>80:
        np.write()
        introdot+=1
        if introdot==24:
            introdot=0
        timeticker=time.ticks_ms()
    introcolor_r=time.ticks_ms()%50
    introcolor_g=(introcolor_r+30)%136
    introcolor_b=(introcolor_r+60)%10
    np[introlist[(introdot)%24]]=(introcolor_r,120+introcolor_g,introcolor_b)
    np[introlist[(introdot+3)%24]]=(0,0,0)
        

    if btn>0:
        for rst in range(150):
            np[rst]=(0,0,0)
        np.write()
        hp.setLeds(0)
        playsnake()
        
        for px in range(150):
            np[px]=(255,0,0)
            np.write()
        for px in range(150):
            np[px]=(0,0,0)
            np.write()

    
        
            