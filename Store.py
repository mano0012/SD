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
        
        self.sockCliente = MySocket.MySocket(20002)
        
        self.data = json.loads('{"A": {"Vagas": {"1": 0, "2": 0, "3": 0} },"B": {"Vagas": {"1": 0, "2":0, "3":0} }, "C": {"Vagas": {"1": 0, "2": 0, "3":0} } }')
        self.dataOcupado = json.loads('{"A": {"Ocupado": {"1": 0, "2": 0, "3": 0} },"B": {"Ocupado": {"1": 0, "2":0, "3":0} }, "C": {"Ocupado": {"1": 0, "2": 0, "3":0} } }')
        

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

    def getMessage(self, lotationType = "Vagas"):
        serializedMsg = self.sockCliente.getMessage()
        print(serializedMsg)
        msg = self.enc.loadMessage(serializedMsg[0])

        if(lotationType == 'Vagas'):
            return msg[lotationType]
        
        return msg

    def handleServer(self, msg):
        building = msg["building"]
        layer = msg["layer"]
        clientType = msg["client"]
        qtd = int(self.data[str(building)]['Vagas'][str(layer)])
        qtdOcupado = int(self.dataOcupado[str(building)]['Ocupado'][str(layer)])

        if qtd > 0:
            self.data[str(building)]['Vagas'][str(layer)] = qtd - 1
            self.dataOcupado[str(building)]['Ocupado'][str(layer)] = qtdOcupado + 1
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
                self.dataOcupado[str(building)]['Ocupado'][str(layer)] = qtdOcupado + 1
                print(self.data)
                return "Authorized"
            else:
                if clientType == "VISITOR":
                    print("NAO AUTORIZADO")
                    return "Unauthorized"
                else:
                    self.data[str(building)]['Vagas'][str(layer)] = qtd - 1
                    self.dataOcupado[str(building)]['Ocupado'][str(layer)] = qtdOcupado + 1
                    return "Authorized"

    def requestLotation(self):
        msg = {"type": "getLotation"}
        lotation = copy.deepcopy(self.dataOcupado)
        free = copy.deepcopy(self.data)

        for server in self.serverList:
            self.sockCliente.closeSocket()
            self.connect(server)
            self.sendMessage(msg)
            data = self.getMessage("Ocupado")
            print(data)
            for buildings in self.dataOcupado:
                for layer in self.dataOcupado[str(buildings)]["Ocupado"]:
                    qtd = int(lotation[str(buildings)]["Ocupado"][str(layer)])
                    freeSlots = int(free[str(buildings)]["Vagas"][str(layer)])

                    freeSlots += int(data[0][str(buildings)]["Vagas"][str(layer)])
                    qtd += int(data[1][str(buildings)]["Ocupado"][str(layer)]) 

                    lotation[str(buildings)]["Ocupado"][str(layer)] = qtd
                    free[str(buildings)]["Vagas"][str(layer)] = qtd
        
        return [lotation, free]
    
    def getLotation(self):
        return [self.data, self.dataOcupado]

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

