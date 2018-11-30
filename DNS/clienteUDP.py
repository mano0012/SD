import socket
import threading
import json
import pickle
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 9998

MESSAGE = json.dumps({"con":"CLIENTE", "type":"WEB"})

msgSerializada = pickle.dumps(MESSAGE)
   
sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_DGRAM) # UDP

sock.sendto(msgSerializada, (UDP_IP, UDP_PORT))