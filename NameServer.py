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
        self.ip = "127.0.0.1"
        self.port = 10000
        self.enc = Enc.Enc()
        self.lock = False
        # Socket UDP
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.s.bind((self.ip, self.port))
        self.servers = []
        self.serverList = queue.Queue()

        self.threads = threadPool.tPool(self.getAddress, MAX_THREADS, THREAD_BLOCK)


        self.totalSlots = json.loads('{"A": {"Vagas": {"1": 1, "2": 2, "3": 3}, "Ocupado": {"1": 0, "2": 0, "3": 0} },"B": {"Vagas": {"1": 5, "2": 6, "3": 7}, "Ocupado": {"1": 0, "2": 0, "3": 0} }, "C": {"Vagas": {"1": 10, "2": 11, "3": 12}, "Ocupado": {"1": 0, "2": 0, "3": 0} } }')

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

        self.addQueueSv((msg["ip"], int(msg["port"])))
        self.servers.append((msg["ip"], int(msg["port"])))

        self.sendToHost(addr, self.servers)

        self.lock = False

    #Terminar getAddress
    def getAddress(self, data, addr):
        message = self.loadMessage(data)

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
