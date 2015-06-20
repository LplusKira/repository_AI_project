# -*- coding: utf-8 -*-
import random
import time
import copy
import action
import operator
import math
from minijudge import MiniJudge

INF = 2147483647
_CardNumPerType_ = 13
_Ordery_ = [10, 11,  9, 4,  3, 12, 1,  13,  5,  8,  6,  7,  2]
_UpperBd_ = 100
_HotThresh_ = 10
_Step_ = 2

class Agent:
   def __init__(self, index = 0):
      self.index = index
   
   def genmove(self, state):
      pass

class PlayerState:
   def __init__(self, history, leg, card, cardNum1, cardNum2, cardNum3, cardNum4, mountNum, point, order, the_specific_small_h):
      self.myCard = MyCard(leg, card)# var card non exist
      cardNum = list()
      cardNum.append(cardNum1)
      cardNum.append(cardNum2)
      cardNum.append(cardNum3)
      cardNum.append(cardNum4)

      self.board = Board(history, mountNum, point, order, cardNum)
      self.power = [30, 30, 20, 70, 80, 0, 150, 0, 50, 80, 60, 80, 100]
      self.counter = 0
      #             1, 2,   3, 4,  5,   6, 7,   8, 9, 10, j, q, k
      if the_specific_small_h is None:
         self.smallh = None
      else:   
         self.smallh = the_specific_small_h

   def __str__(self):
      return str(self.myCard.moves)

   def checkLose(self):
      return len(self.myCard.moves) == 0

   # TODO
   def simulateMove(self, action):
      move = 0
      for c in action.cards_used:
         self.myCard.cards.remove(c)
         move = move + getCardValue(c)
      if len(action.cards_used) == 1 and action.cards_used[0] == 1:
         self.board.nowPoint = 0
      elif move == 13:
         self.board.nowPoint = 99
      elif move == 1 or move == 2 or move == 3 or move == 6 or move == 8:
         self.board.nowPoint += move  
      elif move == 10 or move == 12:
         if action.victim == -1:
            self.board.nowPoint += move
         elif action.victim == -2:
            self.board.nowPoint -= move
      elif move == 4:
         self.order *= -1
      self.myCard.moves.remove(action)

   def Eval(self, userid):
      score = 0
      for card in self.myCard.cards:
         score = score + self.power[getCardValue(card)]
      for cnum in self.board.cardNum:
         score = score - cnum*60
      score = score + 2*self.board.cardNum[userid]
      return score


class MyCard:
   def __init__(self, moves, cards):
      self.moves = moves
      self.cards = cards

class Board:
   def __init__(self, r, rn, p, o, c):
      self.record = r
      self.restNum = rn
      self.nowPoint = p
      self.order = o
      self.cardNum = c

cardType = ['♠ ', '♥ ', '♦ ', '♣ ']
def getCardString(cardIndex):
    cardvalue = 13 if (cardIndex % 13 == 0) else cardIndex % 13
    return str(cardvalue) + cardType[(cardIndex-1)/13]
def getCardValue(cardIndex):
   return cardIndex % 13
def getMoveString(move):
   return str(move)
      
class MonteAgent(Agent):
   """
   The Montecaro agent
   """
   def __init__(self, i = 0):
      self.i = i
      self.count = 0
      #print "Constructing Montecaro Agent, id = ", self.i

   def genmove(self, state):
      if len(state.myCard.moves) < 5 or state.board.cardNum[1]+state.board.cardNum[2]+state.board.cardNum[3] < 8:
         # In any circumstance, when unknown_cards < 17, use monte carlo algorithm
         return self.monteGenmove(state)
      else:
         return self.heuristicgenmove(state)

   # Monte_Carlo_Part
   
   def monteGenmove(self, state):
      # Find the unknown cards
      win_rate = []

      fullCard = self.fullCard()
      temp = self.usedCard(state)

      usedCard = []
      for i in temp:
         for j in i:
            usedCard.append(j)
      usedCard.extend(state.myCard.cards)
      print usedCard

      t = set()
      rep_list = [x for x in usedCard if x in t or t.add(x)]

      if len(rep_list) != 0:
         usedCard = rep_list
         #time.sleep(100)
      
      self.count = self.count + 1
      cards_unknown = [i for i in fullCard if i not in usedCard]
      print "===============================SIMULATION START", self.count, "========================================="
      for candidate in state.myCard.moves:
         for i in range(0, 50):
            print "===============================QQQQQQQQQQQQQQQQQQ", i, "========================================="
            
            cards_1 = state.myCard.cards

            # Shuffle and deal cards
            random.shuffle(cards_unknown)
            dummy = 0
            cards_2 = cards_unknown[dummy : state.board.cardNum[1]]
            dummy += state.board.cardNum[1]
            cards_3 = cards_unknown[dummy : dummy + state.board.cardNum[2]]
            dummy += state.board.cardNum[2]
            cards_4 = cards_unknown[dummy : dummy + state.board.cardNum[3]]
            dummy += state.board.cardNum[3]
            mountain = cards_unknown[dummy:]
            print state.board.cardNum[1] + state.board.cardNum[2] + state.board.cardNum[3]
            print cards_1
            print cards_2
            print cards_3
            print cards_4
            print "mountain", mountain
            # Play under certain condition
            # Build a simulation judge (mc_judge)
            mc_judge = MiniJudge()
            # Replicate situation
            mc_judge.point = copy.deepcopy(state.board.nowPoint)
            mc_judge.clock_wise = copy.deepcopy(state.board.order)
            mc_judge.history = copy.deepcopy(state.board.record)
            mc_judge.smallh = copy.deepcopy(state.smallh)
            # write in the card distribution above
            mc_judge.card = []
            for i in [cards_1, cards_2, cards_3, cards_4]:
               hand = []
               for j in i:
                  hand.append(j)
               mc_judge.card.append(hand)
            #做出已經出完candidate牌的樣子?
            #mc_judge.printBoard()
            try:
               mc_judge.doAction(candidate)
               #print "==================Assign Success========================"
               winner = mc_judge.GameStart()
               if winner == 0: 
                  win_rate.append(candidate)
            except:
               pass
            #print "++++++++++++++++++++++++++++ SIMULATION END ++++++++++++++++++++++++++++++++"
            ##print "++++++++++++++++++++++++++++ WINNER ++++++++++++++++++++++++++++++++", winner
      if len(win_rate) == 0:
         return random.choice(state.myCard.moves)
      else:
         return random.choice(win_rate)

   def fullCard(self):
      fullCard = []
      for i in range(1,53):
         fullCard.append(i)
      return fullCard

   def usedCard(self, state):
      usedCard = []
      for i in state.board.record:
         print i
         usedCard.append(i.cards_used)
      return usedCard

   # Totally by heuristic...
   def heuristicgenmove(self, state):
      move = state.myCard.moves[0]     
      if len(state.myCard.cards) == 1 or len(state.myCard.moves) == 1:
         return move
      if len(state.myCard.cards) == 2:
         for a in range(0, len(state.myCard.moves)):
            m = 0
            for c in state.myCard.moves[a].cards_used:
               m = m + getCardValue(c)
            if len(state.myCard.moves[a].cards_used) == 2:
               if m != 9:
                  continue
               else:
                  movelist = [state.myCard.moves[a]]
                  while a < len(state.myCard.moves)-1:
                     a += 1
                     n = 0
                     for j in state.myCard.moves[a].cards_used:
                        n = n + getCardValue(j)
                     if n != 9:                       
                        return state.myCard.moves[a-1]
                     else:
                        movelist.append(state.myCard.moves[a])
                  return self.chooseMaxCard(state, movelist)
                  #return random.choice(movelist)
      if len(state.myCard.cards) == 3 or 4:
         move = self.pickBest(state)
      if len(state.myCard.cards) > 4:         
         for a in state.myCard.moves:
            m = 0
            for c in a.cards_used:
               m = m + getCardValue(c)
            handCards = len(state.myCard.cards) - len(a.cards_used)
            if handCards == 3 and m != 9: # try to reduce cards to 3
               return a            
         move = self.pickBest(state)
      #print "+++++++++++++++++++++++", move
      move = self.pickBest(state)
      return move

   def chooseMaxCard(self, state, movelist):
      """ return the most-hand-card victim move"""
      cardList = list(state.board.cardNum)
      cardNumList = list(state.board.cardNum)
      cardNumList.sort()      
      cardNumList.reverse()
      victim = list()
      for c in range(0, len(cardNumList)):
         victim.append(cardList.index(cardNumList[c]))
         cardList.remove(cardNumList[c])
      move = list()
      for i in range(0, len(victim)):
         if move == []:
            for m in movelist:
               if ((m.victim-1) == victim[i]):
                  move.append(m)
            if len(move) > 0:
               break
      if len(move) == 0:
         move = movelist
      return random.choice(move)

   def pickBest(self, state):
   # choose 1-card action only, by the card-power in class PlayerState
      p = 0
      best = list()
      for a in state.myCard.moves:
         best.append(a)         
         if len(a.cards_used) > 1:
            continue
         m = 0
         for c in a.cards_used:
            m = m + getCardValue(c)
         power = state.power[m-1]
         if power > p:
            best[:] = []
            p = power
            best.append(a)
         if power == p:
            best.append(a)
      return random.choice(best)

def randomGenmove(state):
   a = len(state.myCard.moves)
   if a == 0:
      return []
   else:
      i = random.randint(0, len(state.myCard.moves)-1)
      return state.myCard.moves[i]


if __name__ == "__main__":
   from action import Action
   cards1 = [4, 5, 13, 16, 24]
   cards2 = [2, 7, 9, 18, 27]
   idx = 1
   act = [Action(idx+2, [8], 1)]
   act.append(Action(idx+2, [4], 0))
   act.append(Action(idx+2, [4, 8], 0))
   ai = ScoutAgent(idx)
   human = HumanAgent(idx+1)
   heu = HeuristicAgent(idx+2)
   record = "1 ChangeCard 9 2"
   state = PlayerState(record, [1, 3, 4, 12], [1,3, 16,24], 3, 4, 0, 2, 33, 99, 1)
   # record, legal, mycard
   state2 = PlayerState(record, act,[4, 8], 3, 4, 0, 2, 33, 99, 1)
   b = human.genmove(state)
   c = heu.genmove(state2)