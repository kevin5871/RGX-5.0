import pygame
from pygame.locals import *

pygame.init()

LOGO = pygame.image.load("assets/logo.png")
LOGO = pygame.transform.scale(LOGO, (400,400))
BACKGROUND = pygame.image.load("assets/MainBackground.jpg")