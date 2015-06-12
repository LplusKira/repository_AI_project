# -*- coding: utf-8 -*-
import random
import time
import copy
import action
import operator
from minijudge import MiniJudge
INF = 2147483647

class Agent:
   def __init__(self, index = 0):
      self.index = index
   
   def genmove(self, state):
      pass

class PlayerState:
   def __init__(self, history, leg, card, cardNum1, cardNum2, cardNum3, cardNum4, mountNum, point, order):
      self.myCard = MyCard(leg, card)# var card non exist
      cardNum = list()
      cardNum.append(cardNum1)
      cardNum.append(cardNum2)
      cardNum.append(cardNum3)
      cardNum.append(cardNum4)
      self.board = Board(history, mountNum, point, order, cardNum)
      self.power = [30, 30, 20, 70, 80, 0, 150, 0, 50, 80, 60, 80, 100 ]
      #             1, 2,   3, 4,  5,   6, 7,   8, 9, 10, j, q, k

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
      print "Constructing Montecaro Agent, id = ", self.i

   def genmove(self, state):
      # In any circumstance, when unknown_cards < 17, use monte carlo algorithm
      if state.board.cardNum[1] + state.board.cardNum[2] + state.board.cardNum[3] + state.board.restNum > 17:
          return self.heuristicgenmove(state)
      else:
          return self.monteGenmove(state)

   # Monte_Carlo_Part
   
   def monteGenmove(self, state):
      # Find the unknown cards
      print "========================================================================"
      win_rate = {}
      fullCard = self.fullCard()
      temp = self.usedCard(state)
      usedCard = []
      for i in temp:
         for j in i:
            usedCard.append(j)
      usedCard.extend(state.myCard.cards)
      cards_unknown = [i for i in fullCard if i not in usedCard]

      for candidate in state.myCard.moves:
         win_point = 0
         for i in range(0, 1067):
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
            
            # Play under certain condition
            # Build a simulation judge (mc_judge)
            mc_judge = MiniJudge()
            # Replicate situation
            mc_judge.point = state.board.nowPoint
            mc_judge.clock_wise = state.board.order
            mc_judge.history = state.board.record
            # write in the card distribution above
            mc_judge.card = []
            for i in [cards_1, cards_2, cards_3, cards_4]:
               hand = []
               for j in i:
                  hand.append(j)
               mc_judge.card.append(hand) 
            print mc_judge.card
            #做出已經出完candidate牌的樣子?
            mc_judge.doAction(candidate)      

            # (Player1在模擬局中，出candidate，之後讓mc_judge自己跑ab_agent跑完全程，回傳輸贏）???
            winner = mc_judge.GameStart()
            print "++++++++++++++++++++++++++++ SIMULATION END ++++++++++++++++++++++++++++++++"
            #print "++++++++++++++++++++++++++++ WINNER ++++++++++++++++++++++++++++++++", winner
            if winner == 0: 
               win_point = win_point + 1
               #print "++++++++++++++++++WIN POINT COUNT+++++++++++++++++++++++++", win_point
            else:
               pass
         # find the win rate of a certain candidate, append it
         win_rate.update({candidate : win_point})
      temp__A.append(str(win_rate))
      print "++++++++++++++++++++++++ temp__A +++++++++++++++++++++++++++++", str(temp__A)
      decided_card = max(win_rate.iteritems(), key=operator.itemgetter(1))[0]
      return decided_card

   def fullCard(self):
      fullCard = []
      for i in range(1,53):
         fullCard.append(i)
      return fullCard

   def usedCard(self, state):
      usedCard = []
      for i in state.board.record:
         usedCard.append(i.cards_used)
      return usedCard

   # Totally by heuristic...
   def heuristicgenmove(self, state):
      move = state.myCard.moves[0]     
      if len(state.myCard.cards) == 1 or len(state.myCard.moves) == 1:
         return move
      if len(state.myCard.cards) == 2:
         p = 0
         for a in state.myCard.moves:
            m = 0
            for c in a.cards_used:
               m = m + getCardValue(c)
            if len(a.cards_used) == 2:
               if m == 9:
                  return a
               else:
                  continue
            power = state.power[m-1]
            if power > p:
               p = power
               move = a
      if len(state.myCard.cards) == 3:
         move = self.pickBest(state)
      if len(state.myCard.cards) > 3:         
         for a in state.myCard.moves:
            m = 0
            for c in a.cards_used:
               m = m + getCardValue(c)
            handCards = len(state.myCard.cards) - len(a.cards_used)
            if handCards == 3 and m != 9: # try to reduce cards to 3
               return a            
         move = self.pickBest(state)
      return move

   def pickBest(self, state):
   # choose 1-card action only, by the card-power in class PlayerState
      p = 0
      for a in state.myCard.moves:
         best = a
         if len(a.cards_used) > 1:
            continue
         m = 0
         for c in a.cards_used:
            m = m + getCardValue(c)
         power = state.power[m-1]
         if power > p:
            p = power
            best = a         
      return best

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
   print c
   #print "Simple agent's action " + ai.genmove(state)
   #print "Human player's action ", human.genmove(state2)
