import random
import time
import copy
import action
from action import getCardsString
from simJudge import JudgeState
from simJudge import SimJudge
from collections import Counter
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
      self.evalName = 'dpeval1'
      self.knownCard = [list() for i in range(4)]
      self.lasti = 0
      #print "Constructing Alpha-Beta Agent, player id = ", self.i

   def genmove(self, state):
      self.state = state
      a = self.scoutGenmove(state)

      return a

   def getKnownCards(self, s):
      restcard = [i+1 for i in range(52)]
      nonUsedCard = [i+1 for i in range(52)]# cards that never showed in this game, always in someone's hand
      nowsmallhindex = 0
      for i in range(self.lasti, len(s.board.record), 1):
         a = s.board.record[i]
         if a.user == 0: # randmountain
            continue
         #print "remove cards " + getCardsString(a.cards_used)
         for c in a.cards_used: # remove used cards
            if c in self.knownCard[a.user-1]:
               self.knownCard[a.user-1].remove(c)
         a.getCardValue()
         if nowsmallhindex < len(s.smallh) and s.smallh[nowsmallhindex].victim/10 == i:
            smalla = s.smallh[nowsmallhindex]
            #print "smalla" + str(smalla)
            if smalla.victim%10 == 9:
               self.knownCard[smalla.user-1] = smalla.cards_used[:]
            else:
               self.knownCard[smalla.user-1] += smalla.cards_used[:]
            nowsmallhindex += 1
            continue
         if a.cardValue == 9: # card9 which is not related to me
            self.knownCard[a.user-1], self.knownCard[a.victim-1] = self.knownCard[a.victim-1], self.knownCard[a.user-1]
            # it works
         elif a.cardValue == 7: # card7 which is not related to me
            self.knownCard[a.victim-1] = []
            
         '''print "knowncards, after " + str(a)
         for i in range(4):
            print "player %d" % (i+1)
            print action.getCardsString(self.knownCard[i])'''
            
      for i in range(4):
         if s.board.cardNum[i] == 0:
            self.knownCard[i] = []
      self.knownCard[self.i-1] = copy.deepcopy(s.myCard.cards) # haha
      '''if len(s.smallh) > 0:
         print "knowncards"
         for i in range(4):
            print "player %d" % i
            print action.getCardsString(self.knownCard[i])'''

      for c in s.myCard.cards:
         restcard.remove(c)
         nonUsedCard.remove(c)
      lastrand = -1
      for i, a in enumerate(s.board.record):
         for c in a.cards_used:
            if c in nonUsedCard:
               nonUsedCard.remove(c)
         if a.user == 0: # only remove cards after lastest randmountain
            lastrand = i
      for i in range(lastrand+1, len(s.board.record), 1):
         for c in s.board.record[i].cards_used:
            restcard.remove(c)
            
      if lastrand == -1:
         nonUsedCard = []
      for i in range(4):
         for c in self.knownCard[i]:
            if c in restcard: restcard.remove(c)
            if c in nonUsedCard: nonUsedCard.remove(c)
      for c in nonUsedCard:
         restcard.remove(c)
      random.shuffle(restcard)
      self.nonUsedCard = nonUsedCard[:]
      self.restcard = restcard[:]

   def fillstate(self, s):    #fill other's card, mountain
      nonUsedCard = self.nonUsedCard[:]
      restcard = self.restcard[:]
      knownCard = copy.deepcopy(self.knownCard)
      #print "nonusedcard " + getCardsString(nonUsedCard)
      #print "restcard" + getCardsString(restcard)
      unknownHandCardNum = 0
      for i in range(4):
         if i+1 != self.i:
            unknownHandCardNum += s.board.cardNum[i] - len(knownCard[i])
      handcard = nonUsedCard[:]
      while len(handcard) < unknownHandCardNum:
         handcard.append(restcard[-1])
         restcard.pop()
      random.shuffle(handcard)
      mountain = restcard[:] # rest
      cards = []
      #print "handcard" + getCardsString(handcard)
      for i in range(4):
         if self.i == i+1:
            cards.append(s.myCard.cards)
         else:
            playercard = self.knownCard[i][:]
            for j in range(s.board.cardNum[i]-len(playercard)):
               playercard.append(handcard[-1])
               handcard.pop()
            cards.append(playercard)
      if len(s.smallh)>0:
         raw_input
      js = JudgeState(4, None, s.board.record, cards, mountain, s.board.nowPoint, s.board.order, self.i)
      return js
   
   def scoutGenmove(self, state, depth = 1, maxTime = 100, replayNum = 1):
      startTime = time.time()
      self.knownCard = [list() for i in range(4)]
      self.endTime = startTime + maxTime
      self.avgScore = {}
      self.getKnownCards(state)
      for i in range(replayNum):
         js = self.fillstate(state)
         self.bestmove = state.myCard.moves[0]
         self.judge = SimJudge(js, self.evalName, self.i, self.knownCard)
         score = self.maxSearch(self.judge, -INF, INF, depth, 0)
      maxscore = -INF
      '''for k,v in self.avgScore.iteritems(): # need to preserve previous sequence...
         print str(v[0]) + "\t%d" % (v[1]/replayNum)
         if maxscore < v[1]:
            maxscore = v[1]
            self.bestmove = v[0]'''
   
      print "use " + str(time.time()-startTime) + "time"
      print "bestmove = " + str(self.bestmove)
      wait_input()
      #if self.bestmove not in state.myCard.moves:
       #  print "abgenmove: no this move"
        # exit()
      self.lasti = len(state.board.record)
      return self.bestmove #todo:

   def maxSearch(self, s, alpha, beta, depth, nowdepth):
      if s.checkLose(self.i):
         return -INF
      if depth == 0:
         #s.printBoard()
         #print "this board score = " + str(s.myEval(self.i))
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
            
            #news.printBoard()
            #print "action = "+ str(a)+ " score = " + str(m)

            if str(a) in self.avgScore:
               self.avgScore[str(a)][1] += m
            else:
               self.avgScore[str(a)] = [a, m]
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
         ##print "i am dead"
         ##s.printBoard()
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
            ##print "search move: " + str(a)  + "  score = " + str(tmp)
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

class CardNumberHeuristicAgent(ScoutAgent):
   def __init__(self, i = 0): # only need to know id
      self.i = i
      self.evalName = 'cardeval'
      self.knownCard = [list() for i in range(4)]
      self.lasti = 0

   def genmove(self, state):
      self.state = state
      a = self.scoutGenmove(state)
      return a

def checkscore(t, m, cp):
   return getRelativeScore(t, cp) > getRelativeScore(m, cp)

def getRelativeScore(scores, myid):
   # if [1, 2, 3, 4], score of 1 is 1*4 - 2 -3 -4
   newscore = scores[myid-1]*5
   for i in range(4):
      newscore -= scores[i]
   return newscore
   
class AllMaxHeuristicAgent(ScoutAgent):
   def __init__(self, i = 0): # only need to know id
      self.i = i
      #self.evalName = 'dpevalall'
      self.evalName = 'dpevalall'
      self.knownCard = [list() for i in range(4)]
      self.lasti = 0
      
   def genmove(self, state):
      self.state = state
      a = self.scoutGenmove_replay(state)
      return a

   def scoutGenmove(self, state, depth = 3, maxTime = 100, replayNum = 1):
      startTime = time.time()
      self.endTime = startTime + maxTime
      self.knownCard = [list() for i in range(4)]
      self.avgScore = {}
      self.getKnownCards(state)
      bestmoveCounter = Counter()
      
      js = self.fillstate(state) # does it changed?
      self.bestmove = state.myCard.moves[0]
      self.judge = SimJudge(js, self.evalName, self.i, self.knownCard)
      alpha = [INF]*4; alpha[self.i-1] = -INF # the worse
      beta = [-INF]*4; beta[self.i-1] = INF # the best
      score = self.allmaxSearch(self.judge, alpha, beta, depth, 0)
      
      print "use " + str(time.time()-startTime) + "time"
      print "bestmove = " + str(self.bestmove)
      self.lasti = len(state.board.record)
      return self.bestmove #todo:

   def scoutGenmove_replay(self, state, depth = 3, maxTime = 100, replayNum = 10):
      startTime = time.time()
      self.endTime = startTime + maxTime
      self.knownCard = [list() for i in range(4)]
      self.avgScore = {}
      self.getKnownCards(state)
      bestmoveCounter = Counter()
      for i in range(replayNum):
         js = self.fillstate(state) # does it changed?
         self.bestmove = state.myCard.moves[0]
         self.judge = SimJudge(js, self.evalName, self.i, self.knownCard)
         alpha = [INF]*4; alpha[self.i-1] = -INF
         beta = [-INF]*4; beta[self.i-1] = INF
         score = self.allmaxSearch(self.judge, alpha, beta, depth, 0)
         bestmoveCounter[self.bestmove] += 1
      self.bestmove = random.choice(bestmoveCounter.most_common(1))[0]
      
      print "use " + str(time.time()-startTime) + "time"
      print "bestmove = " + str(self.bestmove)
      wait_input()
      self.lasti = len(state.board.record)
      return self.bestmove #todo:
   
   def allmaxSearch(self, s, alpha, beta, depth, nowdepth):
      if depth == 0 or s.checkLose() or s.isGameFinished():
         # getRelativeScore(s.myEval(), s.current_player)
         return s.myEval()
      if nowdepth == 0:
         moves = self.state.myCard.moves
      else:
         moves = s.getAction()
      m = [INF, INF, INF, INF] # current lower bound, fail soft
      m[s.current_player-1] = -INF
      al = alpha[:]
      be = beta[:]
      if len(moves) > 0:
         news = copy.deepcopy(s)
         news.doAction(moves[0])
         score = self.allmaxSearch(news, al, be, depth-1, nowdepth+1)[:]
         m = m if checkscore(m, score, s.current_player) else score[:]
         #print "update m" + str(m)
      for a in moves:
         news = copy.deepcopy(s)
         news.doAction(a)
         nullm1 = m[:]; nullm2 = m[:]; nullm2[s.current_player-1] += 1
         
         tmp = self.allmaxSearch(news,nullm1,nullm2,depth-1,nowdepth+1)[:]

         if checkscore(tmp, m, s.current_player): #todo:check
            if depth < 3 or checkscore(tmp,beta, s.current_player):
               m = tmp[:]
            else:
               t = tmp[:]
               m = self.allmaxSearch(news,t,be,depth-1,nowdepth+1)[:]
            if nowdepth == 0:
               self.bestmove = a
               if str(a) in self.avgScore:
                  self.avgScore[str(a)][1] += m[:]
               else:
                  self.avgScore[str(a)] = [a, m[:]]
               ##print "move = " + str(a) + " score = " + str(getRelativeScore(self.avgScore[str(a)][1], self.i))
      return m

if __name__ == "__main__" :
   pass
   while True:
      js = randomGenCards()
      
      

      
