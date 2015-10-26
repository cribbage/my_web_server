#!/usr/bin/env python3

from server import *

def main():
	try:
		server = Server()
	except KeyboardInterrupt:
		server.stop()
		
main()
