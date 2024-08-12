#!/usr/bin/env python3

from cgitb import handler
import socket, select, string, sys, re
from abc import ABC, abstractmethod
from typing import OrderedDict
import time, random
import pygsheets
import pandas as pd
from uuid import uuid4

from modules.utils.server.Client import Client
import modules.utils.server.Utils as u

class Controller (Client) :   
    def clientSpecificInit(self) :
        self.phase=0
        self.state=-1
        self.subState=0
        self.seenSubStates=0
        self.lastCondition = lambda _ : True
        self.lastMsg = ""
        self.saveDict = dict()
        self.orderPhase1 = u.REPRESENTATIONS.copy()
        self.orderPhase2_Microgesture = u.REP_MICROGESTURE.copy()
        self.orderPhase2_Family_Static_Tap = u.REP_STATIC_TAP.copy()
        self.orderPhase2_Family_Dynamic_Tap = u.REP_DYNAMIC_TAP.copy()
        self.orderPhase2_Family_Static_Swipe = u.REP_STATIC_SWIPE.copy()
        self.orderPhase2_Family_Dynamic_Swipe = u.REP_DYNAMIC_SWIPE.copy()
        self.orderPhase2_Family_Static_Stretch = u.REP_STATIC_STRETCH.copy()
        self.orderPhase2_Family_Dynamic_Stretch = u.REP_DYNAMIC_STRETCH.copy()
        self.orderPhase2_Family_Static_Hold = u.REP_STATIC_HOLD.copy()
        self.orderPhase2_Family_Dynamic_Hold = u.REP_DYNAMIC_HOLD.copy()
        self.orderPhase2 = []
        self.orderPhase3 = u.REPRESENTATIONS.copy()
        self.orderPhase5 = u.REPRESENTATIONS.copy()
        # self.file = open("exp1.txt", mode="w", encoding='utf-8')
        
        self.gc = pygsheets.authorize(service_file='/home/lambevin/Work/Stage/Hololens2Discoverability/Assets/PythonServer/exp2iihm-b2528d90bd91.json')
        self.sh = self.gc.open('Experience 2')
        self.wks = self.    sh.sheet1 # sheet1 is name of first worksheet

        # To initialize google sheet
        # wks.update_row(1, sorted(list(self.saveDict.keys())), col_offset=0)
        
        # To add a row to the google sheet
        self.new_row_index = 2

        while len(list(filter(lambda x: x != "", self.wks.get_row(self.new_row_index))))>0 :
            self.new_row_index+=1    
        

    def saveAnswer(self, word) :
        try :
            new_key = self.getKeyFromStr(str(u.analyseControlerMsg(self.lastMsg)["Message"]))
        except :
            new_key = str(u.analyseControlerMsg(self.lastMsg)["Message"])
        if new_key!=None :
            self.saveDict[new_key] = word
            self.saveData()

    def getKeyFromStr(self, stri) :
        return {
            'P1_Connectez le dispositif et appuyez sur entrée quand vous êtes prêt·e': None,
            'Appuyez sur entrée pour continuer' : None,
            'Quel est votre âge?': 'Age',
            'Quel est votre genre?': 'Gender',
            'Avez vous pris part à notre précédente étude en ligne? [y/n]': 'Previous study done',
            'Statique ou dynamique? [s/d]': 'Pref Static/Dynamic',
            'Seed Phase 1': 'Seed P1',
            'Seed Phase 2 | Microgesture': 'Seed P2 MG',
            'Seed Phase 2 | Family for static Tap' : 'Seed P2 F ST',
            'Seed Phase 2 | Family for dynamic Tap' : 'Seed P2 F DT',
            'Seed Phase 2 | Family for static Swipe' : 'Seed P2 F SSw',
            'Seed Phase 2 | Family for dynamic Swipe' : 'Seed P2 F DSw',
            'Seed Phase 2 | Family for static Stretch' : 'Seed P2 F SSt',
            'Seed Phase 2 | Family for dynamic Stretch' : 'Seed P2 F DSt',
            'Seed Phase 2 | Family for static Hold' : 'Seed P2 F SH',
            'Seed Phase 2 | Family for dynamic Hold' : 'Seed P2 F DH',
            'Seed Phase 3': 'Seed P3',
            'Avez-vous une préférence entre les représentations animées et les non-animées et pourquoi?': 'Pref animation',
            'Avez-vous une préférence entre les différents types de représentations que vous avez rencontrés et pourquoi?': 'Pref family',
        }[stri]


    def saveData(self) :
        keys = list(filter(lambda x: x != "", self.wks.get_row(1)))
        orderedValues = []
        
        for key in keys :
            try :
                if self.saveDict[key]!=None :
                    orderedValues.append(self.saveDict[key])
                else :
                    orderedValues.append('')
            except :
                orderedValues.append('')

        self.wks.update_row(self.new_row_index, orderedValues)  # Updates values in a column from 1st row

    def saveDataAndExit(self) :
        self.saveData()
        self.send("Server shutdown")

    def getType (self) :
        return "Controller"
    
    def requestMessage (self) :
        self.clientPrint('<{0}> '.format(self.getType()))

    def parseBroadcast (self, msg) :
        pattern = "(.*) \| (<(.*)> (.*))"
        matches = re.search(pattern, msg)
        self.clientPrint("\r{0}\n".format(matches.group(2)))
        if matches.group(3)=="Input" :
            self.handleAnswer(matches.group(4))

    def ask(self, msg, function) :
        self.lastCondition = function
        self.requestMessage()
        self.clientPrint(msg+"\n")
        if self.phase in [1,2,3] :
            pattern = "(.*) - (.*)"
            match = re.search(pattern, msg)
            token = match.group(1)
            content = match.group(2)
            self.lastMsg = "{0} - P{1}_{2}".format(token, self.phase, content)
        else :
            self.lastMsg = msg
        self.send(msg)

    def handleAnswer(self, answer) :
        answr = answer
        if self.phase in [1,2,3,5] :
            answr = self.interpret(answer)
            if answr=="Esc":
                self.saveDataAndExit()
                return

        if self.lastCondition(answr) :
            if self.phase==5 :
                if answr in u.ANSW_PHASE2_SWITCH :
                    if answr==u.ANSW_PHASE2_SWITCH[0] :
                        self.previousState()
                    else :
                        self.nextState()
            elif self.phase in [1,3] :
                self.saveAnswer(answr)
                if self.state==len(self.orderPhase1)-1 :
                    self.nextPhase()
                else :
                    self.nextState()
            elif self.phase==2 :
                if answr in u.ANSW_PHASE2_SWITCH :
                    if answr==u.ANSW_PHASE2_SWITCH[0] :
                        self.previousSubState()
                    else :
                        self.nextSubState()
                else :
                    size = len(self.orderPhase2[self.state])
                    if size<4 or self.allSeen(self.orderPhase2[self.state]) :
                        self.send("SUBSTATE - {0}/4 restants".format(size-1))
                        self.orderPhase2[self.state].pop(self.subState%size)
                        self.saveAnswer(answr)
                        if size==1 : # The last item has been poped 2 lines above but is still registered in size
                            self.seenSubStates=0
                            if self.state==len(self.orderPhase2)-1 :
                                self.nextPhase()
                            else :
                                self.nextState()
            elif answr!='':
                self.saveAnswer(answr)
                self.nextState()
            else : 
                self.nextState()
        
        self.askState()
    
    def allSeen(self, microgestures) :
        for microgesture in microgestures :
            if not microgesture["SeenState"] :
                return False
        return True

    def nextState(self) :
        self.state+=1
        self.subState=0
        self.send("STATE - State {0}".format(self.state+1))

    def previousState(self) :
        self.state-=1
        self.subState=0
        self.send("STATE - State {0}".format(self.state+1))

    def previousSubState(self) :
        self.subState-=1

    def nextSubState(self) :
        self.subState+=1

    def nextPhase(self) :
        self.phase += 1
        self.state = 0
        self.subState = 0
        self.send("PHASE - Starting phase {0} with {1} states".format(self.phase+1, str(self.getStateNbrFromPhase())))
        self.send("INFORMATION - {0}".format(self.getInformationFromPhase()))
        self.send("STATE - State {0}".format(self.state+1))
    
    def getStateNbrFromPhase(self) :
        return {
            '0': 3,
            '1': 32,
            '2': 8,
            '3': 32,
            '4': 3,
            '5': 32,
        }[str(self.phase)]
    
    def getInformationFromPhase(self) :
        return {
            '0': "Repondez aux questions qui vous sont posees",
            # '1': "Effectuez le geste qui vous vient naturellement avec l'aide qui apparait sur votre main",
            '1': "Do the gesture that comes to you naturally with the help that appears on your hand",
            '2': "Regardez puis notez d'une mention les 4 representations qui vous sont proposees pour le mouvement suivant :",
            '3': "Comme en phase 1, faites le geste qui vous vient maintenant que vous avez vu toutes les aides et leur sens plusieurs fois",
            '4': "Repondez aux dernieres questions",
            '5': "Vous pouvez desormais explorer les representations proposees pour les divers microgestes",
        }[str(self.phase)]


    def askState(self) :
        if self.phase==0 :
            if self.state==0 :
                self.saveDict["Id"] = self.sessionId
                self.send("PHASE - Starting phase {0} with {1} states".format(self.phase+1, str(self.getStateNbrFromPhase())))
                self.send("INFORMATION - {0}".format(self.getInformationFromPhase()))
                self.send("STATE - State {0}".format(self.state+1))
                self.ask("MESSAGE - Quel est votre âge?", lambda x : x.isdigit())
            elif self.state==1 :
                self.ask("MESSAGE - Quel est votre genre?", lambda _ : True)
            elif self.state==2 :
                self.ask("MESSAGE - Avez vous pris part à notre précédente étude en ligne? [y/n]", lambda x : (x=="y") or (x=="n"))
            elif self.state==3 :
                self.ask("MESSAGE - Statique ou dynamique? [s/d]", lambda x : (x=="s") or (x=="d"))
            else :
                self.nextPhase()
                self.shuffleSeeds()
                self.ask("MESSAGE - Connectez le dispositif et appuyez sur entrée quand vous êtes prêt·e", lambda _ : True)
                self.state-=1 # compensate the increments due to the enter
        elif self.phase==1 :
            self.ask("REPRESENTATION - {0}".format(self.orderPhase1[self.state]), lambda x : x in u.REP_MICROGESTURE)
        elif self.phase==2 :
            size = len(self.orderPhase2[self.state])
            microgesture = self.orderPhase2[self.state][self.subState%size]
            self.ask("REPRESENTATION - {0}".format(microgesture["Representation"]), 
                    lambda x : x in u.ANSW_PHASE2)
            if not microgesture["SeenState"] :
                self.orderPhase2[self.state][self.subState%size]["SeenState"] = True
                self.seenSubStates+=1
                self.send("SUBSTATE - {0}/4 vus".format(self.seenSubStates))
        elif self.phase==3 :
            self.ask("REPRESENTATION - {0}".format(self.orderPhase3[self.state]), lambda x : x in u.REP_MICROGESTURE)
        elif self.phase==4 :
            if self.state==0 :
                self.ask("MESSAGE - Appuyez sur entrée pour continuer", lambda _ : True)
            elif self.state==1 :
                self.ask("MESSAGE - Avez-vous une préférence entre les représentations animées et les non-animées et pourquoi?", lambda _ : True)
            elif self.state==2 :
                self.ask("MESSAGE - Avez-vous une préférence entre les différents types de représentations que vous avez rencontrés et pourquoi?", lambda _ : True)
            else :
                self.nextPhase()
                self.ask("MESSAGE - C'est la fin de l'expérience. Appuyez sur Entrée pour passer en mode libre. Vous pourrez ensuite appuyer sur Echap pour sauvegarder les données", lambda _ : True)
                self.state-=1 # compensate the increments due to the enter
        else :
            size = len(self.orderPhase5)
            self.ask("REPRESENTATION - {0}".format(self.orderPhase5[self.state%size]), lambda x : x in u.ANSW_PHASE2)

    def interpret(self, key) :
        if key=="'7'":
            self.send("DETECTED - Tap")
            return "Tap"
        elif key=="'9'":
            self.send("DETECTED - Swipe")
            return "Swipe"
        elif key=="'3'":
            self.send("DETECTED - Stretch")
            return "Stretch"
        elif key=="'1'":
            self.send("DETECTED - Hold")
            return "Hold"
        elif key=="'s'":
            self.send("DETECTED - Very bad")
            return "Very bad"
        elif key=="'d'":
            self.send("DETECTED - Bad")
            return "Bad"
        elif key=="'f'":
            self.send("DETECTED - Quite bad")
            return "Quite bad"
        elif key=="'g'":
            self.send("DETECTED - Quite good")
            return "Quite good"
        elif key=="'h'":
            self.send("DETECTED - Good")
            return "Good"
        elif key=="'j'":
            self.send("DETECTED - Very good")
            return "Very good"
        elif key=="'('":
            self.send("DETECTED - Previous")
            return "Previous"
        elif key=="'-'":
            self.send("DETECTED - Next")
            return "Next"
        elif key=="'\\x1b'":
            self.send("DETECTED - Server shutdown")
            return "Esc"
    
    def shuffleSeeds(self) :
        self.orderPhase1 = self.saveSeedAndShuffleList("Seed Phase 1", self.orderPhase1)
        self.orderPhase2_Microgesture = self.saveSeedAndShuffleList("Seed Phase 2 | Microgesture", self.orderPhase2_Microgesture)

        for microgesture in u.REP_MICROGESTURE :
            for state in u.REP_STATE :
                dictKey = "Seed Phase 2 | Family for {0} {1}".format("static" if state=="S" else "dynamic", microgesture)
                if state=="S" :
                    if microgesture=="Tap" :
                        self.orderPhase2_Family_Static_Tap = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Static_Tap))

                    elif microgesture=="Swipe" :
                        self.orderPhase2_Family_Static_Swipe = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Static_Swipe))
                    elif microgesture=="Stretch" :
                        self.orderPhase2_Family_Static_Stretch = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Static_Stretch))
                    else :
                        self.orderPhase2_Family_Static_Hold = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Static_Hold))
                else :
                    if microgesture=="Tap" :
                        self.orderPhase2_Family_Dynamic_Tap = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Dynamic_Tap))
                    elif microgesture=="Swipe" :
                        self.orderPhase2_Family_Dynamic_Swipe = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Dynamic_Swipe))
                    elif microgesture=="Stretch" :
                        self.orderPhase2_Family_Dynamic_Stretch = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Dynamic_Stretch))
                    else :
                        self.orderPhase2_Family_Dynamic_Hold = self.addSeenState(self.saveSeedAndShuffleList(dictKey, self.orderPhase2_Family_Dynamic_Hold))
        
        rep_static = {"Tap": [self.orderPhase2_Family_Static_Tap], 
                      "Swipe": [self.orderPhase2_Family_Static_Swipe], 
                      "Stretch": [self.orderPhase2_Family_Static_Stretch], 
                      "Hold": [self.orderPhase2_Family_Static_Hold]}
        rep_dynamic = {"Tap": [self.orderPhase2_Family_Dynamic_Tap], 
                      "Swipe": [self.orderPhase2_Family_Dynamic_Swipe], 
                      "Stretch": [self.orderPhase2_Family_Dynamic_Stretch], 
                      "Hold": [self.orderPhase2_Family_Dynamic_Hold]}

        orderStatic, orderDynamic = [], []
        for microgesture in self.orderPhase2_Microgesture :
            orderStatic += rep_static[microgesture]
            orderDynamic += rep_dynamic[microgesture]
        
        
        
        if self.saveDict[self.getKeyFromStr("Statique ou dynamique? [s/d]")]=="s" :
            self.orderPhase2 = orderStatic + orderDynamic
        else :
            self.orderPhase2 = orderDynamic + orderStatic
    
        self.orderPhase3 = self.saveSeedAndShuffleList("Seed Phase 3", self.orderPhase3)
        
    
    def saveSeedAndShuffleList(self, dictKey, listToShuffle) :
        self.saveDict[self.getKeyFromStr(dictKey)] = int(uuid4())
        random.Random(self.saveDict[self.getKeyFromStr(dictKey)]).shuffle(listToShuffle)
        return listToShuffle
    
    def addSeenState(self, locallist) :
        for i in range(len(locallist)) :
            locallist[i] = {"Representation" : locallist[i], "SeenState" : False}
        return locallist

def launch(args) :
	client = Controller(args=args)
	client.run()

if __name__ == "__main__" :
	launch(sys.argv[1:])

