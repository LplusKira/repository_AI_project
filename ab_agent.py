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
      
class ScoutAgent(Agent):
   def __init__(self, i = 0, cards = list()): # only need to know id
      self.i = i
      print "Constructing Simple Agent, player id = ", self.i

   def genmove(self, state):
      return randomGenmove(state)


   def abGenmove(self, state, depth = 5, maxTime = 10):
      startTime = time.time()
      self.endTime = startTime + maxTime
      if state.board.nowPoint < 90: # do easy heuristic
         return randomGenmove(state)
      else:
         score = self.search(state, -INF, INF, depth)
         #print "search best move = " + action + "score = " + score
         print "use " + str(time.time()-startTime) + "time"
         return randomGenmove(state) #temp

   def search(self, s, alpha, beta, depth): # fail soft negascout
      if state.checkLose():
         return -INF
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
      moves = list()
      for m in state.myCard.moves:
         moves.append(getMoveString(m) + ",\n")
      print "The card you have: ", s
      print "The legal move you can take: "
      for i in range(0, len(moves)):
         print "move index:", i, moves[i], 
      print "The point now is: ", state.board.nowPoint
      move = raw_input("pick the move by input the move index: ")   
      while ((move.isdigit() == False) or (int(move) < 0) or (int(move) >= len(state.myCard.moves))):
         move = raw_input("The move index value is illegal, try again: ")                   
      print "The move you take is: ", state.myCard.moves[int(move)]
      return state.myCard.moves[int(move)]
   

class MonteAgent(Agent):
   """
   The Montecaro agent
   """
   def __init__(self, i = 0):
      self.i = i
      print "Constructing Montecaro Agent, id = ", self.i

   def genmove(self, state):
      othersCard = 0
      for cardNum in state.cardNum:
          othersCard = othersCard + len(cardNum)
      knownCard = 52 - (state.board.restNum + othersCard - state.cardNum[self.i])
      if knownCard < 17:
          return randomGenmove(state)
      else:
          return self.monteGenmove(state)

   # TODO: Can use other heuristic here
   def monteGenmove(self, state):
      i = MontecaroSearch(state)
      return state.myCard.moves[i]
      
class HeuristicAgent(Agent):
   """
   Only use heuristics.
   """
   def __init__(self, i = 0):
      self.i = i
      print "Constructing Heuristic Agent, id = ", self.i

   # Totally by heuristic...
   def genmove(self, state):
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
      print state.myCard.moves[i]
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
