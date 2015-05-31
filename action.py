# coding: utf-8

class Action:
    def __init__(self, u = 0, c = list(), v = 0):
        self.user = u
        self.cards_used = c #_MaxCombCardNum_
        self.victim = v

    def __str__(self):
        return "user id: " + str(self.user) \
             + " card" + getCardsString(self.cards_used) \
             + " victim id: " + str(self.victim)

cardType = ['♠ ', '♥ ', '♦ ', '♣ ']
def getCardsString(l):
    s = ""
    for card in l:
        s += getCardString(card) + ", "
    return s
def getCardString(cardIndex):
    cardvalue = 13 if (cardIndex % 13 == 0) else cardIndex % 13
    return str(cardvalue) + cardType[(cardIndex-1)/13]


