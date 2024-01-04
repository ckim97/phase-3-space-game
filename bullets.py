import pygame
import os

class Bullets(pygame.sprite.Sprite):
    DAMAGE = 5
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Assets", "Charge_1.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.x += 10