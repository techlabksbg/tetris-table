/**
 * Small colored spotlight demo, same as in python
 * for speed comparison.
 * @author Ivo Blöchliger
 */

#include "tetristable.h"

#include <vector>
using namespace std;

extern TetrisTable t;

float dist(int x, int y, vector<float> &v) {
    return (x-v[0])*(x-v[0]) + (y-v[1])*(y-v[1]);
}

void colorSpotlightDemo() {
    vector<vector<float>> points;
    vector<float> angles;
    vector<float> omegas;
    vector<vector<float>> vecs;
    for (int i=0; i<3; i++) {
        points.push_back(vector<float>{});
        points[i].push_back(rand()%10);
        points[i].push_back(rand()%15);
        angles.push_back(random(10000)/10000.0*2*PI);
        omegas.push_back(random(10000)/10000.0*0.004+0.004);
        vecs.push_back(vector<float>{0.0, 0.0});
    }
    while (t.getButtons()==0) {
        for (int i=0; i<3; i++) {
            vecs[i][0] = cos(angles[i])*0.2;
            vecs[i][1] = sin(angles[i])*0.2;
            angles[i]+=omegas[i];
            for (int j=0; j<2; j++) {
                points[i][j]+=vecs[i][j];
            }
            points[i][0] = fmodf(points[i][0], 10);
            if (points[i][0]<0) points[i][0]+=10;
            points[i][1] = fmodf(points[i][1], 15);
            if (points[i][1]<0) points[i][1]+=15;
        }
        for (int x=0; x<10; x++) {
            for (int y=0; y<15; y++) {
                uint32_t c = 0;
                for (int i=0; i<3; i++) {
                    c = (c<<8) | ((int)(1.0/(1.0+2.0*dist(x,y,points[i]))*255));
                }
                t.setPixel(x,y,c);
            }
        }
        t.show();
    }
}