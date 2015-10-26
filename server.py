import socket

from global_vars import *
from client import *

class Server(socket.socket):	
	def __init__(self):	
		super().__init__()
		self.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.bind((HOST,PORT))	
		self.clients = {}
		self.serve()	
		
	def serve(self):
		while True:
			self.listen(1)
			client = Client(*self.accept())
			self.clients[client.ip] = client
	
	def stop():
		self.close()
