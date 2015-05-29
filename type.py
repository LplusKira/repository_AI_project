# -*- coding: utf-8 -*-
_InitCardsPerPlayer_ = 5
_TotalPlayerNum_ = 4
_IamDead_ = -1
_MaxCombCardNum_ = 5
_cardNum_ = 52
_MaxActionLength_ = 20
_MaxComb_ = 32

import random
import time
from action import Action
from ab_agent import ScoutAgent

class PossibleCombination:
    def __init__(self, comb = list()):
        self.combination = comb

class State:
    def __init__(self, c, h, l, pcn, m, p, cw):
        self.card = c
        self.one_run_history = h #list of actions
        self.what_player_can_do = l #list of actions
        self.playersCardNum = pcn
        self.mountain_remaining = m
        self.points = p
        self.clock_wise = cw

class Judge:
    def __init__(self, h = list(), c = [[0 for x in range(5)] for x in range(4)], m=list(), p=0, cw=1, cp=1):
        players = list()
        players.append(ScoutAgent())
        #fake action
        self._possibleActions_ = list()
        self._possibleActions_.append(Action())
        self._possibleActions_.append(Action())
        self._possibleActions_.append(Action())
        self._possibleActions_.append(Action())
        random.shuffle(players)
        self.player = players

        self.history = h #action list
        self.card = c # need to sort by cardvalue,two dimension list
        self.mountain = m
        self.point = p
        self.clock_wise = cw
        self.current_player = cp
        self.GameStart()
        
    def GameStart(self):
        self._possibleActions_ = list()
        self.initBoard()
        self.rand4Cards()
        self.printBoard()
        av = self.getAction()
        print av
        
        while not self.isGameFinished():
            state = ab_agent.PlayerState(self.history, self._possibleActions_, self.card[self.current_player], len(self.card[0]), len(self.card[1]), len(self.card[2]), len(self.card[3]), len(self.mountain), self.point, self.clock_wise)
            a = self.player[self.current_player].genmove(state)
            self.doAction(a)

        winner = 0
        for i in range(4):
            if len(self.card[i]) > 0:
                winner = i
        print "winner is " + i

    def rand4Cards(self):
        original_cards = list()
        random.seed(time.time())
	for i in range(_cardNum_):
            original_cards.append(i + 1)
        for i in range(_TotalPlayerNum_):
            for counter in range(_InitCardsPerPlayer_):
                pick = random.randint(0,1024) % len(original_cards)
                self.card[i][counter] = original_cards[pick]
                original_cards.pop(pick)
        #//	TODO:	set mountain
        for i in range(len(original_cards)):
            pick = random.randint(0, 1024) % len(original_cards);
            self.mountain.append(original_cards[pick])
            original_cards.pop(pick)
    
    def initBoard(self):
        self.current_player = 1
        self.clock_wise = 1 #1 and -1
        self.playerNum = 4
        self.isDead = [False]*self.playerNum

    def isGameFinished(self):
        deadcount = 0
        for i in range(self.playerNum):
            if self.isDead[i]:
                deadcount += 1
        if deadcount == self.playerNum -1:
            print(gamefinished)
            return True
        return False

    def printBoard(self):
        print "mountnum = " + str(len(self.mountain)) + ".Now %dth Move. Player %d" % (len(self.history), self.current_player) + "\n" \
            + "North(id = 1):" + (getCardsString(self.card[0])) \
            + "East(id = 2):" + (getCardsString(self.card[1])) \
            + "South(id = 3):" + (getCardsString(self.card[2])) \
            + "West(id = 4):" + (getCardsString(self.card[3])) 
    
    def doAction(self, a):
        self.history.append(a)
        self.current_player += self.clock_wise
        if self.current_player == 0:
            self.current_player = 4
        elif self.current_player == 5:
            self.current_player = 1
        self.current_player += self.clock_wise

        
    def getAction(self): # get legal action list
        card = self.card[self.current_player];
        isuse = [False]*len(card) # size = card
        av = list()
        a = Action(self.current_player)
        while nextbool(av, len(card)):
            nowv = 0
            a.cards = []
            for i in range(len(card)):
                if isuse[i]:
                    nowv += card[i]%13
                    a.cards.append(card[i])
                    
            if nowv > 13:
                continue
            else:
                nowv %= 13 
        if nowv == 7 or nowv == 9:
            for i in range(_TotalPlayerNum_):
                if i == self.current_player or self.isDead[i]:
                    continue
                a.victim = i
                av.append(a)
        elif nowv == 5:
            for i in range(_TotalPlayerNum_):
                if self.isDead[i] == 0:
                    continue
                a.victim = i
                av.append(a)
        elif nowv == 10 or nowv == 12:
            value = 10 if (nowv == 10) else 20
            if self.point + value <= 99:
                a.victim = -1
                av.append(a)
            if self.point - value >= 0:
                a.victim = -2
                av.append(a)
        else:
            av.append(a)#do not consider victim
        return av

    def checkRule(self, a): #assume cards exist #a=action
        cardValue = 0
        for i in range(_MaxCombCardNum_):
            cardValue += a.cards_used[i]
            if(a.cards_used[i] == 1):#space one
                iszero = True
        if iszero and cardValue == 1:
            return True

        cardValue = cardValue % 13
        if cardValue == 7:
            if a.victim > 0 and a.victim <= 4 and a.victim != a.user and len(card[a.victim-1]) >= 1:#//now user id?
                return True
        elif cardValue == 9:
            if a.victim > 0 and a.victim <= 4 and a.victim != a.user:#//now user id?
                return True
        elif cardValue == 5:
            if a.victim > 0 and a.victim <= 4:
                return True
        elif cardValue == 12 or cardValue == 10:
            value = 20 if (cardValue % 13 == 12) else 10
            if a.victim == -1 and self.point + value <= 99 or a.victim == -2 and self.point - value >= 0:
                return True
        elif cardValue == 4 or cardValue == 11 or cardValue == 13:
            return True
        else:
            if self.point+cardValue <= 99:
                return True
        return False

def nextbool(vb, n):
    nowv = 0
    n = len(vb)
    for i in range(n):
        nowv *= 2
        nowv += 1 if (vb[i]) else 0
    nowv = nowv +1
    print "nowv in nextbool:" + str(nowv)
    if nowv >= power(2, n):
        return False
    for i in range(n, 0, -1):
        vb[i] = True if (nowv%2) else False
        nowv /= 2
    print vb
    return True

cardType = ['♠ ', '♥ ', '♦ ', '♣ ']
def getCardsString(l):
    s = ""
    for card in l:
        s += getCardString(card) + ", "
    s += "\n"
    return s
def getCardString(cardIndex):
    return str(cardIndex % 13 + 1) + cardType[(cardIndex-1)/13]

if __name__ == "__main__" :
    j = Judge()
