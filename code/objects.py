#remember to cite the photos?

import pygame
import random

class GameObject(pygame.sprite.Sprite): 
    def __init__(self, x, y, image, radius):
        super(GameObject, self).__init__()
        self.x, self.y, self.image, self.radius = x, y, image, radius
        self.velocity = (0, 0)
        self.updateRect()

    def updateRect(self):
        (w, h) = self.image.get_size()
        self.width, self.height = (w, h)
        self.rect = pygame.Rect(self.x - w/2, self.y - h/2, w, h)

    def update(self, screenWidth, screenHeight): 
        (vx, vy) = self.velocity
        self.x += vx
        self.y += vy
        self.updateRect()

class Player(GameObject): 
    @staticmethod
    def init():
        alpha = 64
        Player.image = pygame.image.load('images/Kosby.png').convert_alpha()
        Player.collide_image = Player.image.copy()
        Player.collide_image.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        Player.walk1 = pygame.image.load('images/Kosby_walk.png').convert_alpha()
        Player.collide_walk1 = Player.walk1.copy()
        Player.collide_walk1.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        Player.walk2 = pygame.image.load('images/Kosby_walk2.png').convert_alpha()
        Player.collide_walk2 = Player.walk2.copy()
        Player.collide_walk2.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        Player.jump = pygame.image.load('images/Kosby_jump.png').convert_alpha()
        Player.collide_jump = Player.jump.copy()
        Player.collide_jump.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)
        Player.attack = pygame.image.load('images/Kosby_throw.png').convert_alpha()
        Player.collide_attack = Player.attack.copy()
        Player.collide_attack.fill((255, 255, 255, alpha), None, pygame.BLEND_RGBA_MULT)

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, Player.image, 10)
        self.right_image = Player.image
        self.left_image = pygame.transform.flip(Player.image, True, False)
        self.walkRight1 = Player.walk1
        self.walkLeft1 = pygame.transform.flip(Player.walk1, True, False)
        self.walkRight2 = Player.walk2
        self.walkLeft2 = pygame.transform.flip(Player.walk2, True, False)
        self.jumpRight = Player.jump
        self.jumpLeft = pygame.transform.flip(Player.jump, True, False)
        self.attackRight = Player.attack
        self.attackLeft = pygame.transform.flip(Player.attack, True, False)
        #for collision image
        self.rightCollide_image = Player.collide_image
        self.leftCollide_image = pygame.transform.flip(Player.collide_image, True, False)
        self.collideWalkRight1 = Player.collide_walk1
        self.collideWalkLeft1 = pygame.transform.flip(Player.collide_walk1, True, False)
        self.collideWalkRight2 = Player.collide_walk2
        self.collideWalkLeft2 = pygame.transform.flip(Player.collide_walk2, True, False)
        self.collideJumpRight = Player.collide_jump
        self.collideJumpLeft = pygame.transform.flip(Player.collide_jump, True, False)
        self.collideAttackRight = Player.collide_attack
        self.collideAttackLeft = pygame.transform.flip(Player.collide_attack, True, False)
        Hat.init()
        self.hat = pygame.sprite.Group()
        self.frame = 0
        self.direction = 1 #-1 is left, 1 is right
        self.onGround = True #for flying
        self.blood = 3
        self.lives = 3
        self.butlerCollision = False #detect collision with enemies
        self.bomberCollision = False
        self.jumperCollision = False
        self.gunmanCollision = False
        self.chandelierCollision = False
        #bomb and bullet are just too hard

    def update(self, screenWidth, screenHeight, keysPressed):
        super(Player, self).update(screenWidth, screenHeight)
        if self.butlerCollision or self.bomberCollision or self.gunmanCollision or self.chandelierCollision or self.jumperCollision: 
            self.image = self.rightCollide_image if (self.direction == 1) else self.leftCollide_image
            if keysPressed(pygame.K_LEFT):
                self.move(self.collideWalkLeft1, self.collideWalkLeft2, -1) #(image1, image2, direction)
            if keysPressed(pygame.K_RIGHT):
                self.move(self.collideWalkRight1, self.collideWalkRight2, 1)
            if keysPressed(pygame.K_UP): #set velocity to 0 when self.onGround = False
                self.playerJump()
            if (not self.onGround):
                self.playerLand(screenWidth, screenHeight)
            if keysPressed(pygame.K_SPACE):
                self.image = self.collideAttackRight if self.direction == 1 else self.collideAttackLeft
                if len(self.hat) == 0: self.hat.add(Hat(self))   
        else:         
            self.image = self.right_image if (self.direction == 1) else self.left_image
            if keysPressed(pygame.K_LEFT):
                self.move(self.walkLeft1, self.walkLeft2, -1) #(image1, image2, direction)
            if keysPressed(pygame.K_RIGHT):
                self.move(self.walkRight1, self.walkRight2, 1)
            if keysPressed(pygame.K_UP): #set velocity to 0 when self.onGround = False
                self.playerJump()
            if (not self.onGround):
                self.playerLand(screenWidth, screenHeight)
            if keysPressed(pygame.K_SPACE):
                self.image = self.attackRight if self.direction == 1 else self.attackLeft
                if len(self.hat) == 0: self.hat.add(Hat(self))

    def move(self, movingImage1, movingImage2, direction): 
        if (self.frame <= 20):
            self.image = movingImage1 
        else:
            self.image = movingImage2
            if (self.frame == 40): self.frame = 0 
        self.frame += 1
        if direction == -1: self.x -= 7
        else: self.x += 7 
        self.direction = direction

    def playerJump(self):
        if (self.onGround):
            if self.butlerCollision or self.bomberCollision or self.gunmanCollision or self.chandelierCollision or self.jumperCollision: 
                self.image = self.collideJumpRight if self.direction == 1 else self.collideJumpLeft
            else:
                self.image = self.jumpRight if self.direction == 1 else self.jumpLeft
            vx, vy = self.velocity
            self.velocity = (vx, -40) #arbitrary number, fits best with the speed
            self.onGround = False

    def playerLand(self, screenWidth, screenHeight):
        if self.butlerCollision or self.bomberCollision or self.gunmanCollision or self.chandelierCollision or self.jumperCollision:  
            self.image = self.collideJumpRight if self.direction == 1 else self.collideJumpLeft
        else:
            self.image = self.jumpRight if self.direction == 1 else self.jumpLeft
        vx, vy = self.velocity
        vy += 4
        if (vy >= 40):
            self.y = screenHeight-56-self.height/2
            vy = 0
            self.onGround = True
        self.velocity = (vx, vy)

    def getAttacked(self):
        if self.blood > 0: 
            self.blood -= 1

class Hat(GameObject): 
    @staticmethod
    def init():
        Hat.image = pygame.image.load('images/hat.png').convert_alpha()
        Hat.image2 = pygame.image.load('images/hat2.png').convert_alpha()
        Hat.time = 30*2

    def __init__(self, player):
        super(Hat, self).__init__(player.x, player.y, Hat.image, 10)
        self.frame = 0
        self.direction = player.direction
        self.hatSpeed = 7
        self.velocity = (self.hatSpeed,0) if self.direction == 1 else (-self.hatSpeed,0)

    def update(self, player, screenHeight, screenWidth):
        super(Hat, self).update(screenWidth, screenHeight)
        self.frame += 1
        if (self.frame >= 30):
            vx, vy = self.velocity
            self.velocity = (-self.hatSpeed, vy) if self.direction == 1 else (self.hatSpeed, vy) 
        if self.frame > 5 and pygame.sprite.collide_circle(self, player) or self.frame > Hat.time:
            self.kill()

class Blood(GameObject):
    @staticmethod
    def init():
        Blood.image = pygame.transform.scale(pygame.image.load('images/heart.png').convert_alpha(), (20, 20))

    def __init__(self, x, y):
        super(Blood, self).__init__(x, y, Blood.image, 10)

    def update(self, player, screenHeight, screenWidth):
        super(Blood, self).update(screenWidth, screenHeight)

#Enemies
class Enemy(GameObject): 
    def __init__(self, x, y, standImage, walkImage):
        super(Enemy, self).__init__(x, y, standImage, 10) 
        self.right_image = standImage
        self.left_image = pygame.transform.flip(standImage, True, False)
        self.walkRight = walkImage
        self.walkLeft = pygame.transform.flip(walkImage, True, False)
        self.velocity = (2,0)
        self.originalX = x
        self.frame = 0
        self.direction = 1

    def update(self, screenWidth, screenHeight): #move fuction
        super(Enemy, self).update(screenWidth, screenHeight)
        if (not isinstance(self, Jumper)): #jumpers follow their own weird movements
            if (self.frame <= 25):
                self.image = self.walkRight if (self.direction == 1) else self.walkLeft
            else:
                self.image = self.right_image if (self.direction == 1) else self.left_image
                if self.frame == 50: self.frame = 0 
            self.frame += 1
            if self.x >= 5*screenWidth or self.x <= 0 or self.x >= self.originalX + 200 or self.x <= self.originalX - 200:
                (vx, vy) = self.velocity
                self.velocity = (-vx, vy)
                self.direction = -1*self.direction

class Butler(Enemy): 
    @staticmethod
    def init():
        Butler.image = pygame.image.load('images/butler1.png').convert_alpha()
        Butler.walk = pygame.image.load('images/butler2.png').convert_alpha()

    def __init__(self, x, y):
        super(Butler, self).__init__(x, y, Butler.image, Butler.walk)

    def update(self, player, screenWidth, screenHeight):
        super(Butler, self).update(screenWidth, screenHeight)

class Gunman(Enemy): 
    @staticmethod
    def init():
        Gunman.image = pygame.image.load('images/gunman2.png').convert_alpha()
        Gunman.walk = pygame.image.load('images/gunman.png').convert_alpha()

    def __init__(self, x, y):
        super(Gunman, self).__init__(x, y, pygame.transform.flip(Gunman.image, True, False), pygame.transform.flip(Gunman.walk, True, False))
        Bullet.init()
        self.bullets = pygame.sprite.Group()

    def update(self, player, screenWidth, screenHeight):
        super(Gunman, self).update(screenWidth, screenHeight)
        if (self.x <= player.x <= self.x + 200): #to the left of player
            self.attack(1)
        elif (self.x >= player.x >= self.x - 200): #to the right of player
            self.attack(-1)
        else: self.velocity = (2,0) if (self.direction == 1) else (-2,0)
        self.bullets.update(screenWidth, screenHeight)

    def attack(self, direction): 
        self.direction = direction
        vx, vy = self.velocity
        self.velocity = (0, vy)
        self.image = self.right_image if direction == 1 else self.left_image
        if (len(self.bullets) == 0): self.bullets.add(Bullet(self))

class Bullet(GameObject): 
    @staticmethod
    def init():
        Bullet.image = pygame.image.load('images/bullets.png').convert_alpha()
        Bullet.time = 50*2 

    def __init__(self, gunman):
        super(Bullet, self).__init__(gunman.x, gunman.y, Bullet.image, 10)
        self.direction = gunman.direction
        self.velocity = (7,0) if self.direction == 1 else (-7,0)
        self.frame = 0

    def update(self, screenHeight, screenWidth):
        super(Bullet, self).update(screenWidth, screenHeight)
        self.frame += 1
        if (self.frame > Bullet.time): 
            self.kill()

class Chandelier(GameObject): 
    @staticmethod
    def init():
        Chandelier.image = pygame.image.load('images/chandelier.png').convert_alpha()

    def __init__(self, x, y):
        super(Chandelier, self).__init__(x, y, Chandelier.image, 10)

    def update(self, player, screenWidth, screenHeight):
        super(Chandelier, self).update(screenWidth, screenHeight)
        if self.x - self.width/2 <= player.x <= self.x + self.width/2:
            vx, vy = self.velocity
            self.velocity = vx, 8
        if (self.y >= screenHeight): self.kill()

class Bomber(Enemy): 
    @staticmethod
    def init():
        Bomber.image = pygame.image.load('images/bomber2.png').convert_alpha()
        Bomber.walk = pygame.image.load('images/bomber1.png').convert_alpha()
        Bomber.walk2 = pygame.image.load('images/bomber3.png').convert_alpha()

    def __init__(self, x, y):
        super(Bomber, self).__init__(x, y, pygame.transform.flip(Bomber.walk2, True, False), Bomber.walk)
        self.standRight = pygame.transform.flip(Bomber.image, True, False)
        self.standLeft = Bomber.image
        Bomb.init()
        self.bombs = pygame.sprite.Group()

    def update(self, player, screenWidth, screenHeight):
        super(Bomber, self).update(screenWidth, screenHeight)
        if (self.x <= player.x <= self.x + 200): #to the left of player
            self.attack(1)            
        elif (self.x >= player.x >= self.x - 200): #to the right of player
            self.attack(-1)
        else: self.velocity = (2,0) if (self.direction == 1) else (-2,0)
        self.bombs.update(screenWidth, screenHeight)

    def attack(self, direction):
        self.direction = direction
        vx, vy = self.velocity
        self.velocity = (0, vy)
        self.image = self.standRight if direction == 1 else self.standLeft
        if (len(self.bombs) == 0): self.bombs.add(Bomb(self))

class Bomb(GameObject): 
    @staticmethod
    def init():
        Bomb.image = pygame.image.load('images/bomb.png').convert_alpha()

    def __init__(self, bomber):
        super(Bomb, self).__init__(bomber.x, bomber.y, Bomb.image, 10)
        self.direction = bomber.direction
        vx = random.randint(2,4)
        self.velocity = (vx, -10) if self.direction == 1 else (-vx, -10)
        self.frame = 0

    def update(self, screenHeight, screenWidth):
        super(Bomb, self).update(screenWidth, screenHeight)
        self.frame += 1
        if (self.y > screenHeight): 
            self.kill()
        if (self.frame == 20): 
            vx, vy = self.velocity
            self.velocity = (vx, -vy)

class Jumper(Enemy): 
    @staticmethod
    def init():
        Jumper.image = pygame.image.load('images/jumper.png').convert_alpha()
        Jumper.jump = pygame.image.load('images/jumper2.png').convert_alpha()

    def __init__(self, x, y):
        super(Jumper, self).__init__(x, y, pygame.transform.flip(Jumper.image, True, False), pygame.transform.flip(Jumper.jump, True, False))
        self.velocity = (-2,-5)
        self.direction = -1

    def update(self, player, screenWidth, screenHeight):
        super(Jumper, self).update(screenWidth, screenHeight)
        self.frame += 1
        vx, vy = self.velocity
        if (vy == 5):
            self.image = self.right_image if self.direction == 1 else self.left_image
        elif (vy == -5): 
            self.image = self.walkRight if self.direction == 1 else self.walkLeft
        if (self.frame == 30): #y-direction
            vx, vy = self.velocity
            self.velocity = (vx, -vy)
            self.frame = 0
        if self.x >= 5*screenWidth or self.x <= 0 or self.x >= self.originalX + 200 or self.x <= self.originalX - 200:#x-direction
            (vx, vy) = self.velocity
            self.velocity = (-vx, vy)
            self.direction = -self.direction

class FrontGate(GameObject): 
    @staticmethod
    def init():
        FrontGate.image = pygame.image.load('images/door2.png').convert_alpha()

    def __init__(self, x, y):
        super(FrontGate, self).__init__(x, y, FrontGate.image, 10)
        self.width, self.height = self.image.get_size()

class Door(GameObject): 
    @staticmethod
    def init():
        Door.image = pygame.image.load('images/door.png').convert_alpha()

    def __init__(self, x, y):
        super(Door, self).__init__(x, y, Door.image, 10)
        self.width, self.height = self.image.get_size()

class Martini(GameObject): 
    @staticmethod
    def init():
        Martini.image1 = pygame.image.load('images/martini.png').convert_alpha()
        Martini.image2 = pygame.image.load('images/martini2.png').convert_alpha()

    def __init__(self, x, y):
        super(Martini, self).__init__(x, y, Martini.image1, 10)
        self.frame = 0

    def update(self, screenHeight, screenWidth):
        super(Martini, self).update(screenWidth, screenHeight)
        self.frame += 1
        if (self.frame <= 25):
            self.image = Martini.image1
        elif (25 <= self.frame < 50):
            self.image = Martini.image2 
        if self.frame == 50: self.frame = 0 

class Slenderman(GameObject): 
    @staticmethod
    def init():
        Slenderman.image = pygame.transform.scale(pygame.image.load('images/slenderman.png').convert_alpha(), (24, 118))

    def __init__(self, x, y):
        super(Slenderman, self).__init__(x, y, Slenderman.image, 10)
        self.right_image = Slenderman.image #facing right
        self.left_image = pygame.transform.flip(Slenderman.image, True, False)
        self.direction = 1

    def update(self, screenHeight, screenWidth):
        super(Slenderman, self).update(screenWidth, screenHeight)
        self.image = self.right_image if self.direction == 1 else self.left_image

#Decorations
class Ceiling(GameObject): 
    @staticmethod
    def init():
        Ceiling.image = pygame.image.load('images/ceiling.png').convert_alpha()

    def __init__(self, x, y):
        super(Ceiling, self).__init__(x, y, Ceiling.image, 10)
        self.width, self.height = self.image.get_size()

class Pole(GameObject): 
    @staticmethod
    def init():
        Pole.image = pygame.image.load('images/pole.png').convert_alpha()

    def __init__(self, x, y):
        super(Pole, self).__init__(x, y, Pole.image, 10) 
        self.width, self.height = self.image.get_size()

class Floor(GameObject): 
    @staticmethod
    def init():
        Floor.image = pygame.image.load('images/floor.png').convert_alpha()

    def __init__(self, x, y):
        super(Floor, self).__init__(x, y, Floor.image, 10) 
        self.width, self.height = self.image.get_size()

class Bench(GameObject): 
    @staticmethod
    def init():
        Bench.image = pygame.image.load('images/bench.png').convert_alpha()

    def __init__(self, x, y):
        super(Bench, self).__init__(x, y, Bench.image, 10)
        self.width, self.height = self.image.get_size()

class Bookshelf1(GameObject): 
    @staticmethod
    def init():
        Bookshelf1.image = pygame.image.load('images/bookshelf.png').convert_alpha()

    def __init__(self, x, y):
        super(Bookshelf1, self).__init__(x, y, Bookshelf1.image, 10)
        self.width, self.height = self.image.get_size()

class Bookshelf2(GameObject): 
    @staticmethod
    def init():
        Bookshelf2.image = pygame.image.load('images/bookshelf2.png').convert_alpha()

    def __init__(self, x, y):
        super(Bookshelf2, self).__init__(x, y, Bookshelf2.image, 10)
        self.width, self.height = self.image.get_size()

class Clock(GameObject): 
    @staticmethod
    def init():
        Clock.image = pygame.image.load('images/clock.png').convert_alpha()

    def __init__(self, x, y):
        super(Clock, self).__init__(x, y, Clock.image, 10)
        self.width, self.height = self.image.get_size()

class Hanger(GameObject): 
    @staticmethod
    def init():
        Hanger.image = pygame.image.load('images/hanger.png').convert_alpha()

    def __init__(self, x, y):
        super(Hanger, self).__init__(x, y, Hanger.image, 10)
        self.width, self.height = self.image.get_size()

class Recording(GameObject): 
    @staticmethod
    def init():
        Recording.image = pygame.image.load('images/recording.png').convert_alpha()

    def __init__(self, x, y):
        super(Recording, self).__init__(x, y, Recording.image, 10)
        self.width, self.height = self.image.get_size()

class Window1(GameObject): 
    @staticmethod
    def init():
        Window1.image = pygame.image.load('images/window.png').convert_alpha()

    def __init__(self, x, y):
        super(Window1, self).__init__(x, y, Window1.image, 10)
        self.width, self.height = self.image.get_size()

class Window2(GameObject): 
    @staticmethod
    def init():
        Window2.image = pygame.image.load('images/window2.png').convert_alpha()

    def __init__(self, x, y):
        super(Window2, self).__init__(x, y, Window2.image, 10)
        self.width, self.height = self.image.get_size()

class Princess(GameObject):
    @staticmethod
    def init():
        Princess.image = pygame.transform.flip(pygame.image.load('images/princess.png').convert_alpha(), True, False)

    def __init__(self, x, y):
        super(Princess, self).__init__(x, y, Princess.image, 10)
        self.width, self.height = self.image.get_size()

class Page(GameObject):
    @staticmethod
    def init():
        Page.image1 = pygame.transform.scale(pygame.image.load('images/page1.png').convert_alpha(), (40, 55))
        Page.image2 = pygame.transform.scale(pygame.image.load('images/page2.png').convert_alpha(), (40, 55))
        Page.image3 = pygame.transform.scale(pygame.image.load('images/page3.png').convert_alpha(), (40, 55))
        Page.image4 = pygame.transform.scale(pygame.image.load('images/page4.png').convert_alpha(), (40, 55))
        Page.image5 = pygame.transform.scale(pygame.image.load('images/page5.png').convert_alpha(), (40, 55))
        Page.image6 = pygame.transform.scale(pygame.image.load('images/page6.png').convert_alpha(), (40, 55))
        Page.image7 = pygame.transform.scale(pygame.image.load('images/page7.png').convert_alpha(), (40, 55))
        Page.image8 = pygame.transform.scale(pygame.image.load('images/page8.png').convert_alpha(), (40, 55))

    def __init__(self, x, y):
        image = random.choice([Page.image1, Page.image2, Page.image3, Page.image4, Page.image5, Page.image6, Page.image7, Page.image8])
        super(Page, self).__init__(x, y, image, 10)
        self.width, self.height = self.image.get_size()

class Freddy(GameObject):
    @staticmethod
    def init():
        Freddy.image = pygame.transform.scale(pygame.image.load('images/freddy.png').convert_alpha(), (90, 100))

    def __init__(self, x, y):
        super(Freddy, self).__init__(x, y, Freddy.image, 10)
        self.width, self.height = self.image.get_size()

class Grave(GameObject):
    @staticmethod
    def init():
        Grave.image = pygame.transform.scale(pygame.image.load('images/grave.png').convert_alpha(), (50, 72))

    def __init__(self, x, y):
        super(Grave, self).__init__(x, y, Grave.image, 10)
        self.width, self.height = self.image.get_size()

class BloodWall(GameObject):
    @staticmethod
    def init():
        BloodWall.image = pygame.image.load('images/bloodWall.png').convert_alpha()

    def __init__(self, x, y):
        super(BloodWall, self).__init__(x, y, BloodWall.image, 10)
        self.width, self.height = self.image.get_size()