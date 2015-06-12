import random
import time
import copy
import action
from simJudge import JudgeState
from simJudge import SimJudge
INF = 2147483647

def wait_input():
   #raw_input()
   pass

class Agent: # todo:how to remove this
   def __init__(self, index = 0):
      self.index = index
   
   def genmove(self, state):
      pass

class ScoutAgent(Agent):
   def __init__(self, i = 0): # only need to know id
      self.i = i
      #print "Constructing Alpha-Beta Agent, player id = ", self.i

   def genmove(self, state):
      self.state = state
      a = self.scoutGenmove(state)
      return a

   def fillstate(self, s):    #fill other's card, mountain
      restcard = [i+1 for i in range(52)]
      nonUsedCard = [i+1 for i in range(52)]# cards that never showed in this game, always in someone's hand
      for c in s.myCard.cards:
         restcard.remove(c)
      lastrand = -1
      for i, a in enumerate(s.board.record):
         for c in a.cards_used:
            if c in nonUsedCard:
               nonUsedCard.remove(c)
         if a.user == 0: # after lastest randmountain
            lastrand = i
      for i in range(lastrand+1, len(s.board.record), 1):
         for c in s.board.record[i].cards_used:
            restcard.remove(c)
      random.shuffle(restcard)

      if lastrand == -1:
         nonUsedCard = []
      unknownHandCardNum = 0
      for i in range(4):
         if i+1 != self.i:
            unknownHandCardNum += s.board.cardNum[i]
      handcard = nonUsedCard
      while len(handcard) < unknownHandCardNum:
         handcard.append(restcard[-1])
         restcard.pop()
      mountain = restcard # rest
      cards = []
      for i in range(4):
         if self.i == i+1:
            cards.append(s.myCard.cards)
         else:
            playercard = []
            for j in range(s.board.cardNum[i]):
               playercard.append(handcard[-1])
               handcard.pop()
            cards.append(playercard)

      js = JudgeState(4, None, s.board.record, cards, mountain, s.board.nowPoint, s.board.order, self.i)
      return js
   
   def scoutGenmove(self, state, depth = 1, maxTime = 100, replayNum = 20):

      #print state.the_specific_small_h
      """
                        print "it's scout speaking"
                  
                        for i in range(len(state.the_specific_small_h)):
                           print "usr == " + str(state.the_specific_small_h[i].user) + ", cards == "
                           for j in range(len(state.the_specific_small_h[i].cards_used)):
                              print  state.the_specific_small_h[i].cards_used[j]
                           print "operation == " + str(state.the_specific_small_h[i].victim)
                        #time.sleep(1)"""

      startTime = time.time()
      self.endTime = startTime + maxTime
      self.avgScore = {}
      # todo: remove redunant moves
      js = self.fillstate(state)
      self.bestmove = state.myCard.moves[0]
      self.judge = SimJudge(js)
      score = self.maxSearch(self.judge, -INF, INF, depth, 0)
      print "use " + str(time.time()-startTime) + "time"
      print "bestmove = " + str(self.bestmove)
      #self.judge.printBoard()
      wait_input()
      #if self.bestmove not in state.myCard.moves:
       #  print "abgenmove: no this move"
        # exit()
      return self.bestmove #todo:

   # todo: remove redundant move from server(4h, 4s...) after getaction()
   # todo: remember some structure to win 
   # fix: in fact, can are not playing with randomagent, but a smart agent
   # idea: all max search for each player's evaluation
           # not every player want to kill me...
   # every player have different evaluation value...
   '''
   test result:
   heuristic        depth result(2000times) techniques
   cardnum            1   38.35%
   power              2   ?%              power = [0, 20, 10, 10, 60, 80, -30, 10, -50, 80, 80, 60, 100, 80]
   dynamic-power      2   ?% (56% vs heuristic) self.dpeval(), when card < 2, preserve 9 as killer.
   dynamic-power      2   36.6% (% vs heuristic) self.dpeval1(), when card < 2, preserve 9 as killer.
   dynamic-power      1   37.7% (% vs heuristic) self.dpeval1(), when card < 2, preserve 9 as killer.
   dynamic-power      1   38% (% vs heuristic) self.dpeval1(), remember cards
   dynamic-power      1   39.85% (% vs heuristic) self.dpeval1(), remember cards, no trim getaction in simjudge
   '''
   def maxSearch(self, s, alpha, beta, depth, nowdepth):
      #print "maxsearch"
      if s.checkLose(self.i):
         #print "i am dead"
         #s.printBoard()
         return -INF
      if depth == 0:
         return s.myEval(self.i)
      if nowdepth == 0:
         moves = self.state.myCard.moves
      else:
         moves = s.getAction()
      m = -INF # current lower bound, fail soft
      if len(moves) > 0:
         news = copy.deepcopy(s)
         news.doAction(moves[0])
         if news.current_player == self.i:
            score = self.maxSearch(news, alpha, beta, depth-1, nowdepth+1)
         else:
            score = self.minSearch(news, alpha, beta, depth-1, nowdepth+1) 
         m = max(m, score)
         if m >= beta:
            #print "beta cutoff %d %d %d" % (m, score, beta) + str(moves[0])
            return m
      for a in moves:
         news = copy.deepcopy(s)
         news.doAction(a)
         if news.current_player == self.i: # next node is max
            tmp = self.maxSearch(news,m,m+1,depth-1,nowdepth+1)
         else: #minnode
            tmp = self.minSearch(news,m,m+1,depth-1,nowdepth+1)

         if tmp > m: #todo:check
            if depth < 3 or tmp >= beta:
               m = tmp
            else:
               if news.current_player == self.i: # next node is max
                  m = self.maxSearch(news,tmp,beta,depth-1,nowdepth+1)
               else: #minnode
                  m = self.minSearch(news,tmp,beta,depth-1,nowdepth+1)
            if nowdepth == 0:
               self.bestmove = a
         if nowdepth == 0:
            #print "search max move: " + str(a)  + "  score = " + str(m)
            wait_input()
         if m >= beta: # cut off
            #print "beta cutoff %d %d" % (m, beta) + str(a)
            return m
      return m

   def minSearch(self, s, alpha, beta, depth, nowdepth):
      #print "minsearch"
      if s.checkLose(self.i):
         #print "i am dead"
         #s.printBoard()
         return INF #?
      if depth == 0:
         return s.myEval(self.i)
      moves = s.getAction()
      m = INF # current lower bound, fail soft
      if len(moves) > 0:
         news = copy.deepcopy(s)
         news.doAction(moves[0])
         if news.current_player == self.i:
            score = self.maxSearch(news, alpha, beta, depth-1, nowdepth+1)
         else:
            score = self.minSearch(news, alpha, beta, depth-1, nowdepth+1) 
         m = min(m, score)
         if m <= alpha:
            #print "alpha cutoff %d %d [%d, %d]" % (m, score, alpha, beta) + str(moves[0])
            return m
      for a in moves:
         news = copy.deepcopy(s)
         news.doAction(a)
         if news.current_player == self.i: # next node is max
            tmp = self.maxSearch(news,m-1,m,depth-1,nowdepth+1)
         else: #minnode
            tmp = self.minSearch(news,m-1,m,depth-1,nowdepth+1)

         if tmp < m: #todo:check
            if depth < 3 or tmp <= alpha:
               m = tmp
            else:
               if news.current_player == self.i: # next node is max
                  m = self.maxSearch(news,alpha,tmp,depth-1,nowdepth+1)
               else: #minnode
                  m = self.minSearch(news,alpha,tmp,depth-1,nowdepth+1)
            if nowdepth == 0:
               self.bestmove = a
         if nowdepth == 0:
            pass
            #print "search min move: " + str(a)  + "  score = " + str(tmp)
         else:
            indent = ""
            for i in range(nowdepth):
               indent += "    "
            #print indent + "search min move "+ str(a)  + "  score = " + str(tmp)
         if m <= alpha: # cut off
            #print "alpha cutoff %d [%d, %d]" % (m, alpha, beta) + str(a)
            return m 
      return m

   def search(self, s, alpha, beta, depth, nowdepth): # fail soft negascout
      if s.checkLose(self.i):
         print "i am dead"
         s.printBoard()
         return -INF
      #if depth == 0 or self.timeUp(): # or some heuristic
      if depth == 0:
         return s.myEval(self.i) if s.current_player == self.i else -s.myEval(self.i)#todo:not depth = 2
      m = -INF # current lower bound, fail soft
      n = beta # current upper bound
      if nowdepth == 0:
         moves = copy.deepcopy(self.state.myCard.moves)
      else:
         moves = s.getAction()
      for a in moves:
         news = copy.deepcopy(s)
         news.doAction(a)
         if news.current_player == self.i: # next node is max
            tmp = self.search(news, min(alpha, m), n, depth-1, nowdepth+1)
         else: #minnode
            tmp = -self.search(news, -n, -max(alpha, m), depth-1, nowdepth+1)

         if tmp > m: #todo:check
            if n == beta or depth < 3 or tmp >= beta:
               m = tmp
            else:
               if news.current_player == self.i: # maxnode
                  m = self.search(news, tmp, beta, depth-1, nowdepth+1) #research
               else: #minnode
                  m = -self.search(news, -beta, -tmp, depth-1, nowdepth+1) #research
            if nowdepth == 0:
               self.bestmove = a
         if nowdepth == 0:
            print "search move: " + str(a)  + "  score = " + str(tmp)
            wait_input()
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
