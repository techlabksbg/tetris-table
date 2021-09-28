largeknobs=true;

resetbutton = 12.5;

thick=4;  // material thickness
pthick=0.5;  // Dicke Pappe
// A2: 420 x 594
twidth=414;  // total width
theight=588;  // total height

led=100.0/3;   // square for 1 led
ledw=10;     // total leds x
ledh=15;     // total leds y

eps=0.001;   // for boolean ops

idepth=50;   // inner depth
tdepth=idepth+2*thick;  // total depth

screendepth=26;
glassthick=2;

screenoffset=1;   // inner offset
screenborder=1;  // offset from inner border

shortborder = (theight-ledh*led)/2+screenoffset;
longborder = (twidth-ledw*led)/2+screenoffset;

shortnumdents=9;
longnumdents=13;

lednotch=14;

//include <cover.scad>

module corner(r=0.5,rr=0.2) {
    
    difference() {
        union() {
            translate([-r,-r]) square([r+rr, r+rr]);
            translate([rr,rr]) circle(r=r);
        } // end union, start difference
        translate([rr,-r]) circle(r=rr);
        translate([-r,rr]) circle(r=rr);
    }
    
    //circle(r=r);
}
        

module dents(num, size, missing=0,booloff=eps,r=0,corners=0) {
    l=size/(2*num+1);
    union() {
        for (i=[(0+missing):(num-missing-1)]) {
            translate([l*(i*2+1),-booloff]) {
                if (r==0) {
                    square([l,thick+booloff]);
                    if (corners>0) {
                        translate([l,thick+booloff]) corner(corners);
                        translate([0,thick+booloff]) rotate([0,0,90]) corner(corners);
                        translate([l,0]) rotate([0,0,-90]) corner(corners);
                        rotate([0,0,180]) corner(corners);
                        
                    }
                } else {
                    square([l,thick+booloff-r]);
                    translate([r,0]) square([l-2*r,thick+booloff]);
                    translate([r,thick+booloff-r]) circle(r=r);
                    translate([l-r,thick+booloff-r]) circle(r=r);
                }
            }
        }
    } 
}

module shortdents() {
    numdents=shortnumdents;
    union() {
        dents(numdents,twidth);
        translate([0,shortborder-thick-screenborder]) {
            dents(numdents,twidth,1,0);
        }
    }
}

module longdents() {
    numdents=longnumdents;
    rotate([0,0,-90]) { translate([-theight,0]) {
    union() {
        dents(numdents,theight);
        translate([0,longborder-thick-screenborder]) {
            dents(numdents,theight,1,0);
        }
    }
    }}
}

module paramKnobs(dia) {
    dist = twidth/19*2;
    union() { for (i=[0:3]) {
        translate([(i-1.5)*dist+twidth/2,(shortborder-screenborder)/2]) {
            circle(d=dia);
        }
    }}
}

module knobs() {
    if (largeknobs) {
        paramKnobs(28);
    } else {
        paramKnobs(12.5);
    }
}

module stickHole() {
    translate([0.2*twidth,shortborder/2-thick/2]) {
        circle(d=24);
    }
}

function streben() = [thick+76, (theight-thick)/2, theight-(thick+76)-thick];

module wallStreben(wall=true) {
    for (i=streben()) {
        translate([i,0]) {
            if (wall) {
                translate([thick,0]) rotate([0,0,90]) dents(2,idepth,0,0);
            } else {
                translate([thick/2, (longborder-screenborder)/2]) {
                    square([thick,10],true);
                }
            }
        }
    }
}


module cover() {
    difference() {
        square([twidth,theight]);
        union() {
            translate([twidth/2, theight/2]) {
                roundSquare([led*ledw-2*screenoffset,led*ledh-2*screenoffset],12,true);
            }
            shortdents();
            knobs();
            translate([0,theight]) { scale([1,-1,1]) {
                shortdents();
                knobs();
            }}
            longdents();
            translate([twidth,0]) { scale([-1,1,1]) {
                longdents();
            }}
            
            translate([twidth,0]) rotate([0,0,90]) wallStreben(false);
            scale([-1,1,1]) rotate([0,0,90]) wallStreben(false);
            joystickholder(2);
            scale([-1,-1,1]) translate([-twidth,-theight]) joystickholder(2);
        }
    }
}

module roundSquare(dim=[1,1],r=0.2,centered=false) {
    translate(centered ? [-dim[0]/2,-dim[1]/2] : [0,0]) {
        union() {
            translate([0,r]) square([dim[0],dim[1]-2*r]);
            translate([r,0]) square([dim[0]-2*r,dim[1]]);
            translate([r,r]) circle(r);
            translate([dim[0]-r,r]) circle(r);
            translate([r,dim[1]-r]) circle(r);
            translate([dim[0]-r,dim[1]-r]) circle(r);
        }
    }
}

module shortWall(outer=true, front=true) {
    mis = outer ? 0 : 1;
    union() {
    difference() {
        union() {
            if (!outer) {
                translate([longborder-screenborder,0]) {
                    square([twidth-2*(longborder-screenborder),idepth]);
                }
            } else {
                translate([thick,0]) {
                    square([twidth-2*thick,idepth]);
                }                
            }
            translate([0,idepth]) {
                dents(shortnumdents,twidth, mis,eps,1);
            }
            if (outer) {
                translate([thick,0]) {
                    rotate([0,0,90]) {
                        dents(2,idepth,0,eps,1);
                    }
                }
                translate([twidth,0]) {
                    scale([-1,1,1]) {
                        translate([thick,0]) {
                            rotate([0,0,90]) {
                                dents(2,idepth,0,eps,1);
                            }
                        }
                    }
                }        
            } else {
                translate([longborder-screenborder,0]) {
                    rotate([0,0,90]) {
                        dents(2,idepth,0,eps,1);
                    }
                }
                translate([twidth-longborder+screenborder+thick,0]) {
                    scale([-1,1,1]) {
                        translate([thick,0]) {
                            rotate([0,0,90]) {
                                dents(2,idepth,0,eps,1);
                            }
                        }
                    }
                }
            }
        } // union, start difference
        if (!outer) {
            /*translate([(longborder-screenborder)/2, idepth/2]) roundSquare([10,30],3,true);
            translate([twidth-(longborder-screenborder)/2, idepth/2]) roundSquare([10,30],3,true);
            translate([longborder-screenborder-thick,0]) {
                square([thick,idepth/2]);
            }
            translate([twidth-longborder+screenborder,0]) {
                square([thick,idepth/2]);
            } */
            translate([longborder-screenoffset,idepth-screendepth-thick]) {
                for (i=[0:ledw-1]) {
                    translate([i*led+led/2-lednotch/2,0]) {
                        square([lednotch, (front && (i % (ledw-1)==0)) ? 2*thick : thick]);
                    }
                }
                if (!front) {
                    for (i=[0:(ledw/2-1)]) {
                        translate([(0.5+2*i)*led-5,thick-eps]) {
                            square([led+10,thick+eps]);
                        }
                    }
                } else {
                    for (i=[0:(ledw/2-2)]) {
                        translate([(0.5+2*i+1)*led-5,thick-eps]) {
                            square([led+10,thick+eps]);
                        }
                    }
                }
            }
        } else { // if outer
            translate([longborder-screenborder,0]) {
                rotate([0,0,90]) {
                    dents(2,idepth,0,0);
                }
            }
            translate([twidth-longborder+screenborder+thick,0]) {
                rotate([0,0,90]) {
                    dents(2,idepth,0,0);
                }
            }
            if (front) {
                translate([twidth-thick-16,idepth-15]) roundSquare([8,12],2,true);
                translate([twidth-longborder-20,idepth/3])
                    circle(d=resetbutton);
                translate([twidth-longborder-20,idepth-15]) {
                    circle($fn=20,d=6);
                    translate([7.2,0]) square([1,2.5],true);
                }
            }
        }
        joystickholder(1);
    } // difference
    } // union
}



module querStreben() {
    w = longborder-screenborder-2*thick;
    difference() {
        union() {
            square([w,idepth]);
            translate([w/2-5, idepth-eps-2]) roundSquare([10,thick+eps+2],1);
            rotate([0,0,90]) dents(2,idepth,0,eps,1);
            translate([w,0]) scale([-1,1,1]) rotate([0,0,90]) dents(2,idepth,0,eps,1);
        }
        translate([w/2,idepth/2]) roundSquare([13,30],4,true);
    } 
}

module longOuterWall(left=true) {
    difference() {
        union() {
            square([theight,idepth]);
            //dents(numdents,theight,1,0);
            translate([0,idepth]) dents(longnumdents,theight);
        }
        translate([thick-eps,0]) {
            rotate([0,0,90]) {
                dents(2,idepth);
            }
        }
       translate([theight,0]) {
            scale([-1,1,1]) {
                translate([thick-eps,0]) {
                    rotate([0,0,90]) {
                        dents(2,idepth);
                    }
                }
            }
        }        
        wallStreben();
        if (!left) {
            $fn=32;
            translate([100,idepth/2]) circle(d=11);
            d = 2.5;
            translate([thick+6+1+d/2, idepth-1-d/2]) circle(d=d);
            translate([thick+76-1-d/2, idepth-1-d/2]) circle(d=d);
            translate([thick+6+1+d/2, 1+d/2]) circle(d=d);
            translate([thick+76-1-d/2, 1+d/2]) circle(d=d);
            
        }
        /*
        if (left) translate([thick+shortborder-screenborder-thick,0]) {
            rotate([0,0,90]) {
                dents(2,idepth,0,0);
            }
        }
        translate([theight-shortborder+screenborder+thick,0]) {
            rotate([0,0,90]) {
                dents(2,idepth,0,0);
            }
        }*/
    }
}

module longInnerWall(left=true) {
    difference() {
        union() {
            translate([thick,0]) {
                square([theight-2*thick,idepth]);
            }
            translate([0,idepth]) dents(longnumdents,theight,1,r=1);            
            translate([thick,0]) {
                rotate([0,0,90]) {
                    dents(2,idepth);
                }
            }
           translate([theight,0]) {
                scale([-1,1,1]) {
                    translate([thick,0]) {
                        rotate([0,0,90]) {
                            dents(2,idepth);
                        }
                    }
                }
            }                    
        } // end union, start difference
        translate([(shortborder-screenborder)/2, idepth/2]) roundSquare([10,30],3,true);
            translate([theight-(shortborder-screenborder)/2, idepth/2]) roundSquare([10,30],3,true);
        translate([shortborder-screenborder,0]) {
            rotate([0,0,90]) {
                dents(2,idepth,0,0);
            }
        }            
        translate([theight-shortborder+screenborder+thick,0]) {
            rotate([0,0,90]) {
                dents(2,idepth,0,0);
            }
        } 
        wallStreben();
        translate([0,idepth-screendepth-thick]) dents(longnumdents,theight,1, corners=0.5);
        translate([shortborder+33.33*2-2, idepth-screendepth-thick-4]) circle(r=1.5);
        translate([shortborder+33.33*3-2, idepth-screendepth-thick-4]) circle(r=1.5);
        translate([theight-(shortborder+33.33*2-2), idepth-screendepth-thick-4]) circle(r=1.5);
        translate([theight-(shortborder+33.33*3-2), idepth-screendepth-thick-4]) circle(r=1.5);
    }
}

module ledPlate() {
    difference() {
    union() {
    translate([longborder-screenborder,shortborder-screenborder]) {
        square([led*ledw+2*(screenborder-screenoffset), led*ledh+2*(screenborder-screenoffset)]);
        for (i=[0:(ledw-1)]) {
            translate([screenborder-screenoffset+led*(i+0.5)-lednotch/2,-thick]) {
                roundSquare([lednotch,thick+eps+2],1);
                translate([0,led*ledh+2*(screenborder-screenoffset)+thick-2]) {
                    roundSquare([lednotch,thick+eps+2],1);
                }
            }
        }
    }
    translate([longborder-screenborder,0]) rotate([0,0,90]) dents(longnumdents,theight,1,eps,1);
    translate([twidth-(longborder-screenborder),0]) scale([-1,1,1]) rotate([0,0,90]) dents(longnumdents,theight,1,eps,1);
    } // end union, start difference
        
        translate([longborder-screenoffset, shortborder-screenoffset]) {
        for (i=[0:(ledw-1)]) {
            for (j=[0:(ledh-1)]) {
                translate([(i+0.5)*led,(j+0.5)*led]) circle(d=12);
            }
            translate([(i+0.5)*led + (2*(i%2)-1)*8, 2*led-2]) circle(d=1.5);
            translate([(i+0.5)*led - (2*(i%2)-1)*8, 3*led-2]) circle(d=1.5);
            translate([(i+0.5)*led + (2*(i%2)-1)*8, 13*led+2]) circle(d=1.5);
            translate([(i+0.5)*led - (2*(i%2)-1)*8, 12*led+2]) circle(d=1.5);
        }}
        
    } // end difference
}

module longpap() {
    roundx=2;
    roundy=2;
    l = ledh*led-1;
    h = screendepth-glassthick;
    union() {
        difference() {
            translate([0.5,0]) square([l,h]);
            for (i=[1:(ledh-1)]) {
                translate([i*led-pthick/2,-eps]) {
                    square([pthick,h/2+eps]);
                    translate([pthick-eps,-eps]) square([roundx+eps,roundy+eps]);
                    translate([-roundx,-eps]) square([roundx+eps,roundy+eps]);
                }
            }
        }
        for (i=[1:(ledh-1)]) {
            translate([i*led-pthick/2,-eps]) {
                translate([pthick+roundx,roundy]) scale([roundx,roundy]) circle($fn=20, r=1);
                translate([-roundx,roundy]) scale([roundx,roundy]) circle($fn=20,r=1);
            }
        }
    }
}

module shortpap() {
    roundx=2;
    roundy=2;

    l = ledw*led+2*screenborder;
    h = screendepth-glassthick;
    union() {
        difference() {
            square([l,h]);
            for (i=[1:(ledw)]) {
                if (i<ledw) {
                    translate([i*led-pthick/2+screenborder,h/2]) {
                        square([pthick,h/2+eps]);
                        translate([pthick,h/2-roundy]) square([roundx,roundy+eps]);
                        translate([-roundx,h/2-roundy]) square([roundx+eps,roundy+eps]);
                    }
                }
                translate([(i-0.5)*led+screenborder,0])
                    square([12,2],true);
            }
        }
        for (i=[1:(ledw-1)]) {
            translate([i*led-pthick/2+screenborder,h/2]) {
                
                translate([pthick+roundx,h/2-roundy]) scale([roundx,roundy]) circle($fn=20, r=1);
                translate([-roundx,h/2-roundy]) scale([roundx,roundy]) circle($fn=20,r=1);
            }
        }
    }
}

// 0 holder plate
// 1 dents
// 2 top hole
module joystickholder(type=0) {
    // holes long: inner: 23mm, outer: 29.6 -> center 26.3
    // holes short: inner: 16.5, outer: 23.3 -> center 19.9
    dx = 26.3;
    dy = 20.0;
    depth=17;
    hole=27;
    screwhole=2.3;
    dent=12;
    //xoffset = 72;
    xoffset = 304.5;
    jwidth = shortborder-screenborder-2*thick;
    jlength = 38; // (outer+2*4)
    if (type==0) { // holder plate
        difference() {
            union() {
                square([jlength,jwidth]);
                translate([0,jwidth]) square([dent,thick]);
                translate([0,-thick]) square([dent,thick]);
                translate([jlength-dent,jwidth]) square([dent,thick]);
                translate([jlength-dent,-thick]) square([dent,thick]);
            } // begin difference
            translate([1,-1]) {
                translate([(jlength-dx)/2, (jwidth-dy)/2]) circle($fn=24,d=screwhole);
                translate([jlength-(jlength-dx)/2, (jwidth-dy)/2]) circle($fn=24,d=screwhole);
                translate([jlength-(jlength-dx)/2, jwidth-(jwidth-dy)/2]) circle($fn=24,d=screwhole);
                translate([(jlength-dx)/2, jwidth-(jwidth-dy)/2]) circle($fn=24,d=screwhole);
            }
            translate([0,jlength/2-1]) scale([0.4,1]) circle($fn=32,d=18);
        }
    } else if (type==1) { // dents
        translate([xoffset,idepth-depth-thick]) square([dent,thick]);
        translate([xoffset+jlength-dent,idepth-depth-thick]) square([dent,thick]);
    } else if (type==2) { // top hole
        translate([xoffset+jlength/2,shortborder/2]) circle($fn=64,d=hole);
    }
}



module parts() {
    $fn=32;
translate([-twidth-thick,0]) cover();
for (i=[0:3]) {
    translate([0,-(i+1)*(tdepth+thick)]) {
        translate([-twidth-thick,0]) shortWall(i%2==0, i<2);
        
        if (i<2) {
            longInnerWall(i%2==0);
        } else {
            longOuterWall(i%2==0);
        }
    }        
}
//translate([0,400]) rotate([0,0,-90]) 
ledPlate();

for (i=[0:5]) {
    translate([twidth+i*(longborder+thick),shortborder+thick]) {
        querStreben();
        if (i<2) {
            translate([0,60]) joystickholder(0);
        }
    }
}
for (i=[1:(ledh-1)]) {
    translate([-ledw*led-10, -i*(screendepth+4)-5*tdepth]) scale([1,1-(i%2)*2,1]) translate([0,-10])shortpap();
}
for (i=[1:(ledw-1)]) {
    translate([0, -i*(screendepth+4)-5*tdepth]) scale([1,1-(i%2)*2,1]) translate([0,-10]) longpap();
}
} // end parts

module case3d() {
color([1,0,0,0.2]) linear_extrude(height=thick) cover();


translate([0,thick,-idepth]) rotate([90,0,0])
color([0,1,0,0.2]) linear_extrude(height=thick) shortWall(true, true);

translate([0,shortborder-screenborder,-idepth]) rotate([90,0,0])
color([0,1,0,0.2]) linear_extrude(height=thick) shortWall(false, true);

translate([0,theight,-idepth]) rotate([90,0,0])
color([0,1,0,0.2]) linear_extrude(height=thick) shortWall(true, false);

translate([0,theight-(shortborder-screenborder)+thick,-idepth]) rotate([90,0,0])
color([0,1,0,0.2]) linear_extrude(height=thick) shortWall(false, false);

color([1,1,0,0.5])
translate([0,0,-screendepth-thick])
linear_extrude(height=thick) ledPlate();

color([0,0,1,0.2]) {
    translate([longborder-screenborder-thick,0,-idepth])
    rotate([0,0,90]) rotate([90,0,0])
    linear_extrude(height=thick) 
    longInnerWall(true);
    
    translate([twidth-longborder+screenborder,0,-idepth])
    rotate([0,0,90]) rotate([90,0,0])
    linear_extrude(height=thick) 
    longInnerWall(false);
    
   
    translate([0,0,-idepth])
    rotate([0,0,90]) rotate([90,0,0])
    linear_extrude(height=thick) 
    longOuterWall(true);

    translate([twidth-thick,0,-idepth])
    rotate([0,0,90]) rotate([90,0,0])
    linear_extrude(height=thick) 
    longOuterWall(false);
    
}

color([1,0,1,0.3]) {
    for (i=streben()) {
        translate([thick,i+thick,-idepth])
        rotate([90,0,0])
        linear_extrude(height=thick)
        querStreben();

        translate([thick+twidth-longborder+screenborder,i+thick,-idepth])
        rotate([90,0,0])
        linear_extrude(height=thick)
        querStreben();
    }
}

color([0,1,1,0.3]) {
    for (i=[1:(ledh-1)]) {
        translate([longborder-screenborder, shortborder+i*led-pthick/2, -screendepth]) 
        rotate([90,0,0])
            linear_extrude(height=pthick) shortpap();
    }
    for (i=[1:(ledw-1)]) {
        translate([longborder-screenborder+i*led-pthick/2, shortborder-screenborder, -screendepth])
       rotate([0,0,90]) 
        rotate([90,0,0])
            linear_extrude(height=pthick) longpap();
    }     
}
}

parts();
//case3d();
//translate([0,screendepth]) longpap();
//shortpap();
/*
joystickholder(0);
joystickholder(1);
joystickholder(2);
*/
