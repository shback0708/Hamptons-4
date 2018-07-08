import csv
import string
from player import *
from event import *

def convertDataInto2DList(string, delimiter=","):
    #this function should convert the given data into 2D list
    final = []
    step1 = string.splitlines()
    for i in range(1,len(step1)):
        lst = step1[i].split(delimiter)
        for j in range(len(lst)):
            element = lst[j]
            try:
                lst[j] = element.replace('\"','').strip()
            except:
                pass
        final.append(lst)
    return final

#then we will use calculateData to get the necessary data we need
def calculateData(eventCodes, gameLineupData, playByPlay):
    #do whatever calculations necessary 
    #eventCodes, gameLineupData, playByPlay are all 2d lists that we can loop through 
    return 0;







#finally we will have the data and convert that into csv which will be 
#in Hamptons4 CSV

def convertToCSV(string):
    return 0;




#The main function that will run at the end, everything above will be helper functions
def runMain():
    gameLineup = open("NBA Hackathon - Game Lineup Data Sample (50 Games).txt","r").read()
    eventCodes = open("NBA Hackathon - Event Codes.txt","r").read()
    playByPlay = open("pbp_sample_sorted.csv","r").read() #sorted using a Microsoft Excel table
    gameLineup = convertDataInto2DList(gameLineup,"\t")
    eventCodes = convertDataInto2DList(eventCodes,"\t")
    playByPlay = convertDataInto2DList(playByPlay)

runMain()