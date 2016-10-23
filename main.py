import pygame, sys, os
from pong import driver
from pong import disp_title_screen

#Set basepath
basepath = os.path.dirname(os.path.realpath(__file__))+os.path.sep
os.chdir(basepath)

#Initialize pygame
pygame.init()
pygame.mixer.init()
pygame.font.init()

#Set screen information
size = width, height = 1440, 900

#Set screen
screen = pygame.display.set_mode(size)

#Play or quit
while 1:
	play_or_quit = disp_title_screen(screen, width, height)
	if play_or_quit:
		driver(basepath, screen, width, height)
	else:
		sys.exit()