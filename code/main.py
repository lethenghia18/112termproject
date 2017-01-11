#Run this file to play game

import pygame
from objects import *
import random
from pygamegame import PygameGame
from camera import *
from level import *
from slenderman_level import *
from game import *

class Main(PygameGame):
    def init(self): 
        self.mode = "Main Menu"
        pygame.mixer.music.load('music/Intro.wav')
        pygame.mixer.music.play(-1)
        self.text = [ "The mysterious Jay Kotsby and the lovely Daisy BuStehlik", 
                        "are madly in love. But oh no! Daisy is kidnapped and",
                        "trapped in the 3-story Slender Mansion by the evil Slenderman",
                        "and his servants! Can you help Jay Kotsby find the love",
                        "of his life?",
                        "",
                        "Use arrow keys to move left and right. Up arrow to jump.",
                        "Space to attack by throwing hat.",
                        "",
                        "Press Enter to begin Kotsby's journey, or B to go Back",
                        "to Main Menu. Good luck, old sport!"
                    ]

    def mousePressed(self, x, y): pass

    def keyPressed(self, keyCode, mod): 
        if keyCode == pygame.K_RETURN:
            Game.init(self)
            Game(600,432).run()
        elif keyCode == pygame.K_i: 
            self.mode = "Help"
        elif keyCode == pygame.K_b:
            self.mode = "Main Menu"

    def timerFired(self, dt): pass

    def drawMenu(self, screen):
        background = pygame.transform.scale(pygame.image.load("images/opening.png").convert_alpha(), (600,432))
        font = pygame.font.Font(None, 36)
        playText = font.render("Press Enter to Play!", False, (255,255,255))
        helpText = font.render("Press I for Instructions (Please Read!)", False, (255,255,255))
        playPos = playText.get_rect()
        playPos.centerx = background.get_rect().centerx 
        playPos.centery = background.get_rect().centery + 50
        helpPos = helpText.get_rect()
        helpPos.centerx = background.get_rect().centerx 
        helpPos.centery = background.get_rect().centery 
        background.blit(playText, playPos)
        background.blit(helpText, helpPos)
        screen.blit(background, (0, 0))

    def drawHelp(self, screen): 
        background1 = pygame.transform.scale(pygame.image.load("images/opening.png").convert_alpha(), (600,432))
        image = pygame.image.load("images/Kosby.png").convert_alpha()
        background2 = pygame.Surface((500,332))
        background2.fill((0,0,0))
        font = pygame.font.Font("Adobe Caslon Pro.ttf", 20)
        for i in range(len(self.text)):
            text = font.render(self.text[i], False, (255,255,255))
            textPos = text.get_rect()
            textPos.left = background2.get_rect().centerx - 245
            textPos.centery = 20 + 20*i
            background2.blit(text, textPos)
        background2.blit(image, (background2.get_rect().centerx-10, 250))
        background1.blit(background2, (50, 50))
        screen.blit(background1, (0, 0))

    def redrawAll(self, screen): 
        if self.mode == "Main Menu": 
            self.drawMenu(screen)
        elif self.mode == "Help":
            self.drawHelp(screen)
            

Main(600,432).run()
