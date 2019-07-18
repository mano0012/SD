import Enc
import json
import MySocket
import threadPool

MAX_THREADS = 100
THREAD_BLOCK = 10

#TESTE = True
TESTE = False

class Store:
    def __init__(self):
        self.enc = None
        if TESTE:
            self.sockCliente = MySocket.MySocket("127.0.0.1", 20000)
            self.data = json.loads('{"A": {"Vagas": {"1": 30, "2":30, "3":30} },"B": {"Vagas": {"1": 6, "2":30} }, "C": {"Vagas": {"1": 10, "2":10, "3":10} } }')
        else:
            self.sockCliente = MySocket.MySocket("127.0.0.1", 20001)
            self.data = json.loads('{"A": {"Vagas": {"1": 30, "2":30, "3":30} },"B": {"Vagas": {"1": 0, "2":30} }, "C": {"Vagas": {"1": 10, "2":10, "3":10} } }')
        
        #self.sockCliente = MySocket.MySocket("127.0.0.1", 20002)
        #self.data = json.loads('{"A": {"Vagas": {"1": 30, "2":30, "3":30} },"B": {"Vagas": {"1": 4, "2":30} }, "C": {"Vagas": {"1": 10, "2":10, "3":10} } }')
        
        #self.sockCliente = MySocket.MySocket("127.0.0.1", 20003)
        #self.data = json.loads('{"A": {"Vagas": {"1": 30, "2":30, "3":30} },"B": {"Vagas": {"1": 6, "2":30} }, "C": {"Vagas": {"1": 10, "2":10, "3":10} } }')

        self.serverNumber = 1
        self.serverList = []

        #self.data = json.loads('{"A": {"Vagas": {"1": 30, "2":30, "3":30} },"B": {"Vagas": {"1": 6, "2":30} }, "C": {"Vagas": {"1": 10, "2":10, "3":10} } }')
        self.list = []

    def setEncoder(self, encoder):
        self.enc = encoder

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
        print(msg['Vagas'])
        return msg['Vagas']

    def handleServer(self, msg):
        building = msg["building"]
        layer = msg["layer"]
        qtd = int(self.data[str(building)]['Vagas'][str(layer)])

        if msg["client"] == "VISITOR":
            if qtd > 0:
                print("STORE AUTH")
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
                    print("STORE AUTH")
                    self.data[str(building)]['Vagas'][str(layer)] = qtd - 1
                    print(self.data)
                    return "Authorized"
                else:
                    print("STORE UNAUTH")
                    return "Unauthorized"
        else:
            self.data[str(building)]['Vagas'][str(layer)] = qtd - 1
            print(self.data)
            return "Authorized"

    def connect(self, addr):
        print("ADDR")
        print(addr)
        self.sockCliente.createClientTCP()
        print("CRIADO SOCKET")
        self.sockCliente.connect(addr)

    def doTrick(self):
        print("Requesting slots...")
        msg = {"type": "getSlot", "building": "B", "layer": 1}
        for server in self.serverList:
            print(server)
            self.sockCliente.closeSocket()
            self.connect(server)
            self.sendMessage(msg)
            data = self.getMessage()
            print(data)

    def sendMessage(self, msg):
        self.sockCliente.sendTCP(self.enc.prepareMsg(msg))


#FALTA FAZER A INTERAÇÃO ENTRE AS STORES E OS SERVIDORES
#Funciona assim:
#Servidor se conecta em uma store, solicita uma vaga, a store concede ou nega a vaga, servidor retorna para o cliente.
#Começa com 1 store. Testa. Depois vai aumentando as stores.
#De acordo com o aumento, as vagas devem ser divididas igualmente
