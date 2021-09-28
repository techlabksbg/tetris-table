from gpanel import *


  
SIZE=40


class NeoPixel:
    def __init__(self, pin, num, timing):
        self.mouse={"x":0, "y":0, "b":0}
        this = self
        def mouseMovedCallback(x,y):
            this.mouse["x"] = x
            this.mouse["y"] = y
            this.mouse["b"] = (1 if isLeftMouseButton() else (2 if isRightMouseButton() else 0))
        
        def mouseReleasedCallback(x,y):
            this.mouse["b"] = 0
            
            
        makeGPanel(Size(SIZE*10,SIZE*17),mouseMoved = mouseMovedCallback, mouseDragged = mouseMovedCallback, mousePressed=mouseMovedCallback, mouseReleased=mouseReleasedCallback);
        window(0,10,0,17);
        self.pixel = []
        self.num=num
        for i in range(0,num):
            self.pixel.append((0,0,0))
        
            
    
    def __getitem__(self, index):
        return self.pixel[index]
    
    def __setitem__(self,index, what):
        self.pixel[index]=what
    
    def write(self):
        for i in range(0,self.num):
            x=i//15
            y=i%15
            if (x%2==1):
                y = 14-y
            x = 9-x
            y=y+1 
            #print(str(i)+" -> x="+str(x)+" y="+str(y))
            setColor(makeColor(self.pixel[i]))
            fillRectangle(x, y, x+1, y+1)
            
    def showButtons(self, how):
        for i in range(0,8):
            setColor("red" if ((how >> i) & 1 == 1) else "darkred")
            fillCircle((3-i%4 if i>3 else i%4)+3.5, (i//4)*16+0.5, 0.5)
    def getTaste(self):
        if kbhit():
            return getKey();
        return None