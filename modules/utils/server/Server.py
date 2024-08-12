#!/usr/bin/env python

from logging import shutdown
import socket, select
from datetime import datetime
import sys, re, random, serial
from uuid import uuid4

import modules.utils.server.Utils as u

class Server:
	RECV_BUFFER = 4096 

	def __init__ (self, host, port) :
		self.host = host
		self.port = port
		self.isRunning = False
		# List to keep track of socket descriptors
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serverSocket.bind((host, port))
		self.serverSocket.listen(10)
		self.connectionDict = {}
		self.sessionId = str(uuid4())

	def parseMessage (self, sock, msg) :
		# Edit for your purpose
		# We broadcast the msg to all other clients for this tutorial
		for socketName in self.connectionDict:
			socket = self.connectionDict[socketName]

			if socket != self.serverSocket and socket != sock :
				try :
					socket.send(msg.encode())
				except :
					# Assume client disconnected if it refused the message
					socket.close()
					self.connectionDict.pop(socketName)

	def awake (self) :
		# Boolean to keep the server running
		self.isRunning = True
		# Add server socket to the list of readable connections
		self.connectionDict["Server"] = self.serverSocket
		print("Chat server started on port {0} of host {1}".format(self.port, self.host))
	
	def shutdown (self) :
		print("Server shutdown")
		self.serverSocket.close()
		exit

	def run (self) :
		self.awake()
		while self.isRunning :
			self.runningLoop()
		self.shutdown()

	def getKey (dict, val) :
		for key, value in dict.items() :
			if val == value :
				return key
		return "key doesn't exist"

	def runningLoop (self) :

		# Obtain list of readable sockets
		read_sockets, write_sockets, error_sockets = select.select(self.connectionDict.values() , [], [])

		for sock in read_sockets :
			# New client request
			if sock == self.serverSocket :

				# Add new client
				client, addr = self.serverSocket.accept()
				Server.Broadcast_data(client, "<Server> Take this id [{0}] and tell me your name".format(self.sessionId))
				# Recieve message
				while True :
					type = client.recv(Server.RECV_BUFFER).decode()
					if type :
						break
				self.connectionDict[type] = client

				sys.stdout.write("\r{0} ({1}, {2}) connected\n".format(type, addr[0], addr[1]))
				Server.Broadcast_data(client, "<Server> You can awake")
				# Recieve message
				while True :
					awaken = client.recv(Server.RECV_BUFFER).decode()
					if awaken :
						break

			
			# New message from a client
			else :			
				sockName = Server.getKey(self.connectionDict, sock)	
				try :
					# Recieve message
					data = sock.recv(Server.RECV_BUFFER).decode()

					if data :
						for msg in data.split('|') :
							if msg!="" :
								# Parse valid message
								if msg=="Server shutdown" :
									self.isRunning = False
								else :
									now = datetime.now()
									self.parseMessage(sock, "\r[{0}] {1} | <{2}> {3}\n".format(now, sock.getpeername(), sockName, msg))
				
				except :
					# Assume client disconnected if they failed to send the meesage

					Server.Broadcast_data(sock, "{0} is offline".format(sockName))
					print("{0} is offline".format(sockName))
					
					sock.close()
					self.connectionDict.pop(sockName)
					continue

	def Broadcast_data (client, msg) :
		client.send(msg.encode())

def launch() :
	serv = Server(u.SERVER_IP, u.PORT)
	serv.run()

if __name__ == "__main__":
	launch()