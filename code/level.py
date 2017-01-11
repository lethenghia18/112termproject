import pygame
from objects import *
import random
from pygamegame import PygameGame
from camera import *

class Level(PygameGame):
    def __init__(self, player, worldWidth, width, height):
        self.player = player
        self.player.x = 100 #initial position of player
        self.player.blood = 3
        self.players = pygame.sprite.Group(player)
        self.width, self.height = width, height
        self.worldWidth = worldWidth
        self.marginY = 50 #account for the display of lives up top of screen
        self.camera = Camera(player, self.worldWidth, self.height)
        self.createBackground()
        self.isGameOver = False
        self.loseLive = False #in Lose Live screen
        self.enemyFrame = []

        Blood.init()
        self.blood = pygame.sprite.Group()
        for i in range(1,4):
            self.blood.add(Blood(i*25, 25))

        #Characters
        Butler.init()
        self.butlers = pygame.sprite.Group()
        
        Bomber.init()
        self.bombers = pygame.sprite.Group()

        Chandelier.init()
        self.chandeliers = pygame.sprite.Group()
        self.lightX, self.lightY = 38, 39

        Jumper.init()
        self.jumpers = pygame.sprite.Group()

        Martini.init()
        self.martinis = pygame.sprite.Group()

        Gunman.init()
        self.gunmen = pygame.sprite.Group()

        Princess.init()
        self.princess = pygame.sprite.Group()

        self.enemies = pygame.sprite.Group() 

    def createBackground(self):
        Ceiling.init()
        self.ceilX, self.ceilY = 256, 16
        self.ceilings = pygame.sprite.Group()
        for i in range(255, 3100, 255):
            self.ceilings.add(Ceiling(i, 50 + self.ceilY)) #50 for the display of lives
        
        Floor.init()
        self.floorX, self.floorY = 206, 28
        self.floors = pygame.sprite.Group()
        for i in range(206, 3100, 205):
            self.floors.add(Floor(i, self.height - self.floorY))
        Pole.init()
        self.poleX, self.poleY = 16, 146
        self.poles = pygame.sprite.Group()
        for i in range(30, 180, 30):
            self.poles.add(Pole(i*self.poleX, 2*self.ceilY + 50 + self.poleY)) #50 for the display of lives
        FrontGate.init()
        self.frontGate = pygame.sprite.Group(FrontGate(100, self.height - 2*self.floorY - 64))
        Door.init()
        self.frontDoor = pygame.sprite.Group(Door(100, self.height - 2*self.floorY - 64))
        self.backDoor = pygame.sprite.Group(Door(self.worldWidth-100, self.height - 2*self.floorY - 64))
        Hanger.init()
        self.hangers = pygame.sprite.Group(Hanger(250, self.height-2*self.floorY - 31))
        Recording.init()
        self.recordings = pygame.sprite.Group(Recording(400, self.height-2*self.floorY - 32))
        Window1.init()
        self.window1X = 48
        self.windows1 = pygame.sprite.Group()
        for i in range(7,100,20):
            self.windows1.add(Window1(i*self.window1X, self.height/2.5))
        Window2.init()
        self.window2X = 144
        self.windows2 = pygame.sprite.Group()
        for i in range(15, 100, 20):
            self.windows2.add(Window2(i*self.window1X, self.height/2.5))
        Bench.init()
        self.benches = pygame.sprite.Group()
        self.benchX = 48
        for i in range(13,100,40):
            self.benches.add(Bench(i*self.benchX, self.height-2*self.floorY-10))
        Clock.init()
        self.clocks = pygame.sprite.Group()
        self.clockX = 16
        for i in range(50, 200, 120):
            self.clocks.add(Clock(i*self.clockX, self.height-2*self.floorY-48))
        Bookshelf1.init()
        self.bookshelves1 = pygame.sprite.Group()
        self.bookshelves1X = 48
        for i in range(24, 100, 20):
            self.bookshelves1.add(Bookshelf1(i*self.bookshelves1X, self.height-2*self.floorY - 79))
        Bookshelf2.init()
        self.bookshelves2 = pygame.sprite.Group()
        self.bookshelves1X = 48
        for i in range(22, 60, 20):
            self.bookshelves2.add(Bookshelf2(i*self.bookshelves1X, self.height/3))

#Function below is developed based on code @https://www.pygame.org/docs/tut/tom/games2.html
    def drawGameOver(self, screen): 
        background = pygame.transform.scale(pygame.image.load("images/tombstone.png").convert_alpha(), (self.width, self.height))
        font = pygame.font.Font('Adobe Caslon Pro.ttf', 25)
        text = font.render("You succumbed to Slenderman's evil, old sport! :-(", False, (255,255,255))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery - 100
        text2 = font.render("Try Again? Press Enter", False, (255,255,255))
        textpos2 = text2.get_rect()
        textpos2.centerx = background.get_rect().centerx
        textpos2.centery = background.get_rect().centery - 20
        background.blit(text, textpos)
        background.blit(text2, textpos2)
        screen.blit(background, (0, 0))

    def drawLoseLive(self, screen, level):
        background = pygame.Surface(screen.get_size())
        image = pygame.image.load('images/Kosby.png').convert_alpha()
        background.fill((0, 0, 0))
        font = pygame.font.Font(None, 36)
        levelText = font.render("Level %d" % (level), False, (255,255,255))
        levelTextpos = levelText.get_rect()
        levelTextpos.centerx = background.get_rect().centerx
        levelTextpos.centery = background.get_rect().centery - 50
        text = font.render("x %s" % (self.player.lives), False, (255,255,255))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx + 10
        textpos.centery = background.get_rect().centery
        imagePos = image.get_rect()
        imagePos.centerx = background.get_rect().centerx - 25
        imagePos.centery = background.get_rect().centery
        background.blit(levelText, levelTextpos)
        background.blit(text, textpos)
        background.blit(image, imagePos)
        screen.blit(background, (0, 0))

    def drawLives(self, screen): 
        background = pygame.Surface((self.width, 50))
        image = pygame.image.load('images/live.png').convert_alpha()
        background.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        text = font.render("x %s" % (self.player.lives), False, (0,0,0))
        textpos = text.get_rect()
        textpos.centerx = 50
        textpos.centery = background.get_rect().centery
        imagePos = image.get_rect()
        imagePos.centerx = 20
        imagePos.centery = background.get_rect().centery
        background.blit(text, textpos)
        background.blit(image, imagePos)
        screen.blit(background, (0, 0))
        self.blood.draw(screen)

    def drawInBetweenLevels(self, screen, level):
        self.drawLoseLive(screen, level)

    def update(self): #change blood number
        self.newBlood = pygame.sprite.Group()
        for i in range(4, self.player.blood + 4):
            self.newBlood.add(Blood(i*25,25))
        self.blood = self.newBlood
        if len(self.enemies) != 0: #make dead enemy jump up and fail
            self.enemies.update(self.player, self.width, self.height)
            for enemy in self.enemies:
                if (isinstance(enemy, Jumper)): enemy.velocity = (0, 5)
                vx, vy = enemy.velocity
                enemy.velocity = (0, vy+2)
                if enemy.y > self.height:
                    enemy.kill()

    def playSadMusic(self):
        pygame.mixer.music.load('music/GameOver.wav')
        pygame.mixer.music.play()

    def isPlayerColliding(self, sprites):
        if len(sprites) != 0: 
            sprite = sprites.sprites()[0] 
            if (isinstance(sprite, Butler)):
                isColliding = self.player.butlerCollision
            elif (isinstance(sprite, Bomber)):
                isColliding = self.player.bomberCollision
            elif (isinstance(sprite, Chandelier)):
                isColliding = self.player.chandelierCollision
            elif (isinstance(sprite, Jumper)):
                isColliding = self.player.jumperCollision
            elif (isinstance(sprite, Gunman)):
                isColliding = self.player.gunmanCollision
            elif isinstance(sprite, Bomb) or isinstance(sprite, Bullet): 
                print(pygame.sprite.groupcollide(self.players, sprites, False, True, #collide with bombs
                    pygame.sprite.collide_rect))
                if pygame.sprite.groupcollide(self.players, sprites, False, True, #collide with bombs
                    pygame.sprite.collide_rect):
                    if not self.loseLive: 
                        self.player.getAttacked()
                        if self.player.blood == 0 and self.player.lives == 0:
                            self.isGameOver = True 
                            self.playSadMusic()
                        elif self.player.blood == 0 and self.player.lives > 0:
                            self.loseLive = True
            elif isinstance(sprite, Martini):
                if pygame.sprite.groupcollide(self.players, self.martinis, False, True, 
                pygame.sprite.collide_rect):
                    if self.player.blood < 3: self.player.blood += 1 
            if pygame.sprite.groupcollide(self.players, sprites, False, False, #loseBlood, loseLive or gameOver
                    pygame.sprite.collide_rect):
                    if not self.loseLive: 
                        if (not isColliding): 
                            self.player.getAttacked()
                            isColliding = True
                        if self.player.blood == 0 and self.player.lives == 0:
                            self.isGameOver = True 
                            self.playSadMusic()
                        elif self.player.blood == 0 and self.player.lives > 0:
                            self.loseLive = True
            else: 
                isColliding = False
            if (isinstance(sprite, Butler)):
                self.player.butlerCollision = isColliding
            elif (isinstance(sprite, Bomber)):
                self.player.bomberCollision = isColliding
            elif (isinstance(sprite, Chandelier)):
                self.player.chandelierCollision = isColliding
            elif (isinstance(sprite, Jumper)):
                self.player.jumperCollision = isColliding
            elif (isinstance(sprite, Gunman)):
                self.player.gunmanCollision = isColliding

    def isHatColliding(self, sprites):
        dead = pygame.sprite.groupcollide(self.player.hat, sprites, False, True, 
                pygame.sprite.collide_rect)
        if dead: 
            hat = self.player.hat.sprites()[0]
            for enemy in dead[hat]:
                enemy.velocity = (0, -10)
                self.enemies.add(enemy)
            (vx, vy) = self.player.hat.sprites()[0].velocity #reverse velocity of hat
            self.player.hat.sprites()[0].velocity = (-vx, vy)

    def draw_background(self, screen): 
        self.camera.draw_sprites(screen, self.ceilings)
        self.camera.draw_sprites(screen, self.floors)
        self.camera.draw_sprites(screen, self.poles)
        self.camera.draw_sprites(screen, self.backDoor)
        self.camera.draw_sprites(screen, self.hangers)
        self.camera.draw_sprites(screen, self.windows1)
        self.camera.draw_sprites(screen, self.windows2) 
        self.camera.draw_sprites(screen, self.recordings)
        self.camera.draw_sprites(screen, self.benches)
        self.camera.draw_sprites(screen, self.clocks)
        self.camera.draw_sprites(screen, self.bookshelves1)
        self.camera.draw_sprites(screen, self.bookshelves2)
        self.drawLives(screen)
        self.camera.draw_sprites(screen, self.enemies)

class Level1(Level): 
    def __init__(self, player, worldWidth, width, height):
        super(Level1, self).__init__(player, worldWidth, width, height)
        for i in range(370, 2500, 500):
            self.butlers.add(Butler(i, height - 56 - 29))
        for i in range(1300, 2500, 500):
            self.bombers.add(Bomber(i, height - 56 - 29))
            if i == 1800: self.bombers.add(Bomber(i+100, height-56-29))
        self.frame = 0 #really bad way to handle losing lives screen
        self.level = 1
        self.bgColor = pygame.Color(240, 128, 128)

    def update(self): 
        if self.loseLive: #this if else statement really helps with the blood and live screen situations
            if self.frame == 0: self.player.lives -= 1
            self.frame += 1
            if self.frame == 25: 
                self.__init__(self.player, self.worldWidth, self.width, self.height)
        elif not self.isGameOver: #only update when game is not over
            super(Level1, self).update() #this super has to be behind the frame, because you want to update the blood and lives after you lose lives 
            self.player.hat.update(self.player, self.width, self.height)
            self.butlers.update(self.player, self.width, self.height)
            self.bombers.update(self.player, self.width, self.height)
            self.isHatColliding(self.butlers)
            self.isHatColliding(self.bombers)
            self.isPlayerColliding(self.butlers)
            for bomber in self.bombers: 
                self.isPlayerColliding(bomber.bombs)
            self.isPlayerColliding(self.bombers)

    def draw_background(self, screen):
        screen.fill(self.bgColor)
        super(Level1, self).draw_background(screen)
        self.camera.draw_sprites(screen, self.frontGate)
        self.camera.draw_sprites(screen, self.player.hat)
        self.camera.draw_sprites(screen, self.butlers)
        self.camera.draw_sprites(screen, self.bombers)
        for bomber in self.bombers:
            self.camera.draw_sprites(screen, bomber.bombs)
        self.camera.draw_sprites(screen, self.players)
        if self.isGameOver: 
            self.drawGameOver(screen)
        if self.loseLive:
            self.drawLoseLive(screen, self.level)

class Level2(Level): 
    def __init__(self, player, worldWidth, width, height):
        super(Level2, self).__init__(player, worldWidth, width, height)
        for i in range(370, 2500, 300):
            self.butlers.add(Butler(i, height - 56 - 29))
        for i in range(800, 2500, 300):
            self.bombers.add(Bomber(i, height - 56 - 29))
            if i == 1800: self.bombers.add(Bomber(i+100, height-56-29))
        for i in range(1200, 2500, 500):
            self.chandeliers.add(Chandelier(i, 50 + 39)) #chandelier.height = 79
        for i in range(1850, 3000, 1000):
            self.martinis.add(Martini(i, height/2))
        self.frame = 0
        self.level = 2
        self.bgColor = pygame.Color(0, 205, 0)
        #add a few jumpers

    def update(self): 
        if self.loseLive:
            if self.frame == 0: self.player.lives -= 1
            self.frame += 1
            if self.frame == 25: 
                self.__init__(self.player, self.worldWidth, self.width, self.height)
        elif not self.isGameOver: 
            super(Level2, self).update()
            self.player.hat.update(self.player, self.width, self.height)
            self.butlers.update(self.player, self.width, self.height)
            self.bombers.update(self.player, self.width, self.height)
            self.chandeliers.update(self.player, self.width, self.height)
            self.jumpers.update(self.player, self.width, self.height)
            self.martinis.update(self.width, self.height)
            self.isHatColliding(self.butlers)
            self.isHatColliding(self.bombers)
            self.isPlayerColliding(self.martinis)
            self.isPlayerColliding(self.butlers)
            for bomber in self.bombers: 
                self.isPlayerColliding(bomber.bombs)
            self.isPlayerColliding(self.bombers)
            self.isPlayerColliding(self.chandeliers)
            
    def draw_background(self, screen):
        screen.fill(self.bgColor)
        super(Level2, self).draw_background(screen)
        self.camera.draw_sprites(screen, self.frontDoor)
        self.camera.draw_sprites(screen, self.player.hat)
        self.camera.draw_sprites(screen, self.butlers)
        self.camera.draw_sprites(screen, self.bombers)
        for bomber in self.bombers:
            self.camera.draw_sprites(screen, bomber.bombs)
        self.camera.draw_sprites(screen, self.chandeliers)
        self.camera.draw_sprites(screen, self.jumpers)
        self.camera.draw_sprites(screen, self.martinis)
        self.camera.draw_sprites(screen, self.players)
        if self.isGameOver: 
            self.drawGameOver(screen)
        if self.loseLive:
            self.drawLoseLive(screen, self.level)

class Level3(Level): 
    def __init__(self, player, worldWidth, width, height):
        super(Level3, self).__init__(player, worldWidth, width, height)
        for i in range(300, 2000, 300):
            self.butlers.add(Butler(i, height - 56 - 29))
        for i in range(1000, 3000, 700):
            self.bombers.add(Bomber(i, height - 56 - 29))
        for i in range(1700, 3000, 500):
            self.chandeliers.add(Chandelier(i, 50 + 39)) #chandelier.height = 79
        for i in range(600, 2500, 500):
            self.jumpers.add(Jumper(i, height - 56 - 32))
        for i in range(1300, 2500, 500):
            self.gunmen.add(Gunman(i, height - 56 - 32))
            self.gunmen.add(Gunman(i + 100, height - 56 - 32))
        for i in range(1400, 3000, 1400):
            self.martinis.add(Martini(i, height/2))
        self.princess.add(Princess(self.worldWidth - 50, height - 56 - 32))
        self.frame = 0
        self.level = 3
        self.bgColor = pygame.Color(0, 245, 255)

    def update(self): 
        if self.loseLive:
            if self.frame == 0: self.player.lives -= 1
            self.frame += 1
            if self.frame == 25: 
                self.__init__(self.player, self.worldWidth, self.width, self.height)
        elif not self.isGameOver: 
            super(Level3, self).update()
            self.player.hat.update(self.player, self.width, self.height)
            self.butlers.update(self.player, self.width, self.height)
            self.bombers.update(self.player, self.width, self.height)
            self.chandeliers.update(self.player, self.width, self.height)
            self.martinis.update(self.width, self.height)
            self.gunmen.update(self.player, self.width, self.height)
            self.isHatColliding(self.butlers)
            self.isHatColliding(self.bombers)
            self.isHatColliding(self.jumpers)
            self.jumpers.update(self.player, self.width, self.height)
            self.isHatColliding(self.gunmen)
            self.isPlayerColliding(self.martinis)
            self.isPlayerColliding(self.butlers)
            for bomber in self.bombers: 
                self.isPlayerColliding(bomber.bombs)
            self.isPlayerColliding(self.bombers)
            self.isPlayerColliding(self.chandeliers)
            self.isPlayerColliding(self.jumpers)
            self.isPlayerColliding(self.gunmen)
            for gunman in self.gunmen: 
                self.isPlayerColliding(gunman.bullets)
        
    def draw_background(self, screen):
        screen.fill(self.bgColor)
        super(Level3, self).draw_background(screen)
        self.camera.draw_sprites(screen, self.frontDoor)
        self.camera.draw_sprites(screen, self.player.hat)
        self.camera.draw_sprites(screen, self.butlers)
        self.camera.draw_sprites(screen, self.bombers)
        for bomber in self.bombers:
            self.camera.draw_sprites(screen, bomber.bombs)
        self.camera.draw_sprites(screen, self.chandeliers)
        self.camera.draw_sprites(screen, self.jumpers)
        self.camera.draw_sprites(screen, self.martinis)
        self.camera.draw_sprites(screen, self.gunmen)
        for gunman in self.gunmen:
            self.camera.draw_sprites(screen, gunman.bullets)
        self.camera.draw_sprites(screen, self.players)
        self.camera.draw_sprites(screen, self.princess)
        if self.isGameOver: 
            self.drawGameOver(screen)
        if self.loseLive:
            self.drawLoseLive(screen, self.level)
            