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


class Rickroll():
    def __init__(self, helper):
        self.helper = helper
        
        
    def play(self):
        while self.helper.getButtons()!=255:
            pass
        gamma = [i*i//256 for i in range(256)]
        try:
            while self.helper.getButtons()==255:
                f = open("rickroll.raw","rb")
                for i in range(533):
                    for y in range(10):
                        for x in range(15):
                            r = gamma[ord(f.read(1))]
                            g = gamma[ord(f.read(1))]
                            b = gamma[ord(f.read(1))]
                            self.helper.setPixel(y,x,(r,g,b))
                    self.helper.np.write()
                    if self.helper.getButtons()!=255:
                        break
                f.close()
        except:
            pass
        while self.helper.getButtons()==255:
            pass
        
