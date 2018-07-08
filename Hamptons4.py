import csv
from player.py import *

gameLineup = open("NBA Hackathon - Game Lineup Data Sample (50 Games).txt","r").read()

eventCodes = open("NBA Hackathon - Event Codes.txt","r").read()

playByPlay = open("NBA Hackathon - Play by Play Data Sample (50 Games).txt","r").read()

#lets assume that gameLineup, eventCodes, and playByPlay are all strings
#now we will use convertStringInto2DList to convert the given string into 2D list

rawData = "hello my name is Daniel"

def convertDataInto2DList(string):
    #this function should convert the given data into 2D list
    final = []
    step1 = string.splitlines();
    for i in range(1,len(step1)):
        final.append(step1[i].split("\t"))
    return final

print(convertDataInto2DList(gameLineup));

#then we will use calculateData to get the necessary data we need
def calculateData(eventCodes, gameLineupData, playByPlay):
    #do whatever calculations necessary 
    #eventCodes, gameLineupData, playByPlay are all 2d lists that we can loop through 
    return 0;







#finally we will have the data and convert that into csv which will be 
#in Hamptons4 CSV

def convertToCSV(string):
    return 0;