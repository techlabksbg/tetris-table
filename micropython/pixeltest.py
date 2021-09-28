import machine
import neopixel
np = neopixel.NeoPixel(machine.Pin(4), 150, timing=True)

i=0;
while True:
    np[i] = (100,20,50)
    np[(i+149)%150] = (0,0,0)
    np.write()
    i=(i+1)%150
    
