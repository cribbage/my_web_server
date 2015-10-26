import threading

from global_vars import *
from request import *
from response import *

class Client(threading.Thread):
	def __init__(self,client,addr):
		super().__init__()
		self.c = client
		self.ip, self.port = addr
		self.start()
				
	def run(self):
		try:	
			req = Request(self.c.recv(1024).decode('utf-8'),self.c)
			Response(req,self.c)
			self.c.close()
		except:
			pass

