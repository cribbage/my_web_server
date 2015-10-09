#!/usr/local/bin/python
import socket 
import os
import sys
import time
from os import curdir, sep

HOST = 'localhost'
PORT = 6969
TIMEOUT = 1
FILES = {'.jpg':{'mimeType':'image/jpg','mode':'rb'},
		'.txt':{'mimeType':'text/html','mode':'r'},
		'.html':{'mimeType':'text/html','mode':'r'},
		'.gif':{'mimeType':'image/gif','mode':'rb'}}


class Request():
	def __init__(self,request):
		self.path = '/'
		self.mode = ''
		self.mimeType = ''	
		self.req = str(request)
		self.getRequest()
		
	def getPath(self):
		Path = self.req[5:self.req[5:].find('/1')]
		if len(Path) != 0 :	
			self.path = Path
	
	def getPost(self):
		try:
			self.path,posts = self.path.split('?')
			f = open("posts.txt",'w+')
			for p in posts.split('&'):
				f.write(p+"\n")
			f.close()
		except:
			return	
	
	def getRequest(self):
		if 'GET' in self.req:
			self.getPath()
			self.getPost()	
			
		elif 'POST' in self.req:
			self.getPath() 
			self.getPost()	

class SocketRequestHandler(socket.socket):	
	def __init__(self):	
		socket.socket.__init__(self)
		self.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		self.bind((HOST,PORT))	
		self.authorized = True
	
	def addrInAuth(self,addr):
		f = open('authorized.txt','r+')
		if str(addr[0]) not in f.read():
			self.req.path = 'authorize.html'
			self.authorized = False
		f.close()
		
	def getConnection(self):
		self.listen(100)
		self.client,addr = self.accept()	
		self.req = Request(self.client.recv(1024).decode('utf-8'))
		self.req.getRequest()
		self.writeAddr(addr)
		print("Connection From: " + str(addr))
#		self.addrInAuth(addr)
		self.doGet()
		
				
	def writeAddr(self,addr):
		f = open("currentAddr.txt",'w')
		f.write(str(addr[0]))
		f.close()
		
	def runScript(self):
		files = [f for f in os.listdir('.') if os.path.isfile(f)]
		for f in files:
			if self.req.path == f:
				os.system(f)
			
	def sendBytes(self,message):
		self.client.send(bytes(message,'utf-8'))
		
	def sendReply(self,code):	
		try:
			self.prepHeaders()
			f = open(self.req.path,self.req.mode)
			self.sendResponse(code)
			self.sendHeader()
			if self.req.mimeType == "text/html":
				self.sendBytes(f.read())
			else:
				self.client.send(f.read())
			f.close()		
		except:
			self.sendError(404,"Something is not there.")
			return

	def sendHeader(self):
		self.prepHeaders()
		self.sendBytes("Content-Type:"+self.req.mimeType+"\r\n\r\n")
	
	def sendResponse(self,code):
		if code == 404:
			resp = ' Not Found\r\n'
		else:
			resp = ' OK\r\n'
		print("Sending: "+str(code))	
		self.sendBytes('HTTP/1.0 '+str(code)+resp)
		
	def sendError(self,code,message):	 
		self.req.mimeType = "text/html" 
		self.req.mode = 'r'
		self.sendResponse(code)
		self.sendHeader()
		ERR = open('error.txt','r') 		       
		self.sendBytes(ERR.read().replace('BFC',str(code)).replace('MSG',message))
		ERR.close()
		
	def isAuthorized(self):
		curAddr = open("currentAddr.txt",'r').read()
		addrs = open('authorized.txt','r').read().strip('\n').split('\n')
		newfile = ''
		self.authorized = False
		for ad in addrs:
			try:
				a,t = ad.split(',')
				if a == curAddr and time.time() <= float(t)+TIMEOUT:
					newfile+= a+','+str(time.time())+'\n'
					self.authorized = True
				else:
					newfile += a+t+'\n'
			except ValueError:
				continue
		open('authorized.txt','w').write(newfile)			
	
	def prepHeaders(self):
		for tpe in FILES:
			if self.req.path.endswith(tpe):
				self.req.mimeType = FILES[tpe]['mimeType']
				self.req.mode = FILES[tpe]['mode']
	
	def redirect(self):
		if not self.authorized and 'authorize' not in self.req.path:				
			self.req.path = "authorize.py"	
		if self.req.path=='/':
			self.req.path='home.txt'
		if self.req.path.endswith('.py'):
			self.runScript()
			self.req.path = 'script.txt'
			
	def clearPost(self):
		f = open("posts.txt",'w+')
		f.write('')
		f.close()
				
	def doGet(self):
		self.redirect()
	#	self.isAuthorized()
		self.sendReply(200)        
		self.clearPost()
		self.client.close()
		
def Main():	
	s = SocketRequestHandler()	
	s.getConnection()
	s.client.close()
	
while True:
	Main()	
	
