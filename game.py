#Holds the game class
from player import *

class Game(object):
    def __init__(self, gameID, team1, team2):
        self.ID = gameID
        self.team1, self.team2 = team1, team2
        self.inFreeThrow = False #variable to check how substitutions affect RPM within free throws
        self.queuedSubs = set()
        self.playersAppeared = dict() #maps playerID to player object

    #for debugging purposes
    def __repr__(self):
        return self.ID

    def __hash__(self):
        return hash(self.ID)

    def __eq__(self, other):
        return (isinstance(other, Game) and (self.ID == other.ID))

    #creates a player and adds him to self.playersAppeared
    def createPlayer(self, PID, team):
        if PID in self.playersAppeared:
            return
        self.playersAppeared[PID] = Player(PID, self.ID, team)

    #updates lineups at the start of periods
    def updateLineup(self, team1Lineup, team2Lineup):
        lineup = team1Lineup.union(team2Lineup)
        for player in team1Lineup:
            self.createPlayer(player, self.team1)
        for player in team2Lineup:
            self.createPlayer(player, self.team2)
        for player in self.playersAppeared:
            self.playersAppeared[player].onCourt = False
        for person in lineup:
            self.playersAppeared[person].onCourt = True

    #handles substitutions
    def substitute(self, playerOut, playerIn, team):
        if playerIn not in self.playersAppeared:
            self.createPlayer(playerIn, team)
        self.playersAppeared[playerOut].onCourt = False
        self.playersAppeared[playerIn].onCourt = True

    #handles queued substitutions after free throws
    def doQueuedSubs(self):
        for sub in self.queuedSubs: #sub: (playerIn, playerOut, team)
            self.substitute(sub[0], sub[1], sub[2])

    #handles updating RPM's when points are scored
    def updateRPM(self, points, team):
        for player in self.playersAppeared:
            self.playersAppeared[player].updateRPM(points, team)