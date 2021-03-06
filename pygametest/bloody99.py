import pygame, sys, os, math, random
from pygame.locals import *
sys.path.append("../")
from judge import Judge
from logger import Game, logger
from ab_agent import PlayerState
from action import Action

# http://blog.ez2learn.com/2008/11/28/play-pygame/
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
white = (255,255,255)
black = (0, 0, 0)
block_color = (53,115,255)
bright_green = (124,252,0)
bright_red = (170,1,20)

display_width = 800
display_height = 600

SCREEN_SIZE = (788, 788) 

clock = pygame.time.Clock()

cardImg = pygame.image.load('yuki_for_steam.bmp')
car_width = 73

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(screen, text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    screen.blit(TextSurf, TextRect)


def button(screen, msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()         
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)

def quitGame():
    pygame.quit()
    quit()
    
class Bloody99:
    def __init__(self):
        self.judge = Judge() #need to pause it
        self.initGame()

    def loadImg(self):
        self.background_img_file = 'Image/Nostalgy.gif'
        self.beginning_bg_file = 'Image/AIposter.gif'
        self.cardImgFileName = list()
        self.cardImgFileName.append('Image/01s.gif')
        self.cardImgFileName.append('Image/02s.gif')
        self.cardImgFileName.append('Image/03s.gif')
        self.cardImgFileName.append('Image/04s.gif')
        self.cardImgFileName.append('Image/05s.gif')
        self.cardImgFileName.append('Image/06s.gif')
        self.cardImgFileName.append('Image/07s.gif')
        self.cardImgFileName.append('Image/08s.gif')
        self.cardImgFileName.append('Image/09s.gif')
        self.cardImgFileName.append('Image/10s.gif')
        self.cardImgFileName.append('Image/11s.gif')
        self.cardImgFileName.append('Image/12s.gif')
        self.cardImgFileName.append('Image/13s.gif')
        self.cardImgFileName.append('Image/01h.gif')
        self.cardImgFileName.append('Image/02h.gif')
        self.cardImgFileName.append('Image/03h.gif')
        self.cardImgFileName.append('Image/04h.gif')
        self.cardImgFileName.append('Image/05h.gif')
        self.cardImgFileName.append('Image/06h.gif')
        self.cardImgFileName.append('Image/07h.gif')
        self.cardImgFileName.append('Image/08h.gif')
        self.cardImgFileName.append('Image/09h.gif')
        self.cardImgFileName.append('Image/10h.gif')
        self.cardImgFileName.append('Image/11h.gif')
        self.cardImgFileName.append('Image/12h.gif')
        self.cardImgFileName.append('Image/13h.gif')
        self.cardImgFileName.append('Image/01d.gif')
        self.cardImgFileName.append('Image/02d.gif')
        self.cardImgFileName.append('Image/03d.gif')
        self.cardImgFileName.append('Image/04d.gif')
        self.cardImgFileName.append('Image/05d.gif')
        self.cardImgFileName.append('Image/06d.gif')
        self.cardImgFileName.append('Image/07d.gif')
        self.cardImgFileName.append('Image/08d.gif')
        self.cardImgFileName.append('Image/09d.gif')
        self.cardImgFileName.append('Image/10d.gif')
        self.cardImgFileName.append('Image/11d.gif')
        self.cardImgFileName.append('Image/12d.gif')
        self.cardImgFileName.append('Image/13d.gif')
        self.cardImgFileName.append('Image/01c.gif')
        self.cardImgFileName.append('Image/02c.gif')
        self.cardImgFileName.append('Image/03c.gif')
        self.cardImgFileName.append('Image/04c.gif')
        self.cardImgFileName.append('Image/05c.gif')
        self.cardImgFileName.append('Image/06c.gif')
        self.cardImgFileName.append('Image/07c.gif')
        self.cardImgFileName.append('Image/08c.gif')
        self.cardImgFileName.append('Image/09c.gif')
        self.cardImgFileName.append('Image/10c.gif')
        self.cardImgFileName.append('Image/11c.gif')
        self.cardImgFileName.append('Image/12c.gif')
        self.cardImgFileName.append('Image/13c.gif')
        self.iBack_Card = 'Image/back101.gif'
        # load the image
        self.background = pygame.image.load(self.background_img_file).convert()
        self.beginning_bg = pygame.image.load(self.beginning_bg_file).convert()
        self.cardImg = list()
        for i in range(0, len(self.cardImgFileName)):
            self.cardImg.append(pygame.image.load(self.cardImgFileName[i]).convert())
        self.Back_Card = pygame.image.load(self.iBack_Card).convert()
        self.Back_Card90 = pygame.transform.rotate(self.Back_Card , 90)
        self.Back_Cardn90 = pygame.transform.rotate(self.Back_Card , -90)

    def initPos(self):
        self.player_card_x = SCREEN_SIZE[0]/2 - self.Back_Card90.get_width() 
        self.player_card_y = SCREEN_SIZE[1] - self.cardImg[0].get_height()
        self.p2_card_x = SCREEN_SIZE[0] - self.Back_Card90.get_width() - 10
        self.p2_card_y = SCREEN_SIZE[1]/2 - self.cardImg[0].get_height()
        self.p3_card_x = SCREEN_SIZE[0]/2 - self.Back_Card90.get_width()
        self.p3_card_y = 10 
        self.p4_card_x = 10
        self.p4_card_y = SCREEN_SIZE[1]/2 - self.cardImg[0].get_height()
        self.click_move_x = self.cardImg[0].get_width()/6
        self.click_move_y = self.cardImg[0].get_height()/6

    def num_to_cards(self, num):
        return self.cardImg[num-1]

    def runGame(self):
        i = 1 
        self.prevCard = list()
        log = logger("bloody99.txt")
        self.fill_background()
        for k in range(i):
            pygame.display.update()
            self.judge = Judge()
            self.judge._possibleActions_ = list()
            self.judge.initBoard()
            self.judge.rand4Cards()
            self.fill_background()
            self.resetCardPos()
            if self.judge.isDead[0] == False:
                self.display_player1()
            elif self.judge.isDead[1] == False:
                self.display_player2()
            elif self.judge.isDead[2] == False:
                self.display_player3()
            elif self.judge.isDead[3] == False:
                self.display_player4()
            pygame.display.update()
            
            while not self.judge.isGameFinished():
                self.judge._possibleActions_ = self.judge.getAction()
                if len(self.judge._possibleActions_) == 0:
                    self.judge.setDead(self.judge.current_player)
                    self.judge.changeNextPlayer()
                    continue
                self.fill_background()
                self.resetCardPos()
                self.display_allPlayers()
                self.display_desktop(self.prevCard)
                pygame.display.update()
                state = PlayerState(self.judge.history, self.judge._possibleActions_, self.judge.card[self.judge.current_player-1], len(self.judge.card[0]), len(self.judge.card[1]), len(self.judge.card[2]), len(self.judge.card[3]), len(self.judge.mountain), self.judge.point, self.judge.clock_wise, self.judge.small_h[self.judge.current_player-1]) #get playerstate
                
                if self.judge.player[self.judge.current_player-1].__class__.__name__ == "HumanAgent":
                    click = True
                    while click:
                        for event in pygame.event.get():
                            if event.type == QUIT:
                                pygame.quit()
                                exit()
                            if event.type == MOUSEBUTTONDOWN:
                                if event.button == 1:
                                    self.clickCard(pygame.mouse.get_pos())
                                if event.button == 3:
                                    cards_used = []
                                    for cardIdx in range(len(self.card_clicked_list)):
                                        if self.card_clicked_list[cardIdx] == 1:
                                            cards_used.append(self.judge.card[self.judge.current_player-1][cardIdx])
                                    a = self.judge.player[self.judge.current_player-1].pygameGenmove(self.judge.current_player, cards_used)
                                    a.user = self.judge.current_player
                                    a.victim = self.chooseVictim(a)
                                    if self.judge.checkRule(a) == True and len(cards_used) > 0:
                                        click = False
                                        for v in a.cards_used:
                                            a.cardValue += 13 if (v % 13 == 0) else v % 13
                                        self.fill_background()
                                        self.resetCardPos()
                                        self.display_allPlayers()
                                        self.display_desktop(self.prevCard)
                                        pygame.display.update()       
                                        if a.cardValue == 9:
                                            self.exchangeCards(a.user, a.victim, a.cards_used)
                                            pygame.time.delay(300) 
                                        self.judge.doAction(a)                
                                        if a.cardValue == 7:
                                            self.pickOneCard(a.user, a.victim)
                                            pygame.time.delay(300) 
                                            self.getOneCard(a.user, a.victim)
                                            pygame.time.delay(300) 
                                        self.fill_background()
                                        self.resetCardPos()
                                        self.display_allPlayers()
                                        self.prevCard = a.cards_used
                                        self.display_desktop(self.prevCard)
                                        pygame.display.update()
                                        break
                                    elif self.judge.checkRule(a) == False and len(cards_used) > 0:
                                        font = pygame.font.Font(None, 40)
                                        text = font.render("ILLEGAL MOVE!!", 1, white)
                                        self.window.blit(text, (self.desk_mid_x*2/3+20, self.desk_mid_y-50))   
                                        pygame.display.update()
                                        continue
                                    else:
                                        self.fill_background()
                                        self.resetCardPos()
                                        self.display_allPlayers()
                                        self.display_desktop(self.prevCard)
                                        pygame.display.update()                                        
                                        continue
                else:                          
                    a = self.judge.player[self.judge.current_player-1].genmove(state)
                    for v in a.cards_used:
                        a.cardValue += 13 if (v % 13 == 0) else v % 13
                    self.fill_background()
                    self.resetCardPos()
                    self.display_allPlayers()
                    self.display_desktop(self.prevCard)
                    pygame.display.update()       
                    if a.cardValue == 9:
                        self.exchangeCards(a.user, a.victim, a.cards_used)
                        pygame.time.delay(300) 
                    self.judge.doAction(a)                
                    if a.cardValue == 7:
                        self.pickOneCard(a.user, a.victim)
                        pygame.time.delay(600) 
                        self.getOneCard(a.user, a.victim)
                        pygame.time.delay(600) 
                    else:
                        pygame.time.delay(1500) 
                    self.fill_background()
                    self.resetCardPos()
                    self.display_allPlayers()
                    self.prevCard = a.cards_used
                    self.display_desktop(self.prevCard)
                    pygame.display.update()
                
            winner = 0
            for i in range(4):
                if self.judge.isDead[i] == False:
                    winner = i
            if winner == 0:
                s = "South "
            elif winner == 1:
                s = "East "
            elif winner == 2:
                s = "North "
            else:
                s = "West "
            if self.judge.player[winner].__class__.__name__ == "HumanAgent":
                font = pygame.font.Font(None, 40)
                text = font.render("You Win!", 1, white)
                self.window.blit(text, (self.desk_mid_x - 20, self.desk_mid_y/2+50))   
                pygame.display.update()
            else:
                font = pygame.font.Font(None, 40)
                #text = font.render(s + ": " + self.judge.player[winner].__class__.__name__ + " is the WINNER!!", 1, white)
                text = font.render(s + "is the WINNER!!", 1, white)
                self.window.blit(text, (self.desk_mid_x*2/3-50, self.desk_mid_y/2+50))   
                pygame.display.update()
            g = Game(i, self.judge.player, str(winner+1))
            log.logGame(g)
        pygame.time.delay(2500) 
        self.screen.blit(self.beginning_bg, (0, 0))
        pygame.display.update()
        clock.tick(60)

    def fill_background(self):
        for y in range(0, SCREEN_SIZE[1], self.background.get_height()):
            for x in range(0, SCREEN_SIZE[0], self.background.get_width()):
                self.window.blit(self.background, (x, y))

    def resetCardPos(self):
        self.player_card_pos = [[0 for x in range(2)] for x in range(len(self.judge.card[0]))]
        for i in range(0, len(self.judge.card[0])):
            self.player_card_pos[i][0] = self.player_card_x + i*self.Back_Card.get_width()/2
            self.player_card_pos[i][1] = self.player_card_y 
        self.card_clicked_list = [0 for x in range(len(self.judge.card[0]))]        
        self.p2_card_pos = [[0 for x in range(2)] for x in range(len(self.judge.card[1]))]
        self.p3_card_pos = [[0 for x in range(2)] for x in range(len(self.judge.card[2]))]
        self.p4_card_pos = [[0 for x in range(2)] for x in range(len(self.judge.card[3]))]
        for i in range(0, len(self.judge.card[1])):
            self.p2_card_pos[i][0] = self.p2_card_x
            self.p2_card_pos[i][1] = self.p2_card_y + i*self.Back_Card90.get_height()/2
        for i in range(0, len(self.judge.card[2])):
            self.p3_card_pos[i][0] = self.p3_card_x + i*self.Back_Card.get_width()/2
            self.p3_card_pos[i][1] = self.p3_card_y
        for i in range(0, len(self.judge.card[3])):
            self.p4_card_pos[i][0] = self.p4_card_x
            self.p4_card_pos[i][1] = self.p4_card_y + i*self.Back_Cardn90.get_height()/2

    def display_allPlayers(self):
        self.display_player1()
        self.display_player2()
        self.display_player3()
        self.display_player4()

    def display_player1(self, skipIdx = list()):        
        if len(skipIdx) > 0:
            for x in range(0, len(self.judge.card[0])):
                skip = False
                for i in range(0, len(skipIdx)):
                    if skipIdx[i] != x:
                        continue
                    else:
                        skip = True
                        break
                if skip != True:
                    self.window.blit(self.num_to_cards(self.judge.card[0][x]), (self.player_card_pos[x][0], self.player_card_pos[x][1]))
        else:
            for x in range(0, len(self.judge.card[0])):
                self.window.blit(self.num_to_cards(self.judge.card[0][x]), (self.player_card_pos[x][0], self.player_card_pos[x][1]))
        font = pygame.font.Font(None, 30)
        if self.judge.current_player == 1:
            word = "South: " + self.judge.player[0].__class__.__name__ 
            text = font.render(word, 1, blue)
            self.window.blit(text, (self.player_card_x,self.player_card_y-50))

    def display_player2(self, skipIdx = list()):
        if len(skipIdx) > 0:
            for x in range(0, len(self.judge.card[1])):
                skip = False
                for i in range(0, len(skipIdx)):
                    if skipIdx[i] != x:
                        continue
                    else:
                        skip = True
                        break
                if skip != True:
                    self.window.blit(self.Back_Card90, (self.p2_card_pos[x][0], self.p2_card_pos[x][1]))
        else:
            for x in range(0, len(self.judge.card[1])):
                self.window.blit(self.Back_Card90, (self.p2_card_pos[x][0], self.p2_card_pos[x][1]))
        if self.judge.current_player == 2:
            font = pygame.font.Font(None, 30)
            #word = "East: " + self.judge.player[1].__class__.__name__ 
            word = "East" 
            text = font.render(word, 1, blue)
            self.window.blit(text, (self.p2_card_x-80, self.p2_card_y-50))

    def display_player3(self, skipIdx = list()):
        if len(skipIdx) > 0:
            for x in range(0, len(self.judge.card[2])):
                skip = False
                for i in range(0, len(skipIdx)):
                    if skipIdx[i] != x:
                        continue
                    else:
                        skip = True
                        break
                if skip != True:
                    self.window.blit(self.Back_Card, (self.p3_card_pos[x][0], self.p3_card_pos[x][1]))
        else:
            for x in range(0, len(self.judge.card[2])):
                self.window.blit(self.Back_Card, (self.p3_card_pos[x][0], self.p3_card_pos[x][1]))
        if self.judge.current_player == 3:
            font = pygame.font.Font(None, 30)
            #word = "North: " + self.judge.player[2].__class__.__name__ 
            word = "North" 
            text = font.render(word, 1, blue)
            self.window.blit(text, (self.p3_card_x, self.p3_card_y + self.Back_Card90.get_width()))

    def display_player4(self, skipIdx = list()):
        if len(skipIdx) > 0:
            for x in range(0, len(self.judge.card[3])):
                skip = False
                for i in range(0, len(skipIdx)):
                    if skipIdx[i] != x:
                        continue
                    else:
                        skip = True
                        break
                if skip != True:
                    self.window.blit(self.Back_Cardn90, (self.p4_card_pos[x][0], self.p4_card_pos[x][1]))
        else:
            for x in range(0, len(self.judge.card[3])):
                self.window.blit(self.Back_Cardn90, (self.p4_card_pos[x][0], self.p4_card_pos[x][1]))
        if self.judge.current_player == 4:
            font = pygame.font.Font(None, 30)
            #word = "West: " + self.judge.player[3].__class__.__name__ 
            word = "West" 
            text = font.render(word, 1, blue)
            self.window.blit(text, (self.p4_card_x, self.p4_card_y-50))

    def display_desktop(self, cards):
        self.desk_card_pos = [[0 for x in range(2)] for x in range(len(cards))]
        self.desk_mid_x = SCREEN_SIZE[0]/2 - len(cards)*self.cardImg[0].get_width()/2
        self.desk_mid_y = SCREEN_SIZE[1]/2 - self.cardImg[0].get_height()/2
        for i in range(0, len(cards)):
            self.desk_card_pos[i][0] = self.desk_mid_x + i*self.cardImg[0].get_width()
            self.desk_card_pos[i][1] = self.desk_mid_y
        for i in range(0, len(cards)):
            self.window.blit(self.num_to_cards(cards[i]), (self.desk_card_pos[i][0], self.desk_card_pos[i][1]))
        font = pygame.font.Font(None, 40)
        text = font.render("Point: " + str(self.judge.point), 1, white)
        self.window.blit(text, (SCREEN_SIZE[0]-150,10))
        
    def clickCard(self, mousePos):
        for i in range(0, len(self.judge.card[0])):
            if i == len(self.judge.card[0])-1:
                x = 1
            else:
                x = 0
            if self.player_card_x <= mousePos[0] < self.player_card_x + (i+1+x)*self.cardImg[0].get_width()/2:
                if self.card_clicked_list[i] == 0:
                    # choose the card
                    if self.player_card_y <= mousePos[1] < self.player_card_y + self.cardImg[0].get_height():
                        self.moveCard_player([0,-1], i)
                        self.card_clicked_list[i] = 1
                        break                
                elif self.card_clicked_list[i] == 1:
                    # cancel the choosed card
                    if self.player_card_y - self.click_move_y <= mousePos[1] < self.player_card_y - self.click_move_y + self.cardImg[0].get_height():
                        self.moveCard_player([0,1], i)
                        self.card_clicked_list[i] = 0
                        break

    def moveCard_player(self, dist, idx, skipIdx = list(), skipDuo = (-1,list())):
        oldy = self.player_card_pos[idx][1]
        while abs(self.player_card_pos[idx][1] - oldy) <= self.click_move_y:
            self.player_card_pos[idx][0] += dist[0]
            self.player_card_pos[idx][1] += dist[1]
            self.fill_background()
            self.display_player1(skipIdx)
            if skipDuo[0] == -1:
                self.display_player2()
                self.display_player3()
                self.display_player4()
            elif skipDuo[0] == 2:
                self.display_player2(skipDuo[1])
                self.display_player3()
                self.display_player4()
            elif skipDuo[0] == 3:
                self.display_player3(skipDuo[1])
                self.display_player2()
                self.display_player4()
            elif skipDuo[0] == 4:
                self.display_player4(skipDuo[1])
                self.display_player2()
                self.display_player3()
            self.display_desktop(self.prevCard)
            clock.tick(60)
            pygame.display.update()

    def moveCard_p2(self, dist, idx, skipIdx = list(), skipDuo = (-1,list())):
        oldx = self.p2_card_pos[idx][0]
        while abs(self.p2_card_pos[idx][0] - oldx) <= self.click_move_x:
            self.p2_card_pos[idx][0] += dist[0]
            self.p2_card_pos[idx][1] += dist[1]
            self.fill_background()
            self.display_player2(skipIdx)
            if skipDuo[0] == -1:
                self.display_player1()
                self.display_player3()
                self.display_player4()
            elif skipDuo[0] == 1:
                self.display_player1(skipDuo[1])
                self.display_player3()
                self.display_player4()
            elif skipDuo[0] == 3:
                self.display_player3(skipDuo[1])
                self.display_player1()
                self.display_player4()
            elif skipDuo[0] == 4:
                self.display_player4(skipDuo[1])
                self.display_player1()
                self.display_player3()
            self.display_desktop(self.prevCard)
            clock.tick(60)
            pygame.display.update()

    def moveCard_p3(self, dist, idx, skipIdx = list(), skipDuo = (-1,list())):
        oldy = self.p3_card_pos[idx][1]
        while abs(self.p3_card_pos[idx][1] - oldy) <= self.click_move_y:
            self.p3_card_pos[idx][0] += dist[0]
            self.p3_card_pos[idx][1] += dist[1]
            self.fill_background()
            self.display_player3(skipIdx)
            if skipDuo[0] == -1:
                self.display_player1()
                self.display_player2()
                self.display_player4()
            elif skipDuo[0] == 1:
                self.display_player1(skipDuo[1])
                self.display_player2()
                self.display_player4()
            elif skipDuo[0] == 2:
                self.display_player2(skipDuo[1])
                self.display_player1()
                self.display_player4()
            elif skipDuo[0] == 4:
                self.display_player4(skipDuo[1])
                self.display_player1()
                self.display_player2()
            self.display_desktop(self.prevCard)
            clock.tick(60)
            pygame.display.update()

    def moveCard_p4(self, dist, idx, skipIdx = list(), skipDuo = (-1,list())):
        oldx = self.p4_card_pos[idx][0]
        while abs(self.p4_card_pos[idx][0] - oldx) <= self.click_move_x:
            self.p4_card_pos[idx][0] += dist[0]
            self.p4_card_pos[idx][1] += dist[1]
            self.fill_background()
            self.display_player4(skipIdx)
            if skipDuo[0] == -1:
                self.display_player1()
                self.display_player2()
                self.display_player3()
            elif skipDuo[0] == 1:
                self.display_player1(skipDuo[1])
                self.display_player2()
                self.display_player3()
            elif skipDuo[0] == 2:
                self.display_player2(skipDuo[1])
                self.display_player1()
                self.display_player3()
            elif skipDuo[0] == 3:
                self.display_player3(skipDuo[1])
                self.display_player1()
                self.display_player2()
            self.display_desktop(self.prevCard)
            clock.tick(60)
            pygame.display.update()

    def chooseVictim(self, action):
        # 5 7 9(!= user)  10 12 (-1 -2) click the button then set the action.victim to it.
        cardvalue = 0
        for card in action.cards_used:
            if card % 13 != 0:
                cardvalue += card % 13
            else:
                cardvalue += 13
        if cardvalue > 13 or cardvalue < 1:
            return 0
        elif cardvalue == 5:
            w, h = 100, 50                        
            if self.judge.isDead[0] == False:
                button(self.screen, "South",self.player_card_x, self.player_card_y, w, h, green, bright_green)
            if self.judge.isDead[1] == False:
                button(self.screen, "East",self.p2_card_x, self.p2_card_y, w, h, green, bright_green)
            if self.judge.isDead[2] == False:
                button(self.screen, "North",self.p3_card_x, self.p3_card_y, w, h, green, bright_green)
            if self.judge.isDead[3] == False:
                button(self.screen, "West", self.p4_card_x, self.p4_card_y, w, h, green, bright_green)
            pygame.display.update()
            click = True
            while click:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = False
                            mousePos = pygame.mouse.get_pos()
                            if self.judge.isDead[0] == False and self.player_card_x < mousePos[0] < self.player_card_x + w and self.player_card_y < mousePos[1] < self.player_card_y + h:
                                victim = 1
                            elif self.judge.isDead[1] == False and self.p2_card_x < mousePos[0] < self.p2_card_x + w and self.p2_card_y < mousePos[1] < self.p2_card_y + h:
                                victim = 2
                            elif self.judge.isDead[2] == False and self.p3_card_x < mousePos[0] < self.p3_card_x + w and self.p3_card_y < mousePos[1] < self.p3_card_y + h:
                                victim = 3
                            elif self.judge.isDead[3] == False and self.p4_card_x < mousePos[0] < self.p4_card_x + w and self.p4_card_y < mousePos[1] < self.p4_card_y + h:
                                victim = 4
                            else:
                                click = True
            pygame.display.update()
            return victim
        elif cardvalue == 7 or cardvalue == 9:
            w, h = 100, 50            
            if self.judge.isDead[1] == False:
                button(self.screen, "East",self.p2_card_x, self.p2_card_y, w, h, green, bright_green)
            if self.judge.isDead[2] == False:
                button(self.screen, "North",self.p3_card_x, self.p3_card_y, w, h, green, bright_green)
            if self.judge.isDead[3] == False:
                button(self.screen, "West", self.p4_card_x, self.p4_card_y, w, h, green, bright_green)
            pygame.display.update()
            click = True
            while click:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = False
                            mousePos = pygame.mouse.get_pos()
                            if self.judge.isDead[1] == False and self.p2_card_x < mousePos[0] < self.p2_card_x + w and self.p2_card_y < mousePos[1] < self.p2_card_y + h:
                                victim = 2
                            elif self.judge.isDead[2] == False and self.p3_card_x < mousePos[0] < self.p3_card_x + w and self.p3_card_y < mousePos[1] < self.p3_card_y + h:
                                victim = 3
                            elif self.judge.isDead[3] == False and self.p4_card_x < mousePos[0] < self.p4_card_x + w and self.p4_card_y < mousePos[1] < self.p4_card_y + h:
                                victim = 4
                            else:
                                click = True
            pygame.display.update()
            return victim
        elif cardvalue == 10 or cardvalue == 12:
            w, h = 100, 50            
            value = 10 if cardvalue == 10 else 20
            button(self.screen, "+"+str(value), SCREEN_SIZE[0]/3-w/2, SCREEN_SIZE[1]/2 , w, h, green, bright_green)
            button(self.screen, "-"+str(value), 2*SCREEN_SIZE[0]/3-w/2, SCREEN_SIZE[1]/2 , w, h, green, bright_green)
            pygame.display.update()
            click = True
            while click:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = False
                            mousePos = pygame.mouse.get_pos()
                            if SCREEN_SIZE[0]/3-w/2 < mousePos[0] < SCREEN_SIZE[0]/3-w/2 + w and SCREEN_SIZE[1]/2 < mousePos[1] < SCREEN_SIZE[1]/2 + h:
                                victim = -1
                            elif 2*SCREEN_SIZE[0]/3-w/2 < mousePos[0] < 2*SCREEN_SIZE[0]/3-w/2 + w and SCREEN_SIZE[1]/2 < mousePos[1] < SCREEN_SIZE[1]/2 + h:
                                victim = -2
                            else:
                                click = True
            return victim
        if cardvalue == 10 or cardvalue == 12:
            button(self.screen, "-"+str(cardvalue), SCREEN_SIZE[1]/3, SCREEN_SIZE[0]/2 , 100, 50, green, bright_green)
            button(self.screen, "+"+str(cardvalue), 2*SCREEN_SIZE[1]/3, SCREEN_SIZE[0]/2 , 100, 50, green, bright_green)
            pygame.display.update()
            return -1

    def pickOneCard(self, userIdx, victim):
        i = self.judge.p
        if victim == 1:
            self.moveCard_player([0,-1], i, [], [userIdx, [len(self.judge.card[userIdx-1])-1]])
        elif victim == 2:
            self.moveCard_p2([-1,0], i, [], [userIdx, [len(self.judge.card[userIdx-1])-1]])
        elif victim == 3:
            self.moveCard_p3([0,1], i, [], [userIdx, [len(self.judge.card[userIdx-1])-1]])
        elif victim == 4:
            self.moveCard_p4([1,0], i, [], [userIdx, [len(self.judge.card[userIdx-1])-1]])

    def getOneCard(self, userIdx, victim):
        self.fill_background()
        self.resetCardPos()
        self.display_desktop(self.prevCard)
        if userIdx == 1:
            self.player_card_pos[len(self.judge.card[userIdx-1])-1][1] -= self.click_move_y * 3
            self.display_player1()
            self.display_player2()
            self.display_player3()
            self.display_player4()
            self.moveCard_player([0,1], len(self.judge.card[0])-1)
        elif userIdx == 2:
            self.p2_card_pos[len(self.judge.card[userIdx-1])-1][0] -= self.click_move_x * 3
            self.display_player1()
            self.display_player2()
            self.display_player3()
            self.display_player4()
            self.moveCard_p2([1,0], len(self.judge.card[1])-1)
        elif userIdx == 3:
            self.p3_card_pos[len(self.judge.card[userIdx-1])-1][1] += self.click_move_x * 3
            self.display_player1()
            self.display_player2()
            self.display_player3()
            self.display_player4()
            self.moveCard_p3([0,-1], len(self.judge.card[2])-1)
        elif userIdx == 4:
            self.p4_card_pos[len(self.judge.card[userIdx-1])-1][0] += self.click_move_x * 3
            self.display_player1()
            self.display_player2()
            self.display_player3()
            self.display_player4()
            self.moveCard_p4([-1,0], len(self.judge.card[3])-1)
        pygame.display.update()
    
    def exchangeCards(self, userIdx, victim, cards_used):
        self.fill_background()
        self.prevCard = cards_used
        userSkipCard = list()
        for x in range(0, len(self.judge.card[userIdx-1])):
            for y in range(0, len(cards_used)):
                if self.judge.card[userIdx-1][x] == cards_used[y]:
                    userSkipCard.append(x)
        self.resetCardPos()
        self.display_desktop(self.prevCard)
        if userIdx == 1:
            for i in range(0, len(self.judge.card[userIdx-1])):
                self.moveCard_player([0,-1], i, userSkipCard)
        elif userIdx == 2:
            for i in range(0, len(self.judge.card[userIdx-1])):
                self.moveCard_p2([-1,0], i, userSkipCard)
        elif userIdx == 3:
            for i in range(0, len(self.judge.card[userIdx-1])):
                self.moveCard_p3([0,1], i, userSkipCard)
        elif userIdx == 4:
            for i in range(0, len(self.judge.card[userIdx-1])):
                self.moveCard_p4([1,0], i, userSkipCard)
        if victim == 1:
            for i in range(0, len(self.judge.card[victim-1])):
                self.moveCard_player([0,-1], i, [], [userIdx, userSkipCard])
        elif victim == 2:
            for i in range(0, len(self.judge.card[victim-1])):
                self.moveCard_p2([-1,0], i, [], [userIdx, userSkipCard])
        elif victim == 3:
            for i in range(0, len(self.judge.card[victim-1])):
                self.moveCard_p3([0,1], i, [], [userIdx, userSkipCard])
        elif victim == 4:
            for i in range(0, len(self.judge.card[victim-1])):
                self.moveCard_p4([1,0], i, [], [userIdx, userSkipCard])
        pygame.display.update()       

    def initGame(self):
        pygame.init()
        pygame.display.set_caption('Bloody99')

        self.window = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]))
        self.screen = pygame.display.get_surface()
        self.loadImg()
        self.initPos()
        pos = (0, 0)
        self.screen.blit(self.beginning_bg, (0, 0))

        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            # things need to update
            button(self.screen, "START!",100,400,200,50,green,bright_green,self.runGame)
            button(self.screen, "QUIT",100,500,200,50,red,bright_red,quitGame)
            pygame.display.update()
            clock.tick(15)

if __name__ == "__main__":
    game = Bloody99()
