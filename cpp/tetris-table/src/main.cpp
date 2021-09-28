#include <Arduino.h>

#include "tetristable.h"

TetrisTable t;

void setup() {
  Serial.begin(115200);
  t.begin();
}

void loop() {
  unsigned long start = millis();
  for (int i=0; i<150; i++) {
    //Serial.printf("x=%d, y=%d\n", i%10, i/10);
    t.setPixel(i%10, i/10, t.color(i*13%256, (i*17+100)%256, (i*28+200)%256));
    t.show();
    //delay(10);
    t.setButtonLEDs(1 << (i%8));
    //Serial.println(t.getButtons());
  }
  start = millis()-start;
  Serial.printf("150 cycles in %ld ms -> %f fps\n", start, (1000*150.0/start));
  t.pixels->clear();
  
}