import Enc
import json
import MySocket
import threadPool

MAX_THREADS = 100
THREAD_BLOCK = 10
class Store:
    def __init__(self):
        self.enc = Enc.Enc()
        self.threads = threadPool.tPool(self.run, MAX_THREADS, THREAD_BLOCK)
        self.sockServer = MySocket.MySocket("127.0.0.1", 20002)
        self.sockCliente = MySocket.MySocket("127.0.0.1", 20003)
        self.sockServer.createServerTCP()
        self.sockCliente.createClientTCP()

        self.data = json.loads('{"A": {"Vagas": {"1": 30, "2":30, "3":30} },"B": {"Vagas": {"1": 10, "2":10} }, "C": {"Vagas": {"1": 10, "2":10, "3":10} } }')
        self.list = []
        #print(self.data['A']['Vagas']['3'])

    def run(self, connection):
        print("RODOU")
        connection.shutdown(2)
        connection.close()
        self.threads.repopulate()
    
    def waitClient(self):
        while True:
            con, client = self.sockServer.accept()

            print("Cliente ", client, " conectado")
            t = self.threads.getThread([con])

            t.start()

    def connect(self):
        self.sockCliente.connect("127.0.0.1", 20000)
        #self.sockCliente.closeSocket()


store = Store()
store.connect()

#FALTA FAZER A INTERAÇÃO ENTRE AS STORES E OS SERVIDORES
