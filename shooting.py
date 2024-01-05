import pygame
import os
import random
from bullets import Bullets

class Shooting(pygame.sprite.Sprite):
    VEL = 20
    WIDTH, HEIGHT = 1400, 700
    def __init__(self, x, y, health=5):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = 80
        self.height = 65
        self.speed = self.VEL 
        self.health = health
        self.speed_boost = 400
        self.original_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "speed.png")).convert_alpha(), (self.width, self.height))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))

    @classmethod
    def create_random_speed(cls):
        instance = cls(0, 0)
        x = cls.WIDTH
        y = random.randint(0, cls.HEIGHT - instance.height)
        return cls(x, y)
    

    def handle_player_bullets(self, main_bullets):
        for main_bullet in main_bullets:
            if self.rect.colliderect(main_bullet.rect):
                if isinstance(main_bullet, Bullets):
                    main_bullets.remove(main_bullet)

    def update(self):
        self.rect.x -= self.speed