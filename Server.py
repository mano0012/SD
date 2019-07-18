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
DNS_IP = "172.31.88.8"
DNS_PORT = 10000

#TESTE = True
TESTE = False

class Server:
    def __init__(self):
        self.extIp = "172.31.85.113"
        self.localIp = "127.0.0.1"

        self.enc = Enc.Enc()
        self.store = Store.Store()

        self.store.setEncoder(self.enc)

        self.port = 11001

        self.serverList = []

        self.serverSock = None

        self.threads = threadPool.tPool(self.run, MAX_THREADS, THREAD_BLOCK)

        self.register()

        self.closeSocket()
    
        self.createSocketTCP()

        print("Server is set up.")
        
    def handleServer(self, msg):
        print("SERVER HANDLER")
        ip = msg["ip"]
        port = int(msg["port"])
        address = (ip, port)
        self.serverList.append(address)
        self.store.setServerList(self.serverList)

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
            
                if msg["type"] == "Server":
                    self.handleServer(msg)
                    break

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

        connection.shutdown(2)
        connection.close()

        self.threads.repopulate()

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
        print("CHEGOU")
        if self.createSocketUDP():
            
            print("ENTROU")
            sendMsg = {"type":"registerServer", "int": str(self.localIp), "ext":str(self.extIp), "port":str(self.port)}
            print(sendMsg)
            self.sendUDP((DNS_IP, DNS_PORT), self.enc.prepareMsg(sendMsg))
            data, _ = self.sock.recvfrom(1024)
            message = self.enc.loadMessage(data)
            self.serverList = message[0:len(message) - 1]
            self.store.setServerList(self.serverList)
            
            if len(self.serverList) == 0:
                self.sendUDP((DNS_IP, DNS_PORT), self.enc.prepareMsg({"type": "getSlots"}))
                data, _ = self.sock.recvfrom(1024)
                totalSlots = self.enc.loadMessage(data)
                self.store.setLotation(totalSlots)

            for server in self.serverList:
                msg = {"type": "Server", "ip": str(self.localIp), "port": str(self.port) }
                self.store.connect(server)
                self.store.sendMessage(msg)
                self.store.closeConnection()
                    

    def sendTCP(self, serializedMsg):
        self.sock.sendall(serializedMsg)

    def createSocketTCP(self):
        self.sock = socket.socket(socket.AF_INET,  # Internet
                                  socket.SOCK_STREAM)  # TCP

        #self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.sock.bind(('0.0.0.0', self.port))
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

            self.sock.bind(("0.0.0.0", self.port))
        except:
            return False
        
        return True

    def sendUDP(self, host, serializedMessage):
        self.sock.sendto(serializedMessage, host)

sv = Server()
sv.waitClient()