# coding: utf-8

class Action:
    def __init__(self, u = 0, c = list(), v = 0):
        self.user = u
        self.cards_used = list(c) #_MaxCombCardNum_
        self.victim = v
        self.cardValue = 0

    def getCardValue(self):
        value = 0
        for card in self.cards_used:
            v = 13 if (card % 13 == 0) else card % 13
            value += v
        self.cardValue = value

    def __str__(self):
        return "user id: " + str(self.user) \
             + " card: " + getCardsString(self.cards_used) \
             + " cardvalue: " + str(self.cardValue) \
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
def getCardValue(cardIndex):
   cardvalue = 13 if (cardIndex % 13 == 0) else cardIndex % 13
   return cardvalue


