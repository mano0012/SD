import Enc
import json
import socket
import pickle

DNS_IP = "172.31.88.8"
DNS_PORT = 10000

class Admin:
    def __init__(self):
        self.serverAddr = None
        self.sock = None
        self.ip = "172.31.93.40"
        self.port = 8000
    
    def connect(self):
        print("Fazendo solicitação ao servidor de nomes")
        self.serverAddr = self.getServerAddr()
        print("Endereço recebido: " + str(self.serverAddr))
        self.closeSocket()
        self.createSocketTCP()

        self.sock.connect(self.serverAddr[0])
        print("Conectado ao servidor " + str(self.serverAddr[0]))
        return True

    def run(self):
        if self.connect():
            option = -1
            while option != '0':
                option = input("1- Verificar Lotação\n2- Adicionar Vagas\n0- Sair\nSelecione a opção: ")
                
                if option=='1':
                    msg = {"type": "adminLotation"}
                    self.sendTCP(self.prepareMsg(msg))
                    lotation = self.getResponse()
                    print("\nLA = Lotação atual")
                    print("LM = Lotação máxima")
                    print("===========================")
                    print("Predio\tAndar\tLA/LM")
                    for building in lotation:
                        for layer in lotation[building]['Vagas']:
                            total = int(lotation[str(building)]['Ocupado'][str(layer)]) + int(lotation[str(building)]['Vagas'][str(layer)])
                            print(str(building) + '\t' + str(layer) + '\t' + str(lotation[building]['Ocupado'][layer]) + '/' + str(total))
                    print("===========================")
                elif option=='2':
                    building = input("Selecione o prédio (A, B ou C): ")

                    while(building != 'A' and building != 'B' and building != 'C'):
                        building = input("Prédio inválido, prédios disponiveis: A, B, C\nSelecione o prédio: ")

                    layer = input("Selecione o andar (1, 2 ou 3): ")

                    while(int(layer) < 1 or int(layer) > 3):
                        layer = input("Andar inválido, andares disponiveis: 1, 2, 3\nSelecione o andar: ")

                    slots = int(input("Digite a quantidade de vagas que serão adicionadas: "))
                    
                    msg = {"type": "adminAddSlot", "building": building, "layer": layer, "slots": slots}
                    self.sendTCP(self.prepareMsg(msg))
                    
                    print('\n' + self.getResponse()+'\n')

        self.sendTCP(self.prepareMsg({"type": "shutdown"}))

    def getServerAddr(self):
        self.closeSocket()
        self.createSocketUDP()
        self.sendUDP((DNS_IP, DNS_PORT), self.prepareMsg({"type": "requestServer"}))
        data, _ = self.sock.recvfrom(1024)
        return [self.loadMessage(data)]

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

    def getResponse(self):
        data, _ = self.sock.recvfrom(1024)

        return self.loadMessage(data)

Admin().run()
