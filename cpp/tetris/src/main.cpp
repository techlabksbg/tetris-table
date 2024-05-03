#include <Arduino.h>

#include "tetristable.h"
#include "colorspotlight.h"
#include "tetris.h"

TetrisTable t;
Tetris *tetris;

void setup() {
  Serial.begin(115200);
  t.begin();
  t.pixels->clear();
  t.show();
  tetris = new Tetris(&t);
}


void loop() {  
  tetris->loop(); 
}