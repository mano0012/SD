import socket
import threading
import pickle
import time

HOST = ''              # Endereco IP do Servidor
PORT = 9997            # Porta que o Servidor esta

def conectado(con, cliente):
	
	print ("Cliente conectado server SQL")

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