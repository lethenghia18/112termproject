import pygame
from objects import *
import random
from camera import *
from level import Level 
import time
from datetime import datetime, timedelta

class SlendermanLevel(Level): #slenderman level
    
    def __init__(self, player, worldWidth, width, height):
        super(SlendermanLevel, self).__init__(player, worldWidth, width, height)
        Slenderman.init()
        self.player.x = self.worldWidth - 100
        self.player.direction = -1
        self.slenderman = Slenderman(2000, self.height - 56 - 59) #118 is the height of slenderman
        self.slendermen = pygame.sprite.Group(self.slenderman)
        self.isWin = False 
        self.isGameOver = False 
        self.count = 0 #count seconds of encountering slenderman
        self.frame = 0
        self.slenderPosition = [None, None]
        self.encounter = False #detect encounter with slenderman
        self.distanceDeath = 150
        self.timeDeath = 180
        self.lightRadius = 100
        self.slenderSound = pygame.mixer.Sound("music/Slender_Death.wav")
        self.sadMusic = pygame.mixer.Sound("music/GameOver.wav")
        self.happyMusic = pygame.mixer.Sound("music/Win.wav")
        self.countdown = 240 #in seconds
        self.startTime = 0
        self.endTime = 0
        self.winText = ["After that day, Jay Kotsby and Daisy BuStehlik live happily",
                        "ever after. Before they leave, Kotsby takes one last look", 
                        "at the Slender Mansion...",
                        "",
                        '"[Kotsby] believed in the green light, the orgastic future that', 
                        "year by year recedes before us. It eluded us then, but that's", 
                        "no matter - tomorrow we will run faster, stretch out our arms", 
                        'farther...And one fine morning---',
                        "",
                        "So we beat on, boats against the current, borne back ceaselessly", 
                        'into the past..."',
                        "                       --- F. Scott Fitzgerald, The Great Gatsby"
                        "",
                        "                                       Play Again? Press Enter"
                        ]

    def createBackground(self):
        super(SlendermanLevel, self).createBackground()
        Page.init()
        self.pages = pygame.sprite.Group()
        for i in range(300, 2500, 500):
            self.pages.add(Page(i, self.height/2 + 100))
        Freddy.init()
        self.freddy = pygame.sprite.Group()
        for i in range(600, 2900, 2000):
            self.freddy.add(Freddy(i, self.height/2 + 100))
        Grave.init()
        self.graves = pygame.sprite.Group()
        for i in range(1000, 2900, 1000):
            self.graves.add(Grave(i, self.height - 56 - 36))
        BloodWall.init()
        self.bloodWall = pygame.sprite.Group(BloodWall(1600, self.height/2 + 100))

    def update(self, startTime, screenWidth, screenHeight): 
        self.slendermen.update(screenWidth, screenHeight)
        #SlendermanLevel.countdown -= 1
        self.endTime = time.time()
        self.startTime = startTime
        if not self.isGameOver: #only update when game is over
            if self.countdown - (self.endTime - self.startTime) <= 0: 
                self.isGameOver = True
                self.slenderman.kill()
                self.sadMusic.play()
            if len(self.slendermen) != 0: 
                slenderman = self.slendermen.sprites()[0]
                slenderman.direction = - self.player.direction
                distance = abs(slenderman.x - self.player.x)
                if (distance <= 5): 
                    #this is better than slenderman.x == self.player.x because in the latter, sometimes, player glosses through slenderman without dying
                    self.encounter = True
                    self.slenderSound.play()
                    if self.count < self.timeDeath - 40: self.count = self.timeDeath - 20 
                    else: self.count += 1 
                    if self.count == self.timeDeath: 
                        self.isGameOver = True
                        self.slenderman.kill() #kill slenderman as long as game is over, in order for the music to work 
                        self.slenderSound.stop()
                        self.sadMusic.play()
                elif (distance <= self.distanceDeath):
                    self.count += 1
                    self.encounter = True
                    self.slenderSound.play()
                    if self.count == self.timeDeath: 
                        self.isGameOver = True
                        self.slenderman.kill() 
                        self.slenderSound.stop()
                        self.sadMusic.play()
                else: #move slenderman
                    self.encounter = False
                    self.slenderSound.stop()
                    self.count = 0 
                    self.frame += 1
                    if self.frame == 100:
                        if self.level == 4: self.slenderman.x = self.slenderPosition[random.randint(0,1)]
                        elif self.level == 5: self.slenderman.x = self.slenderPosition[random.randint(0,3)]
                        elif self.level == 6: self.slenderman.x = self.slenderPosition[random.randint(0,5)]
                        if (self.player.x - 150 <= slenderman.x < self.player.x): #to the left of player
                            self.slenderman.x -= 200
                        elif (self.player.x < slenderman.x <= self.player.x + 150):
                            self.slenderman.x += 200
                        self.frame = 0
    
    def drawClock(self, screen):
        background = pygame.Surface((self.width, 50))
        background.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        sec = timedelta(seconds=(self.countdown - (self.endTime - self.startTime))) 
        #convert seconds to minute:second; too lazy to write myself thus copied from
        #http://stackoverflow.com/questions/4048651/python-function-to-convert-seconds-into-minutes-hours-and-days
        d = datetime(1,1,1) + sec
        text = font.render("%d:%d" % (d.minute, d.second), False, (255,255,255)) 
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        background.blit(text, textpos)
        screen.blit(background, (0, 0))

    def drawEncounter(self, screen): 
        image = pygame.transform.scale(pygame.image.load('images/slenderGameOver.png').convert_alpha(), (self.width, self.height))
        imagePos = image.get_rect()
        imagePos.centerx = screen.get_rect().centerx
        imagePos.centery = screen.get_rect().centery 
        if self.count < self.timeDeath - 50:
            for i in range(self.count):
                pygame.draw.line(screen, pygame.Color(255,255,255), (0, random.randint(0, self.height)), (self.width, random.randint(0, self.height)), 2)
        elif self.timeDeath - 20 > self.count >= self.timeDeath - 50:
            self.slenderman.x = self.player.x - 6 if self.player.direction == -1 else self.player.x + 6
            self.slendermen.update(self.width, self.height)
            self.camera.draw_sprites(screen, self.slendermen)
            if self.count%2 == 0:
                screen.blit(image, (0,0))
        elif self.count >= self.timeDeath - 20:
            screen.blit(image, (0,0))

    def drawInBetweenLevels(self, screen, level):
        background = pygame.Surface(screen.get_size())
        image = pygame.transform.scale(pygame.image.load("images/slenderman.png"), (24, 118))
        background.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        levelText = font.render("Level %d" % (level), False, (255,255,255))
        levelTextpos = levelText.get_rect()
        levelTextpos.centerx = background.get_rect().centerx
        levelTextpos.centery = background.get_rect().centery - 50
        imagePos = image.get_rect()
        imagePos.centerx = background.get_rect().centerx
        imagePos.centery = background.get_rect().centery + 50
        background.blit(levelText, levelTextpos)
        background.blit(image, imagePos)
        screen.blit(background, (0, 0))

    def drawWin(self, screen): 
        background1 = pygame.transform.scale(pygame.image.load("images/ending.png").convert_alpha(), (600,432))
        font = pygame.font.Font("Adobe Caslon Pro.ttf", 20)
        for i in range(len(self.winText)):
            text = font.render(self.winText[i], False, (255, 20, 147))
            textPos = text.get_rect()
            textPos.left = background1.get_rect().centerx - 240
            textPos.centery = 90 + 24*i
            background1.blit(text, textPos)
        screen.blit(background1, (0, 0))

    def drawFlashLight(self, screen):
        background = pygame.Surface((1000,432*2), pygame.SRCALPHA)
        background.fill((0, 0, 0, 255))
        pygame.draw.circle(background, (0,0,255,0), (int(self.player.x - self.camera.rect.left), int(self.player.y - 15)), self.lightRadius) 
        screen.blit(background, (0, 0))

    def draw_background(self, screen):
        self.camera.draw_sprites(screen, self.ceilings)
        self.camera.draw_sprites(screen, self.floors)
        self.camera.draw_sprites(screen, self.poles)
        self.camera.draw_sprites(screen, self.backDoor)
        self.camera.draw_sprites(screen, self.hangers)
        self.camera.draw_sprites(screen, self.windows1)
        self.camera.draw_sprites(screen, self.windows2) 
        self.camera.draw_sprites(screen, self.recordings)
        self.camera.draw_sprites(screen, self.clocks)
        self.camera.draw_sprites(screen, self.pages)
        self.camera.draw_sprites(screen, self.freddy)
        self.camera.draw_sprites(screen, self.graves)
        self.camera.draw_sprites(screen, self.bloodWall)
        self.camera.draw_sprites(screen, self.frontDoor)
        self.camera.draw_sprites(screen, self.slendermen)
        self.drawFlashLight(screen)
        self.camera.draw_sprites(screen, self.players)
        self.drawClock(screen)
        if self.encounter: 
            self.drawEncounter(screen)
        if self.isGameOver:
            self.drawGameOver(screen)

class SlendermanLevel1(SlendermanLevel): 
    def __init__(self, player, worldWidth, width, height):
        super(SlendermanLevel1, self).__init__(player, worldWidth, width, height)
        self.slenderPosition = [random.randint(300,1400), random.randint(1400,2500)]
        self.level = 4
        self.timeDeath = 180 #this is more for the frame than countdown time
        self.lightRadius = 100
        self.bgColor = pygame.Color(25, 25, 112)

    def update(self, startTime, screenWidth, screenHeight): 
        super(SlendermanLevel1, self).update(startTime, screenWidth, screenHeight)
        
    def draw_background(self, screen):
        screen.fill(self.bgColor)
        super(SlendermanLevel1, self).draw_background(screen)

class SlendermanLevel2(SlendermanLevel): 
    def __init__(self, player, worldWidth, width, height):
        super(SlendermanLevel2, self).__init__(player, worldWidth, width, height)
        self.slenderPosition = [random.randint(300,1100), random.randint(1100,1900), random.randint(1900,2700), self.player.x - 200]
        self.level = 5
        self.timeDeath = 160
        self.lightRadius = 75
        self.bgColor = pygame.Color(85, 107, 47)

    def update(self, startTime, screenWidth, screenHeight): 
        self.slenderPosition[3] = self.player.x - 200 if self.player.direction == -1 else self.player.x + 200 
        super(SlendermanLevel2, self).update(startTime, screenWidth, screenHeight)
        #make slenderman move

    def draw_background(self, screen):
        screen.fill(self.bgColor)
        super(SlendermanLevel2, self).draw_background(screen)

class SlendermanLevel3(SlendermanLevel): 
    def __init__(self, player, worldWidth, width, height):
        super(SlendermanLevel3, self).__init__(player, worldWidth, width, height)
        self.slenderPosition = [random.randint(0,750), random.randint(750,1500), random.randint(1500,2250), random.randint(2250,3000), self.player.x - 200, self.player.x - 400]
        self.level = 6
        self.timeDeath = 140
        self.lightRadius = 50
        self.bgColor = pygame.Color(128, 0, 0)
        #increse the frequency of encountering slenderman as level progresses

    def update(self, startTime, screenWidth, screenHeight): 
        self.slenderPosition[4] = self.player.x - 200 if self.player.direction == -1 else self.player.x + 200 
        self.slenderPosition[5] = self.player.x - 200 if self.player.direction == -1 else self.player.x + 200 
        super(SlendermanLevel3, self).update(startTime, screenWidth, screenHeight)
        if self.player.x == self.frontGate.sprites()[0].x: 
            self.isWin = True
            self.happyMusic.play()


    def draw_background(self, screen):
        screen.fill(self.bgColor)
        super(SlendermanLevel3, self).draw_background(screen)
        self.camera.draw_sprites(screen, self.frontGate)
        self.camera.draw_sprites(screen, self.players)
        self.drawFlashLight(screen)
        self.drawClock(screen)
        if self.encounter: self.drawEncounter(screen)
        if self.isGameOver: self.drawGameOver(screen)
        if self.isWin: self.drawWin(screen)