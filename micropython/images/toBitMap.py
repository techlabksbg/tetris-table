import sys

typ = sys.stdin.readline().rstrip()
if typ!="P3":
    raise NotImplementedError("Kann nur PNM-Dateien vom Typ P3 konvertieren")

line = ""

rgb = True

if len(sys.argv)>1 and sys.argv[1]=="bw":
    rgb = False


while True:
    line = sys.stdin.readline().rstrip()
    if line[0]!='#':
        break

sx,sy = list(map(lambda x:int(x), line.split(" ")))
mcol = int(sys.stdin.readline())

res = "RGB_Bitmap(%d,%d,(" % (sx,sy)
if not rgb:
    res = "BW_Bitmap(%d,%d,(" % (sx,sy)


for y in range(sy):
    l = 0
    for x in range(sx):
        c = 0;
        for i in range(3):
            c = (c<<8) | int(int(sys.stdin.readline())/mcol*255)
        if rgb:
            res += "0x%x,"%c
        else:
            l |= (1 if c==0 else 0) << x
    if not rgb:
        res += bin(l)+","

res += "))"
print(res)


