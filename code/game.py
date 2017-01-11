#Run this file to play game

import pygame
from objects import *
import random
from pygamegame import PygameGame
from camera import *
from level import *
from slenderman_level import *
#in this world, width is 3000, and height is 432
class Game(PygameGame):
    def init(self): 
        self.worldWidth = 3000
        self.floor = 28
        Player.init()
        player1 = Player(100, self.height-3*self.floor)
        self.player1 = pygame.sprite.Group(player1)
        self.level1 = Level1(player1, self.worldWidth, self.width, self.height)
        self.level2 = Level2(player1, self.worldWidth, self.width, self.height)
        self.level3 = Level3(player1, self.worldWidth, self.width, self.height)
        player2 = Player(100, self.height-3*self.floor) 
        #just work better with 2 people. Not the best, but couldn't really figure out why (or didn't have time)
        self.player2 = pygame.sprite.Group(player2)
        self.slendermanLevel1 = SlendermanLevel1(player2, self.worldWidth, self.width, self.height)
        self.slendermanLevel2 = SlendermanLevel2(player2, self.worldWidth, self.width, self.height)
        self.slendermanLevel3 = SlendermanLevel3(player2, self.worldWidth, self.width, self.height)
        self.level = 1 #keep track of level
        self.frame = 0
        self.inBetweenLevels = True
        self.startTime = 0
        self.timeOn = False
        self.meetPrincess = False
        pygame.mixer.music.load('music/Level1n2.wav')
        pygame.mixer.music.play()
        self.text = ['"Oh Jay, I am so glad you are here!" - Daisy (not Princess Peach) rejoices.',
                    'But the challenge is yet to be over. Jay Kotsby has to find his way out',
                    'of the Mansion. This time, it is haunted by Slenderman himself! Legend',
                    'says that if you stare in his eyes long enough, he will kidnap you...',
                    'But this Slenderman is friendlier than most Slendermen: if you notice',
                    'any anomalies, simply turn away in the other direction and wait a bit; ',
                    'Slenderman will disappear. Also, you only have 4 minutes to escape!',
                    'And you only have 1 live! Can you help Jay Kotsby escape the Mansion?',
                    '',
                    'Hint: To get out of the Mansion, you simmply go the opposite way you', 
                    'go in. Good luck, old sport!',
                    '',
                    'Use arrow keys to move left and right. Press Enter to continue.'
                    ]

    def keyPressed(self, keyCode, mod): 
        if keyCode == pygame.K_RETURN and self.level == 3 and self.player1.sprites()[0].x >= self.level3.backDoor.sprites()[0].x:
            self.inBetweenLevels = True
            self.level += 1
            self.meetPrincess = False
        elif keyCode == pygame.K_RETURN and ((self.level1.isGameOver) or (self.level2.isGameOver) or (self.level3.isGameOver) or (self.slendermanLevel1.isGameOver) or (self.slendermanLevel2.isGameOver) or (self.slendermanLevel3.isGameOver) or self.slendermanLevel3.isWin):
            if self.slendermanLevel1.isGameOver: self.slendermanLevel1.sadMusic.stop()
            elif self.slendermanLevel2.isGameOver: self.slendermanLevel2.sadMusic.stop()
            elif self.slendermanLevel3.isGameOver: self.slendermanLevel3.sadMusic.stop()
            elif self.slendermanLevel3.isWin: self.slendermanLevel3.happyMusic.stop()
            self.init()
            self.run()

    def levelUpdate(self):
        if self.level == 1: level = self.level1
        elif self.level == 2: level = self.level2
        elif self.level == 3: level = self.level3
        elif self.level == 4: 
            if not self.timeOn:
                self.startTime = time.time()
                self.timeOn = True
            level = self.slendermanLevel1
        elif self.level == 5: level = self.slendermanLevel2
        elif self.level == 6: level = self.slendermanLevel3
        if self.level <= 3: 
            player = self.player1.sprites()[0] 
            level.update()
            level.camera.update()
            self.player1.update(self.width, self.height, self.isKeyPressed)
            if player.x == level.backDoor.sprites()[0].x:
                if self.level == 3: #special case for level 3: message from the princess
                    self.meetPrincess = True
                    pygame.mixer.music.fadeout(3000)
                else:
                    self.inBetweenLevels = True
                    self.level += 1
                    if self.level < 3: 
                        pygame.mixer.music.load('music/Level1n2.wav')
                        pygame.mixer.music.play(-1)
                    elif self.level == 3: 
                        pygame.mixer.music.load('music/Level3.wav')
                        pygame.mixer.music.play(-1)
                    player.x = 100 
        elif self.level >= 4: 
            pygame.mixer.music.stop()
            player = self.player2.sprites()[0] 
            level.update(self.startTime, self.width, self.height)
            level.camera.update()
            self.player2.update(self.width, self.height, self.isKeyPressed)
            if self.level < 6 and player.x == level.frontDoor.sprites()[0].x:
                self.inBetweenLevels = True
                self.level += 1
                player.x = self.worldWidth - 100 

    def timerFired(self, dt):
        if self.inBetweenLevels: #display screen in between levels
            self.frame += 1
            if (self.frame == 80): 
                self.inBetweenLevels = False 
                #SlendermanLevel.countdown += 2 #account for lost frames
                self.frame = 0
        self.levelUpdate()

    def drawMessage(self, screen):
        background = pygame.Surface(screen.get_size())
        background.fill((0,0,0))
        image = pygame.image.load("images/Princess.png").convert_alpha()
        font = pygame.font.Font("Adobe Caslon Pro.ttf", 20)
        for i in range(len(self.text)):
            text = font.render(self.text[i], False, (255,255,255))
            textPos = text.get_rect()
            textPos.left = background.get_rect().centerx - 290
            textPos.centery = 20 + 24*i
            background.blit(text, textPos)
        background.blit(image, (background.get_rect().centerx-10, 350))
        screen.blit(background, (0, 0))

    def redrawAll(self, screen):
        if self.level == 1:
            self.level1.draw_background(screen)
        elif self.level == 2:
            self.level2.draw_background(screen)
        elif self.level == 3:
            self.level3.draw_background(screen)
        elif self.level == 4:
            self.slendermanLevel1.draw_background(screen)
        elif self.level == 5:
            self.slendermanLevel2.draw_background(screen)
        elif self.level == 6:
            self.slendermanLevel3.draw_background(screen)
        if self.meetPrincess:
            self.drawMessage(screen)
        if self.inBetweenLevels:
            if self.level <= 3: 
                self.level1.drawInBetweenLevels(screen, self.level)
            elif 3 <= self.level <= 6:
                self.slendermanLevel1.drawInBetweenLevels(screen, self.level)


#Game(600,430).run() #ceil+floor+pole+50 for displaying lives
