class RGB_Bitmap:
    def __init__(self, x,y,pixels):
        self.x = x
        self.y = y
        self.p = pixels

    def setPixel(self, np, x,y,what):
        x=9-x
        if x%2==1:
            y=14-y
        np[x*15+y] = what

    def draw(self, np, atx, aty):
        for x in range(self.x):
            for y in range(self.y):
                a = a+atx
                b = b+aty
                if (a>=0 and a<10 and b>=0 and b<15):
                    self.setPixel(np, a,b,pixels[x+(self.y-1-y)*self.y])

                

class BW_Bitmap:
    def __init__(self, x,y,lines):
        self.x = x
        self.y = y
        self.l = lines

    def setPixel(self, np, x,y,what):
        x=9-x
        if x%2==1:
            y=14-y
        np[x*15+y] = what

    def draw(self, np, atx, aty, fgcolor, bgcolor):
        for x in range(self.x):
            for y in range(self.y):
                a = a+atx
                b = b+aty
                if (a>=0 and a<10 and b>=0 and b<15):
                    pixel = (self.lines[y] >> x) & 1
                    if pixel==1 and fgcolor!=None:
                        self.setPixel(np, a,b, fgcolor)
                    if pixel==0 and bgcolor!=None:
                        self.setPixel(np, a,b, bgcolor)


