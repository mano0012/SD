import pickle
import socket
import json
import threadPool
import Enc

MAX_THREADS = 100
THREAD_BLOCK = 10
DNS_IP = "127.0.0.1"
#DNS_IP = "172.31.88.8"
DNS_PORT = 10001

class Server:
    def __init__(self):
        #self.ip = "172.31.85.113"
        self.enc = Enc.Enc()
        self.ip = "127.0.0.1"
        self.port = 11002
        self.serverList = []
        self.sock = None

        self.threads = threadPool.tPool(self.run, MAX_THREADS, THREAD_BLOCK)

        self.register()

        self.closeSocket()
    
        self.createSocketTCP()

        self.lotation = 0

        print("Server is set up.")
        
    def handleServer(self, msg):
        address = msg["address"]
        self.serverList.append(address)

    def run(self, connection):
        while True:
            try:
                msg = self.getMessage(connection)
                if(msg["type"] == "Server"):
                    self.handleServer(msg)
                else:
                    print(msg["lockId"])
                    print(msg["code"])

                    if (msg["lockId"] == 5):
                        connection.send(self.enc.prepareMsg("Authorized"))
                    else: connection.send(self.enc.prepareMsg("Unauthorized"))
            except:
                print("End of connection")
                break

    def waitClient(self):
        while True:
            con, client = self.sock.accept()

            print("Cliente ", client, " conectado")
            t = self.threads.getThread([con])

            t.start()

    def getMessage(self, connection):
        serializedMsg = connection.recv(1024)
        msg = self.enc.loadMessage(serializedMsg)
        return msg

    def verifyClient(self, data, address):
        message = self.enc.loadMessage(data)

        print(message)


    def register(self):
        self.closeSocket()

        if self.createSocketUDP():
            print('ENTROU')
            self.sendUDP((DNS_IP, DNS_PORT), self.enc.prepareMsg("registerServer"))
            data, addr = self.sock.recvfrom(1024)
            message = self.enc.loadMessage(data)
            self.serverList = message[0:len(message) - 1]

            print(self.serverList)

            for server in message:
                ip, port = server
                if ip != self.ip or port != self.port:
                    #chamaServer
                    print(ip)
                    print(port)

    def sendTCP(self, serializedMsg):
        self.sock.send(serializedMsg)

    def createSocketTCP(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_STREAM)  # TCP

        self.sock.bind((self.ip, self.port))
        self.sock.listen(1)

    def closeSocket(self):
        try:
            self.sock.close()
        except:
            pass

    def createSocketUDP(self):
        try:
            self.sock = socket.socket(socket.AF_INET,  # Internet
                                socket.SOCK_DGRAM)

            self.sock.bind((self.ip, self.port))
        except:
            return False
        
        return True

    def sendUDP(self, host, serializedMessage):
        self.sock.sendto(serializedMessage, host)

sv = Server()
sv.waitClient()