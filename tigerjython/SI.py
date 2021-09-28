import time
import random
import letters
pixelArray = [0 for i in range (10)]

if not hasattr(time, 'ticks_ms'):
    from types import MethodType
    def ticks_ms(self):
        return int(round(self.time() * 1000))
    time.ticks_ms = MethodType(ticks_ms, time)
    
    def sleep_ms(self,a):
        time.sleep(a/1000.0)
    time.sleep_ms = MethodType(sleep_ms, time)

class SpaceInvaders:
    def __init__(self,helper):
        self.helper = helper
        self.letters = letters.Letters(self.helper)
        ledcycle={'v':0}
        this = self
        def ledcyclefun():
            this.helper.setLeds(1 << ledcycle['v'])
            ledcycle['v']=(ledcycle['v']+1)%8
        self.ledcyclefun=ledcyclefun

    #convert score to quaternary and store results in array
    def convertToQuaternary(self,i):
        self.pixelArray = [0,0,0,0,0,0,0,0,0,0]
        if(i-262144>=0):
            self.pixelArray[0]=i//262144
            i-=self.pixelArray[0]*262144
        if(i-65536>=0):
            self.pixelArray[1]=i//65536
            i-=self.pixelArray[1]*65536
        if(i-16384>=0):
            self.pixelArray[2]=i//16384
            i-=self.pixelArray[2]*16384
        if(i-4096>=0):
            self.pixelArray[3]=i//4096
            i-=self.pixelArray[3]*4096
        if(i-1024>=0):
            self.pixelArray[4]=i//1024
            i-=self.pixelArray[4]*1024
        if(i-256>=0):
            self.pixelArray[5]=i//256
            i-=self.pixelArray[5]*256
        if(i-64>=0):
            self.pixelArray[6]=i//64
            i-=self.pixelArray[6]*64
        if(i-16>=0):
            self.pixelArray[7]=i//16
            i-=self.pixelArray[7]*16
        if(i-4>=0):
            self.pixelArray[8]=i//4
            i-=self.pixelArray[8]*4
        pixelArray[9]=i
    #shoot projectile and handle hit mechanics
    def shoot(self):
        for i in range(2,12):
            self.helper.setPixel(self.shipPosition,i,(255,255,255))
            if((self.shipPosition==self.enemyX)and(i==self.enemyY)): #upon hit
                self.enemyPresent=False
                self.score += (50+10*self.streak)
                self.dropTimeMs /= 1.01
                self.streak +=1
                if(self.enemyType==1): #special type 1 doubles drop time
                    self.dropTimeMs *= 2
                elif(self.enemyType==2): #special type 2 regenerates 1 health
                    self.health+=1
                    if self.health>10:
                        self.health=10
                elif(self.enemyType==3): #trololol
                    self.dropTimeMs = 10
                    self.gotTrolled = True #uMadBro?
            self.helper.np.write()
            self.helper.setPixel(self.shipPosition,i,(0,0,0))
            time.sleep(0.01)
    #spawn enemy, normal or special type
    def spawnEnemy(self):
        self.enemyX=random.randint(0,9)
        self.enemyY=12
        self.enemyPresent = True
        self.random=random.randint(0,100)
        if(self.random>98):
            self.enemyType=1
        elif(self.random>96):
            self.enemyType=2
        elif(self.random>94):
            self.enemyType=3
        else:
            self.enemyType=0
        
        
    def play(self):
        self.score = 0
        self.pixelArray = [0,0,0,0,0,0,0,0,0,0]
        self.health = 10
        self.shipPosition = 5
        self.projectilePosition = 2
        self.dropTimeMs = 200
        self.enemyPresent = False
        self.enemyX = 0
        self.enemyY = 0
        self.nextDrop = 0
        self.buttonRepTime = 100
        self.nextButtonRep = 0
        self.streak = 1
        self.enemyType = 0
        self.gotTrolled = False #didn't get trolled... yet
        for i in range(10):
            for j in range(15):
                self.helper.setPixel(i,j,(0,0,0))
        while (self.health>0):
            #Score display
            self.convertToQuaternary(self.score)
            print(self.pixelArray)
            for i in range(10):
                if (self.pixelArray[i]==0):
                    self.color = (0,0,0)
                if (self.pixelArray[i]==1):
                    self.color = (255,0,0)
                if (self.pixelArray[i]==2):
                    self.color = (0,225,0)
                if (self.pixelArray[i]==3):
                    self.color = (0,0,225)
                self.helper.setPixel(i+1,13,self.color)
            self.helper.np.write()
            #health display
            for i in range(10):
                self.helper.setPixel(i,14,(0,0,0))
                self.color = (0,0,0)
                if (i<self.health):
                    self.color = (0,255,0)
                    self.helper.setPixel(i,14,self.color)
            self.helper.np.write()
            #ship behavior
            for i in range(10):
                self.helper.setPixel(i,0,(0,0,0))
            b = self.helper.getButtons()^255
            if((b&2==2)and(self.shipPosition>0)and(time.ticks_ms()>self.nextButtonRep)):
                self.shipPosition-=1
                self.nextButtonRep = time.ticks_ms()+self.buttonRepTime
            if((b&8==8)and(self.shipPosition<9)and(time.ticks_ms()>self.nextButtonRep)):
                self.shipPosition+=1
                self.nextButtonRep = time.ticks_ms()+self.buttonRepTime
            self.helper.setPixel(self.shipPosition,0,(255,0,0))
            self.helper.np.write()
            if((b&4==4)):
                self.shoot()
            if(self.enemyPresent==False):
                self.spawnEnemy()
            #display enemies with their colors
            if(self.enemyPresent==True):
                if(self.enemyType==0):
                    self.helper.setPixel(self.enemyX,self.enemyY,(255,255,255))
                elif(self.enemyType==1):
                    self.helper.setPixel(self.enemyX,self.enemyY,(0,0,255))
                elif(self.enemyType==2):
                    self.helper.setPixel(self.enemyX,self.enemyY,(0,255,0))
                else:
                    self.helper.setPixel(self.enemyX,self.enemyY,(255,0,0))
            self.helper.np.write()
            #drop it
            if(time.ticks_ms()>self.nextDrop):
                self.helper.setPixel(self.enemyX,self.enemyY,(0,0,0))
                self.enemyY-=1
                #if enemy reaches lower end of screen
                if(self.enemyY<0):
                    self.spawnEnemy()
                    self.health-=1
                    self.dropTimeMs /= 1.1
                    self.streak = 1
                self.nextDrop = time.ticks_ms()+self.dropTimeMs
        #game over messages
        if (self.gotTrolled==True):
            self.letters.animateString(4,"U MAD BRO? ;-)   ",(255,0,0), 50, callback=self.ledcyclefun)
        self.letters.animateString(4,str(self.score)+" POINTS GET REKT NOOB",(255,0,0), 50, callback=self.ledcyclefun)
                
                
    
from helper import Helper #import der Klasse
helper = Helper() #erzeugen der Instanz
si=SpaceInvaders(helper)
si.play()
