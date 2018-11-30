import socket
import threading
import json
import pickle
import time

HOST = ''              # Endereco IP do Servidor
PORT = 9998            # Porta que o Servidor esta

class DNS:
	def __init__(self):
		self.services = ["WEB", "SQL", "CHAT"]
		self.serverList = self.services
		
		#Socket UDP
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

		self.s.bind((HOST, PORT))
			
		for i in range(len(self.services)):
			self.serverList[i] = list()
			
		#Settar as configurações da thread
			
	def run(self):
		#while True:
		data, addr = self.s.recvfrom(1024)
		#Settar uma thread para rodar
		
		message = json.loads(pickle.loads(data))
		
		print(message["type"])
	'''	
	def sendMsg():
	
	def msgRecebida(self, msg, addr):
		if msg == "SERVER":
			self.addServer(type, addr)
			
		else:
		
		
	'''


ddd = DNS()

ddd.run()




'''


























def conectado(con, cliente):
	
	print ("Cliente conectado server WEB")

	while True:
		msgSerializada = con.recv(1024)
		print ("Cliente: ", cliente)
		msg = pickle.loads(msgSerializada)
		
		if msg == 'exit': break
		
		print ("Mensagem: ", msg)
	
		msg = 'RECEBIDO'
		
		msgSerializada = pickle.dumps(msg)
		
		con.send(msgSerializada)
	

	print ('Finalizando conexao do cliente ', cliente)
	
	con.close()
	
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

orig = (HOST, PORT)
 
s.bind(orig)
s.listen(1)

while True:
	con, cliente = s.accept()
	t = threading.Thread(target=conectado ,args=(con, cliente))
	t.start()

s.close()
'''