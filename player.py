#Holds the player class, used to keep track of data for a player

class Player(object):
    def __init__(self, personID, gameID, team, onCourt=True, rpm=0):
        self.PID = personID
        self.game = gameID
        self.team = team
        self.onCourt = onCourt
        self.rpm = rpm

    #for debugging purposes
    def __repr__(self):
        return self.PID

    def __hash__(self):
        return hash((self.PID, self.game))

    def __eq__(self, other):
        return (isinstance(other, Player) and (self.PID == other.PID) and (self.game == other.game))

    #updates a player's RPM based on how many points were scored and which team scored
    def updateRPM(self, points, team):
        if self.onCourt == False:
            pass
        else:
            add = 1
            if self.team != team:
                add = -1
            self.rpm += add*points