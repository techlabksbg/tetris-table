try:
  import usocket as socket
except:
  import socket
import os


class BareServer:
    def __init__(self):
        pass

    def web_page(self):
        return bytearray("<!DOCTYPE html>\n<html><body><h1>Hi</h1></body></html>\n".encode())

    def parseRequest(self, conn):
        request = conn.recv(4096).decode()
        # print(request)
        lines = request.split("\r\n")
        # print(lines)
        method,url,http = lines[0].split(" ")
        header = []
        body = ""
        i = 0
        clen = 0
        for l in lines[1:]:
            # print("->"+l+"<-")
            if l=="":
                # print(lines[(i+1):])
                body = "".join(lines[(i+1):])
                # print(body)
                break
            parts = l.split(": ",1)
            if parts[0]=="Content-Length":
                clen = int(parts[1])
            header.append([parts[0], parts[1]])
            i+=1
        # print("clen=%d, bodylen=%d" %(clen, len(body)))
        while len(body)<clen:
            body+=conn.recv(4096).decode()
            # print("bodylen now = %d" % len(body))
        return method, url, header,body

    def responseOK(self, answer, html=True):
        r = "HTTP/1.1 200 OK\r\n"
        if html:
            r += "Content-Type: text/html; charset=UTF-8\r\n"
        else:
            r += "Content-Type: text/plain; charset=UTF-8\r\n"
        r += "Server: TetrisTable\r\n"
        r += "Content-Length: "+str(len(answer))+"\r\n"
        r += "Connection: close\r\n\r\n"
        r += answer
        return bytearray(r.encode())
    
    def responseERROR(self, code, answer):
        r = "HTTP/1.1 "+str(code)+"\r\n"
        r += "Content-Type: text/plain; charset=UTF-8\r\n"
        r += "Server: TetrisTable\r\n"
        r += "Content-Length: "+str(len(answer))+"\r\n"
        r += "Connection: close\r\n\r\n"
        r += answer
        return bytearray(r.encode())


    def indexpage(self, msg=""):
        answer = "<!DOCTYPE html>\n<html><body>"
        if len(msg)>0:
            answer += msg
        answer += "<a href='/quit'><h3>Quit Webserver</h3></a>"
        answer += "<h1>Upload</h1><form method='post' enctype='multipart/form-data'><input type='file' id='myfile' name='myfile'><input type='submit'></form>"
        answer += "<h1>Files</h1><ul>\n"
        for f in os.listdir():
            answer += "<li><a href=\""+f+"\">"+f+"</a></li>\n"
        answer += "</ul></body></html>\n"
        return self.responseOK(answer)


    def get(self,url):        
        if url=="/":
            return self.indexpage()
        filename = url[1:]
        print("Trying "+filename)
        if os.path.exists(filename):
            with open(filename) as f:
                contents = f.readlines()
            return self.responseOK("".join(contents), False)
        return self.responseERROR(404, "File "+filename+" not found!");


    def post(self, url, header, body):
        head = body.split("\r\n", 4)
        sep = head[0]
        fcontents = head[4].split("\r\n"+sep)[0]
        filename = head[1].split("filename=")[1][1:-1]
        with open(filename, "w") as f:
            f.write(fcontents)
        print(fcontents)
        # return self.responseOK(fcontents, False)
        return self.indexpage("<h1>File "+filename+" written</h1>"+str(len(fcontents))+" Bytes written")

    def serve(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 8080))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            #print('Got a connection from %s' % str(addr))
            #request = conn.recv(4096)
            #print(request)
            #print("** len = %d **\n" % len(request))
            #request = request.decode()
            method, url, header,body = (self.parseRequest(conn))
            if method=="GET":
                if url=="/quit":
                    conn.close()
                    s.close()
                    break
                response = self.get(url)
            elif method=="POST":
                response = self.post(url, header, body)
            else:
                response = self.responseERROR(404,"Method "+method+" not implemented")
            conn.sendall(response)
            conn.close()



if __name__ == "__main__":
    b = BareServer()
    b.serve()

