# -*- coding: utf-8 -*-
import random
import time
import copy
import action
INF = 2147483647

class Agent:
   def __init__(self, index = 0):
      self.index = index
   
   def genmove(self, state):
      pass

class State:
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

   def simulateMove(self, action):
      pass

   def Eval(self, userid):
      score = 0
      for card in self.myCard.cards:
         score = score + self.power[getCardValue(card)]
      for cnum in self.board.cardNum:
         score = score - cnum*60
      score = score + 2*self.board.cardNum[userid]
      return score

def parseHistory(history):
   h = history.split()
   return History(h[0], h[1], h[2], h[3])
   
class History:
   def __init__(self, i, m, c, t):
      self.index = i
      self.move = m
      self.cards = c
      self.target = t

   def __str__(self):
      s = ""
      for card in self.cards:
         s = s + getCardString(card) + ", "
      return "index = " + str(self.index) + "\ncard = " + s + "\nact = " + str(self.move) + "target = " + str(self.target)

class MyCard:
   def __init__(self, moves, cards):
      self.moves = moves
      self.cards = cards

class Board:
   def __init__(self, r, rn, p, o, c):
      self.record = parseHistory(r)
      self.restNum = rn
      self.nowPoint = p
      self.order = o
      self.cardNum = c

cardType = ['♠ ', '♥ ', '♦ ', '♣ ']
def getCardString(cardIndex):
   return str(cardIndex % 13) + " " + cardType[cardIndex/13]
def getCardValue(cardIndex):
   return cardIndex % 13
      
class ScoutAgent(Agent):
   def __init__(self, i = 0, cards = list()): # only need to know id
      self.i = i
      print "Constructing Simple Agent, player id = ", self.i

   def genmove(self, state):
      return self.abGenmove(state)
      
   def randomGenmove(self, state):
      i = random.randint(0, len(state.myCard.moves)-1)
      f = open("playerlog", "w")
      f.write(str(state.myCard.moves[i]))
      return state.myCard.moves[i]

   def abGenmove(self, state, depth = 5, maxTime = 10):
      startTime = time.time()
      self.endTime = startTime + maxTime
      if state.board.nowPoint < 90: # do easy heuristic
         return self.randomGenmove(state)
      else:
         score = self.search(state, -INF, INF, depth)
         #print "search best move = " + action + "score = " + score
         print "use " + str(time.time()-startTime) + "time"
         return self.randomGenmove(state) #temp

   def search(self, s, alpha, beta, depth): # fail soft negascout
      if state.checkLose():
         return -INFORMATION
      if depth == 0 or self.timeUp(): # or some heuristic
         return s.Eval(self.i) if depth%2 == 0 else -s.Eval(self.i) #todo:check
      m = -INF # current lower bound, fail soft
      n = beta # current upper bound
      for a in state.myCard.moves:
         news = copy.deepcopy(s)
         news.simulateMove(a)
         tmp = -self.search(news, -n, -max(alpha, m), depth-1)
         if tmp > m: #todo:check
            if n == beta or depth < 3 or tmp >= beta:
               m = tmp
            else:
               m = -self.search(news, -beta, -tmp, depth-1) #research
         if m >= beta: # cut off
            return m 
         n = max(alpha, m) + 1 # set up null window
      return m

   def timeUp(self):
      nowTime = time.time()
      if nowTime > self.endTime:
         return True
      else:
         return False
         
class HumanAgent(Agent):
   """
   The human agent, action decided by human.
   """
   def __init__(self, i = 0):
      self.i = i
      print "Constructing Human Agent, id = ", self.i

   def genmove(self, state):
      return self.humanGenmove(state)

   def humanGenmove(self, state):
      s = ""
      for card in state.myCard.cards:
         s = s + getCardString(card) + ", "
      print "The card you have: ", s
      print "The legal move you can take: ", state
      print "The point now is: ", state.board.nowPoint
      move = raw_input("pick the move by input the move index: ")   
      while ((move.isdigit() == False) or (int(move) < 0) or (int(move) >= len(state.myCard.moves))):
         move = raw_input("The move index value is illegal, try again: ")                   
      print "The move you take is: ", state.myCard.moves[int(move)]
      f = open("playerlog", "w")
      f.write(str(state.myCard.moves[int(move)]))
      return state.myCard.moves[int(move)]
   

class MonteAgent(Agent):
   """
   The Montecaro agent
   """
   def __init__(self, i = 0):
      self.i = i
      print "Constructing Montecaro Agent, id = ", self.i

   def genmove(self, state):
      knownCard = 0
      if knownCard < 17:
          return randGenmove(state)
      else:
          return monteGenmove(state)

   # TODO: Can use other heuristic here
   def randomGenmove(self, state):
      i = random.randint(0, len(state.myCard.moves)-1)
      f = open("playerlog", "w")
      f.write(str(state.myCard.moves[i]))
      return state.myCard.moves[i]

   def monteGenmove(self, state):
      i = MontecaroSearch(state)
      f = open("playerlog", "w")
      f.write(str(state.myCard.moves[i]))
      return state.myCard.moves[i]
      

if __name__ == "__main__":
   cards1 = [4, 5, 13, 16, 24]
   cards2 = [2, 7, 9, 18, 27]
   idx = 1
   ai = ScoutAgent(idx)
   human = HumanAgent(idx+1)
   record = "1 ChangeCard 9 2"
   state = State(record, [1, 3, 4, 12], [1, 16,24], 3, 4, 0, 2, 33, 99, 1)
   # record, legal, mycard
   state2 = State(record, [2, 7, 9], [2,7], 3, 4, 0, 2, 33, 99, 1)
   b = human.genmove(state)
   #print "Simple agent's action " + ai.genmove(state)
   #print "Human player's action ", human.genmove(state2)
