import socket
import pickle
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def waitingResponse():
	data = s.recv(1024)
	
	msg = pickle.loads(data)
	
	print ("RESPOSTA RECEBIDA: ", msg)
	
class Cliente:
	def setCamposSocket(self, h, p):

		HOST = h
		PORT = p
		dest = (HOST, PORT)
		
		return dest
		

	def conecta(self, dest):
		s.connect(dest)
		
	def enviaMSG(self):
		
		while True:
			msg = input("Informe seu nome: ")
			
			msgSerializada = pickle.dumps(msg)

			s.send(msgSerializada)
			
			if msg == 'exit': break
			
			t = threading.Thread(target=waitingResponse , args = ())
			t.start()
			
			
			
	def exit(self):
		s.close()
		
		
cliente = Cliente()

dest = cliente.setCamposSocket('127.0.0.1',9996)
cliente.conecta(dest)
cliente.enviaMSG()
cliente.exit()