import csv

gameLineup = open("Downloads/NBA Hackathon - Game Lineup Data Sample (50 Games).txt","r").read()

eventCodes = open("NBA Hackathon - Event Codes.txt","r").read()

playByPlay = open("NBA Hackathon - Play by Play Data Sample (50 Games).txt","r").read()

print(gameLineup);
rawData = "hello my name is Daniel"

def convertDataInto2DList(rawData):
    #this function should convert the given data into 2D list
    final = rawData.split();
    return final;


def calculateData(eventCodes, gameLineupData, playByPlay):
    #do whatever calculations necessary 
    #eventCodes, gameLineupData, playByPlay are all 2d lists that we can loop through 
    return 0;

print(convertDataInto2DList(rawData));