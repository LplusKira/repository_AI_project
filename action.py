
class Action:
    def __init__(self, u = 0, c = list(), v = 0):
        self.user = u
        self.cards_used = c #_MaxCombCardNum_
        self.victim = v

    def __str__(self):
        return "user = " + str(self.user) \
             + " card" + str(self.cards_used) \
             + " victim " + str(self.victim)
        
