from enum import Enum
import getpass
import pickle
import socket
import json

#DNS_IP = "172.31.88.8"
DNS_IP = "127.0.0.1"
DNS_PORT = 10001
MAX_LOTATION = 1

ENUM = ["VISITOR", "FUNC", "ADMIN"]

class Cliente:
    def __init__(self):
        self.serverAddr = None
        self.sock = None
        self.ip = "127.0.0.1"
        #self.ip = "172.31.93.40"
        self.port = 9990

    def connect(self):
        self.serverAddr = self.getServerAddr()
        print(self.serverAddr)
        self.closeSocket()
        self.createSocketTCP()

        self.sock.connect(self.serverAddr[0])
        
        return True
    

    def validate(self, data, passwdCode):
        if self.makeRequest(data, passwdCode):
            if self.getResponse() == "Authorized":
                return True
            return False
        else: 
            return False

    def getResponse(self):
        data, _ = self.sock.recvfrom(1024)

        return self.loadMessage(data)

    def makeRequest(self, data, passwdCode):
        msg = {"type": "CLIENT", "building": data[0], "layer": data[1], "client": ENUM[int(passwdCode)]}
        self.sendTCP(self.prepareMsg(msg))

        return True

    def sendTCP(self, serializedMsg):
        self.sock.sendall(serializedMsg)

    def createSocketTCP(self):
        self.sock = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)  # TCP

        self.sock.bind((self.ip, self.port))

    def closeSocket(self):
        try:
            self.sock.close()
        except:
            pass

    def getServerAddr(self):
        self.closeSocket()
        self.createSocketUDP()
        self.sendUDP((DNS_IP, DNS_PORT), self.prepareMsg({"type": "requestServer"}))
        data, _ = self.sock.recvfrom(1024)
        return [self.loadMessage(data)]

    def createSocketUDP(self):
        self.sock = socket.socket(socket.AF_INET,
                             socket.SOCK_DGRAM)

        self.sock.bind((self.ip, self.port))

    def convertJson(self, message):
        try:
            msg = json.dumps(message)
            return msg
        except:
            return message

    def loadJson(self, message):
        try:
            msg = json.loads(message)
            return msg
        except:
            return message

    def loadMessage(self, message):
        return self.loadJson(pickle.loads(message))

    def prepareMsg(self, msg):
        jsonMsg = self.convertJson(msg)

        serializedMsg = pickle.dumps(jsonMsg)

        return serializedMsg

    def sendUDP(self, host, serializedMessage):
        self.sock.sendto(serializedMessage, host)