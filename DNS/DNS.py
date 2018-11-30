import socket
import threading
import pickle
import time

HOST = ''              # Endereco IP do Servidor
PORT = 9996            # Porta que o Servidor esta

class DNS:
	def __init__(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		orig = (HOST, PORT)
		self.s.bind(orig)
		self.s.listen(1)
		self.lista = list()
		
		#Cria lista de servers		
		self.lista.append(['mySQL','127.0.0.1',9997])
		self.lista.append(['HTTP','127.0.0.1',9998])
		self.lista.append(['CHAT','127.0.0.1',9999])
		self.lista.append(['DNS','127.0.0.1',9996])
				
		self.listen()

	def getAddress(self, host):
		for i in self.lista:
			name, address, port = i
			if name == host: return address, port
			
		return -1
		
	def listen(self):
		while True:
			con, cliente = self.s.accept()
			t = threading.Thread(target = self.clienteConectado ,args=(con, cliente))
			t.start()
	
	def clienteConectado(self,con, cliente):
		print ("Cliente conectado server DNS")
		
		msgSerializada = con.recv(1024)
		msg = pickle.loads(msgSerializada)
		
		print ("MENSAGEM RECEBIDA DO CLIENTE: ",msg)
			
		host = self.getAddress(msg)
		
		msgSerializada = pickle.dumps(host)
		
		print ("MSG QUE SERA ENVIADA: ",host)
		
		con.send(msgSerializada)
		
		con.close()
		
	def exit(self):
		self.s.close()
	
dns = DNS()