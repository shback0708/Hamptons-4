#Holds the event class

class Event(object):
    def __init__(self, eventType, eventDesc, actionType, actionDesc):
        self.eventType, self.eventDesc = eventType, eventDesc
        self.actionType, self.actionDesc = actionType, actionDesc