#Holds the player class

class Player(object):
    def __init__(self, PersonID, gameID, team, onCourt=True, rpm=0):
        self.PID
        self.game = gameID
        self.team = team
        self.onCourt = onCourt
        self.rpm = rpm

    #for debugging purposes
    def __repr__(self):
        return self.PID + " in game " + self.game

    def __hash__(self):
        return hash((self.PID, self.game))

    def __eq__(self, other):
        return (isinstance(other, Player) and (self.PID == other.PID) and (self.game == other.game))

    def substitute(self):
        self.onCourt = not self.onCourt

    def updateRPM(self, points, team):
        if self.onCourt == False:
            pass
        else:
            add = 1
            if self.team != team:
                add = -1
            self.rpm += add*points
