#Holds the event class

class Event(object):
    def __init__(self, eventType, eventDesc, actionType, actionDesc):
        self.eventType, self.eventDesc = eventType, eventDesc
        self.actionType, self.actionDesc = actionType, actionDesc

    #for debugging purposes
    def __repr__(self):
        return self.eventDesc + ": " + self.actionDesc

    def __hash__(self):
        return hash((self.eventType,self.actionType))

    def __eq__(self, other):
        return (isinstance(other, Event) and (self.actionType == other.actionType) 
            and (self.eventType == other.actionType))