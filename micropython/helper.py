import machine


class Helper:
    MCP_ADDRESS = 0x27
    
    # Ports, an dem die Joysticks hängen (X,Y,Switch)
    JOYSTICKS = [[34,35,32],[33,25,26]]
    
    def __init__(np, mcp):
        self.np = np
        self.mcp = mcp
        self.joyPorts = [[machine.ADC(machine.Pin(JOYSTICKS[0][0])), 
                          machine.ADC(machine.Pin(JOYSTICKS[0][1])), 
                          machine.Pin(JOYSTICKS[0][2],machine.Pin.IN, machine.Pin.PULL_UP)],
                         [machine.ADC(machine.Pin(JOYSTICKS[1][0])), 
                          machine.ADC(machine.Pin(JOYSTICKS[1][1])), 
                          machine.Pin(JOYSTICKS[1][2],machine.Pin.IN, machine.Pin.PULL_UP)]]
        
        
        
    def setPixel(self, x,y,c):
        self.np[x+y]=c   # Diese Funktion muss ersetzt werden, je nachdem, wie der LED-Streifen eingebaut ist
        
    def getButtons(self):
        return self.mcp.getButtons()   # Diese Funtion muss eventuell angepasst werden, wenn die Buttons anders angeschlossen sind.
    
    def setLeds(self,l):
        self.mcp.setLeds(l)  # Diese Funktion muss enventuell angepasst werden, wenn die LEDs anders angeschlossen sind.
        
    def getLeds(self):
        return self.mcp.getLeds() # Dito
    
    def getJoyStick(self, n):
        return [self.joyPorts[n][0].read(), self.joyPorts[n][1].read(), self.joyPorts[n][1].value()]
    
        
    
        
