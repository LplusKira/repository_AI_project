class Game:
   def __init__(self, i, pl, win):
      self.idx = i
      self.players = list()
      for p in pl:
         self.players.append(p.__class__.__name__)
      self.winner = win

   def __str__(self):
      s = "Game Round:" + str(self.idx) + "\n"
      i = 1
      for p in self.players:
         s = s + "Player" + str(i) + ":" + str(p) + "\n"
         i = i + 1
      s = s + "Winner: " + str(self.winner) + "\n"
      return s

class logger:
   def __init__(self):
      self.games = list()

   def logGame(self, g):
      self.games.append(g)

   def __str__(self):
      s = "\nThe result is log below:\n"
      for g in self.games:
         s = s + str(g)
      return s
