import pygame
import random

pygame.init()
 
screen = pygame.display.set_mode([854,480])
screen.fill([255,255,255])
 
mainloop = True
xy = (0, 0)

fontsize = 35
color = (32, 32, 32)
myFont = pygame.font.SysFont("None", fontsize)
    
delta = 1
fps = 30
 
Clock = pygame.time.Clock()
 
while mainloop:
    tickFPS = Clock.tick(fps)
    pygame.display.set_caption("Press Esc to quit. Location: %.2f, %.2f, FPS: %.2f" % (xy[0], xy[1], Clock.get_fps()))
    
    
    screen.fill((255,255,255))
    screen.blit(myFont.render("I love pygame!", 0, (color)), (xy[0],xy[1]))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mainloop = False 
    pygame.display.update()
 
pygame.quit() 
