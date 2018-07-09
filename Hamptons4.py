import csv
import string
#below we import classes that help with the main function
from player import *
from event import *
from game import *


#a simple class used to help keep track of data that we use between functions
class Data(object):
    def __init__(self, lineupFile, eventCodeFile, pbpFile):
        self.dataInit(lineupFile, eventCodeFile, pbpFile)
        self.gamesInit()
        self.eventsInit()

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

    #initializes the events as objects
    def eventsInit(self):
        events = set()
        for event in self.ec:
            eventType, actionType, eventDesc, actionDesc = int(event[0]), int(event[1]), event[2], event[3]
            events.add(Event(eventType, eventDesc, actionType, actionDesc))
        self.events = events


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

#after we run runMain, then we will have to convert the strings into csv file
#which will literally take 3 to 5 lines 