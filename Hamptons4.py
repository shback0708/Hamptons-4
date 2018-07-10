import csv
#below we import classes that help with the main function
from player import *
from game import *

#a simple class used to help keep track of data that we use between functions
#Attributes: 
#self.lineups: contains nested dictionaries/sets as follows: games -> teams -> periods -> players
#self.games: dictionary with self.games[gameID] = Game (object)
#self.ec: contains events in 2D list form
#self.events: contains the events in dictionary form: self.events[(eventType,actionType)] = 
#           eventDesc + ": " + actionDesc
#self.pbp: is a list of all each play from the play-by-play document; each line is in the form a dictionary 
#           mapping each heading to its value
#self.gamesPBP: is a dictionary mapping each gameID to its plays from self.pbp
class Data(object):
    def __init__(self, lineupFile, eventCodeFile, pbpFile):
        self.dataInit(lineupFile, eventCodeFile, pbpFile)
        self.gamesInit()
        self.eventsInit()
        self.pbpInit()

    #transforms given from .txt and .csv form to a more usable format
    def dataInit(self, lineupFile, eventCodeFile, pbpFile):
        gameLineup = open(lineupFile,"r").read()
        gameLineup = convertDataInto2DList(gameLineup,"\t")
        self.lineups, self.games = organizeLineups(gameLineup)
        eventCodes = open(eventCodeFile,"r").read()
        self.ec = convertDataInto2DList(eventCodes,"\t")
        playByPlay = open(pbpFile,"r").read()
        self.pbp = convertDataInto2DList(playByPlay)

    #initializes games as objects
    def gamesInit(self):
        newDict = dict()
        for game in self.games:
            team1, team2 = list(self.lineups[game].keys())[0], list(self.lineups[game].keys())[1]
            newDict[game] = Game(game,team1,team2)
        self.games = newDict

    #initializes the events as a dictionary
    def eventsInit(self):
        events = dict()
        for event in self.ec:
            key = (event[0], event[1])
            val = event[2] + ": " + event[3]
            events[key] = val
        self.events = events

    #organizes play-by-play data to make it easier to work with
    def pbpInit(self):
        #the different types of data within the play-by-play
        headings = ["GameID", "eventNum", "eventType", "period", "WCTime", "PCTime", "actionType", "op1", 
            "op2", "op3", "teamID", "person1", "person2", "teamIDType"]
        newList = []
        for play in self.pbp:
            d = dict()
            for i in range(len(headings)):
                d[headings[i]] = play[i]
            newList.append(d)
        self.pbp = newList
        self.gamesPBP = dict()
        for playList in self.pbp:
            if playList["GameID"] not in self.gamesPBP:
                self.gamesPBP[playList["GameID"]] = []
            self.gamesPBP[playList["GameID"]].append(playList)

    #for debugging purposes
    def printEvent(self, play):
        gameID, eventType, period, PCTime = play["GameID"], play["eventType"], play["period"], play["PCTime"]
        actionType, op1, teamID, p1, p2 = play["actionType"], play["op1"], play["teamID"], play["person1"], play["person2"]
        try:
            playType = self.events[(eventType, actionType)]
            minutes = str(int((int(PCTime)/10)//60))
            seconds = str((int(PCTime)/10)%60)
            if seconds.index(".") == 1: seconds = "0" + seconds
            if seconds[-1] == "0": seconds = seconds[:-2]
            print("Game: " + gameID + " Period", period, ":", minutes + ":" + seconds, teamID + " --", p1, playType)
        except:
            pass

    #runs a play
    def runPlay(self, play, currentGame):
        gameID, eventType, period, actionType = play["GameID"], int(play["eventType"]), play["period"], int(play["actionType"])
        op1, op2, op3, p1, p2 = play["op1"], play["op2"], play["op3"], play["person1"], play["person2"]
        #events that do not affect which players are on the court or scoring do not matter, for RPM purposes
        passEvents = [13,11,10,9,7,6,5,4,2]
        if eventType in passEvents:
            pass
        elif eventType == 12: #start of period
            currentGame.updateLineup(self.lineups[gameID], period)
        elif eventType == 8: #substitutions
            if currentGame.inFreeThrow:
                currentGame.queuedSubs.add((p1, p2))
            else:
                currentGame.substitute(p1, p2)
        elif eventType == 6: #fouls
            if op1 != "0" or op3 != "0":
                currentGame.inFreeThrow = True
        elif eventType == 3: #free throws
            ends = [10,12,15,16,17,19,20,22,26,29] # the "x of x" free throws
            if actionType in ends:
                currentGame.inFreeThrow = False
                currentGame.doQueuedSubs()
            currentGame.updateRPM(int(op1), p1)
        elif eventType == 1: #made shots
            currentGame.updateRPM(int(op1), p1)

    #runs through each game's play-by-play
    def runPBP(self):
        for game in self.gamesPBP: #game is a gameID in string form
            currentGame = self.games[game] #currentGame is an object Game
            for play in self.gamesPBP[game]: #runs through each play in currentGame
                self.printEvent(play)
                self.runPlay(play, currentGame)

    #function to do the csv writing
    def returnFinal(self):
        final = [["Game_ID", "Player_ID", "Player_Plus/Minus"]]
        for game in self.games:
            for player in self.games[game].playersAppeared:
                person = self.games[game].playersAppeared[player]
                if person.rpm>0:
                    person.rpm = "+" + str(person.rpm)
                final += [[str(game), str(person), person.rpm]]
        with open("Hamptons_4_Q1_BBALL.csv", "w", newline = "") as fp:
            a = csv.writer(fp, delimiter = ',')
            a.writerows(final)

##################################Data above, helpers below#####################################

#this function should convert the given data into 2D list
def convertDataInto2DList(string, delimiter=","):
    final = []
    step1 = string.splitlines()
    for i in range(1,len(step1)):
        lst = step1[i].split(delimiter)
        #for removing some annoying whitespaces
        for j in range(len(lst)):
            element = lst[j]
            try:
                lst[j] = element.replace('\"','').strip()
            except:
                pass
        final.append(lst)
    return final

#turns the lineupData 2D list into dictionaries and sets
#the levels are: games -> teams -> periods -> players
#also returns a set of the games
def organizeLineups(lineupData):
    lineups = dict()
    games = set()
    for lineup in lineupData:
        game, period, person, team = lineup[0], lineup[1], lineup[2], lineup[3]
        games.add(game)
        if game not in lineups:
            lineups[game] = dict()
        if team not in lineups[game]:
            lineups[game][team] = {'1':set(), '2':set(), '3':set(), '4':set()}
        if period == '5' and '5' not in lineups[game][team]: 
            lineups[game][team]['5'] = set()
        lineups[game][team][period].add(person)

    return lineups, games

#The main function that will run at the end, everything above will be helper functions
def runMain():
    lineupFile = "NBA Hackathon - Game Lineup Data Sample (50 Games).txt"
    eventCodeFile = "NBA Hackathon - Event Codes.txt"
    #we used a Microsoft Excel table to sort this according to game, period, time, etc.
    #this is why it's in a .csv form, not .txt
    pbpFile = "pbp_sample_sorted.csv"
    data = Data(lineupFile, eventCodeFile, pbpFile)
    data.runPBP()
    data.returnFinal()

runMain()