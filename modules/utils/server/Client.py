#!/usr/bin/env python3

import socket, select, string, sys
from abc import ABC, abstractmethod
import re

import time
import modules.utils.server.Utils as u

class Client :
	def __init__ (self, host, port, args) :
		self.host = host
		self.port = port
		self.sessionId = 0
		self.isRunning = False
		# List to keep track of socket descriptors
		# Create socket instance
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.settimeout(2)
		self.args = args
		self.clientSpecificInit()

	def clientSpecificInit (self) :
		pass

	@abstractmethod
	def getType (self) :
		return "Client"

	#Function to broadcast chat messages to all connected clients
	def parseMessage (self, msg) :
		pattern = "<(.*)> (.*)"
		matches = re.search(pattern, msg)

		if matches and matches.group(1) == "Server" :
			if "tell me your name" in matches.group(2) :
				pattern = "\[(.*)\]"
				match = re.search(pattern, msg)
				self.sessionId = match.group(1)
				self.serverSocket.send(self.getType().encode())
				time.sleep(0.5)
			elif matches.group(2)=="You can awake" :
				self.clientSpecificAwake()
				time.sleep(0.5)
				self.serverSocket.send("Awaken".encode())
		else :
			self.parseBroadcast(msg)

	@abstractmethod
	def parseBroadcast (self, msg) :
		self.clientPrint("\r{0}".format(msg))

	def requestMessage (self) :
		self.clientPrint('<{0}> '.format(self.getType()))

	def awake (self) :
		# Boolean to keep the server running
		self.isRunning = True
		# Attempt to connect to server
		try :
			self.serverSocket.connect((self.host, self.port))
		except :
			self.clientStatePrint('Unable to connect\n')
			sys.exit()
		
		if not ('-c' in self.args) :
			self.clientStatePrint('Successfully connected to remote host.\n')
	
	def clientSpecificAwake(self) :
		pass
	
	def clientSpecificShutdown(self) :
		pass
	
	def clientSpecificInput(self) :
		msg = sys.stdin.readline()
		self.send(msg)
		self.requestMessage()
	
	def shutdown (self) :
		self.clientSpecificShutdown()
		time.sleep(0.5)
		self.serverSocket.close()

	def run (self) :
		self.awake()
		while self.isRunning :
			self.runningLoop()
		self.shutdown()
	
	def runningLoop (self) :
		# Moniter the user's input and the server
		socket_list = [sys.stdin, self.serverSocket]
		
		# Obtain list of readable sockets
		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
		
		for sock in read_sockets :

			# New messages from server
			if sock == self.serverSocket :
	
				# Recieve message
				data = sock.recv(4096).decode()
	
				if not data :
					self.clientStatePrint('\nDisconnected from chat server')
					sys.exit()
	
				else :
					# Parse valid message
					self.parseMessage(data)
			
			# Recieve message from user
			elif not ('-Nv' in self.args) :
				self.clientSpecificInput()
			
	def clientPrint(self, msg) :
		if not ('-Nv' in self.args) :
			sys.stdout.write(msg)
			sys.stdout.flush()
	
	def clientStatePrint(self, msg) :
		if not ('-Ns' in self.args) :
			sys.stdout.write(msg)
			sys.stdout.flush()

	def send(self, msg) :
		self.serverSocket.send(("|"+msg+"|").encode())
		
def launch(args) :
	client = Client(u.CLIENT_IP, u.PORT, args)
	client.run(sys.argv[1:])

if __name__ == "__main__" :
	launch(sys.argv[1:])
