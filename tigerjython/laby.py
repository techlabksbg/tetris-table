import random

class Laby:
    # directions, trigonometric
    VECS=[[1,0], [0,1], [-1,0], [0,-1]];
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Gibt für jede Koordinate an, ob nach links und nach unten gegangen werden kann.
        # Z.B. self.canGo[3,4,0] ist True, wenn von 3,4 auf 4,4 gegangen werden kann
        # self.canGo[3,4,1] ist False, wenn nicht von 3,4 auf 3,5 gegangen werden kann.
        self.canGo = [[[False, False] for y in range(self.height)] for x in range(self.width)]
        
        # Mark enthaelt ein String der Laenge 1, der bei der Ausgabe mit ausgegeben wird.
        self.mark = [[" " for y in range(self.height)] for x in range(self.width)]
        

    
    def clearMarks(self):
        for y in range(self.height):
            for x in range(self.width):
                self.mark[x][y]=" "
      
    # c ist ein Koordinatenpaar        
    def onBoard(self,c):
        return c[0]>=0 and c[0]<self.width and c[1]>=0 and c[1]<self.height
    
  
    def move(self, c,d):
        return (c[0]+Laby.VECS[d][0], c[1]+Laby.VECS[d][1])
    
    # c ist ein Koordinatenpaar, 
    # gibt True zurueck, wenn von c in Richtung d gegangen werden kann.
    def edge(self, c, d):
        if self.onBoard(c) and self.onBoard(self.move(c,d)):
            if d>1:
                c = self.move(c,d)
                d-=2
            return self.canGo[c[0]][c[1]][d]
        return False
        
        
    def setEdge(self, c,d, value=True):
         if self.onBoard(c) and self.onBoard(self.move(c,d)):
            if d>1:
                c = self.move(c,d)
                d-=2
            self.canGo[c[0]][c[1]][d] = value
            
    def __str__(self):
        res = "+" + ("---+"*self.width)+"\n"
        for y in range(self.height):
            line1 = "|"
            line2 = "+"
            for x in range(self.width):
                line1 += " "+self.mark[x][y]+" "
                line1 += " " if self.edge((x,y),0) else "|"
                line2 += "   +" if self.edge((x,y),1) else "---+"
            res+=line1+"\n"+line2+"\n"
        return res
    
    def generate(self):
        todo = [(0,0)] #[(self.width//2,self.height//2)] # Array mit einem Koordinatenpaar
        dirs = ("<", "^", ">", "v")
        randdir = [0,1,2,3]
        while len(todo)>0:
            i = len(todo)-1-int(len(todo)*(random.random()**5))
            v = todo[i]
            del todo[i]
            random.shuffle(randdir)
            for d in randdir:
                n = self.move(v,d)
                if self.onBoard(n) and self.mark[n[0]][n[1]]==" ":
                    todo.append(n)
                    self.setEdge(v,d)
                    self.mark[n[0]][n[1]]=dirs[d]
                    todo.insert(0,v)
                    break
                
                    
                                                
            
# Nur wenn Datei dekt ausgefuehrt wird:    
if __name__== "__main__":
    l = Laby(12,12);
    print(l)
    l.generate()
    print(l)
    l.clearMarks()
    print(l)
  