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
from logger import Game, logger

def simulateAction(self,js,a): #describe how to use this judge
    # js = judgestate(i use fillstate)
    myjudge = SimJudge(js)
    myjudge.doAction(a)

class JudgeState:
    # add transform function in addfun
    def __init__(self,playerNum = 4, playerList = None, h = None, c = None, m=None, p=0, cw=1, cp=1):
        self.playerNum = playerNum
        
        if playerList is None: # no real agents, haha!
            players = list()
            self.player = players
        else: # specify agents
            self.player = playerList
            pass
            random.shuffle(p)
            for player in p:
                players.append()
        if h is None:
            self.history = list()
        else:
            self.history = h #action list
        if c is None:
            self.card = [[0 for x in range(5)] for x in range(4)]
            self.isDead = [None]*4
        else:
            self.card = c # need to sort by cardvalue,two dimension list
            self.isDead = [None]*4
            for i in range(4):
                self.isDead[i] = len(self.card[i]) == 0
        if m is None:
            self.mountain = list()
        else:
            self.mountain = m
        self.point = p
        self.clock_wise = cw
        self.current_player = cp

class SimJudge: # new function: myeval

    def dpEval(self, myid):
        self.power = [0, 20, 10, 10, 60, 80, -30, 10, -50, 80, 80, 60, 100, 80]
        #                   1, 2,   3, 4,  5,   6,    7   8,  9,  10,  j,  q,  k
        self.endpower = [0, 20, 10, 10, 60, 80, -30, 10, -50, 200, 80, 60, 100, 80]
        mycardlen = len(self.card[myid-1])
        score = 60 * mycardlen
        nine = 0
        if mycardlen <= 2:
            for card in self.card[myid-1]:
                if getCardValue(card) == 9:      
                    nine += 1
            score = score + self.endpower[getCardValue(card)]
            if nine > 0:
                score -= 50*(nine-1)
        else:
            for card in self.card[myid-1]:
                if getCardValue(card) == 9:      
                    nine += 1
            score = score + self.power[getCardValue(card)]
        return score

    def dpEval1(self, myid):
        self.power = [0, 20, 10, 10, 60, 80, -30, 10, -50, 80, 80, 60, 100, 80]
        #                   1, 2,   3, 4,  5,   6,    7   8,  9,  10,  j,  q,  k
        self.endpower = [0, 20, 10, 10, 60, 80, -30, 10, -50, 200, 80, 60, 100, 80]
        mycardlen = len(self.card[myid-1])
        score = 60 * mycardlen
        nine = 0
        if mycardlen <= 2:
            for card in self.card[myid-1]:
                if getCardValue(card) == 9:      
                    nine += 1
            score = score + self.endpower[getCardValue(card)]
            if nine > 0:
                score -= 120*(nine-1)
        else:
            for card in self.card[myid-1]:
                if getCardValue(card) == 9:      
                    nine += 1
            score = score + self.power[getCardValue(card)]
        return score
        
    def myEval(self, myid):
        return self.dpEval1(myid)
            
        #print "card " + getCardString(card) + " get %d value" % self.power[getCardValue(card)]
        #for i in range(4):
            #self.isDead

      # todo: specialcase9
        '''if nine >= 1: #do something to consume cards
            score -= 500*(nine-1) #only count one 9
            if mycardlen == 1:
                score += 500
            elif mycardlen == 2: #todo:double9...
                score += 300'''
        '''diff = 0
        for c in self.card:
            diff += len(c)-len(self.card[myid-1]) # other's card is more than mycard
        score = score - 60*diff'''
        #return score
    
    def checkLose(self, i):
        return self.isDead[i-1]

    def __init__(self, s):
        self.power = [0, 20, 10, 10, 60, 80, -30, 10, -50, 80, 80, 60, 100, 80]
        #                   1, 2,   3, 4,  5,   6,    7   8,  9,  10,  j,  q,  k
        self.endpower = [0, 20, 10, 10, 60, 80, -30, 10, -50, 200, 80, 60, 100, 80]
        self.state = s
        self.input_state()
        self.printBoard()
        #self.action = a
        #self.doAction(a)

    def input_state(self):
        self.playerNum = self.state.playerNum
        self.player = self.state.player
        self.history = self.state.history
        self.card = self.state.card
        self.isDead = self.state.isDead
        self.mountain = self.state.mountain
        self.point = self.state.point
        self.clock_wise = self.state.clock_wise
        self.current_player = self.state.current_player

    def output_state(self):
        self.state.playerNum = self.playerNum
        self.state.player = self.player
        self.state.history = self.history
        self.state.card = self.card
        self.state.isDead = self.isDead
        self.state.mountain = self.mountain
        self.state.point = self.point
        self.state.clock_wise = self.clock_wise
        self.state.current_player = self.current_player

    def getJudgeState(self):
        self.output_state()
        return self.state


    def GameStart(self):
        self._possibleActions_ = list()
        self.initBoard()
        self.rand4Cards()
        #self.printBoard()
        
        while not self.isGameFinished():
            self._possibleActions_ = self.getAction()
            if len(self._possibleActions_) == 0:
                #print "%d is dead(cannot move). next one." % self.current_player
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
        #print "winner is " + str(winner+1)
        return self.player, str(winner+1)

    def rand4Cards(self): #do not use in simjudge
        original_cards = list()
        random.seed(time.time()*self.current_player)
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
        #if not self.checkRule(a):
         #   print "simjudge:illegal move"
          #  exit()
        isZero = False
        if len(a.cards_used) == 1:
            actual_card = a.cards_used[0] % 13
            if actual_card == 0:
                actual_card = 13
            if a.cards_used[0] == 1:
                isZero = True
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
        elif isZero:    #   else if the action is Spade 1 or 4, 5, 11, 13 
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
                #print "randmountain, now len = %d" % len(self.mountain)
            self.card[a.user - 1].append(self.mountain[len(self.mountain) - 1])
            self.mountain.pop()

        # check dead
        for i in range(self.playerNum):
            if len(self.card[i]) == 0 and not self.isDead[i]:
                #print "%d is dead(no card). next one." % (i+1)
                self.setDead(i+1) # id
            
        #   TODO: push action a into history
        self.history.append(a)
        #self.printBoard()
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
        #print "next player is %d" % self.current_player
        
    def getAction(self): # get legal action list
        card = copy.deepcopy(self.card[self.current_player-1])
        #remove the same value card
        #print card
        valuelist = []
        newcard = []
        for c in card:
            if c == 1:
                newcard.append(1)
            elif c%13 not in valuelist:
                valuelist.append(c%13)
                newcard.append(c)
        #print "valuelist" + str(valuelist)
                #print "newcard" + getCardsString(newcard)
                #print getCardsString(self.card[self.current_player-1])
        card = newcard

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
                    #random.shuffle(av)
        return av

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

def getCardValue(cardIndex):
   cardvalue = 13 if (cardIndex % 13 == 0) else cardIndex % 13
   return cardvalue
