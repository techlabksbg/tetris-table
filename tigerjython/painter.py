

class Painter():
    
    def __init__(self, helper):
        self.helper = helper
        self.x = 4
        self.y = 7
        
        
    def move(self):
        # Pixel loeschen
        self.helper.setPixel(self.x,self.y, (0,0,0))
        # Pixel anpassen
        j = self.helper.getJoyStick(0) # -> [x,y,b]
        self.x = int(10*j[0]//4096)
        self.y = int(15*j[1]//4096)
        # Pixel zeichnen
        self.helper.setPixel(self.x,self.y, (255,200,0))
        self.helper.np.write()
        
    def play(self):
        while self.helper.getJoyStick(0)[2]==1:
            self.move()
            
        
# Nur wenn Datei direkt ausgefuehrt wird:    
if __name__== "__main__":
    from helper import Helper
    p=Painter(Helper())
    p.play()
    
    
