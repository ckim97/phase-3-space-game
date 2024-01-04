# import pygame
# import os

# class Enemy(pygame.sprite.Sprite):
#       WIDTH, HEIGHT = 1400, 700
#       def __init__(self, x, y, health=5):
#         pygame.sprite.Sprite.__init__(self)
#         self.x = x
#         self.y = y
#         self.health = health
#         self.original_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Assets", "enemy.png")).convert_alpha(), (self.width, self.height)), 180)