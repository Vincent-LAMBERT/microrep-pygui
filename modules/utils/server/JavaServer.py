import random
import socket
import threading
from datetime import datetime
import json
import time
import numpy
from colorama import Fore
# import curtsies
import sys
import select
from abc import ABC, abstractmethod
import os 
if os.name == 'nt' :
    import msvcrt
from uuid import uuid4
import re
import pygsheets

import sshkeyboard

MSG_LENGTH = 1024

FORMAT = 'utf-8'

CLIENT_IP = "localhost"
SERVER_IP = "localhost"
# SERVER_IP = "192.168.37.61"
PORT = 5000

IMAGES = ["f_tu_ic_mc_rc_pc", "f_tu_ic_mc_rc_pf", "f_tu_ic_mc_rc_pu", "f_tu_ic_mc_rd_pb", "f_tu_ic_mc_rf_pc"]

serverFiles = os.path.join(os.path.dirname(__file__), "serverFiles.txt")

def format_data(hostname, data, id) :
    time = datetime.now().strftime('%d/%m/%y  %H:%M:%S.%f')
    return json.dumps({"hostname": hostname, "data": data, "timestamp": time, "id": id})

class JavaServer(threading.Thread):
    
    def __init__(self, mode=None, host="localhost", port=5000):
        threading.Thread.__init__(self)
        self.host = host
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, port))
        self.running = True
        self.server_started = False
        self.mode = mode
        
        self.images = IMAGES.copy()
                        
    def set_mode(self, mode):
        self.mode = mode
                    
    def start_server(self):
        self.server_started = True
        
    def stop_server(self):
        self.server_started = False

    def run(self):
        while self.running:
            if not self.server_started:
                self.server.listen()
                print(f"[LISTENING] Server is listening on {self.host}")
                self.server_started = True
            else:
                conn, addr = self.server.accept()
                print(f"[CONNECTION] {addr} connected.")
                # self.handle_client(conn, addr)
                thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                thread.start()
                print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

    def handle_client(self, conn, addr):
        while self.running:
            try:
                ready_to_read, ready_to_write, in_error = select.select([conn,], [conn,], [], 5)
            except select.error:
                conn.shutdown(2)    # 0 = done receiving, 1 = done sending, 2 = both
                conn.close()
                print(f"[ERROR] Connection {addr} ended.")
                break
            
            # RECEIVE DATA
            if len(ready_to_read) > 0 and len(ready_to_write) > 0:
                msg = conn.recv(MSG_LENGTH).decode(FORMAT)
                if msg:
                    # Remove '\n' from the message
                    msg = msg.replace("\n", "")
                    print(f"[DATA] RECEIVED: {msg}")
                    
                    if self.mode == None :
                        self.mode = self.ask_and_set_mode(conn)
                    
                    if (self.mode == "explorable"):
                        if len(self.images)>0:
                            self.send_data(conn, "[DATA]", self.images.pop())
                            time.sleep(1)
                            # self.send_data(conn, "[ALERT]", "Banane")
                            # self.send_data(conn, "[CONFIRMATION]", [True, False][random.randint(0, 1)])
                            # time.sleep(2)   
                        else :
                            self.close(conn)
                            break
                    
                    if "[CLOSE]" in msg:
                        self.close(conn)
                        break
                    elif "[MODE] EXIT" in msg:
                        self.mode = None
    
    def ask_and_set_mode(self, conn):
        mode = input("\n\nEnter mode: ")
        msg = f"[MODE] {mode}" 
        conn.send(msg.encode(FORMAT))
        conn.send("\n".encode(FORMAT))
        print(f"{msg}\n")
        return mode
    
    def send_data(self, conn, key, data):
        msg = f"{key} {data}"
        if conn is not None:
            conn.send(msg.encode(FORMAT))
            conn.send("\n".encode(FORMAT))
            print(msg)
        else :
            print("[ERROR] Connection is not established.")
    
    def close(self, conn):
        if conn is not None:
            conn.send("[CLOSE]".encode(FORMAT))
            conn.send("\n".encode(FORMAT))
            print("[CLOSE]")
            time.sleep(1)
            self.running = False
        else :
            print("[ERROR] Connection is not established.")

class Server(threading.Thread):
    RECV_BUFFER = 4096
    
    def __init__(self, host, port):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.name = "Server"
        self.isRunning = False
        # List to keep track of socket descriptors
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((host, port))
        self.serverSocket.listen(10)
        self.connectionDict = {}
        self.sessionId = str(uuid4())

    def parseMessage(self, sock, msg) :
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

    def awake(self) :
        # Boolean to keep the server running
        self.isRunning = True
        # Add server socket to the list of readable connections
        self.connectionDict[self.name] = self.serverSocket
        print("Chat server started on port {0} of host {1}".format(self.port, self.host))

    def shutdown(self) :
        self.isRunning = False
        self.serverSocket.close()
        print("Server shutdown")
        sshkeyboard.stop_listening()
        exit

    def run(self) :
        self.awake()
        while self.isRunning :
            try :
                self.runningLoop()
            except :
                exit

    def getKey(dict, val) :
        for key, value in dict.items() :
            if val == value :
                return key
        return "key doesn't exist"

    def runningLoop(self) :
        # Obtain list of readable sockets
        read_sockets, write_sockets, error_sockets = select.select(self.connectionDict.values() , [], [], 5)
        
        for sock in read_sockets :
            
            # New client request
            if sock == self.serverSocket :

                # Add new client
                client, addr = self.serverSocket.accept()
                json_msg = format_data(self.name, "Take this id [{0}] and tell me your name".format(self.sessionId), self.sessionId)
                Server.broadcast_data(client, json_msg)
                # Recieve message
                while True :
                    type = client.recv(Server.RECV_BUFFER).decode()
                    if type :
                        break
                self.connectionDict[type] = client

                sys.stdout.write("\r{0} ({1}, {2}) connected\n".format(type, addr[0], addr[1]))
                json_msg = format_data(self.name, "You can awake".format(self.sessionId), self.sessionId)
                Server.broadcast_data(client, json_msg)
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
                    json_msg = sock.recv(Server.RECV_BUFFER).decode()

                    if json_msg :
                        msg = json.loads(json_msg)
                        data = msg["data"]
                        self.parseMessage(sock, json_msg)
                        
                        # Parse valid message
                        if data=="Server shutdown" :
                            self.shutdown()
                
                except :
                    # Assume client disconnected if they failed to send the meesage
                    msg = "{0} is offline".format(sockName)
                    Server.broadcast_data(sock, msg)
                    print(msg)
                    
                    sock.close()
                    self.connectionDict.pop(sockName)
                    continue

    def broadcast_data(client, msg) :
        client.send(msg.encode())

class Client(threading.Thread) :
    def __init__ (self, host, port, args) :
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.sessionId = 0
        self.isRunning = False
        self.show = True
        # List to keep track of socket descriptors
        # Create socket instance
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.settimeout(2)
        self.args = args
        self.clientSpecificInit()

    def clientSpecificInit(self) :
        pass

    @abstractmethod
    def getType (self) :
        return "Client"

    #Function to broadcast chat messages to all connected clients
    def parseMessage(self, json_msg) :
        msg = json.loads(json_msg)
        hostname, data = msg["hostname"], msg["data"]

        if hostname and hostname == "Server" :
            if "tell me your name" in data :
                self.sessionId = msg["id"]
                self.serverSocket.send(self.getType().encode())
                time.sleep(0.5)
            elif data=="You can awake" :
                self.clientSpecificAwake()
                time.sleep(0.5)
                self.serverSocket.send("Awaken".encode())
        else :
            self.parseBroadcast(msg)

    @abstractmethod
    def parseBroadcast (self, msg) :
        self.clientPrint("\r{0}".format(msg))

    # def requestMessage (self) :
    #     self.clientPrint('<{0}> '.format(self.getType()))

    def awake (self) :
        # Boolean to keep the server running
        self.isRunning = True
        # Attempt to connect to server
        try :
            self.serverSocket.connect((self.host, self.port))
        except :
            self.clientPrint('Unable to connect\n')
            sys.exit()
        
        if not ('-c' in self.args) :
            self.clientPrint('Successfully connected to remote host.\n')

    def clientSpecificAwake(self) :
        pass

    def clientSpecificShutdown(self) :
        pass

    def clientSpecificInput(self) :
        msg = sys.stdin.readline()
        
        # Remove the trailing '\n' character
        msg = msg.replace("\n", "")
        self.send(msg)
        # self.requestMessage()

    def shutdown (self) :
        self.isRunning = False
        self.clientSpecificShutdown()
        time.sleep(0.5)
        self.serverSocket.close()
        print("\nClient shutdown")
        sshkeyboard.stop_listening()
        exit

    def run (self) :        
        self.awake()
        while self.isRunning :
            try :
                self.runningLoop()
            except Exception as e:
                print("Error {0}".format(e))
                self.shutdown()

    def runningLoop (self) :
        # Moniter the user's input and the server
        if os.name == 'nt' :
            socket_list = [self.serverSocket]
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [], 1)
            if msvcrt.kbhit(): read_sockets.append(sys.stdin)
        else :
            socket_list = [self.serverSocket, sys.stdin]
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
        
        # Check if there is a message to read in sys.stdin
        
        for sock in read_sockets :

            # New messages from server
            if sock == self.serverSocket :

                # Recieve message
                data = sock.recv(4096).decode()

                if not data :
                    self.clientPrint('\nDisconnected from chat server')
                    sys.exit()
                else :
                    # Parse valid message
                    self.parseMessage(data)
            
            # Recieve message from user
            elif not ('-Nv' in self.args) :
                self.clientSpecificInput()
            
    def clientPrint(self, msg) :
        if not ('-Nv' in self.args) and self.show:
            sys.stdout.write(msg)
            sys.stdout.flush()

    def send(self, data) :
        json_msg = format_data(self.getType(), data, self.sessionId)
        self.serverSocket.send(json_msg.encode())
        time.sleep(0.5)

class Logger (Client) :
    def clientSpecificInit(self):
        pass
            
    def getType (self) :
        return "Logger"

    def parseBroadcast (self, msg) :
        self.clientPrint("\r{0}\n".format(msg))
        self.file = open("./logs/logs_{0}.txt".format(self.sessionId), mode="a", encoding='utf-8')
        self.file.write("{0}".format(msg))
        self.file.close()
    
    # def requestMessage (self) :
    #     pass
    
    def clientSpecificAwake (self) :
        # Create the log folder if it doesn't exist
        if not os.path.exists("./logs") :
            os.makedirs("./logs")
        self.file = open("./logs/logs_{0}.txt".format(self.sessionId), mode="w", encoding='utf-8')
        self.file.write("---------------------------------------\n")
        self.file.write("------ LOG FILE FOR PYTHON SERVER -----\n")
        self.file.write("---------------------------------------")
        self.file.close()
    
    def clientSpecificShutdown(self) :
        pass
    
    def clientSpecificInput(self) :
        pass

class Input (Client) :
    def clientSpecificInit(self):
        self.directInputMode = False        
        self.input_message = ""
        
    def getType (self) :
        return "Input"

    def parseBroadcast (self, msg) :
        hostname, data = msg["hostname"], msg["data"]
        
        if hostname and hostname=="Controller" :
            if isinstance(data, dict):
                inputMode = data[INPUT_MODE]
                if inputMode==INPUT_DIRECT_MODE :
                    self.directInputMode = True
                    self.clientPrint("\rDirect input mode\n")
                else :
                    self.directInputMode = False
                    self.clientPrint("\rEnter input mode\n")
            
            # if re.search("Direct", cMsg["Message"]) :
            #     self.directInputMode = True
            # else:
            #     self.directInputMode = False

    def requestMessage (self) :
        pass
    
    def clientSpecificAwake(self) :
        self.clientPrint("\r{0}\n".format("----------------------------------------------------------"))
        self.clientPrint("\r{0}\n".format("----------- Discoverability in AR experience 1 -----------"))
        self.clientPrint("\r{0}\n".format("----------------------------------------------------------"))
        self.clientPrint("\r{0}\n".format(""))
        self.clientPrint("\r{0}\n".format("Press enter to start the experience"))

        
    def clientSpecificInput (self) :
        pass
            
    def keyboard_input (self, key) :
        if self.directInputMode :
            self.send(key)
        else :
            # Input not ended
            if key != 'enter':
                print(key, end='')
                sys.stdout.flush()
                self.input_message += key
            else :
                print()
                self.send(self.input_message)
                self.input_message = ""

HOSTNAME = "hostname"
DATA = "data"

INPUT_MODE = "InputMode"
INPUT_DIRECT_MODE = "Direct"
INPUT_ENTER_MODE = "Enter"

PHASE="Phase"
STEP="Step"

class Experiment:
    def __init__(self) -> None:
        self.directInputMode=0
        self.min_phase=0
        self.max_phase=4
        self.phase=self.min_phase
        self.step=0 # We start at zero to take into account the incrementation due to the "I'm ready" message

    # def ask(self, msg, function) :
    #     self.lastCondition = function
    #     self.requestMessage()
    #     self.clientPrint(msg+"\n")
    #     if self.phase in [1,2,3] :
    #         pattern = "(.*) - (.*)"
    #         match = re.search(pattern, msg)
    #         token = match.group(1)
    #         content = match.group(2)
    #         self.lastMsg = "{0} - P{1}_{2}".format(token, self.phase, content)
    #     else :
    #         self.lastMsg = msg
    #     self.send(msg)

    # def handleAnswer(self, answer) :
    #     answr = answer
    #     if self.directInputMode :
    #         answr = self.interpret(answer)
    #         if answr=="Esc":
    #             self.saveDataAndExit()
    #             return

    #     if self.phase in [0,2] :
    #         self.saveAnswer(answr)
    #         if self.step==len(self.orderPhase1)-1 :
    #             self.nextPhase()
    #         else :
    #             self.nextState()
    #     if self.phase in [1,3] :
    #         if answr in ANSW_PHASE2_SWITCH :
    #             if answr==ANSW_PHASE2_SWITCH[0] :
    #                 self.previousState()
    #             else :
    #                 self.nextState()
        
    #     self.askState()

    # def nextState(self) :
    #     self.step+=1
    #     self.clientPrint("STEP - Step {0}".format(self.step))

    # def previousState(self) :
    #     self.step-=1
    #     self.clientPrint("STEP - Step {0}".format(self.step))

    # def nextPhase(self) :
    #     self.phase += 1
    #     self.step = 1
    #     self.clientPrint("PHASE - Starting phase {0} with {1} states".format(self.phase, str(self.getStateNbrFromPhase())))
    #     self.clientPrint("INFORMATION - {0}".format(self.getInformationFromPhase()))
    #     self.clientPrint("STEP - Step {0}".format(self.step))
    
    def getStateNbr(self) :
        return { i: len(self.getInformations()[i][STEP]) for i in range(self.min_phase, self.max_phase+1) }[self.phase]
    
    def getInputModes(self) :
        return { 0:'INPUT_ENTER_MODE', 1: INPUT_ENTER_MODE, 2: INPUT_DIRECT_MODE, 3: INPUT_DIRECT_MODE, 4: "Save and shutdown" }
    
    def getInformations(self) :
        return {
            0: {PHASE: "Preliminary questions", 
                  STEP: { 0: "Consent form",
                          1: "What is your age?",
                          2: "What gender to you identify with?",
                          3: "Are you left or right handed?"}},
            1: {PHASE: "Initial phase", 
                  STEP: { 0: "Free exploration",
                          1: "Explanations"}},
            2: {PHASE: "Learning phase", 
                  STEP: { 0: "Free learning until confident",
                          1: "Learning block 1",
                          2: "Test block 1",
                          3: "Learning block 2",
                          4: "Test block 2",
                          5: "Learning block 3",
                          6: "Test block 3",
                          7: "Learning block 4",
                          8: "Test block 4",
                          9: "Learning block 5",
                          10: "Test block 5",
                          11: "Learning block 6",
                          12: "Test block 6",
                          13: "Learning block 7",
                          14: "Test block 7",}},
            3: {PHASE: "Memory phase", 
                  STEP: { 0: "5 minutes pause",
                          1: "Memory block"}},
            4: {PHASE: "Save and shutdown", 
                  STEP: { 0: "Save",
                          1: "Shutdown"}}            
        }

    # def askState(self) :
    #     if self.phase==0 :
    #         if self.step==0 :
    #             self.saveDict["Id"] = self.sessionId
    #             self.send("PHASE - Starting phase {0} with {1} states".format(self.phase+1, str(self.getStateNbrFromPhase())))
    #             self.send("INFORMATION - {0}".format(self.getInformationFromPhase()))
    #             self.send("STEP - Step {0}".format(self.step+1))
    #             self.ask("MESSAGE - Quel est votre âge?", lambda x : x.isdigit())
    #         elif self.step==1 :
    #             self.ask("MESSAGE - Quel est votre genre?", lambda _ : True)
    #         elif self.step==2 :
    #             self.ask("MESSAGE - Avez vous pris part à notre précédente étude en ligne? [y/n]", lambda x : (x=="y") or (x=="n"))
    #         elif self.step==3 :
    #             self.ask("MESSAGE - Statique ou dynamique? [s/d]", lambda x : (x=="s") or (x=="d"))
    #         else :
    #             self.nextPhase()
    #             self.shuffleSeeds()
    #             self.ask("MESSAGE - Connectez le dispositif et appuyez sur entrée quand vous êtes prêt·e", lambda _ : True)
    #             self.step-=1 # compensate the increments due to the enter
    #     elif self.phase==1 :
    #         self.ask("REPRESENTATION - {0}".format(self.orderPhase1[self.step]), lambda x : x in REP_MICROGESTURE)
    #     elif self.phase==2 :
    #         size = len(self.orderPhase2[self.step])
    #         microgesture = self.orderPhase2[self.step][self.subState%size]
    #         self.ask("REPRESENTATION - {0}".format(microgesture["Representation"]), 
    #                 lambda x : x in ANSW_PHASE2)
    #         if not microgesture["SeenState"] :
    #             self.orderPhase2[self.step][self.subState%size]["SeenState"] = True
    #             self.seenSubStates+=1
    #             self.send("SUBSTATE - {0}/4 vus".format(self.seenSubStates))
    #     elif self.phase==3 :
    #         self.ask("REPRESENTATION - {0}".format(self.orderPhase3[self.step]), lambda x : x in REP_MICROGESTURE)
    #     elif self.phase==4 :
    #         if self.step==0 :
    #             self.ask("MESSAGE - Appuyez sur entrée pour continuer", lambda _ : True)
    #         elif self.step==1 :
    #             self.ask("MESSAGE - Avez-vous une préférence entre les représentations animées et les non-animées et pourquoi?", lambda _ : True)
    #         elif self.step==2 :
    #             self.ask("MESSAGE - Avez-vous une préférence entre les différents types de représentations que vous avez rencontrés et pourquoi?", lambda _ : True)
    #         else :
    #             self.nextPhase()
    #             self.ask("MESSAGE - C'est la fin de l'expérience. Appuyez sur Entrée pour passer en mode libre. Vous pourrez ensuite appuyer sur Echap pour sauvegarder les données", lambda _ : True)
    #             self.step-=1 # compensate the increments due to the enter
    #     else :
    #         size = len(self.orderPhase5)
    #         self.ask("REPRESENTATION - {0}".format(self.orderPhase5[self.step%size]), lambda x : x in ANSW_PHASE2)

    # def interpret(self, key) :
    #     if key=="'7'":
    #         self.send("DETECTED - Tap")
    #         return "Tap"
    #     elif key=="'9'":
    #         self.send("DETECTED - Swipe")
    #         return "Swipe"
    #     elif key=="'3'":
    #         self.send("DETECTED - Stretch")
    #         return "Stretch"
    #     elif key=="'1'":
    #         self.send("DETECTED - Hold")
    #         return "Hold"
    #     elif key=="'s'":
    #         self.send("DETECTED - Very bad")
    #         return "Very bad"
    #     elif key=="'d'":
    #         self.send("DETECTED - Bad")
    #         return "Bad"
    #     elif key=="'f'":
    #         self.send("DETECTED - Quite bad")
    #         return "Quite bad"
    #     elif key=="'g'":
    #         self.send("DETECTED - Quite good")
    #         return "Quite good"
    #     elif key=="'h'":
    #         self.send("DETECTED - Good")
    #         return "Good"
    #     elif key=="'j'":
    #         self.send("DETECTED - Very good")
    #         return "Very good"
    #     elif key=="'('":
    #         self.send("DETECTED - Previous")
    #         return "Previous"
    #     elif key=="'-'":
    #         self.send("DETECTED - Next")
    #         return "Next"
    #     elif key=="'\\x1b'":
    #         self.send("DETECTED - Server shutdown")
    #         return "Esc"
    
    # def shuffleSeeds(self) :
    #     self.orderPhase1 = self.saveSeedAndShuffleList("Seed Phase 1", self.orderPhase1)
    #     self.orderPhase2_Microgesture = self.saveSeedAndShuffleList("Seed Phase 2 | Microgesture", self.orderPhase2_Microgesture)

    #     for microgesture in REP_MICROGESTURE :
    #         for step in REP_STATE :
    #             dictKey = "Seed Phase 2 | Family for {0} {1}".format("static" if step=="S" else "dynamic", microgesture)
    #             if step=="S" :
    #                 if microgesture=="Tap" :
    #                     self.orderPhase2_Family_Static_Tap = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Static_Tap))

    #                 elif microgesture=="Swipe" :
    #                     self.orderPhase2_Family_Static_Swipe = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Static_Swipe))
    #                 elif microgesture=="Stretch" :
    #                     self.orderPhase2_Family_Static_Stretch = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Static_Stretch))
    #                 else :
    #                     self.orderPhase2_Family_Static_Hold = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Static_Hold))
    #             else :
    #                 if microgesture=="Tap" :
    #                     self.orderPhase2_Family_Dynamic_Tap = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Dynamic_Tap))
    #                 elif microgesture=="Swipe" :
    #                     self.orderPhase2_Family_Dynamic_Swipe = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Dynamic_Swipe))
    #                 elif microgesture=="Stretch" :
    #                     self.orderPhase2_Family_Dynamic_Stretch = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Dynamic_Stretch))
    #                 else :
    #                     self.orderPhase2_Family_Dynamic_Hold = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Dynamic_Hold))
        
    #     rep_static = {"Tap": [self.orderPhase2_Family_Static_Tap], 
    #                   "Swipe": [self.orderPhase2_Family_Static_Swipe], 
    #                   "Stretch": [self.orderPhase2_Family_Static_Stretch], 
    #                   "Hold": [self.orderPhase2_Family_Static_Hold]}
    #     rep_dynamic = {"Tap": [self.orderPhase2_Family_Dynamic_Tap], 
    #                   "Swipe": [self.orderPhase2_Family_Dynamic_Swipe], 
    #                   "Stretch": [self.orderPhase2_Family_Dynamic_Stretch], 
    #                   "Hold": [self.orderPhase2_Family_Dynamic_Hold]}

    #     orderStatic, orderDynamic = [], []
    #     for microgesture in self.orderPhase2_Microgesture :
    #         orderStatic += rep_static[microgesture]
    #         orderDynamic += rep_dynamic[microgesture]
        
        
        
    #     if self.saveDict[self.getKeyFromStr("Statique ou dynamique? [s/d]")]=="s" :
    #         self.orderPhase2 = orderStatic + orderDynamic
    #     else :
    #         self.orderPhase2 = orderDynamic + orderStatic
    
    #     self.orderPhase3 = self.saveSeedAndShuffleList("Seed Phase 3", self.orderPhase3)
        
    
    # def saveSeedAndShuffleList(self, dictKey, listToShuffle) :
    #     self.saveDict[self.getKeyFromStr(dictKey)] = int(uuid4())
    #     random.Random(self.saveDict[self.getKeyFromStr(dictKey)]).shuffle(listToShuffle)
    #     return listToShuffle
    
    # def addSeenState(self, locallist) :
    #     for i in range(len(locallist)) :
    #         locallist[i] = {"Representation" : locallist[i], "SeenState" : False}
    #     return locallist
    
    ################## SAVE DATA ##################

    # def saveAnswer(self, word) :
    #     try :
    #         new_key = self.getKeyFromStr(str(analyseControlerMsg(self.lastMsg)["Message"]))
    #     except :
    #         new_key = str(analyseControlerMsg(self.lastMsg)["Message"])
    #     if new_key!=None :
    #         self.saveDict[new_key] = word
    #         self.saveData()

    # def getKeyFromStr(self, stri) :
    #     return {
    #         'P1_Connectez le dispositif et appuyez sur entrée quand vous êtes prêt·e': None,
    #         'Appuyez sur entrée pour continuer' : None,
    #         'Quel est votre âge?': 'Age',
    #         'Quel est votre genre?': 'Gender',
    #         'Avez vous pris part à notre précédente étude en ligne? [y/n]': 'Previous study done',
    #         'Statique ou dynamique? [s/d]': 'Pref Static/Dynamic',
    #         'Seed Phase 1': 'Seed P1',
    #         'Seed Phase 2 | Microgesture': 'Seed P2 MG',
    #         'Seed Phase 2 | Family for static Tap' : 'Seed P2 F ST',
    #         'Seed Phase 2 | Family for dynamic Tap' : 'Seed P2 F DT',
    #         'Seed Phase 2 | Family for static Swipe' : 'Seed P2 F SSw',
    #         'Seed Phase 2 | Family for dynamic Swipe' : 'Seed P2 F DSw',
    #         'Seed Phase 2 | Family for static Stretch' : 'Seed P2 F SSt',
    #         'Seed Phase 2 | Family for dynamic Stretch' : 'Seed P2 F DSt',
    #         'Seed Phase 2 | Family for static Hold' : 'Seed P2 F SH',
    #         'Seed Phase 2 | Family for dynamic Hold' : 'Seed P2 F DH',
    #         'Seed Phase 3': 'Seed P3',
    #         'Avez-vous une préférence entre les représentations animées et les non-animées et pourquoi?': 'Pref animation',
    #         'Avez-vous une préférence entre les différents types de représentations que vous avez rencontrés et pourquoi?': 'Pref family',
    #     }[stri]

    # def saveData(self) :
    #     keys = list(filter(lambda x: x != "", self.wks.get_row(1)))
    #     orderedValues = []
        
    #     for key in keys :
    #         try :
    #             if self.saveDict[key]!=None :
    #                 orderedValues.append(self.saveDict[key])
    #             else :
    #                 orderedValues.append('')
    #         except :
    #             orderedValues.append('')

    #     self.wks.update_row(self.new_row_index, orderedValues)  # Updates values in a column from 1st row

    # def saveDataAndExit(self) :
    #     self.saveData()
    #     self.send("Server shutdown")

class Controller (Client) :   
    def clientSpecificInit(self) :
        self.experiment = Experiment()

    def getType (self) :
        return "Controller"
    
    # def requestMessage (self) :
    #     self.clientPrint('<{0}> '.format(self.getType()))

    def parseBroadcast (self, msg) :
        hostname, data = msg["hostname"], msg["data"]
        # self.saveAnswer(data)
        self.updateExperimentStep()
            
        if self.experiment.phase <= self.experiment.max_phase :
            data = {INPUT_MODE: self.experiment.getInputModes()[self.experiment.phase], PHASE: self.experiment.phase, STEP: self.experiment.step}
            self.send(data)
        else :
            # The experiment is over
            # self.saveData()
            self.send("Server shutdown")
        
    def updateExperimentStep(self) :
        if self.experiment.step < self.experiment.getStateNbr() :
            self.experiment.step+=1
        elif self.experiment.step == self.experiment.getStateNbr() :
            self.experiment.phase+=1
            self.experiment.step=1
            
            # if self.experiment.phase <= self.experiment.max_phase :
                # self.clientPrint("\nPHASE - Starting phase {0} with {1} states\n".format(self.experiment.phase, str(self.experiment.getStateNbrFromPhase())))
                # self.clientPrint("INFORMATION - {0}\n".format(self.experiment.getInformations()[self.experiment.phase][self.experiment.step]))
            
        # if self.experiment.phase <= self.experiment.max_phase :
        #     self.clientPrint("STEP - Step {0}\n".format(self.experiment.step))
            
    def clientSpecificInput(self) :
        pass
    
    
#####################################################
#########      LAUNCHED BY TERMINAL       ###########
#####################################################

if __name__ == "__main__":
    server = JavaServer(host="localhost", port=5000)
    server.start()
    # server = JavaServer(host=SERVER, port=34295)        
    # if "server" in sys.argv:
    #     server = Server(SERVER_IP, PORT)
    #     server.start()
    
    # if "logger" in sys.argv:
    #     logger = Logger(CLIENT_IP, PORT, sys.argv)
        
    #     if "logger" in sys.argv and not ("server" in sys.argv or "controller" in sys.argv or "input" in sys.argv):
    #         logger.show = True
    #     else :
    #         logger.show = False
        
    #     logger.start()
        
    # if "controller" in sys.argv:
    #     controller = Controller(CLIENT_IP, PORT, sys.argv)
        
    #     if "controller" in sys.argv and not ("server" in sys.argv or "logger" in sys.argv or "input" in sys.argv):
    #         controller.show = True
    #     else :
    #         controller.show = False
            
    #     controller.start()
    
    # if "input" in sys.argv:
    #     time.sleep(2)
    #     input = Input(CLIENT_IP, PORT, sys.argv)
    #     input.start()
        
        
    # if "server" in sys.argv and "input" in sys.argv:
    #         time.sleep(1)
            
    #         def on_press_key(key, server, client):
    #             client.keyboard_input(key)
    #             try:
    #                 if key == '²':
    #                     server.shutdown()
    #             except AttributeError:
    #                 pass
    #         on_press = lambda key : on_press_key(key, server, input)
    #         keyboard_thread = threading.Thread(target=sshkeyboard.listen_keyboard, args=(on_press,))
    #         keyboard_thread.start()
    #         keyboard_thread.join()
    #         server.join()
    # else :
    #     if "server" in sys.argv:
    #         time.sleep(1)
            
    #         def on_press_key(key, server):
    #             try:
    #                 if key == '²':
    #                     server.shutdown()
    #             except AttributeError:
    #                 pass
                
    #         on_press = lambda key : on_press_key(key, server)
    #         server_keyboard_thread = threading.Thread(target=sshkeyboard.listen_keyboard, args=(on_press,))
    #         server_keyboard_thread.start()
    #         server_keyboard_thread.join()
    #         server.join()
            
    #     if "input" in sys.argv:
    #         time.sleep(1)
            
    #         def on_press_key(key, client):
    #             client.keyboard_input(key)
                
    #         on_press = lambda key : on_press_key(key, input)
    #         client_keyboard_thread = threading.Thread(target=sshkeyboard.listen_keyboard, args=(on_press, None, None, False, 0.05,))
    #         client_keyboard_thread.start()
    #         client_keyboard_thread.join()