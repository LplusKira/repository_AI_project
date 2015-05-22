import player

class Agent:
   """
   The base agent class, every agent must define the getAction function.
   """
   def __init__(self, index = 0, cards = list()):
      self.index = index
      self.cards = cards
   
   def getAction(self, state):
      """
      other agents should implement their heuristic to getAction
      """
      pass


class State:
   """
   The state of the game which the judge will transmit to the player.
   """
   def __init__(self, history, leg, illeg, cardCount1, cardCount2, cardCount3, cardCount4, mountCount, point, order):
      self.history = player.Intvector()
#      self.leg = player.Intvector()
#      self.illeg = player.Intvector()
#      self.history = list()
      self.leg = list()
      self.illeg = list()
      self.history = history
      self.leg = leg
      self.illeg = illeg
      self.cardCount1 = cardCount1
      self.cardCount2 = cardCount2
      self.cardCount3 = cardCount3
      self.cardCount4 = cardCount4
      self.mountCount = mountCount
      self.point = point
      self.order = order


class Action:
   """
   The action which the player will return to the judge.
   """
   def __init__(self, index, cards, act):
      self.index = index
      self.cards = list()
#      self.cards = player.Intvector()
      self.cards = cards
      self.act = act
      

class SimpleAgent(Agent):
   """
   Randomly decide which action to take
   """
   def __init__(self, index = 0, cards = list()):
      self.index = index
      self.cards = cards
      print "Constructing Simple Agent, id = ", self.index, "cards = ", self.cards

   def getAction(self, state):
      import random
      legalcards = state.leg
      cardIdx = random.randint(0, len(state.leg)-1)
      cards = [state.leg[cardIdx]]
      target = self.index
      act = self.getAct(cards, target)
      action = Action(self.index, cards, act)
      return action

   def getAct(self, cards, target):
      cardpoint = sum(cards)
#      if cardpoint == 5 or cardpoint == 7 or cardpoint == 9:
#         target = random.choice(



class HumanAgent(Agent):
   """
   The human agent, action decided by human.
   """
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
   """
   just for test
   """
   idx = 1
   cards1 = [4, 5, 13, 16, 24]
   cards2 = [2, 7, 9, 18, 27]
   agent = SimpleAgent(idx, cards1)
   p = HumanAgent(idx+1, cards2)
   his = player.Intvector()
   his.push_back(1)
   his.push_back(2)
   state = State(his, [4, 5, 13], [16,24], 3, 4, 0, 2, 33, 99, 1)
   state2 = State(his, [7, 9, 18, 27], [2], 3, 4, 0, 2, 33, 99, 1)
   act = agent.getAction(state)
   print "Simple agent's action ", act.act
#   print act.index
   print "Simple agent picks the card:", act.cards
   act2 = p.getAction(state2)
   print "Human player's action ", act2.act
#   print act2.index
   print "Human player picks the card", act2.cards
