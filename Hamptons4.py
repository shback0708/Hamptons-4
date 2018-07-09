import csv
import string
#below we import classes that help with the main function
from player import *
from event import * #may delete, seems unnecessary rn
from game import *


#a simple class used to help keep track of data that we use between functions
class Data(object):
    def __init__(self, lineupFile, eventCodeFile, pbpFile):
        self.dataInit(lineupFile, eventCodeFile, pbpFile)
        self.gamesInit()
        self.eventsInit()
        self.pbpInit()
        self.rpmData = set()

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
        newSet = set()
        for game in self.games:
            team1, team2 = list(self.lineups[game].keys())[0], list(self.lineups[game].keys())[1]
            newSet.add(Game(game,team1,team2))
        self.games = newSet

    #initializes the events as a dictionary
    def eventsInit(self):
        events = dict()
        for event in self.ec:
            key = (int(event[0]), int(event[1]))
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

    #runs the play-by-play
    def runPBP(self):
        for game in self.gamesPBP:
            for play in self.games[game]:
                gameID, eventType, period, PCTime = play["GameID"], int(play["eventType"]), int(play["period"]), play["PCTime"]
                actionType, op1, teamID, p1, p2 = int(play["actionType"]), play["op1"], play["teamID"], play["person1"], play["person2"]
                elif eventType == 13: #end of period
                    pass
                if eventType == 12: #start of period
                    self.games[gameID].updateLineup(self.lineups[gameID][self.games[gameID].team1][period],
                        self.lineups[gameID][self.games[gameID].team2][period])
                    for player in self.games[gameID].inGame[0]:
                        self.initializePlayer(p1, gameID, teamID)
                elif eventType == 11: #ejection, ignored bc it's handled in substitution
                    pass
                elif eventType == 10: #jump nall
                    if teamID == self.games[gameID].team1:
                        team = 1
                    else:
                        team = 2
                    self.games[gameID].possession = team
                elif eventType == 9: #time outs
                    pass
                elif eventType == 8: #substitutions
                    if self.games[game].inFreeThrow:
                        self.queuedSubs.add((p1,p2,teamID))
                    else:
                        self.games[game].substitute(p1, p2, teamID)
                elif eventType == 7: #violations, ignored bc handled in turnovers
                    pass
                elif eventType == 6: #fouls, ignored bc handled in free throws, turnovers
                    pass
                elif eventType == 5: #turnovers
                    self.games[gameID].possession = 3 - self.games[gameID].possession
                elif eventType == 4: #rebounds
                    if teamID == self.games[gameID].team1:
                        team = 1
                    else:
                        team = 2
                    self.games[gameID].possession = team
                elif eventType == 3: #free throws
                    starts = [11,13,18,21,25,27] #the "1 of" anything free throws
                    ends = [12,15,19,22,26,29] # the "x of x" free throws
                    if actionType in starts:
                        self.games[gameID].inFreeThrow = True
                    elif actionType in ends: 
                        self.games[gameID].inFreeThrow = False
                        self.games[gameID].doQueuedSubs()
                    for player in self.games[gameID].inGame[0]:
                        player.updateRPM(op1, teamID)
                    for player in self.games[gameID].inGame[1]:
                        player.updateRPM(op1, teamID)
                elif eventType == 2: #missed shots
                    pass
                elif eventType == 1: #made shots
                    for player in self.games[gameID].inGame[0]:
                        player.updateRPM(op1, teamID)
                    for player in self.games[gameID].inGame[1]:
                        player.updateRPM(op1, teamID)

    #for debugging purposes
    def printEvent(self, period, PCTime, team, p1, eventType, actionType):
        try:
            event = self.events[(eventType, actionType)]
            print("Period", period, ": ", PCTime, team + "--", p1, event)
        except:
            print(eventType, actionType)

    #initializes a player object
    def initializePlayer(self, PID, GameID, team):
        for person in self.games[gameID].playersAppeared:
            if person.PID == PID:
                return
        newPlayer = Player(PID,GameID,team)
        self.games[gameID].playersAppeared.add(newPlayer)

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



#turns the 2D list into dictionaries and sets

#turns the lineupData 2D list into dictionaries and sets
#the levels are: games -> teams -> periods -> players
#also returns a set of the games
def organizeLineups(lineupData):
    lineups = dict()
    games = set()
    for lineup in lineupData:
        game, period, person, team = lineup[0], int(lineup[1]), lineup[2], lineup[3]
        games.add(game)
        if game not in lineups:
            lineups[game] = dict()
        if team not in lineups[game]:
            lineups[game][team] = {1:set(), 2:set(), 3:set(), 4:set()}
        if period == 5: lineups[game][team][5] = set()
        lineups[game][team][period].add(person)

    return lineups, games


#this function accumulate will run through all the play by play, and add plus
#minus values to our players 
def accumulate(data):
    return 0

#The main function that will run at the end, everything above will be helper functions
def runMain():
    lineupFile = "NBA Hackathon - Game Lineup Data Sample (50 Games).txt"
    eventCodeFile = "NBA Hackathon - Event Codes.txt"
    #we used a Microsoft Excel table to sort this according to game, period, time, etc.
    #this is why it's in a .csv form, not .txt
    pbpFile = "pbp_sample_sorted.csv"
    data = Data(lineupFile, eventCodeFile, pbpFile)
    finalString = accumulate(data)
    return finalString
    #we will be returning game ID, player ID, and player plus minus(which we will have to go through 5
    #quarters and manually add all for each player)

runMain()
