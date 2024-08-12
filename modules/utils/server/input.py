#!/usr/bin/env python

from http import client
import socket, select, string, sys, re
from abc import ABC, abstractmethod
from colorama import Fore
import utils
import curtsies
from threading import Thread

from client import CustomClient

class Input (CustomClient) :
    def getType (self) :
        return "Input"

    def parseBroadcast (self, msg) :
        pattern = "(.*) \| <(.*)> (.*)"
        for match in re.finditer(pattern, msg) :
            new_msg = match.group(3)
            if match and match.group(2)=="Controller" :
                cMsg = utils.analyseControlerMsg(new_msg)
                if re.search("Starting phase ([256]) .*", cMsg["Message"]) :
                    self.directInputMode = not self.directInputMode
                    self.clientPrint("\r{0}\n".format("----------------------------------------------------------"))
                    self.clientPrint("\r{0}\n".format(cMsg["Message"]))
                    self.clientPrint("\r{0}\n".format("----------------------------------------------------------"))

                elif cMsg :
                    if  cMsg["Token"]=="PHASE" :
                        self.clientPrint("\r{0}\n".format("----------------------------------------------------------"))
                        self.clientPrint("\r{0}\n".format(cMsg["Message"]))
                        self.clientPrint("\r{0}\n".format("----------------------------------------------------------"))
                        if re.search("Starting phase ([3]) .*", cMsg["Message"]) :
                            self.clientPrint('\r'+Fore.RED+'CAUTION : YOU MUST TELL TO THE PARTICIPANT TO JUDGE THE \nREPRESENTATIONS ACCORDING TO THE MICROGESTURE DEFINED AND SHOW IT\n TO THEM AT THE START OF EVERY STATE'+Fore.WHITE+'\n')
                    elif cMsg["Token"] in ["REPRESENTATION", "MESSAGE"]  :
                        self.clientPrint("\r{0}\n".format(cMsg["Message"]))
                    
    
    def clientSpecificInput (self) :
        if self.directInputMode :
            self.listenInput()
        else :
            return super().clientSpecificInput()
    
    def listenInput(self) :
        with curtsies.Input(keynames='curses') as input_generator:
            for e in input_generator:
                if isinstance(e, curtsies.events.PasteEvent) :
                    e = "\\n"
                self.send(repr(e))
                self.stillListenServer()
                if repr(e)=="'\\x1b'":
                    self.directInputMode=False
                    break
                if not self.directInputMode :
                    break

    def stillListenServer(self) :
        # Recieve max of 2 messages
        for i in range(4) :
            try :
                data = self.serverSocket.recv(4096).decode()

                if not data :
                    self.clientStatePrint('\nDisconnected from chat server')
                    sys.exit()

                else :
                    # Parse valid message
                    self.parseMessage(data)
            except :
                break

    def requestMessage (self) :
        pass

    def clientSpecificInit(self):
        self.directInputMode=False
        self.listening = False
    
    def clientSpecificAwake(self) :
        self.clientPrint("\r{0}\n".format("----------------------------------------------------------"))
        self.clientPrint("\r{0}\n".format("----------- Discoverability in AR experience 1 -----------"))
        self.clientPrint("\r{0}\n".format("----------------------------------------------------------"))
        self.clientPrint("\r{0}\n".format(""))
        self.clientPrint("\r{0}\n".format("Press enter to start the experience"))

def launch(args) :
	client = Input(utils.CLIENT_IP, utils.PORT, args)
	client.run()

if __name__ == "__main__" :
	launch(sys.argv[1:])
