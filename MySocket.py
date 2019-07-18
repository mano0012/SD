import socket
import Enc
class MySocket:
    def __init__(self, ip, port):
        self.sock = None
        self.ip = ip
        self.port = port

    def getMessage(self):
        return self.sock.recvfrom(2048)

    def sendTCP(self, serializedMsg):
        self.sock.sendall(serializedMsg)

    def createServerTCP(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_STREAM)  # TCP

        self.sock.bind((self.ip, self.port))
        self.sock.listen(5)

        return self.sock

    def createClientTCP(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_STREAM)  # TCP

        self.sock.bind((self.ip, self.port))

        return self.sock


    def accept(self):
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

    def connect(self, server):
        self.sock.connect(server)

    def sendUDP(self, host, serializedMessage):
        self.sock.sendto(serializedMessage, host)