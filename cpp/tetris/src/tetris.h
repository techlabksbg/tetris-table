#pragma once
#include "tetristable.h"

class Tetris {

    public:
    Tetris(TetrisTable *t);
    int loop();
    void begin();

        int blocks[7][4] = {{0,4,8,12},  {1,4,5,8}, {0,1,5,6}, {1,2,4,5}, {0,4,8,9}, {1,5,8,9},{0,1,4,5}};
        uint32_t colors[7] = {0xff0000, 0xffff00, 0x00ff00, 0xff00ff, 0x00ffff, 0x0000ff, 0xff4000};
        int block[4][2];
        int neublock[4][2];
        int blockNumber = 0;
        int feld[10][15];
        unsigned long lastPress[4] = {0,0,0,0};
        unsigned long lastFall = 0;
        unsigned long fallTime = 350;
        int keyRepeat=200;
        unsigned long nextAnimation = 0;
        int animationCount;
        int animatedLines[4] = {-1,-1,-1,-1};
        TetrisTable *t;

    void reset();
    void newblock();
    void showblock(uint32_t color);
    bool testblock();
    void rotate(int dir);
    void setblock(bool erase=true);
    bool down();
    void move(int d);
    int checklines();
};
