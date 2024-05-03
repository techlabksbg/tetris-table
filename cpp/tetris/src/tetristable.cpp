#include "tetristable.h"

#include <Adafruit_MCP23X17.h>
Adafruit_MCP23X17 mcp;

uint32_t letterBitMaps[] = {31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 31599, 32767, 0, 8338, 45, 24445, 10142, 17057, 27611, 18, 17556, 5265, 341, 1488, 5120, 448, 8192, 4772, 15214, 9370, 29347, 14499, 18925, 14543, 31694, 4775, 31727, 14831, 1040, 5136, 17492, 3640, 5393, 8359, 25578, 23530, 15083, 25166, 15211, 29647, 5071, 27598, 23533, 29847, 11044, 23277, 29257, 23549, 24573, 11114, 4843, 28522, 22507, 14478, 9367, 27501, 9581, 24557, 23213, 9389, 29351, 29263, 2184, 31015, 42, 28672, 17, 31640, 15193, 25200, 27508, 26480, 9684, 85872, 23385, 9346, 88324, 22249, 29843, 24568, 23384, 11088, 47960, 158576, 4720, 15600, 25786, 27496, 12136, 32744, 21672, 85352, 30648, 25686, 9234, 13587, 30, 32767};

void TetrisTable::paintChar(int x, int y, char c, uint32_t color, int bg_color) {
    for (int j=0; j<18; j++) {
        int a = x+j%3;
        int b = y+5-j/5;
        if (letterBitMaps[c] & (1<<j)) {
            setPixel(a,b,color);
        } else if (bg_color>=0) {
            setPixel(a,b,bg_color);
        }
        if (j<6 && bg_color>=0) {
            setPixel(x+3,y+j, bg_color);
        }
    }
}

void TetrisTable::paintString(int x, int y, char *s, uint32_t color, int bg_color) {
    while (*s && x<10) {
        if (x>-4) paintChar(x,y,*s,color,bg_color);
        x+=4;
        s++;
    }
}
    
bool TetrisTable::begin() {
    pixels = new Adafruit_NeoPixel(150, 4, NEO_GRB + NEO_KHZ800);
    pixels->clear();

    Wire.begin(MCP_SDA, MCP_SCL);

    if (!mcp.begin_I2C(MCP_ADDR)) {
        Serial.println("MCP not working :-(");
        return false;
    }
    for (int pin=0; pin<8; pin++) {
        mcp.pinMode(pin, INPUT_PULLUP);
    }
    for (int pin=8; pin<16; pin++) {
        mcp.pinMode(pin, OUTPUT);
    }
    setButtonLEDs(0);
    return true;
}

void TetrisTable::setPixel(int x, int y, uint32_t color) {
    if (x<0 || x>9 || y<0 || y>14) return;
    x=9-x;
    int i = x*15+ (x%2==1 ? 14-y%15 : y%15);
    pixels->setPixelColor(i, color);
}

uint32_t TetrisTable::color(uint8_t r, uint8_t g, uint8_t b) {
    return ((uint32_t)r << 16) | ((uint32_t)g <<  8) | b;
}

void TetrisTable::show() {
    pixels->show();
}

void TetrisTable::setButtonLEDs(uint8_t leds) {
    mcp.writeGPIOB(leds);
    ledState = leds;
}
uint8_t TetrisTable::getButtonLEDs() {
    return ledState;
}

uint8_t TetrisTable::getButtons() {
    return mcp.readGPIOA()^255;
}
