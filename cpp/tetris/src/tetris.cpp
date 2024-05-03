#include "tetris.h"

using namespace std;

Tetris::Tetris(TetrisTable *t) {
    this->t = t;
    reset();
}

void Tetris::reset() {
    for (int x=0; x<10; x++) {
        for (int y=0; y<15; y++) {
            feld[x][y] = 0;
        }
    }
    t->pixels->clear();
    newblock();
    setblock(false);
    lastFall = millis();
    nextAnimation = 0;
    for (int i=0; i<4; i++) animatedLines[i]=-1;
    for (int i=0; i<4; i++) {
        lastPress[i] = 0;
    }
}


void Tetris::begin() {
    for (int x=9; x>-20;x--) {
        t->paintString(x,5,"Tetris", 0xff5500);
        t->show();
        delay(200);
    }
    reset();

}

void Tetris::newblock() {
    blockNumber = random(7);
    for (int i=0; i<4; i++) {
        neublock[i][0] = blocks[blockNumber][i]%4+4;
        neublock[i][1] = blocks[blockNumber][i]/4+14;
    }
}

void Tetris::showblock(uint32_t color) {
    for (int i=0; i<4; i++) {
        t->setPixel(block[i][0], block[i][1], color);
    }
    t->show();
}

bool Tetris::testblock() {
    for (int i=0; i<4; i++) {
        if (neublock[i][0]<0 || neublock[i][0]>9 || neublock[i][1]<0) {
            return false;
        }
        if (neublock[i][1]<15 && feld[neublock[i][0]][neublock[i][1]]!=0) {
            Serial.printf("testblock i=%d, at %d,%d feld = %d\n", i, neublock[i][0], neublock[i][1], feld[neublock[i][0]][neublock[i][1]]);
            return false;
        }
    }
    return true;
}

void Tetris::setblock(bool erase) {
    if (erase) showblock(0);
    for (int i=0; i<4; i++) {
        block[i][0] = neublock[i][0];
        block[i][1] = neublock[i][1];
    }
    showblock(colors[blockNumber]);
}

void Tetris::rotate(int dir) {
    int mx=20, my=20;
    int nx=20, ny=20;
    for (int i=0; i<4; i++) {
        if (block[i][0]<mx) mx=block[i][0];
        if (block[i][1]<my) my=block[i][1];
        if (dir>0) {
            neublock[i][0] = -block[i][1];
            neublock[i][1] = block[i][0];
        } else {
            neublock[i][0] = block[i][1];
            neublock[i][1] = -block[i][0];
        }
        if (neublock[i][0]<nx) nx=neublock[i][0];
        if (neublock[i][1]<ny) ny=neublock[i][1];
    }
    int mmx = 0;
    for (int i=0; i<4; i++) {
        neublock[i][0] += (mx-nx);
        neublock[i][1] += (my-ny);
        if (mmx<neublock[i][0]) {
            mmx = neublock[i][0];
        }
    }
    if (testblock()) {
        setblock();
        return;
    }
    if (mmx>9) {
         for (int i=0; i<4; i++) {
            neublock[i][0] -= mmx-9;
         }
    }
    if (testblock()) {
        setblock();
        return;
    }
}

// Returns
//   0  all done
//   1  animation going
int Tetris::checklines() {
    if (nextAnimation>0) {
       if (millis()>nextAnimation) {
            if (animationCount<11) { 
                nextAnimation+=100;
                for (int i=0; i<4; i++) {
                    if (animatedLines[i]>=0) {
                        for (int x=0; x<10; x++) {
                            uint32_t color = 0;
                            if (feld[x][animatedLines[i]]>0) {
                                color = colors[feld[x][animatedLines[i]]-1];
                            }
                            t->setPixel(x,animatedLines[i], color);
                        }
                    }
                }
                animationCount+=1;
                if (animationCount>10) {
                    for (int i=0; i<4; i++) {
                        if (animatedLines[i]>=0) {
                            for (int x=0; x<10; x++) {
                                feld[x][animatedLines[i]] = 0;
                            }
                        }
                    }
                }
                return 1;
            }

            for (int i=0; i<4; i++) {
                if (animatedLines[i]>0) {
                    for (int x=0; x<10; x++) {
                        for (int y=animatedLines[i]; y<15; y++) {
                            feld[x][y]=(y!=14) ? feld[x][y+1] : 0;
                            uint32_t color = 0; 
                            if (feld[x][y]>0) {
                                color = colors[feld[x][y]-1];
                            }
                            t->setPixel(x,y,color);
                        }
                    }
                    animatedLines[i]=-1;
                    nextAnimation = millis()+50;
                    t->show();
                    return 1;
                }
            }
            // Animation has finished
            nextAnimation = 0;
            return 0;
       }
    } else {
        int cleared = 0;
        for (int y=0; y<15; y++) {
            int full = 0;
            for (int x=0; x<10; x++) {
                if (feld[x][y]>0) {
                    full++;
                }
            }
            if (full==10) {
                animatedLines[cleared++]=y;
            }
        }
        if (cleared>0) { // start animation
            nextAnimation=millis();   
            animationCount=0;
            return 1;
        }
    }
    return 0;
}

int Tetris::loop() {
    if (nextAnimation>0) {
        checklines();
        return 0;
    }
    int status = 0;
    auto b = t->getButtons();
    auto now = millis();
    bool pressed[4] = {false, false, false, false};
    for (int i=0; i<4; i++) {
        if (b & (1<<i)) {
            if (lastPress[i]==0 || (now-lastPress[i])>keyRepeat) {
                lastPress[i] = now;
                pressed[i] = true;
            }
        } else {
            lastPress[i] = 0;
        }
    }
    /*if (pressed[3]) {
        //Serial.println("Down");
        if (!down()) {
            status = 1;
        }
        lastFall = millis();
    } */
    if (pressed[3]) {
        move(-1);
        //Serial.println("Left");
    }
    if (pressed[2]) {
        rotate(-1);
        //Serial.println("Rotate");
    }
    if (pressed[1]) {
        rotate(1);
        //Serial.println("Rotate");
    }
    if (pressed[0]) {
        move(1);
        //Serial.println("Right");
    } 

    if (millis()-lastFall > fallTime) {
        lastFall = millis();
        if (!down()) {
            newblock();
            if (!testblock()) {
                status = 1;
            } else {
                setblock();
            }
        }
        //Serial.println("Fall");
    }
    if (status!=0) reset();
    return status;
}

void Tetris::move(int d) {
    for (int i=0; i<4; i++) {
        neublock[i][0] = block[i][0]+d;
        neublock[i][1] = block[i][1];
    }
    if (testblock()) {
        setblock();
    } else {
        Serial.println("Move failed");
    }

}

bool Tetris::down() {
    for (int i=0; i<4; i++) {
        neublock[i][0] = block[i][0];
        neublock[i][1] = block[i][1]-1;
    }
    if (testblock()) {
        setblock();
    } else {
        for (int i=0; i<4; i++) {
            if (block[i][1]>14) {
                return false;
            }
            feld[block[i][0]][block[i][1]] = 1+blockNumber;
        }
        if (checklines()==0) {
            newblock();
            if (testblock()) {
                setblock(false);
            } else {
                return false;
            }
        }
    }
    return true;
}