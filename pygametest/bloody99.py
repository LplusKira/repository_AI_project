import pygame, sys, os, math, random, sys
from pygame.locals import *
sys.path.append("../")
from judge import Judge
from logger import Game, logger

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

    def runGame(self):
                
        i = 1 # no iterate? # i dont know
        log = logger("bloody99.txt")
        for k in range(i):
            j = Judge()
            players, winner = j.GameStart()
            g = Game(i, players, winner)
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

    def doAction(self):
        pass

    def showCard(self):#show card after do anything
        pass
        
    def initGame(self):
        pygame.init()
        pygame.display.set_caption('Bloody99')

        self.window = pygame.display.set_mode((800, 600))
        self.screen = pygame.display.get_surface()
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
