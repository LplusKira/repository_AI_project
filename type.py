_InitCardsPerPlayer_ = 5
_TotalPlayerNum_ = 4
_IamDead_ = -1
_MaxCombCardNum_ = 5

class Action:
    def __init__(self, u = 0, c = list(), v = 0):
        self.user = u
        self.cards_used = c #_MaxCombCardNum_
        self.victim = v

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
    def __init__(self, h = list(), c = [[]], m=list(), p=0, cw=1, cp=1):
        #self.player_state = ps #what is this
        self.history = h #action list
        self.card = c # need to sort by cardvalue,two dimension list
        self.mountain = m
        self.point = p
        self.clock_wise = cw
        self.current_player = cp
        self.GameStart()
        
    '''def rand4Cards(int p1_cards[], int p2_cards[], int p3_cards[], int p4_cards[], vector<int> mountain):
        pass
    def TellAgent(self, int which_agent, state what_happened):
        pass'''

    def GameStart(self):
        pass
    '''        srand(time(NULL));
    initBoard();
    while(!isGameFinished()):
    this.writeFile();//write state
    //call python agent
    //wait it complete
    action a = this.readFile();
    this.doAction(a);
    }
    //maybe judge need more precise history for debug usage
    }'''

    def initBoard(self):
        self.current_player = 1
        clock_wise = 1 #1 and -1
    #cards

    def isGameFinished(self):
        pass
    #return this.card[0].length() == 0...;

    def writeFile(self):
        pass
    #generateStateData();

    def generateStateData(self):
        pass
    '''//including legal actions, history, ...
    //different from judge data, only have partial information
    vector<action> possibleActions = getAction();'''

    def readFile(self):
        pass

    def doAction(self):
        current_player += clock_wise;
    
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
            if a.victim == -1 and this.point + value <= 99 or a.victim == -2 and this.point - value >= 0:
                return true
        elif cardValue == 4 or cardValue == 11 or cardValue == 13:
            return true
        else:
            if this.point+cardValue <= 99:
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

if __name__ == "__main__" :
    j = Judge()
