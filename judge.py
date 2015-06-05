# -*- coding: utf-8 -*-
_InitCardsPerPlayer_ = 5
_TotalPlayerNum_ = 4
_IamDead_ = -1
_MaxCombCardNum_ = 5
_Adding_ = -1
_Minus_ = -2
_ClockWise_ = 1
_MaxPoint_ = 99
_cardNum_ = 52
_MaxActionLength_ = 20
_MaxComb_ = 32

import random
import time
import math
import copy
import sys
from action import *
from ab_agent import ScoutAgent
from ab_agent import RandomAgent
from ab_agent import PlayerState
from ab_agent import HeuristicAgent, HumanAgent
from logger import Game, logger

def simulateAction(self,s,a):# state, action # I skip, let monte carlo do it
    '''myjudge = Judge(s) # todo: build new init function for (judge) state
    myjudge.doAction(a)
    return judge.getJudgeState()
    '''
    
class PossibleCombination:
    def __init__(self, comb = list()):
        self.combination = comb

class Judge:
    def __init__(self, playerList = None, h = None, c = None, m=None, p=0, cw=1, cp=1):
        if playerList is None:
            players = list()
            players.append(ScoutAgent(1))
        #        players.append(HumanAgent(2))
            players.append(HeuristicAgent(2))
            players.append(RandomAgent(3))
            players.append(HeuristicAgent(4))
            self.player = players
        else: # specify agents
            self.player = playerList
            pass
            random.shuffle(p)
            for player in p:
                players.append()

        # because this attribute is mutable, use this way
        # http://stackoverflow.com/questions/2681243/how-should-i-declare-default-values-for-instance-variables-in-python
        if h is None:
            self.history = list()
        else:
            self.history = h #action list
        if c is None:
            self.card = [[0 for x in range(5)] for x in range(4)]
        else:
            self.card = c # need to sort by cardvalue,two dimension list
        if m is None:
            self.mountain = list()
        else:
            self.mountain = m
        self.point = p
        self.clock_wise = cw
        self.current_player = cp
        
    def GameStart(self):
        self._possibleActions_ = list()
        self.initBoard()
        self.rand4Cards()
        self.printBoard()
        
        while not self.isGameFinished():
            self._possibleActions_ = self.getAction()
            if len(self._possibleActions_) == 0:
                print "%d is dead(cannot move). next one." % self.current_player
                self.setDead(self.current_player)
                self.changeNextPlayer()
                continue
            state = PlayerState(self.history, self._possibleActions_, self.card[self.current_player-1], len(self.card[0]), len(self.card[1]), len(self.card[2]), len(self.card[3]), len(self.mountain), self.point, self.clock_wise) #get playerstate
            a = self.player[self.current_player-1].genmove(state)
            self.doAction(a)

        winner = 0
        for i in range(4):
            if self.isDead[i] == False:
                winner = i
        print "winner is " + str(winner+1)
        return self.player, str(winner+1)

    def rand4Cards(self):
        original_cards = list()
        random.seed(time.clock())
    	for i in range(_cardNum_):
            original_cards.append(i + 1)
        for i in range(_TotalPlayerNum_):
            for counter in range(_InitCardsPerPlayer_):
                pick = random.randint(0,1024) % len(original_cards)
                self.card[i][counter] = original_cards[pick]
                original_cards.pop(pick)
        #	TODO:	set mountain
        for i in range(len(original_cards)):
            pick = random.randint(0, 1024) % len(original_cards)
            self.mountain.append(original_cards[pick])
            original_cards.pop(pick)

    def randMountain(self):
        #   TODO:   collecting remained cards into cards_remained
        cards_remained = list()
        for player in range(_TotalPlayerNum_):
            for which_card in range(len(self.card[player])):
                 cards_remained.append(self.card[player][which_card])

        #   TODO:   collecting cards which should be the new moutain
        cards_remained.append(53)
        cards_remained.append(0)
        cards_remained.sort()
        original_cards = list()
        for grid_num in range(len(cards_remained) - 1):
            for between_grid in range(cards_remained[grid_num] + 1, cards_remained[grid_num + 1], 1):
                original_cards.append(between_grid)  

        #   TODO:   set mountain
        for i in range(len(original_cards)):
            pick = random.randint(0, 1024) % len(original_cards)
            self.mountain.append(original_cards[pick])
            original_cards.pop(pick)

    def initBoard(self):
        self.current_player = 1
        self.clock_wise = 1 #1 and -1
        self.playerNum = 4
        self.isDead = [False]*self.playerNum
        self.clock_wise = _ClockWise_ #1 and -1

    def isGameFinished(self):
        deadcount = 0
        for i in range(self.playerNum):
            if self.isDead[i]:
                deadcount += 1
        if deadcount == self.playerNum -1:
            return True
        return False

    def printBoard(self):
        print "mountnum = %d, point = %d" % (len(self.mountain), self.point) + ".Now %dth Move. Player %d" % (len(self.history), self.current_player) + "\n" \
            + "North(id = 1):" + (getCardsString(self.card[0])) + "\n" \
            + "East(id = 2):" + (getCardsString(self.card[1])) + "\n"\
            + "South(id = 3):" + (getCardsString(self.card[2])) + "\n"\
            + "West(id = 4):" + (getCardsString(self.card[3])) 

    def doAction(self, a):
        #   TODO: add effect by the returning action a
        if not self.checkRule(a):
            print "illegal move"
            exit()
        if len(a.cards_used) == 1:
            actual_card = a.cards_used[0] % 13
            if actual_card == 0:
                actual_card = 13
        else:
            actual_card = 0
            for i in range(0, len(a.cards_used), 1):
                actual_card += a.cards_used[i] % 13
        for c in a.cards_used:
            self.card[a.user-1].remove(c)
        if a.victim == _Adding_:    #   if the action is NO harmful: 10, 12(e.g. +- 10; +- 20)    
            if actual_card == 12:
                self.point += 20
            elif actual_card == 10:
                self.point += 10
        elif a.victim == _Minus_:
            if actual_card == 12:
                self.point -= 20
            elif actual_card == 10:
                self.point -= 10           
        elif actual_card == 1:    #   else if the action is Spade 1 or 4, 5, 11, 13 
            self.point = 0
        elif actual_card % 13 == 4:
            self.clock_wise *= -1
        elif actual_card % 13 == 5:
            self.current_player = a.victim
        elif actual_card % 13 == 11:
            pass
        elif actual_card % 13 == 0:
            self.point = _MaxPoint_
        elif actual_card % 13 == 7: #   else if the action is 7, 9
            pick = random.randint(0, len(self.card[a.victim - 1])-1)
            self.card[a.user - 1].append(self.card[a.victim - 1][pick])
            self.card[a.victim - 1].pop(pick)
        elif actual_card % 13 == 9:
            temp = list()
            for i in range(0, len(self.card[a.user - 1]), 1):
                temp.append(self.card[a.user - 1][i])
            for i in range(0, len(self.card[a.user - 1]), 1):
                self.card[a.user - 1].pop()
            for i in range(0, len(self.card[a.victim - 1]), 1):
                self.card[a.user - 1].append(self.card[a.victim - 1][i])
            for i in range(0, len(self.card[a.victim - 1]), 1):
                self.card[a.victim - 1].pop()
            for i in range(0, len(temp), 1):
                self.card[a.victim - 1].append(temp[i])
        else:                   #   else, cards in {1(not spade), 2, 3, 6, 8}
            self.point += actual_card

        #   TODO: pop mountain, assign the card to current user
        if not(actual_card % 13 == 7 or actual_card % 13 == 9):
            if len(self.mountain) == 0:
                self.randMountain()
                print "randmountain, now len = %d" % len(self.mountain)
            self.card[a.user - 1].append(self.mountain[len(self.mountain) - 1])
            self.mountain.pop()

        # check dead
        for i in range(self.playerNum):
            if len(self.card[i]) == 0 and not self.isDead[i]:
                print "%d is dead(no card). next one." % (i+1)
                self.setDead(i+1) # id
            
        #   TODO: push action a into history
        self.history.append(a)
        self.printBoard()
        self.changeNextPlayer()

    def setDead(self, playerid):
        self.isDead[playerid-1] = True
        self.card[playerid-1] = []

    def changeNextPlayer(self):
        self.current_player += self.clock_wise
        if self.current_player < 0:
            self.current_player += self.playerNum
        while self.isDead[self.current_player%self.playerNum - 1]:
            self.current_player += self.clock_wise
            if self.current_player < 0:
                self.current_player += self.playerNum
        self.current_player %= self.playerNum
        if self.current_player == 0:
            self.current_player += self.playerNum
        print "next player is %d" % self.current_player
        
    def getAction(self): # get legal action list
        card = self.card[self.current_player-1]
        isuse = [False]*len(card)
        av = list()
        a_template = Action(self.current_player)
        while nextbool(isuse, len(card)):
            a_card = copy.deepcopy(a_template)
            nowv = 0
            a_card.cards_used = []
            iszero = False
            for i in range(len(card)):
                if isuse[i]:
                    if card[i] == 1:
                        iszero = True
                    cv = 13 if (card[i]%13 == 0) else card[i]%13
                    nowv += cv
                    a_card.cards_used.append(card[i])

            if len(a_card.cards_used) == 1 and iszero:#special case, space one
                a = copy.deepcopy(a_card)
                a.victim = 0
                av.append(a)
                continue
            if nowv > 13:
                continue

            if nowv == 7 or nowv == 9:
                for i in range(_TotalPlayerNum_):
                    if i == self.current_player-1 or self.isDead[i]:
                        continue
                    a = copy.deepcopy(a_card)
                    a.victim = i+1
                    av.append(a)
            elif nowv == 5:
                for i in range(_TotalPlayerNum_):
                    if self.isDead[i]:
                        continue
                    a = copy.deepcopy(a_card)
                    a.victim = i+1
                    av.append(a)
            elif nowv == 10 or nowv == 12:
                value = 10 if (nowv == 10) else 20
                if self.point + value <= 99:
                    a = copy.deepcopy(a_card)
                    a.victim = -1
                    av.append(a)
                if self.point - value >= 0:
                    a = copy.deepcopy(a_card)
                    a.victim = -2
                    av.append(a)
            elif nowv == 4 or nowv == 11 or nowv == 13:
                a = copy.deepcopy(a_card)
                a.victim = 0
                av.append(a)
            else:
                if self.point + nowv <= 99:
                    a = copy.deepcopy(a_card)
                    a.victim = 0
                    av.append(a)
        random.shuffle(av)
        return av

    def checkRule(self, a): #assume cards in action exist
        cardValue = 0
        iszero = False
        for i in range(len(a.cards_used)):
            cardValue += a.cards_used[i]
            if(a.cards_used[i] == 1):#space one
                iszero = True
        if iszero and cardValue == 1:
            return True

        cardValue = cardValue % 13
        if cardValue == 7:
            if a.victim > 0 and a.victim <= self.playerNum and a.victim != a.user and len(self.card[a.victim-1]) >= 1:
                return True
        elif cardValue == 9:
            if a.victim > 0 and a.victim <= self.playerNum and a.victim != a.user:
                return True
        elif cardValue == 5:
            if a.victim > 0 and a.victim <= self.playerNum:
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
    if nowv >= math.pow(2, n):
        return False
    for i in range(n-1, -1, -1):
        vb[i] = True if (nowv%2) else False
        nowv /= 2
    return True

if __name__ == "__main__" :
    if len(sys.argv) == 2: # usage: judge.py [gamenum]
        totalgamenum = int(sys.argv[1]) # [0] is scriptname
    else:
        totalgamenum = 100
    i = 1 # no iterate? # i dont know
    log = logger() 
<<<<<<< HEAD
    while i < 100:
       j = Judge()
       players, winner = j.GameStart()
       g = Game(i, players, winner)
       log.logGame(g)
       i = i + 1
=======
    for k in range(totalgamenum):
        j = Judge()
        players, winner = j.GameStart()
        g = Game(i, players, winner)
        log.logGame(g)
>>>>>>> 575148dd3a08340e77bf5294d0d8c595ecbe40c1
    print log
