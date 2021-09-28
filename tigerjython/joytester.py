from helper import Helper
helper = Helper()

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

while True:
    j=helper.getJoyStick(0)+helper.getJoyStick(1)
    print("X:%d  Y:%d  B:%d       X:%d  Y:%d  B:%d" % (j[0], j[1], j[2], j[3], j[4], j[5]))
    time.sleep_ms(200)
    
    