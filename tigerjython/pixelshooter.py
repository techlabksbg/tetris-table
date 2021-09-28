import helper
import letters
import time
import random
#COLOR_LIST = ["Black", "Red", "Green", "Blue", "Yellow", "Magenta"]
class pixelshooter:
    def __init__(self, helper):
        self.helper = helper
        self.score = 0
        self.currentColor = 0
        self.colors = [(0,0,0), (147,12,12), (11,126,11), (15,15,150), (170,170,26), (150,14,150)]
        self.projectileColors = [(0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (255,0,255)]
        self.shipPosition = 5
        self.blockArray = [[0 for i in range(0,15)] for j in range(0,10)] #Feldgenerierer
        self.hasRight = False #Diese Zeile und die zwei weiteren dienen zur Analyse gleicher benachbarten Farben
        self.hasLeft = False
        self.hasTop = False
        self.lenin = 0
        ledcycle={'v':0}
        this = self
        def ledcyclefun():
            this.helper.setLeds(1 << ledcycle['v'])
            ledcycle['v']=(ledcycle['v']+1)%8
        self.ledcyclefun=ledcyclefun
        self.letters = letters.Letters(self.helper)
        self.reset()
        self.attop = False
        self.shots = 0
        self.blocksPresent = True
        self.colorsPresent = [True for i in range (0,5)]
    
    def reset(self):
        for y in range(0,15):
            for x in range(0,10):
                self.blockArray[x][y]=0
        for i in range(0,150):
            self.helper.np[i]=(0,0,0);
        self.helper.np.write()
        
    def startAnim(self):
        self.letters.animateString(4,"PIXELSHOOTER",(100,255,100), 100, callback=self.ledcyclefun)
        
#Schiessanimation; Schiessmechanik        
    def shoot(self):
        self.shots+=1
        for i in range(0,15):
            if i == 14:
                self.attop = True #Zuoberst -> andocken beim hintersten Platz
                break
            elif(self.blockArray[self.shipPosition][i+1]!=0):
                break
            self.helper.setPixel(self.shipPosition,i,self.projectileColors[self.currentColor])
            self.helper.np.write()
            self.helper.setPixel(self.shipPosition,i,(0,0,0))
            time.sleep(0.01)
        if(self.attop==True):
            self.attop=False#Analyse: Sucht nach benachbarten Bloecken gleicher Farbe und setzt dies beim Nachbarn fort
            if self.shipPosition!=9 and self.blockArray[self.shipPosition+1][i]==self.currentColor:
                self.blockArray[self.shipPosition][i]=0-self.currentColor
                self.blockArray[self.shipPosition+1][i]=0-self.currentColor
                self.hasRight = True
            if self.shipPosition!=0 and self.blockArray[self.shipPosition-1][i]==self.currentColor:
                self.blockArray[self.shipPosition][i]=0-self.currentColor
                self.blockArray[self.shipPosition-1][i]=0-self.currentColor
                self.hasLeft = True
            if self.hasRight==False and self.hasLeft==False:
                self.blockArray[self.shipPosition][i]=self.currentColor
            self.hasRight = False
            self.hasLeft = False
        else:
            if self.blockArray[self.shipPosition][i+1]==self.currentColor:
                self.blockArray[self.shipPosition][i]=0-self.currentColor
                self.blockArray[self.shipPosition][i+1]=0-self.currentColor
                self.hasTop = True
            if self.shipPosition<9 and self.blockArray[self.shipPosition+1][i]==self.currentColor:
                self.blockArray[self.shipPosition][i]=0-self.currentColor
                self.blockArray[self.shipPosition+1][i]=0-self.currentColor
                self.hasRight = True
            if self.shipPosition>0 and self.blockArray[self.shipPosition-1][i]==self.currentColor:
                self.blockArray[self.shipPosition][i]=0-self.currentColor
                self.blockArray[self.shipPosition-1][i]=0-self.currentColor
                self.hasLeft = True
            if self.hasRight==False and self.hasLeft==False and self.hasTop==False:
                self.blockArray[self.shipPosition][i]=self.currentColor
            self.hasTop = False
            self.hasRight = False
            self.hasLeft = False
        for communism in range(0,100):
            for x in range(0,10):
                for y in range(1,15):
                    if self.blockArray[x][y]<0:
                        self.lenin=self.blockArray[x][y]
                        if x<9 and self.blockArray[x+1][y]==abs(self.lenin):
                            self.blockArray[x+1][y]=self.lenin
                        if x>0 and self.blockArray[x-1][y]==abs(self.lenin):
                            self.blockArray[x-1][y]=self.lenin
                        if y<14 and self.blockArray[x][y+1]==abs(self.lenin):
                            self.blockArray[x][y+1]=self.lenin
                        if x>1 and self.blockArray[x][y-1]==abs(self.lenin):
                            self.blockArray[x][y-1]=self.lenin
                        self.blockArray[x][y]=0
                                
    
            
#Farbrandomizer        
    def randomColor(self):
        self.currentColor = random.randint(1,5)
        if(self.colorsPresent[self.currentColor-1]==False):
            self.randomColor()
#Hier faengt der Spass an
    def play(self):
        helper = self.helper
        self.letters.animateString(4,"PIXEL SHOOTER",(255,0,0), 50, callback=self.ledcyclefun)
        #np = self.np
        for i in range(10):
            for j in range(15):
                self.helper.setPixel(i,j,(0,0,0))
        for y in range(8,15):
            for x in range(0,10):
                self.randomColor()
                self.blockArray[x][y]=self.currentColor
        while(self.blocksPresent==True):
            for x in range(0,10):
                for y in range(0,15):
                    if(self.blockArray[x][y]!=0):
                        self.helper.setPixel(x,y,self.colors[abs((self.blockArray[x][y]))])
            for x in range(0,10):
                for y in range(0,15):
                    if(self.blockArray[x][y]==0):
                        self.helper.setPixel(x,y,(0,0,0))
            for i in range(10):
                self.helper.setPixel(i,0,(0,0,0))
            b = self.helper.getButtons()^255
            if((b&2==2)and(self.shipPosition>0)):
                self.shipPosition-=1
            if((b&8==8)and(self.shipPosition<9)):
                self.shipPosition+=1
            self.helper.setPixel(self.shipPosition,0,self.colors[abs(self.currentColor)])
            self.helper.np.write()
            for i in range(0,5):
                self.colorsPresent[i]=False
                for x in range(0,10):
                    for y in range(1,15):
                        if self.blockArray[x][y]==i+1:
                            self.colorsPresent[i]=True
            if((b&4==4)):#Exekutionsbefehl
                self.shoot()
                self.randomColor()
            self.blocksPresent=False
            for x in range(0,10):
                for y in range(1,15):
                    if self.blockArray[x][y]!=0:
                        self.blocksPresent=True
        if(self.shots>93): #"Belobungen" im Abhaengigkeit der Anzahl Schuesse
            self.letters.animateString(4,str(self.shots)+" SHOTS FIRED    PATHETIC",(255,0,0), 50, callback=self.ledcyclefun)
        elif(self.shots>81):
            self.letters.animateString(4,str(self.shots)+" SHOTS FIRED    IT IS OKAY TO BE BAD",(255,0,0), 50, callback=self.ledcyclefun)
        elif(self.shots>69):
            self.letters.animateString(4,str(self.shots)+" SHOTS FIRED    GET LUCKY",(255,0,0), 50, callback=self.ledcyclefun)
        elif(self.shots>57):
            self.letters.animateString(4,str(self.shots)+" SHOTS FIRED    AWESOME",(255,0,0), 50, callback=self.ledcyclefun)
        elif(self.shots>45):
            self.letters.animateString(4,str(self.shots)+" SHOTS FIRED    PIXELSLAYER",(255,0,0), 50, callback=self.ledcyclefun)
        else:
            self.letters.animateString(4,str(self.shots)+" SHOTS FIRED    GODLIKE",(255,0,0), 50, callback=self.ledcyclefun)
#Alles hat ein Ende


from helper import Helper #import der Klasse
helper = Helper() #erzeugen der Instanz
ps=pixelshooter(helper)
ps.play()