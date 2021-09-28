#include <Arduino.h>

#include "tetristable.h"

TetrisTable t;

void setup() {
  Serial.begin(115200);
  t.begin();
}

void loop() {
  for (int i=0; i<150; i++) {
    Serial.printf("x=%d, y=%d\n", i%10, i/10);
    t.setPixel(i%10, i/10, t.color(i*13%256, (i*17+100)%256, (i*28+200)%256));
    t.show();
    delay(100);
    t.setButtonLEDs(1 << (i%8));
    Serial.println(t.getButtons());
  }
  t.pixels->clear();
}