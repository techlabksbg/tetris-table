from config import Config
import time   # time.sleep_ms() und time.ticks_ms()
from bitmaps import BW_Bitmap
from letters import Letters
from bareserver import BareServer
try:
  import usocket as socket
except:
  import socket

import network

import esp
esp.osdebug(None)

import gc


class WebServer:
    def __init__(self, np, buttons):
        self.np = np
        self.buttons = buttons

    def connect(self):
        self.station = network.WLAN(network.STA_IF)

        self.station.active(True)
        self.station.connect(Config.ssid, Config.password)
        
        icon = BW_Bitmap(10,10,(0b1111000,0b110000110,0b1000110001,0b11001100,0b100000010,0b1111000,0b10000100,0b0,0b110000,0b110000))
    
        self.np.fill((0,0,0))
        icon.draw(self.np, 0, 5, (255,255,0))
        self.np.write()
        
        while self.station.isconnected() == False:
            time.sleep_ms(100)
            icon.draw(self.np, 0, 5,(0,0,255))
            self.np.write()

        print('Connection successful')
        print(self.station.ifconfig())

        icon.draw(self.np, 0, 5, (0,255,0))
        ip = self.station.ifconfig()[0].split(".")[3]
        print(ip)
        letters = Letters(self.np)
        for i in range(len(ip)):
            letters.paintChar(i*3, 0, ord(ip[i]), (255 if i==1 else 0, 0,255 if i!=1 else 0))
        self.np.write()



    def play(self):
        gc.collect()
        self.connect()
        b = BareServer()
        b.serve()

