import pygame

#based on super Mario camera work, to scroll the player
#as well as http://stackoverflow.com/questions/14354171/add-scrolling-to-a-platformer-in-pygame

def RelRect(actor, camera):
    return pygame.Rect(actor.rect.x-camera.rect.x, actor.rect.y, actor.rect.w, actor.rect.h)

class Camera(object):
    def __init__(self, player, width, height):
        self.player = player
        self.rect = pygame.display.get_surface().get_rect()
        self.world = pygame.Rect(0, 0, width, height) 
        self.rect.center = self.player.rect.center
        
    def update(self):
        if self.player.rect.centerx > self.rect.centerx:
            self.rect.centerx = self.player.rect.centerx
        if self.player.rect.centerx < self.rect.centerx:
            self.rect.centerx = self.player.rect.centerx
        self.rect.clamp_ip(self.world)

    def draw_sprites(self, surf, sprites):
        for s in sprites:
            surf.blit(s.image, RelRect(s, self))
            #if s.rect.colliderect(self.rect):
            #    surf.blit(s.image, RelRect(s, self))
