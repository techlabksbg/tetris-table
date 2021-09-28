#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <Adafruit_MCP23X17.h>

#define MCP_SDA 23
#define MCP_SCL 22
#define MCP_ADDR 0x26

Adafruit_NeoPixel *pixels;


void setup() {
  Serial.begin(115200);
  pixels = new Adafruit_NeoPixel(150, 4, NEO_GRB + NEO_KHZ800);
  pixels->clear();
  Wire.begin(MCP_SDA, MCP_SCL);  // SDA, SCL

  Wire.beginTransmission(MCP_ADDR);
  Wire.write(0x00);Wire.write(0xff); // All input Reg A
  Wire.endTransmission();

  Wire.beginTransmission(MCP_ADDR);
  Wire.write(0x0c);Wire.write(0xff); // All pullup Reg A
  Wire.endTransmission();

  Wire.beginTransmission(MCP_ADDR);
  Wire.write(0x01);Wire.write(0x00); // All Output B
  Wire.endTransmission();
 
}

void setButtonLEDs(byte leds) {
  Wire.beginTransmission(MCP_ADDR);
  Wire.write(0x13);Wire.write(leds); // Output-State on Reg B
  Wire.endTransmission();  
}

byte getButtons() {
  Wire.beginTransmission(MCP_ADDR);
  Wire.write(0x12);  // Input-State on Reg A
  byte buttons = Wire.read(); 
  Wire.endTransmission();  
  return buttons;
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