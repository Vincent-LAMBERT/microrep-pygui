import re

SERVER_IP = ""
PORT = 5000

# netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=172.23.150.213
# netsh interface portproxy add v4tov4 listenport=5000 listenaddress=0.0.0.0 connectport=5000 connectaddress=172.28.0.1

CLIENT_IP = "localhost"

REP_STATE = ["S", "D"]
REP_FAMILY = ["A", "F", "H", "R"]
REP_MICROGESTURE = ["Tap", "Swipe", "Stretch", "Hold"]
ANSW_PHASE2_NOTE = ["Very bad", "Bad", "Quite bad", "Quite good", "Good", "Very good"]
ANSW_PHASE2_SWITCH = ["Previous", "Next"]
ANSW_PHASE2 = ANSW_PHASE2_NOTE + ANSW_PHASE2_SWITCH
REP_STATIC_TAP = [REP_MICROGESTURE[0] + "_" + family + REP_STATE[0] for family in REP_FAMILY]
REP_DYNAMIC_TAP = [REP_MICROGESTURE[0] + "_" + family + REP_STATE[1] for family in REP_FAMILY]
REP_STATIC_SWIPE = [REP_MICROGESTURE[1] + "_" + family + REP_STATE[0] for family in REP_FAMILY]
REP_DYNAMIC_SWIPE = [REP_MICROGESTURE[1] + "_" + family + REP_STATE[1] for family in REP_FAMILY]
REP_STATIC_STRETCH = [REP_MICROGESTURE[2] + "_" + family + REP_STATE[0] for family in REP_FAMILY]
REP_DYNAMIC_STRETCH = [REP_MICROGESTURE[2] + "_" + family + REP_STATE[1] for family in REP_FAMILY]
REP_STATIC_HOLD = [REP_MICROGESTURE[3] + "_" + family + REP_STATE[0] for family in REP_FAMILY]
REP_DYNAMIC_HOLD = [REP_MICROGESTURE[3] + "_" + family + REP_STATE[1] for family in REP_FAMILY]
REP_TAP = REP_STATIC_TAP + REP_DYNAMIC_TAP
REP_SWIPE = REP_STATIC_SWIPE + REP_DYNAMIC_SWIPE
REP_STRETCH = REP_STATIC_STRETCH + REP_DYNAMIC_STRETCH
REP_HOLD = REP_STATIC_HOLD + REP_DYNAMIC_HOLD
REPRESENTATIONS = REP_TAP + REP_SWIPE + REP_STRETCH + REP_HOLD

def analyseControlerMsg(str) :
    try :
        pattern = "(.*) - (.*)"
        match = re.search(pattern, str)
        token = match.group(1)
        msg = match.group(2)
        return {"Token" : token, "Message" : msg}
    except :
        raise 