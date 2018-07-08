#holds the player class

class Player(object):
    def __init__(self, team, onCourt=True, rpm=0):
        self.team = team
        self.onCourt = onCourt
        self.rpm = rpm
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
