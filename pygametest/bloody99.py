import pygame, sys, os, math, random, time
from pygame.locals import *
sys.path.append("../")
from judge import Judge
from logger import Game, logger
from ab_agent import PlayerState
from action import Action

# http://blog.ez2learn.com/2008/11/28/play-pygame/
red = (200,0,0)
green = (0,200,0)
white = (255,255,255)
black = (0, 0, 0)
block_color = (53,115,255)
bright_green = (124,252,0)
bright_red = (170,1,20)

display_width = 500
display_height = 200

SCREEN_SIZE = (800, 600) 

clock = pygame.time.Clock()

cardImg = pygame.image.load('yuki_for_steam.bmp')
car_width = 73
#monkey_head_file_name = "yuki_for_steam.bmp"
#bg_file_name = "1227798240162.jpg"
#xd_file_name = "test.png"

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
    print(click)
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
            #j.printBoard()
            self.fill_background()
            self.resetCardPos()
            self.display_allPlayers()
            pygame.display.update()
            
            while not self.judge.isGameFinished():
                self.judge._possibleActions_ = self.judge.getAction()
                if len(self.judge._possibleActions_) == 0:
                    #print "%d is dead(cannot move). next one." % j.current_player
                    self.judge.setDead(self.judge.current_player)
                    self.judge.changeNextPlayer()
                    continue
                state = PlayerState(self.judge.history, self.judge._possibleActions_, self.judge.card[self.judge.current_player-1], len(self.judge.card[0]), len(self.judge.card[1]), len(self.judge.card[2]), len(self.judge.card[3]), len(self.judge.mountain), self.judge.point, self.judge.clock_wise, self.judge.small_h[self.judge.current_player-1]) #get playerstate
                
                if self.judge.player[self.judge.current_player-1].__class__.__name__ == "HumanAgent":
                    click = True
                    while click:
                        for event in pygame.event.get():
                            if event.type == QUIT:
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
                                    a.victim = self.chooseVictim(a)
                                    if self.judge.checkRule(a) == True and len(cards_used) != 0:
                                        click = False
                                        break
                                    else:
                                        continue
                else:                          
                    a = self.judge.player[self.judge.current_player-1].genmove(state)
                self.judge.doAction(a)                
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
            g = Game(i, self.judge.player, str(winner+1))
            log.logGame(g)
        '''x = (display_width * 0.45)
        y = (display_height * 0.8)

        x_change = 0
        gameExit = False

        while not gameExit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -5
                    if event.key == pygame.K_RIGHT:
                        x_change = 5
                if event.type == pygame.KEYUP:
                    x_change = 0
            x += x_change

            self.screen.fill(white)
            car(x,y)

            if x > display_width - car_width or x < 0:
                crash()'''

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
        time.sleep(1)
        self.display_player2()
        time.sleep(1)
        self.display_player3()
        time.sleep(1)
        self.display_player4()

    def display_player1(self):
        for x in range(0, len(self.judge.card[0])):
            self.window.blit(self.num_to_cards(self.judge.card[0][x]), (self.player_card_pos[x][0], self.player_card_pos[x][1]))

    def display_player2(self):
        for x in range(0, len(self.judge.card[1])):
            self.window.blit(self.Back_Card90, (self.p2_card_pos[x][0], self.p2_card_pos[x][1]))

    def display_player3(self):
        for x in range(0, len(self.judge.card[2])):
            self.window.blit(self.Back_Card, (self.p3_card_pos[x][0], self.p3_card_pos[x][1]))

    def display_player4(self):
        for x in range(0, len(self.judge.card[3])):
            self.window.blit(self.Back_Cardn90, (self.p4_card_pos[x][0], self.p4_card_pos[x][1]))

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
                        self.moveCard([0,-1], i)
                        self.card_clicked_list[i] = 1
                        break                
                elif self.card_clicked_list[i] == 1:
                    # cancel the choosed card
                    if self.player_card_y - self.click_move_y <= mousePos[1] < self.player_card_y - self.click_move_y + self.cardImg[0].get_height():
                        self.moveCard([0,1], i)
                        self.card_clicked_list[i] = 0
                        break

    def moveCard(self, dist, idx):
        oldy = self.player_card_pos[idx][1]
        while abs(self.player_card_pos[idx][1] - oldy) <= self.click_move_y:
            self.player_card_pos[idx][0] += dist[0]
            self.player_card_pos[idx][1] += dist[1]

        self.fill_background()
        self.display_player1()
        self.display_player2()
        self.display_player3()
        self.display_player4()
        self.display_desktop(self.prevCard)
        pygame.display.update()

    def chooseVictim(self, action):
        # TODO 5 7 9(!= user)  10 12 (-1 -2) click the button then set the action.victim to it.
        cardvalue = 0
        for card in action.cards_used:
            cardvalue += card
        cardvalue = 13 if cardvalue % 13 == 0 else cardvalue % 13
        if cardvalue == 5 or cardvalue == 7 or cardvalue == 9:
            button(self.screen, "East",self.p2_card_x, self.p2_card_y, 100, 50, green, bright_green, self.setVictim(2))
            button(self.screen, "North",self.p3_card_x, self.p3_card_y, 100, 50, green, bright_green, self.setVictim(3))
            button(self.screen, "West", self.p4_card_x, self.p4_card_y, 100, 50, green, bright_green, self.setVictim(4))
            pygame.display.update()
            return 2
        if cardvalue == 10 or cardvalue == 12:
            button(self.screen, "-"+str(cardvalue), SCREEN_SIZE[1]/3, SCREEN_SIZE[0]/2 , 100, 50, red, bright_red)
            button(self.screen, "+"+str(cardvalue), 2*SCREEN_SIZE[1]/3, SCREEN_SIZE[0]/2 , 100, 50, red, bright_red)
            return -1
        return 2

    def setVictim(self, victim):
        # TODO Is this useful?? doing it...
        return victim

    def doAction(self):
        # TODO
        pass

    def showCard(self):#show card after do anything
        # TODO
        pass

    def initGame(self):
        pygame.init()
        pygame.display.set_caption('Bloody99')

        self.window = pygame.display.set_mode((800, 600))
        self.screen = pygame.display.get_surface()
        self.loadImg()
        self.initPos()
        pos = (0, 0)
        self.screen.fill(white)

        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects("Game", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        self.screen.blit(TextSurf, TextRect)

        intro = True
        while intro:
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            # things need to update
            button(self.screen, "GO!",150,450,100,50,green,bright_green,self.runGame)
            button(self.screen, "Quit",550,450,100,50,red,bright_red,quitGame)
            pygame.display.update()
            clock.tick(15)

if __name__ == "__main__":
    game = Bloody99()
