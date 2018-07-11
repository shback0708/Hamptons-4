#Holds the game class, used to keep track of data within a specific game
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
    def updateLineup(self, lineups, period):
        team1Lineup = lineups[self.team1][period]
        team2Lineup = lineups[self.team2][period]
        lineup = team1Lineup.union(team2Lineup)

        #starts by resetting all current players to not on the court
        for player in self.playersAppeared:
            self.playersAppeared[player].onCourt = False

        #next two loops used to create players that haven't appeared in the game yet
        for player in team1Lineup:
            self.createPlayer(player, self.team1)
        for player in team2Lineup:
            self.createPlayer(player, self.team2)

        #marks everyone subbed in at the beginning of the period as on the court
        for person in lineup:
            self.playersAppeared[person].onCourt = True

    #handles substitutions
    def substitute(self, playerOut, playerIn):
        team = self.playersAppeared[playerOut].team #makes sure the two players are on the same team
        self.createPlayer(playerIn, team) #player objects are created for players that haven't appeared yet
        self.playersAppeared[playerOut].onCourt = False
        self.playersAppeared[playerIn].onCourt = True

    #handles queued substitutions after free throws
    def doQueuedSubs(self):
        for sub in self.queuedSubs: #sub: (playerIn, playerOut)
            self.substitute(sub[0], sub[1])
        self.queuedSubs = set()

    #handles updating players' RPM's when points are scored
    def updateRPM(self, points, scorer):
        team = self.playersAppeared[scorer].team

        for player in self.playersAppeared:
            self.playersAppeared[player].updateRPM(points, team) #updated only for players that are on the court

    #for debugging, counts number of player with onCourt == True (total, team1, team2)
    def countOnCourt(self):
        count = 0
        t1count = 0
        t2count = 0

        for player in self.playersAppeared:

            if self.playersAppeared[player].onCourt:
                count += 1

                if self.playersAppeared[player].team == self.team1:
                    t1count += 1
                if self.playersAppeared[player].team == self.team2:
                    t2count += 1

        return count, t1count, t2count

    #again for debugging, checks the sum of all the players' RPM's in the game
    #should be 0 at all times, since any action should result in a net of 0 total RPM
    def totalRPM(self):
        total = 0

        for player in self.playersAppeared:
            total += self.playersAppeared[player].rpm

        return total

    #again for debugging, to see which teams players are on the court
    def checkLineups(self):
        lineups = {self.team1:set(),self.team2:set()}

        for player in self.playersAppeared:

            if self.playersAppeared[player].onCourt:

                if self.playersAppeared[player].team == self.team1:
                    lineups[self.team1].add(self.playersAppeared[player])

                elif self.playersAppeared[player].team == self.team2:
                    lineups[self.team2].add(self.playersAppeared[player])

        return lineups