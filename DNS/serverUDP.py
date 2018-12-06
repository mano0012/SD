import socket
import threading
import json
import pickle
import time

UDP_IP = "127.0.0.55"
UDP_SEND_PORT = 9996
UDP_RECEIVE_PORT = 9991

MESSAGE = json.dumps({"con": "SERVER", "type": "WEB"})

msgSerializada = pickle.dumps(MESSAGE)

sock = socket.socket(socket.AF_INET,  # Internet
                     socket.SOCK_DGRAM)  # UDP

sock.bind((UDP_IP, UDP_RECEIVE_PORT))

sock.sendto(msgSerializada, (UDP_IP, UDP_SEND_PORT))

data, addr = sock.recvfrom(1024)

print(pickle.loads(data))