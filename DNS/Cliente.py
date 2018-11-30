import socket
import pickle
import threading

class Cliente:
	def __init__(self):
		self.s = None

	def newSocket(self):
		self.s.close()
		self.criaSocket()
		
	def criaSocket(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	
	def requestAdress(self, servidor):
		self.setCamposSocket('127.0.0.1',9996)
		
		if self.s is None: self.criaSocket()
		else: self.newSocket()
		
		self.conect()
		
		if servidor is None: msg = input("DIGITE O SERVIDOR: ")
		else: msg = servidor
		
		if msg == "exit": return
		
		msgSerializada = pickle.dumps(msg)

		self.s.send(msgSerializada)
		
		msgSerializada = self.s.recv(1024)
	
		msg = pickle.loads(msgSerializada)
		
		print ("Resposta do server: ",msg)
		
		self.host, self.port = msg
		
		self.newSocket()
		
		self.conect()

	def comunica(self):
		while True:
			print ("ENTROU")
			msg = input("Digite sua mensagem: ")
			
			if msg == 'exit': break
			elif msg == 'mySQL' or msg == 'HTTP': self.requestAdress(msg)
			else:
				print ("MSG QUE IRA PRO DNS: ",msg)
			
				msgSerializada = pickle.dumps(msg)

				self.s.send(msgSerializada)
				
				msgSerializada = self.s.recv(1024)
				
				msg = pickle.loads(msgSerializada)
				
				print ("Resposta do server: ", msg)

	def setCamposSocket(self, h, p):
		self.host = h
		self.port = p
		self.dest = (self.host, self.port)

	def conect(self):
		self.s.connect(self.dest)
		
	def exit(self):
		self.s.close()
		
	def change(self, dest):
		self.s.connect(dest)
			
cliente = Cliente()

cliente.requestAdress(None)

cliente.comunica()

cliente.change(('127.0.0.1',9997))

print ("TROCOU")

cliente.exit()