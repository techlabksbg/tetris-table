import time

# Hack to get ticks_ms() method in Tigerjython working
if not hasattr(time, 'ticks_ms'):
    from types import MethodType
    def ticks_ms(self):
        return int(round(self.time() * 1000))
    time.ticks_ms = MethodType(ticks_ms, time)
    
    def sleep_ms(self,a):
        time.sleep(a/1000.0)
    time.sleep_ms = MethodType(sleep_ms, time)
# END of Hack

class Letters:
    def __init__(self,helper):
        self.helper = helper
        # 3 by 6 Pixels -> 18 Bits als Ganzzahl fuer jeden ASCII-Code
        self.letters = [31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 32767, 0, 8338, 45, 24445, 10142, 17057, 27611, 18, 17556, 5265, 341, 1488, 5120, 448, 8192, 4772, 15214, 9370, 29347, 14499, 18925, 14543, 31694, 4775, 31727, 14831, 1040, 5136, 17492, 3640, 5393, 8359, 25578, 23530, 15083, 25166, 15211, 29647, 5071, 27598, 23533, 29847, 11044, 23277, 29257, 23549, 24573, 11114, 4843, 28522, 22507, 14478, 9367, 27501, 9581, 24557, 23213, 9389, 29351, 29263, 2184, 31015, 42, 28672, 17, 31640, 15193, 25200, 27508, 26480, 9684, 85872, 23385, 9346, 88324, 22249, 29843, 24568, 23384, 11088, 47960, 158576, 4720, 15600, 25786, 27496, 12136, 32744, 21672, 85352, 30648, 25686, 9234, 13587, 30, 32767]

        # Python 2.7 Closure hack, Callback   
        ledcycle={'v':0}
        this = self
        def ledcyclefun():
            this.helper.setLeds(1 << ledcycle['v'])
            ledcycle['v']=(ledcycle['v']+1)%8
        self.ledcyclefun = ledcyclefun
        
    def paintChar(self, x, y, char, color, bgColor=None):
        for j in range(0,18):
            a = x+j%3
            b = y+5-j//3
            if self.letters[char] & (1 << j) !=0:
                if color=="inv":
                    self.helper.invertPixel(a,b)
                else:
                    self.helper.setPixel(a,b,color)
            else:
                if bgColor!=None and bgColor!="inv":
                    self.helper.setPixel(a,b,bgColor)
                        
        if bgColor!=None:
            for i in range(0,6):
                self.helper.setPixel(x+3,y+i,bgColor)
                
                
    
    def animateString(self,y,s,color,delay=300, bgColor=(0,0,0), callback=None):
        l = len(s)
        x = 9
        while x>-4*l:
            for i in range(0,len(s)):
                if (x+4*i > -4 and x+4*i<10):
                    self.paintChar(x+4*i,y,ord(s[i]), color, bgColor)
            self.helper.np.write()
            if callback!=None:
                callback()
            time.sleep_ms(delay)
            if (color=="inv"):
                for i in range(0,len(s)):
                    if (x+4*i > -4 and x+4*i<10):
                        self.paintChar(x+4*i,y,ord(s[i]), color, bgColor)
            x=x-1

                   
                        
    def play(self):
        self.animateString(5,"TETRIS TABLE EF INFORMATIK", "inv", 100, None, self.ledcyclefun)