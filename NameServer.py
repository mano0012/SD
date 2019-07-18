import socket
import threadPool
import pickle
import json
import queue
import Enc

MAX_THREADS = 100
THREAD_BLOCK = 10

class DNS:
    def __init__(self):
        #self.ip = "172.31.88.8"
        self.ip = "127.0.0.1"
        self.port = 10001
        self.enc = Enc.Enc()
        self.lock = False
        # Socket UDP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.s.bind((self.ip, self.port))
        self.servers = []
        self.serverList = queue.Queue()

        self.threads = threadPool.tPool(self.getAddress, MAX_THREADS, THREAD_BLOCK)


        self.totalSlots = {"A": {"Vagas": {"1": 10, "2":10, "3":10} },"B": {"Vagas": {"1": 10, "2":10, "3":10} }, "C": {"Vagas": {"1": 10, "2":10, "3":10} } }

        print("NameService is set up")

    def run(self):
        while True:
            data, addr = self.s.recvfrom(1024)

            t = self.threads.getThread([data, addr])
            print(addr)
            t.start()

    def handleServer(self, addr, msg):
        while(True):
            if(self.lock == False):
                break

        self.lock = True

        print("LOCAL")
        print(msg["int"])
        
        print("ext")
        print(msg["ext"])

        self.addQueueSv((msg["ext"], int(msg["port"])))
        self.servers.append((msg["int"], int(msg["port"])))

        self.sendToHost(addr, self.servers)

        self.lock = False

    #Terminar getAddress
    def getAddress(self, data, addr):
        message = self.loadMessage(data)

        print("MESSAGE: " + str(message))

        if message["type"] == "registerServer":
            print("Adding ", addr, " server.")
            self.handleServer(addr, message)
        elif message["type"] == "getServerList":
            serverList = pickle.dumps(list(self.serverList.queue))
            self.s.sendto(serverList, addr)
        elif message["type"] == "getSlots":
            slots = self.enc.prepareMsg(self.totalSlots)
            self.s.sendto(slots, addr)
        else:
            svAddr = self.getServerAddress()

            self.sendToHost(addr, svAddr)

        self.threads.repopulate()

    def getServerAddress(self):
        svAddr = self.removeQueueSv()

        if svAddr is not None:
            self.addQueueSv(svAddr)

        return svAddr

    def removeQueueSv(self):
        if self.serverList.empty():
            print("QUEUE EMPTY")
            return None

        return self.serverList.get()

    def addQueueSv(self, host):
        self.serverList.put_nowait(host)

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

    def sendToHost(self, host, message):
        jsonMsg = self.convertJson(message)

        if jsonMsg is None:
            msgSerializada = pickle.dumps("ERROR!")
        else:
            msgSerializada = pickle.dumps(message)

        self.s.sendto(msgSerializada, host)

    def exit(self):
        self.s.close()

dns = DNS()
dns.run()
