from global_vars import *

class Response():
	
	statusCodes = {200:' OK\r\n',
					404:' Not Found\r\n'}
	
	def __init__(self,req,client):
		self.req = req
		self.client = client
		self.mode = None
		self.mimeType = None	
		self.sendReply()
				
	def sendBytes(self,message):
		self.client.send(bytes(message,'utf-8'))
		
	def sendReply(self):	
		try:
			self.prepHeaders()
			f = open(self.req.path,self.mode)
			self.sendStatus(200)
			self.sendHeader()
			if self.mimeType == "text/html":
				self.sendBytes(f.read())
			else:
				self.client.send(f.read())
			f.close()		
		except:
			self.sendError(404,"Something is not there.")

	def sendHeader(self):
		self.prepHeaders()
		self.sendBytes("Content-Type:"+self.mimeType+"\r\n\r\n")
	
	def sendStatus(self,code):
		self.sendBytes('HTTP/1.1 '+str(code)+self.statusCodes[code])
		
	def sendError(self,code,message):
		self.mimeType = "text/html" 
		self.mode = 'r'
		self.sendStatus(code)
		self.sendHeader()
		ERR = open('error.txt','r') 		       
		self.sendBytes(ERR.read().replace('BFC',str(code)).replace('MSG',message))
		ERR.close()
		
	def prepHeaders(self):
		for tpe in FILES:
			if self.req.path.endswith(tpe):
				self.mimeType = FILES[tpe]['mimeType']
				self.mode = FILES[tpe]['mode']
