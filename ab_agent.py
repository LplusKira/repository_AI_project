class Agent:
   def __init__(self, index = 0, cards = list()):
      self.index = index
      self.cards = cards
   
   def genMove(self, state):
      pass

class State:
   def __init__(self, history, leg, illeg, cardCount1, cardCount2, cardCount3, cardCount4, mountCount, point, order):
#      self.history = player.Intvector()
#      self.leg = player.Intvector()
#      self.illeg = player.Intvector()
      self.history = history
      self.myCard = MyCard(leg, card)# non exist
      self.cardNum = list()
      self.cardNum.append(cardNum1)
      self.cardNum.append(cardNum2)
      self.cardNum.append(cardNum3)
      self.cardNum.append(cardNum4)
      self.restNum = mountNum
      self.board.nowpoint = point
      self.board.order = order

   def print_state(self):
      print self.myCard.moves

class MyCard:
   def __init__(self, moves, cards):
      self.moves = moves
      self.cards = cards
      
class Action:
   def __init__(self, index, cards, act):
      self.index = index
      self.cards = list()
#      self.cards = player.Intvector()
      self.cards = cards
      self.act = act
      
class ScoutAgent(Agent):
   def __init__(self, i = 0, cards = list()):
      self.i = i
      self.cards = cards
      print "Constructing Simple Agent, player id = ", self.i, "cards = ", self.cards

   def genMove(self, state):
      import random
      legalcards = state.leg
      cardIdx = random.randint(0, len(state.leg)-1)
      cards = [state.leg[cardIdx]]
      target = self.i
      act = self.getAct(cards, target)
      action = Action(self.i, cards, act)
      return action

class HumanAgent(Agent):
   def __init__(self, index = 0, cards = list()):
      self.index = index
      self.cards = cards
      print "Constructing Human Agent, id = ", self.index, "cards = ", self.cards

   def getAction(self, state):
      print "The card you have: ", state.leg, state.illeg
      cards = raw_input("pick the card: ")
      act = 0
      action = Action(self.index, cards, act)
      return action

if __name__ == "__main__":
   idx = 1
   cards1 = [4, 5, 13, 16, 24]
   cards2 = [2, 7, 9, 18, 27]
   agent = ScoutAgent(idx, cards1)
   p = HumanAgent(idx+1, cards2)
   #his = player.Intvector()
   #his.push_back(1)
   #his.push_back(2)
   his = [1,2]
   state = State(his, [4, 5, 13], [16,24], 3, 4, 0, 2, 33, 99, 1)
   state2 = State(his, [7, 9, 18, 27], [2], 3, 4, 0, 2, 33, 99, 1)
   act = agent.genMove(state)
   print "Simple agent's action ", act.act
#   print act.index
   print "Simple agent picks the card:", act.cards
   act2 = p.genMove(state2)
   print "Human player's action ", act2.act
#   print act2.index
   print "Human player picks the card", act2.cards
