#include "tetristable.h"

#include <Adafruit_MCP23X17.h>
Adafruit_MCP23X17 mcp;

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
