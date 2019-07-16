import socket
import Enc
class MySocket:
    def __init__(self, ip, port):
        self.sock = None
        self.ip = ip
        self.port = port

    def sendTCP(self, serializedMsg):
        self.sock.send(serializedMsg)

    def createSocketTCP(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_STREAM)  # TCP

        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)

        return self.sock

    def waitClient(self):
        while True:
            return self.sock.accept()
    

    def closeSocket(self):
        try:
            self.sock.close()
        except:
            pass

    def createSocketUDP(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                            socket.SOCK_DGRAM)

        self.sock.bind((self.ip, self.port))

        return self.sock

    def sendUDP(self, host, serializedMessage):
        self.sock.sendto(serializedMessage, host)