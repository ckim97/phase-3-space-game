import pygame
import os
import random
from bullets import Bullets

class Health(pygame.sprite.Sprite):
    VEL = 15
    WIDTH, HEIGHT = 1400, 700
    def __init__(self, x, y, health=5):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = 200
        self.height = 185
        self.speed = self.VEL 
        self.health = health
        self.healing = 25
        self.original_image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "health.png")).convert_alpha(), (self.width, self.height))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))

    @classmethod
    def create_random_health(cls):
        instance = cls(0, 0)
        x = cls.WIDTH
        y = random.randint(0, cls.HEIGHT - instance.height)
        return cls(x, y)
    

    def handle_player_bullets(self, main_bullets):
        for main_bullet in main_bullets:
            if self.rect.colliderect(main_bullet.rect):
                if isinstance(main_bullet, Bullets):
                    self.take_damage(main_bullet.DAMAGE)
                    main_bullets.remove(main_bullet)

    def update(self):
        self.rect.x -= self.speed