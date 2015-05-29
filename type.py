_InitCardsPerPlayer_ = 5
_TotalPlayerNum_ = 4
_IamDead_ = -1
_MaxCombCardNum_ = 5
_cardNum_ = 52
_MaxActionLength_ = 20
_MaxComb_ = 32

import random
import time
import action
import ab_agent

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
        #self.player_state = ps #what is this
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
        self.player = ab_agent.ScoutAgent()
        self._possibleActions_.append(action.Action())
        self._possibleActions_.append(action.Action())
        self._possibleActions_.append(action.Action())
        self._possibleActions_.append(action.Action())
        state = ab_agent.PlayerState(self.history, self._possibleActions_, self.card[self.current_player], len(self.card[0]), len(self.card[1]), len(self.card[2]), len(self.card[3]), len(self.mountain), self.point, self.clock_wise)
        self.player.genmove(state)

        
        '''while(not self.isGameFinished()):
        this.writeFile()
            for i in range(_MaxComb_ * _MaxActionLength_):
                parsingBuf_possibleActions[i] = '\0';
            for i in range(_possibleActions_.size()):
                sprintf(ourBuf, "%d %d %d %d %d %d %d;", _possibleActions_[i].user, _possibleActions_[i].cards_used[0], _possibleActions_[i].cards_used[1], _possibleActions_[i].cards_used[2], _possibleActions_[i].cards_used[3], _possibleActions_[i].cards_used[4], _possibleActions_[i].victim);
                strncat(parsingBuf_possibleActions, ourBuf, strlen(ourBuf));

    if((pid = fork()) == 0) //  child
    {
      //  TODO: transmit history, _possibleActions_
      execlp(_PlayerExecName_, _PlayerExecName_, parsingBuf_possibleActions ,(char*)0);
    }

    //  TODO: wait for your child to be dead...
    waitpid(-1, &status, 0);'''

        a = self.readFile()
        self.doAction(a)
    def rand4Cards(self):
        original_cards = list()
        random.seed(time.time())
	for i in range(_cardNum_):
            original_cards.append(i + 1)
        for i in range(_TotalPlayerNum_):
            for counter in range(_InitCardsPerPlayer_):
                pick = random.randint(0,1024) % len(original_cards)
                self.card[i][counter] = original_cards[pick]
                swap(original_cards[pick], original_cards[len(original_cards) - 1])
                original_cards.pop()
        #//	TODO:	set mountain
        for i in range(len(original_cards)):
            pick = random.randint(0, 1024) % len(original_cards);
            self.mountain.append(original_cards[pick])
            swap(original_cards[pick], original_cards[len(original_cards) - 1])
            original_cards.pop()
    
    def initBoard(self):
        self.current_player = 1
        self.clock_wise = 1 #1 and -1
    #cards

    def isGameFinished(self):
        pass
    #return this.card[0].length() == 0...;

    def printBoard(self):
        pass
    
    def writeFile(self):
        pass
    #generateStateData();

    def generateStateData(self):
        _possibleActions_ = self.getAction()

    def readFile(self):
        pass

    def doAction(self, a):
        self.history.append(a)
        self.current_player += self.clock_wise
        if self.current_player == 0:
            self.current_player = 4
        elif self.current_player == 5:
            self.current_player = 1
        self.current_player += self.clock_wise

    def TellAgent(self, which_agent, what_happened):
        pass
        
    def getAction(self): # get legal action list
        card = self.card[current_player];
        isuse = [False]*len(card) # size = card
        av = list()
        a = Action(self.current_player)
        while(nextbool(av, n)):
            nowv = 0
            a.cards = []
            for i in range(n):
                if isuse[i]:
                    nowv += card[i]%13
                    a.cards.append(card[i])
                    
            if nowv > 13:
                continue
            else:
                nowv %= 13 #?
            
        if nowv == 7 or nowv == 9:
            for i in range(_TotalPlayerNum_):
                if i == self.current_player or self.card[i].length() == 0: #todo: isdead?
                    continue
                a.victim = i
                av.append(a)
        elif nowv == 5:
            for i in range(_TotalPlayerNum_):
                if self.card[i].length() == 0: #todo: isdead?
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
                iszero = true
        if iszero and cardValue == 1:
            return true

        cardValue = cardValue % 13
        if cardValue == 7:
            if a.victim > 0 and a.victim <= 4 and a.victim != a.user and len(card[a.victim-1]) >= 1:#//now user id?
                return true
        elif cardValue == 9:
            if a.victim > 0 and a.victim <= 4 and a.victim != a.user:#//now user id?
                return true
        elif cardValue == 5:
            if a.victim > 0 and a.victim <= 4:
                return true
        elif cardValue == 12 or cardValue == 10:
            value = 20 if (cardValue % 13 == 12) else 10
            if a.victim == -1 and self.point + value <= 99 or a.victim == -2 and self.point - value >= 0:
                return true
        elif cardValue == 4 or cardValue == 11 or cardValue == 13:
            return true
        else:
            if self.point+cardValue <= 99:
                return true
        return false

def nextbool(vb, n):
    nowv = 0
    for i in range(n):
        nowv *= 2
        nowv += 1 if (vb[i]) else 0
    nowv = nowv +1
    print nowv
    if nowv >= power(2, n):
        return False, vb
    for i in range(n, 0, -1):
        vb[i] = True if (nowv%2) else False
        nowv /= 2
    print vb
    return True, vb

def swap(a, b):
    c = a
    a = b
    b = c

if __name__ == "__main__" :
    j = Judge()
