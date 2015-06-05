from judge import Judge

def simulateAction(self,s,a):# state, action # I skip, let monte carlo do it
    myjudge = SimJudge(s) # todo: build new init function for (judge) state
    print "simulate"
    return judge.getJudgeState()

class JudgeState:
    def __init__(self,playerList = None, h = None, c = None, m=None, p=0, cw=1, cp=1):
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

class SimJudge(Judge):
    def __init__(self, s, a):
        self.state = s
        self.input_state()
        self.action = a
        self.doAction(a)

    def input_state(self):
        self.player = self.state.player
        self.history = self.state.history
        self.card = self.state.card
        self.mountain = self.state.mountain
        self.point = self.state.point
        self.clock_wise = self.state.closk_wise
        self.current_player = self.state.current_player

    def output_state(self):
        self.state.player = self.player
        self.state.history = self.history
        self.state.card = self.card
        self.state.mountain = self.mountain
        self.state.point = self.point
        self.state.closk_wise = self.clock_wise
        self.state.current_player = self.current_player

    def getJudgeState(self):
        self.output_state()
        return self.state
