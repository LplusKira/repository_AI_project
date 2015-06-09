import pygame, sys, os, math, random, sys
from pygame.locals import *
sys.path.append("../")
from judge import Judge
from logger import Game, logger
from ab_agent import PlayerState

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
        self.iP_1c = 'Image/01c.gif'
        self.iP_1d = 'Image/01d.gif'
        self.iP_1h = 'Image/01h.gif'
        self.iP_1s = 'Image/01s.gif'
        self.iP_2c = 'Image/02c.gif'
        self.iP_2d = 'Image/02d.gif'
        self.iP_2h = 'Image/02h.gif'
        self.iP_2s = 'Image/02s.gif'
        self.iP_3c = 'Image/03c.gif'
        self.iP_3d = 'Image/03d.gif'
        self.iP_3h = 'Image/03h.gif'
        self.iP_3s = 'Image/03s.gif'
        self.iP_4c = 'Image/04c.gif'
        self.iP_4d = 'Image/04d.gif'
        self.iP_4h = 'Image/04h.gif'
        self.iP_4s = 'Image/04s.gif'
        self.iP_5c = 'Image/05c.gif'
        self.iP_5d = 'Image/05d.gif'
        self.iP_5h = 'Image/05h.gif'
        self.iP_5s = 'Image/05s.gif'
        self.iP_6c = 'Image/06c.gif'
        self.iP_6d = 'Image/06d.gif'
        self.iP_6h = 'Image/06h.gif'
        self.iP_6s = 'Image/06s.gif'
        self.iP_7c = 'Image/07c.gif'
        self.iP_7d = 'Image/07d.gif'
        self.iP_7h = 'Image/07h.gif'
        self.iP_7s = 'Image/07s.gif'
        self.iP_8c = 'Image/08c.gif'
        self.iP_8d = 'Image/08d.gif'
        self.iP_8h = 'Image/08h.gif'
        self.iP_8s = 'Image/08s.gif'
        self.iP_9c = 'Image/09c.gif'
        self.iP_9d = 'Image/09d.gif'
        self.iP_9h = 'Image/09h.gif'
        self.iP_9s = 'Image/09s.gif'
        self.iP_10c = 'Image/10c.gif'
        self.iP_10d = 'Image/10d.gif'
        self.iP_10h = 'Image/10h.gif'
        self.iP_10s = 'Image/10s.gif'
        self.iP_11c = 'Image/11c.gif'
        self.iP_11d = 'Image/11d.gif'
        self.iP_11h = 'Image/11h.gif'
        self.iP_11s = 'Image/11s.gif'
        self.iP_12c = 'Image/12c.gif'
        self.iP_12d = 'Image/12d.gif'
        self.iP_12h = 'Image/12h.gif'
        self.iP_12s = 'Image/12s.gif'
        self.iP_13c = 'Image/13c.gif'
        self.iP_13d = 'Image/13d.gif'
        self.iP_13h = 'Image/13h.gif'
        self.iP_13s = 'Image/13s.gif'
        self.iP_pass = 'Image/pass.jpg'
        self.iBack_Card = 'Image/back101.gif'
        # load the image
        self.background = pygame.image.load(self.background_img_file).convert()
        self.P_1c = pygame.image.load(self.iP_1c).convert()
        self.P_1d = pygame.image.load(self.iP_1d).convert()
        self.P_1h = pygame.image.load(self.iP_1h).convert()
        self.P_1s = pygame.image.load(self.iP_1s).convert()
        self.P_2c = pygame.image.load(self.iP_2c).convert()
        self.P_2d = pygame.image.load(self.iP_2d).convert()
        self.P_2h = pygame.image.load(self.iP_2h).convert()
        self.P_2s = pygame.image.load(self.iP_2s).convert()
        self.P_3c = pygame.image.load(self.iP_3c).convert()
        self.P_3d = pygame.image.load(self.iP_3d).convert()
        self.P_3h = pygame.image.load(self.iP_3h).convert()
        self.P_3s = pygame.image.load(self.iP_3s).convert()
        self.P_4c = pygame.image.load(self.iP_4c).convert()
        self.P_4d = pygame.image.load(self.iP_4d).convert()
        self.P_4h = pygame.image.load(self.iP_4h).convert()
        self.P_4s = pygame.image.load(self.iP_4s).convert()
        self.P_5c = pygame.image.load(self.iP_5c).convert()
        self.P_5d = pygame.image.load(self.iP_5d).convert()
        self.P_5h = pygame.image.load(self.iP_5h).convert()
        self.P_5s = pygame.image.load(self.iP_5s).convert()
        self.P_6c = pygame.image.load(self.iP_6c).convert()
        self.P_6d = pygame.image.load(self.iP_6d).convert()
        self.P_6h = pygame.image.load(self.iP_6h).convert()
        self.P_6s = pygame.image.load(self.iP_6s).convert()
        self.P_7c = pygame.image.load(self.iP_7c).convert()
        self.P_7d = pygame.image.load(self.iP_7d).convert()
        self.P_7h = pygame.image.load(self.iP_7h).convert()
        self.P_7s = pygame.image.load(self.iP_7s).convert()
        self.P_8c = pygame.image.load(self.iP_8c).convert()
        self.P_8d = pygame.image.load(self.iP_8d).convert()
        self.P_8h = pygame.image.load(self.iP_8h).convert()
        self.P_8s = pygame.image.load(self.iP_8s).convert()
        self.P_9c = pygame.image.load(self.iP_9c).convert()
        self.P_9d = pygame.image.load(self.iP_9d).convert()
        self.P_9h = pygame.image.load(self.iP_9h).convert()
        self.P_9s = pygame.image.load(self.iP_9s).convert()
        self.P_10c = pygame.image.load(self.iP_10c).convert()
        self.P_10d = pygame.image.load(self.iP_10d).convert()
        self.P_10h = pygame.image.load(self.iP_10h).convert()
        self.P_10s = pygame.image.load(self.iP_10s).convert()
        self.P_11c = pygame.image.load(self.iP_11c).convert()
        self.P_11d = pygame.image.load(self.iP_11d).convert()
        self.P_11h = pygame.image.load(self.iP_11h).convert()
        self.P_11s = pygame.image.load(self.iP_11s).convert() 
        self.P_12c = pygame.image.load(self.iP_12c).convert()
        self.P_12d = pygame.image.load(self.iP_12d).convert()
        self.P_12h = pygame.image.load(self.iP_12h).convert()
        self.P_12s = pygame.image.load(self.iP_12s).convert() 
        self.P_13c = pygame.image.load(self.iP_13c).convert()
        self.P_13d = pygame.image.load(self.iP_13d).convert()
        self.P_13h = pygame.image.load(self.iP_13h).convert()
        self.P_13s = pygame.image.load(self.iP_13s).convert() 
        self.Back_Card = pygame.image.load(self.iBack_Card).convert()
        self.Back_Card90 = pygame.transform.rotate(self.Back_Card , 90)
        self.Back_Cardn90 = pygame.transform.rotate(self.Back_Card , -90)

    def num_to_cards(self, num):
        if 0==num:
            return self.P_1c
        if 1==num:
            return self.P_1d
        if 2==num:
            return self.P_1h
        if 3==num:
            return self.P_1s
        if 4==num:
            return self.P_2c
        if 5==num:
            return self.P_2d 
        if 6==num:
            return self.P_2h
        if 7==num:
            return self.P_2s
        if 8==num:
            return self.P_3c
        if 9==num:
            return self.P_3d
        if 10==num:
            return self.P_3h
        if 11==num:
            return self.P_3s
        if 12==num:
            return self.P_4c
        if 13==num:
            return self.P_4d
        if 14==num:
            return self.P_4h
        if 15==num:
            return self.P_4s
        if 16==num:
            return self.P_5c
        if 17==num:
            return self.P_5d
        if 18==num:
            return self.P_5h
        if 19==num:
            return self.P_5s
        if 20==num:
            return self.P_6c
        if 21==num:
            return self.P_6d
        if 22==num:
            return self.P_6h
        if 23==num:
            return self.P_6s
        if 24==num:
            return self.P_7c
        if 25==num:
            return self.P_7d
        if 26==num:
            return self.P_7h
        if 27==num:
            return self.P_7s
        if 28==num:
            return self.P_8c
        if 29==num:
            return self.P_8d
        if 30==num:
            return self.P_8h
        if 31==num:
            return self.P_8s
        if 32==num:
            return self.P_9c
        if 33==num:
            return self.P_9d
        if 34==num:
            return self.P_9h
        if 35==num:
            return self.P_9s
        if 36==num:
            return self.P_10c
        if 37==num:
            return self.P_10d
        if 38==num:
            return self.P_10h
        if 39==num:
            return self.P_10s
        if 40==num:
            return self.P_11c
        if 41==num:
            return self.P_11d
        if 42==num:
            return self.P_11h
        if 43==num:
            return self.P_11s
        if 44==num:
            return self.P_12c
        if 45==num:
            return self.P_12d
        if 46==num:
            return self.P_12h
        if 47==num:
            return self.P_12s
        if 48==num:
            return self.P_13c
        if 49==num:
            return self.P_13d
        if 50==num:
            return self.P_13h
        if 51==num:
            return self.P_13s


    def runGame(self):
                
        i = 1 
        log = logger("bloody99.txt")
        self.fill_background()
        for k in range(i):
            pygame.display.update()
            j = Judge()
            j._possibleActions_ = list()
            j.initBoard()
            j.rand4Cards()
            #j.printBoard()
            self.display_initBoard(j)
            pygame.display.update()
            
            while not j.isGameFinished():
                j._possibleActions_ = j.getAction()
                if len(j._possibleActions_) == 0:
                    #print "%d is dead(cannot move). next one." % j.current_player
                    j.setDead(j.current_player)
                    j.changeNextPlayer()
                    continue
                state = PlayerState(j.history, j._possibleActions_, j.card[j.current_player-1], len(j.card[0]), len(j.card[1]), len(j.card[2]), len(j.card[3]), len(j.mountain), j.point, j.clock_wise) #get playerstate
                a = j.player[j.current_player-1].genmove(state)
                j.doAction(a)                
#                self.display_all(j)
                pygame.display.update()
                

            winner = 0
            for i in range(4):
                if j.isDead[i] == False:
                    winner = i
            g = Game(i, j.player, str(winner+1))
            log.logGame(g)
        print log
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

    def display_initBoard(self, judge):
        # TODO
        self.player_card_loc = [[0,0], [0,0], [0,0], [0,0], [0,0]]
        self.p2_card_loc = [[0,0], [0,0], [0,0], [0,0], [0,0]]
        self.p3_card_loc = [[0,0], [0,0], [0,0], [0,0], [0,0]]
        self.p4_card_loc = [[0,0], [0,0], [0,0], [0,0], [0,0]]
        self.player_card_x = SCREEN_SIZE[0]/2 - self.Back_Card90.get_width() 
        self.player_card_y = SCREEN_SIZE[1] - self.P_1c.get_height()
        self.p2_card_x = SCREEN_SIZE[0] - self.Back_Card90.get_width() - 10
        self.p2_card_y = SCREEN_SIZE[1]/2 - self.P_1c.get_height()
        self.p3_card_x = SCREEN_SIZE[0]/2 - self.Back_Card90.get_width()
        self.p3_card_y = 10 
        self.p4_card_x = 10
        self.p4_card_y = SCREEN_SIZE[1]/2 - self.P_1c.get_height()
        for i in range(0, 5):
            self.player_card_loc[i][0] = self.player_card_x + i*self.Back_Card.get_width()/2
            self.player_card_loc[i][1] = self.player_card_y 
            self.p2_card_loc[i][0] = self.p2_card_x
            self.p2_card_loc[i][1] = self.p2_card_y + i*self.Back_Card90.get_height()/2
            self.p3_card_loc[i][0] = self.p3_card_x + i*self.Back_Card.get_width()/2
            self.p3_card_loc[i][1] = self.p3_card_y
            self.p4_card_loc[i][0] = self.p4_card_x
            self.p4_card_loc[i][1] = self.p4_card_y + i*self.Back_Cardn90.get_height()/2

        for x in range(0, len(judge.card[0])):
            self.window.blit(self.num_to_cards(judge.card[0][x]), (self.player_card_loc[x][0], self.player_card_loc[x][1]))

        for x in range(0, len(judge.card[1])):
            self.window.blit(self.Back_Card90, (self.p2_card_loc[x][0], self.p2_card_loc[x][1]))

        for x in range(0, len(judge.card[2])):
            self.window.blit(self.Back_Card, (self.p3_card_loc[x][0], self.p3_card_loc[x][1]))

        for x in range(0, len(judge.card[3])):
            self.window.blit(self.Back_Cardn90, (self.p4_card_loc[x][0], self.p4_card_loc[x][1]))

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
