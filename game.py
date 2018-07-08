#Holds the game class

class Game(object):
    def __init__(self, gameID, team1, team2, period=1, PCTime=7200):
        self.ID = gameID
        self.period, self.PCTime = period, PCTime
        self.team1, self.team2 = team1, team2

    #for debugging purposes
    def __repr__(self):
        return self.ID

    def __hash__(self):
        return hash(self.ID)

    def __eq__(self, other):
        return (isinstance(other, Game) and (self.ID == other.ID))

    def updateTime(self, PCTime=7200, period=""):
        self.PCTime = PCTime
        if period != "": self.period = period

