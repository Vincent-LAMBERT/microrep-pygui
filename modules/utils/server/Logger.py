#!/usr/bin/env python

import os
import socket, select, string, sys
from abc import ABC, abstractmethod
import utils

from modules.utils.server.Client import Client
import modules.utils.server.Utils as u

class Logger (Client) :
    def clientSpecificAwake (self) :
        # Create the log folder if it doesn't exist
        if not os.path.exists("./logs") :
            os.makedirs("./logs")
        self.file = open("./logs/logs_{0}.txt".format(self.sessionId), mode="w", encoding='utf-8')
        self.file.write("---------------------------------------\n")
        self.file.write("------ LOG FILE FOR PYTHON SERVER -----\n")
        self.file.write("---------------------------------------")
        self.file.close()

    def getType (self) :
        return "Logger"

    def parseBroadcast (self, msg) :
        self.clientPrint("\r{0}\n".format(msg.strip('\n')))
        self.file = open("./logs/logs_{0}.txt".format(self.sessionId), mode="a", encoding='utf-8')
        self.file.write("{0}".format(msg))
        self.file.close()
    
    def requestMessage (self) :
        pass
    
    def clientSpecificShutdown(self) :
        pass
    
    def clientSpecificInput(self) :
        pass

def launch(args) :
	client = Logger(u.CLIENT_IP, u.PORT, args)
	client.run()

if __name__ == "__main__" :
	launch(sys.argv[1:])
