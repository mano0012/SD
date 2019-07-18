import pickle
import socket
import json
import threadPool
import Enc
import sys
import queue
import Store

MAX_THREADS = 100
THREAD_BLOCK = 10
DNS_IP = "127.0.0.1"
#DNS_IP = "172.31.88.8"
DNS_PORT = 10001

#TESTE = True
TESTE = False

class Server:
    def __init__(self):
        #self.ip = "172.31.85.113"
        self.enc = Enc.Enc()
        self.store = Store.Store()

        self.store.setEncoder(self.enc)

        self.ip = "127.0.0.1"
        if TESTE:
            self.port = 11000
        else:
            self.port = 11001
        #self.port = 11002
        #self.port = 11003

        self.serverList = []
        self.criticalLock = False
        self.criticalQueue = queue.Queue()

        self.serverSock = None

        self.threads = threadPool.tPool(self.run, MAX_THREADS, THREAD_BLOCK)

        self.register()

        self.closeSocket()
    
        self.createSocketTCP()

        self.lotation = 0

        print("Server is set up.")
        self.store.doTrick()
        
    def handleServer(self, msg):
        print("SERVER HANDLER")
        ip = msg["ip"]
        port = int(msg["port"])
        address = (ip, port)
        self.serverList.append(address)
        self.store.setServerList(self.serverList)
        print(self.serverList)

    def handleSlots(self, msg):
        return self.store.handleSlot(msg)

    '''
    def addQueue(self, connection):
        if self.criticalLock:
            self.criticalQueue.put_nowait(connection)
        else:
            self.criticalLock = True
            while self.criticalQueue.qsize() != 0:
                con = self.criticalQueue.get()
    '''   
    def run(self, connection):
        while True:
            try:
                msg = self.getMessage(connection)
            
                print("MENSAGEM " + str(msg))
                if msg["type"] == "Server":
                    self.handleServer(msg)
                    break
                elif msg["type"] == "getSlot":
                    print("FOI AKI")
                    qtd = self.handleSlots(msg)
                    print('QTD: ', qtd)
                    connection.send(self.enc.prepareMsg(qtd))
                    break
                else:
                    retorno = self.store.handleServer(msg)
                    print(retorno)
                    connection.sendall(self.enc.prepareMsg(retorno))
            except:
                print("END OF CONNECTION")
                connection.shutdown(2)
                connection.close()

        print("CLOSING CONNECTION")
        connection.shutdown(2)
        connection.close()

        self.threads.repopulate()
        print("FINALIZOU A THREAD")

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
        if self.createSocketUDP():
            self.sendUDP((DNS_IP, DNS_PORT), self.enc.prepareMsg("registerServer"))
            data, _ = self.sock.recvfrom(1024)
            message = self.enc.loadMessage(data)
            self.serverList = message[0:len(message) - 1]
            self.store.setServerList(self.serverList)
            print("SENDING REGISTER")
            for server in self.serverList:
                msg = {"type": "Server", "ip": str(self.ip), "port": str(self.port) }
                self.store.connect(server)
                self.store.sendMessage(msg)
                self.store.closeConnection()
                    

    def sendTCP(self, serializedMsg):
        self.sock.sendall(serializedMsg)

    def createSocketTCP(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_STREAM)  # TCP

        self.sock.bind((self.ip, self.port))
        self.sock.listen(5)

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