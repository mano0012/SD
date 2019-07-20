import Enc
import json
import MySocket
import threadPool
import copy

MAX_THREADS = 100
THREAD_BLOCK = 10

class Store:
    def __init__(self):
        self.enc = None
        
        self.sockCliente = MySocket.MySocket(20001)
        
        self.data = json.loads('{"A": {"Vagas": {"1": 0, "2": 0, "3": 0}, "Ocupado": {"1": 0, "2": 0, "3": 0} },"B": {"Vagas": {"1": 0, "2":0, "3":0}, "Ocupado": {"1": 0, "2": 0, "3": 0} }, "C": {"Vagas": {"1": 0, "2": 0, "3":0}, "Ocupado": {"1": 0, "2": 0, "3": 0} } }')
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
        msg = self.enc.loadMessage(serializedMsg[0])
        
        return msg

    def handleServer(self, msg):
        building = msg["building"]
        layer = msg["layer"]
        clientType = msg["client"]
        qtd = int(self.data[str(building)]['Vagas'][str(layer)])
        qtdOcupado = int(self.data[str(building)]['Ocupado'][str(layer)])

        if qtd > 0:
            self.data[str(building)]['Vagas'][str(layer)] = qtd - 1
            self.data[str(building)]['Ocupado'][str(layer)] = qtdOcupado + 1
            return "Authorized"
        else:
            msg = {"type": "getSlot", "building": building, "layer": layer}
            print("Requesting slots...")
            for server in self.serverList:
                print(server)
                self.sockCliente.closeSocket()
                self.connect(server)
                self.sendMessage(msg)
                data = self.getMessage()
                print(data)
                
                self.data[str(building)]['Vagas'][str(layer)] += int(data["Vagas"])

            qtd = int(self.data[str(building)]['Vagas'][str(layer)])
            
            if qtd > 0:
                self.data[str(building)]['Vagas'][str(layer)] = qtd - 1
                self.data[str(building)]['Ocupado'][str(layer)] = qtdOcupado + 1
                return "Authorized"
            else:
                if clientType == "VISITOR":
                    return "Unauthorized"
                else:
                    self.data[str(building)]['Vagas'][str(layer)] = qtd - 1
                    self.data[str(building)]['Ocupado'][str(layer)] = qtdOcupado + 1
                    return "Authorized"

    def requestLotation(self):
        msg = {"type": "getLotation"}
        lotation = copy.deepcopy(self.data)

        for server in self.serverList:
            self.sockCliente.closeSocket()
            self.connect(server)
            self.sendMessage(msg)
            data = self.getMessage()
            for buildings in self.data:
                for layer in self.data[str(buildings)]["Ocupado"]:
                    qtd = int(lotation[str(buildings)]["Ocupado"][str(layer)])
                    freeSlots = int(lotation[str(buildings)]["Vagas"][str(layer)])

                    freeSlots += int(data[str(buildings)]["Vagas"][str(layer)])
                    qtd += int(data[str(buildings)]["Ocupado"][str(layer)]) 

                    lotation[str(buildings)]["Ocupado"][str(layer)] = qtd
                    lotation[str(buildings)]["Vagas"][str(layer)] = freeSlots
        
        return lotation
    
    def getLotation(self):
        return self.data

    def addSlots(self, msg):
        building = msg["building"]
        layer = msg["layer"]
        slots = msg["slots"]

        qtd = int(self.data[str(building)]['Vagas'][str(layer)])
        qtd += int(slots)
        self.data[str(building)]['Vagas'][str(layer)] = qtd

        return ("Foram adicionadas " + str(slots) + " vagas ao prédio " + str(building) + " andar " + str(layer))
                
    def connect(self, addr):
        self.sockCliente.createClientTCP()
        self.sockCliente.connect(addr)

    def sendMessage(self, msg):
        self.sockCliente.sendTCP(self.enc.prepareMsg(msg))

