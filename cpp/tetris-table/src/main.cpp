#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <Adafruit_MCP23X17.h>

#define MCP_SDA 23
#define MCP_SCL 22
#define MCP_ADDR 0x20

Adafruit_NeoPixel *pixels;
Adafruit_MCP23X17 mcp;



void setup() {
  Serial.begin(115200);
  pixels = new Adafruit_NeoPixel(150, 4, NEO_GRB + NEO_KHZ800);
  pixels->clear();

  Wire.begin(MCP_SDA, MCP_SCL);

  if (!mcp.begin_I2C(MCP_ADDR)) {
    Serial.println("MCP not working :-(");
  }

  for (int pin=0; pin<8; pin++) {
    mcp.pinMode(pin, INPUT_PULLUP);
  }
  for (int pin=8; pin<16; pin++) {
    mcp.pinMode(pin, OUTPUT);
  }
 
}

void setButtonLEDs(uint8_t leds) {
  mcp.writeGPIOB(leds);
}

uint8_t getButtons() {
  return mcp.readGPIOA()^255;
}



void loop() {
  for (int i=0; i<150; i++) {
    pixels->setPixelColor(i, pixels->Color(20,50,0));
    pixels->show();
    delay(100);
    setButtonLEDs(1 << (i%8));
    Serial.println(getButtons());
  }
  pixels->clear();
}