from global_vars import *

class Request():
	def __init__(self,request,client):	
		self.req = request.split(' ')
		self.method = self.req[0]
		self.path = self.req[1][1:]
		self.queryString = self.getQuery()
		self.postData = self.getPostData(client) if self.method == 'POST' else None	
	
	def getPostData(self,client):
		postBody = client.recv(1024).decode('utf-8')
		postData = {}
		for pair in postBody.split('&'):
			key,value = pair.split('=')
			postData[key] = value
		return postData
		
	def getQuery(self):
		try:
			queryData = {}
			self.path,qs = self.path.split('?')
			for pair in qs.split('&'):
				key,value = pair.split('=')
				queryData[key] = value
			return queryData
		except:
			return None

