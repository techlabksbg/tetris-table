import machine
import time
from machine import I2C

class MCP:
    def __init__(self,address=0x26, np=None):
        self.address = address
        self.i2c=I2C(sda=machine.Pin(23), scl=machine.Pin(22))
        self.rega = bytearray(1)
        self.rega[0]=0;
        self.regb = bytearray(1)
        reg = bytearray(1)
        reg[0]=0xff
        self.i2c.writeto_mem(self.address, 0x00, reg)  # All Input Register A
        self.i2c.writeto_mem(self.address, 0x0c, reg)  # All Pullups Register A
        reg[0]=0x00
        self.i2c.writeto_mem(self.address, 0x01, reg)  # All Output Register B

    def setLeds(self, what):
        self.regb[0] = what
        self.i2c.writeto_mem(self.address, 0x13, self.regb)  # Write to GPIOB
        
    def getLeds(self):
        return self.regb
    
    def getButtons(self):
        self.i2c.readfrom_mem_into(self.address, 0x12,self.rega) # Read GPIOA
        return self.rega[0]

# GPIO 0x12 (A), 0x13 (B)



