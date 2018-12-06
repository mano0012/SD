import socket
import threadPool
import pickle
import json
import queue

#ALTERAR PARA TCP

HOST = ''  # Endereco IP do Servidor
PORT = 9996  # Porta que o Servidor esta

MAX_THREADS = 100
THREAD_BLOCK = 10

class DNS:
    def __init__(self):
        self.services = ["WEB", "SQL", "CHAT"]
        self.serverList = self.services.copy()

        # Socket UDP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.s.bind((HOST, PORT))

        for i in range(len(self.services)):
            self.serverList[i] = queue.Queue()

        self.threads = threadPool.tPool(self.getAddress, MAX_THREADS, THREAD_BLOCK)

        print("DNS is set up")

    def run(self):
        while True:
            data, addr = self.s.recvfrom(1024)

            t = self.threads.getThread([data, addr])

            t.start()

    #Terminar getAddress
    def getAddress(self, data, address):
        message = json.loads(pickle.loads(data))
        hasService = False

        print("RECEIVED: ", message)

        for i in range(len(self.services)):
            if self.services[i] == message["type"]:
                hasService = True
                if message["con"] == "SERVER":
                    self.addQueueSv(i, address)
                    self.sendToHost(address, "DONE!")
                else:
                    svAddr = self.getServerAddress(i)

                    self.sendToHost(address, svAddr)

        if not hasService:
            self.sendToHost(address, "ERROR! This service is not available")

    def getServerAddress(self, index):
        print("SELECTED SERVER: ", self.services[index])
        svAddr = self.removeQueueSv(index)

        if svAddr is not None:
            self.addQueueSv(index, svAddr)

        return svAddr

    def removeQueueSv(self, index):
        if self.serverList[index].empty():
            print("QUEUE EMPTY")
            return None

        return self.serverList[index].get()

    def addQueueSv(self, index, host):
        self.serverList[index].put(host)

    def sendToHost(self, host, message):
        print("SEND: ", message)
        if message is None:
            msgSerializada = pickle.dumps("ERROR! No server is available")
        else:
            msgSerializada = pickle.dumps(message)

        self.s.sendto(msgSerializada, host)

    def exit(self):
        self.s.close()

dns = DNS()
dns.run()
