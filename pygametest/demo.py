import pygame, sys, os, math
from pygame.locals import * 
 
pygame.init() 
 
window = pygame.display.set_mode((800, 600)) 
pygame.display.set_caption('Demo') 
screen = pygame.display.get_surface() 

monkey_head_file_name = "yuki_for_steam.bmp"
bg_file_name = "1227798240162.jpg"
xd_file_name = "test.png"

monkey_surface = pygame.image.load(monkey_head_file_name).convert_alpha()
bg_surface = pygame.image.load(bg_file_name).convert_alpha()
xd_surface = pygame.image.load(xd_file_name).convert_alpha()

pos = (0, 0)
screen.fill((0, 0, 0))
screen.blit(bg_surface, (0, 0)) 
screen.blit(monkey_surface, pos) 
pygame.display.flip()

angle = 0.0
runningFlag = True

def getDeltaPost(surface, angle, rotated):
    angle %= 360
    if angle > 0 and angle < 90:
        y = -math.sin(math.radians(angle)) * surface.get_width()
        x = 0
    elif angle >= 90 and angle < 180:
        x = math.cos(math.radians(angle)) * surface.get_width()
        y = -rotated.get_height()
    elif angle >= 180 and angle < 270:
        x = -rotated.get_width()
        y = -rotated.get_height() - (math.sin(math.radians(angle)) * surface.get_width())
    elif angle >= 270:
        y = 0
        x = -rotated.get_width() + (math.cos(math.radians(angle)) * surface.get_width())
    else:
        x = 0
        y = 0
    return x, y
 
def input(events):
   global pos, angle, runningFlag
   for event in events: 
      if event.type == QUIT: 
         runningFlag = False
      elif event.type == MOUSEMOTION:
         pos = event.pos
      else: 
         print event

   screen.fill((0, 0, 0))
   screen.blit(bg_surface, (0, 0)) 
   screen.blit(monkey_surface, pos, None)

   r = pygame.transform.rotozoom(monkey_surface, angle, 1)
   x, y = getDeltaPost(monkey_surface, angle, r)
   px, py = pos
   screen.blit(r, (px + x, py + y))

   r = pygame.transform.rotozoom(xd_surface, angle + 60, 1)
   x, y = getDeltaPost(xd_surface, angle + 60, r)
   px, py = pos
   screen.blit(r, (px + x, py + y))
   
   pygame.display.flip()

   angle += 1
 
while runningFlag: 
   input(pygame.event.get())

pygame.quit()
