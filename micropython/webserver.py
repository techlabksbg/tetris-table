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
    
        self.np.fill(0)
        icon.draw(self.np, 0, 5,0xffff00)
        self.np.write()
        
        while self.station.isconnected() == False:
            time.sleep_ms(100)
            icon.draw(self.np, 0, 5,0x0000ff)
            self.np.write()

        print('Connection successful')
        print(station.ifconfig())

        icon.draw(self.np, 0, 5,0x00ff00)
        ip = station.ifconfig()[0].split(".")[3]
        letters = Letters(self.np)
        for i in len(ip):
            letters.drawChar(ip[i], i*3, 0)
        self.np.write()



    def play(self):
        gc.collect()
        self.connect()
        b = BareServer()
        b.serve()

