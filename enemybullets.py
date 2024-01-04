import pygame
import os

class EnemyBullets(pygame.sprite.Sprite):
    DAMAGE = 5
    base_speed = 12  

    def __init__(self, x, y, phase=None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join("Assets", "enemy_bullet.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = self.calculate_speed(phase)

    def calculate_speed(self, phase):
        if phase is not None and phase % 10 == 0:
            return self.base_speed + 2  
        else:
            return self.base_speed

    def update(self):
        self.rect.x -= self.speed
