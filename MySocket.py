import socket
import Enc
class MySocket:
    def __init__(self, ip, port):
        self.sock = None
        self.ip = ip
        self.port = port

    def sendTCP(self, serializedMsg):
        self.sock.send(serializedMsg)

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
        print(socket.SHUT_RDWR)
        try:
            self.sock.close()
        except:
            pass

    def createSocketUDP(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                            socket.SOCK_DGRAM)

        self.sock.bind((self.ip, self.port))

        return self.sock

    def connect(self, host, port):
        server = (host, port)
        self.sock.connect(server)

    def sendUDP(self, host, serializedMessage):
        self.sock.sendto(serializedMessage, host)