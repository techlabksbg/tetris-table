# Version fuer TigerJython

class MCP:
    def __init__(self, address=0x20, np=None):
        self.np = np

    def setLeds(self,what):
        self.np.showButtons(what)
        
    def getButtons(self):
        k=self.np.getTaste()
        keys=['a','s','d','f','r','e', 'w','q']
        #print(k)
        try:
            i = keys.index(k)
            print(str(k)+" -> "+str(i))
            if (i>=0 and i<8):
                print (1<<i) ^ 255
                return (1<<i) ^ 255
        except:
            return 255


