import Enc
import json
import MySocket
import threadPool

MAX_THREADS = 100
THREAD_BLOCK = 10

class Store:
    def __init__(self):
        self.enc = None
        
        self.sockCliente = MySocket.MySocket(20000)
        
        self.data = json.loads('{"A": {"Vagas": {"1": 0, "2": 0, "3": 0} },"B": {"Vagas": {"1": 0, "2":0, "3":0} }, "C": {"Vagas": {"1": 0, "2": 0, "3":0} } }')
        

        self.serverNumber = 1
        self.serverList = []

        self.list = []

    def setEncoder(self, encoder):
        self.enc = encoder

    def setLotation(self, total):
        self.data = total

    def handleSlot(self, msg):
        building = msg["building"]
        layer = msg["layer"]
        div = 0
        
        qtd = int(self.data[str(building)]['Vagas'][str(layer)])

        if qtd > 0:
            div = int(qtd / self.serverNumber)
            
            if div < 1:
                div = 1
            
            qtd -= div

            self.data[str(building)]['Vagas'][str(layer)] = qtd


        msg = {"Vagas": div}

        return msg

    def handleSync(self, msg):
        building = msg["building"]
        layer = msg["layer"]
        qtd = int(self.data[str(building)]['Vagas'][str(layer)])
        self.data[str(building)]['Vagas'][str(layer)] = qtd - 1

    def getResponse(self, connection):
        serializedMsg = connection.recv(1024)
        msg = self.enc.loadMessage(serializedMsg)
        convertedMsg = json.loads(msg)
        return convertedMsg

    def closeConnection(self):
        self.sockCliente.closeSocket()

    def setServerList(self, serverList):
        self.serverList = serverList
        self.serverNumber = len(serverList) + 1

    def getMessage(self):
        serializedMsg = self.sockCliente.getMessage()
        print(serializedMsg)
        msg = self.enc.loadMessage(serializedMsg[0])
        return msg['Vagas']


    def handleServer(self, msg):
        building = msg["building"]
        layer = msg["layer"]
        qtd = int(self.data[str(building)]['Vagas'][str(layer)])

        if qtd > 0:
            self.data[str(building)]['Vagas'][str(layer)] = qtd - 1
            print(self.data)
            return "Authorized"
        else:
            msg = {"type": "getSlot", "building": building, "layer": layer}
            print("Requesting slots...")
            for server in self.serverList:
                print(server)
                self.sockCliente.closeSocket()
                self.connect(server)
                print(msg)
                self.sendMessage(msg)
                data = self.getMessage()
                
                self.data[str(building)]['Vagas'][str(layer)] += int(data)

            qtd = int(self.data[str(building)]['Vagas'][str(layer)])
            
            if qtd > 0:
                self.data[str(building)]['Vagas'][str(layer)] = qtd - 1
                print(self.data)
                return "Authorized"
            else:
                
                if msg["client"] == "VISITOR":
                    return "Unauthorized"
                else:
                    self.data[str(building)]['Vagas'][str(layer)] = qtd - 1
                    return "Authorized"

    def connect(self, addr):
        self.sockCliente.createClientTCP()
        self.sockCliente.connect(addr)

    def sendMessage(self, msg):
        self.sockCliente.sendTCP(self.enc.prepareMsg(msg))

