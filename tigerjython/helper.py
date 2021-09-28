#
# TIGERJYTHON Version. Diese Datei funktioniert auf dem ESP32 nicht!
#


import machine
import neopixel
import mcp





class Helper:
    
    # Ports, an dem die Joysticks haengen (X,Y,Switch)
    JOYSTICKS = [[34,35,25],[33,32,26]]
    # Adresse vom PortExpander
    MCP_ADDRESS = 0x27
    
    def __init__(self):
        self.np = neopixel.NeoPixel(machine.Pin(4), 150, timing=True)
        self.np.write();
        self.mcp = mcp.MCP(Helper.MCP_ADDRESS, self.np)
        self.joyPorts = [[machine.ADC(machine.Pin(Helper.JOYSTICKS[0][0])), 
                          machine.ADC(machine.Pin(Helper.JOYSTICKS[0][1])), 
                          machine.Pin(Helper.JOYSTICKS[0][2],machine.Pin.IN, machine.Pin.PULL_UP)],
                         [machine.ADC(machine.Pin(Helper.JOYSTICKS[1][0])), 
                          machine.ADC(machine.Pin(Helper.JOYSTICKS[1][1])), 
                          machine.Pin(Helper.JOYSTICKS[1][2],machine.Pin.IN, machine.Pin.PULL_UP)]]
        
        
    # Nullpunkt unten links, x nach rechts, y nach oben
    def pixelNumber(self, x,y):
        return (9-x)*15 + (y if x%2==1 else 14-y) 
    
    
    def setPixel(self, x,y,c):
        if (x>=0 and x<=9 and y>=0 and y<=14):
            n = self.pixelNumber(x,y)
            self.np[n]=c   
        
    def getPixel(self, x,y):
        if (x>=0 and x<=9 and y>=0 and y<=14):
            n = self.pixelNumber(x,y)
            return self.np[n]
        return (0,0,0)
        
    def invertPixel(self, x,y):
        if (x>=0 and x<=9 and y>=0 and y<=14):
            n = self.pixelNumber(x,y)
            c = self.np[n]
            self.np[n]=  (255-c[0], 255-c[1], 255-c[2])
            
    # Pixel mit Transparenz (a=0 durchsichtig, a=1 voll deckend), adaptiert vom Code von Fabio
    def setPixelMix(self,x,y,c,a):
        i=pixelNumber(x,y)
        self.np[i] = (int(c[0]*a+self.np[i][0]*(1-a)),int(c[1]*a+self.np[i][1]*(1-a)),int(c[2]*a+self.np[i][2]*(1-a)))
        
        
    def getButtons(self):
        return self.mcp.getButtons()
    
    def setLeds(self,l):
        self.mcp.setLeds(l)
        
    def getLeds(self):
        return self.mcp.getLeds()
    
    def getJoyStick(self, n):        
        x=self.np.mouse["x"]
        y=self.np.mouse["y"]
        b=self.np.mouse["b"]
        if b==n+1:
            b=0
        else:
            b=1
        if (n==0 and y>8 ) or (n==1 and y<9):
            x=1800
            y=1800
        else:
            x=int(x*4095/9)
            if n==0:
                y=int(y*4095/8)
            else:
                y=int((y-8)*4095/9)
        return [int(x),int(y),b]
    
        
    
        
