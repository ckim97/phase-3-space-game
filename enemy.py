import pygame
import os
import random
from bullets import Bullets
from enemybullets import EnemyBullets

class Enemy(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 1400, 700
    DAMAGE = 10
    def __init__(self, x, y, health=5):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = 85
        self.height = 70
        self.original_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join("Assets", "enemy.png")).convert_alpha(), (self.width, self.height)), 180)
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.last_shot = pygame.time.get_ticks()
        self.bullet_cooldown = 1000
        self.starting_health = health
        self.remaining_health = health
        self.show_collision_image = False
        self.collision_timer = 200
        self.last_collision_time = 0
        self.is_destroyed = False
        self.destroyed_time = 0  

    @classmethod
    def create_random_enemy(cls):
        instance = cls(0, 0)
        x = cls.WIDTH
        y = random.randint(0, cls.HEIGHT - instance.height)
        return cls(x, y)
    
    def handle_shooting(self, enemy_bullets):
        current_time = pygame.time.get_ticks()
        if not self.show_collision_image and current_time - self.last_shot > self.bullet_cooldown:
            enemy_bullet = EnemyBullets(self.rect.centerx, self.rect.centery)
            enemy_bullets.append(enemy_bullet)
            self.last_shot = current_time

    def handle_player_bullets(self, main_bullets):
        for main_bullet in main_bullets:
            if self.rect.colliderect(main_bullet.rect):
                if isinstance(main_bullet, Bullets):
                    self.take_damage(main_bullet.DAMAGE)
                    main_bullets.remove(main_bullet)

    def take_damage(self, damage):
        self.remaining_health -= damage
        if self.remaining_health <= 0:
            self.remaining_health = 0
            print(self.remaining_health)
            self.show_collision_image = True
            self.is_destroyed = True
            self.destroyed_time = pygame.time.get_ticks()  

            destroyed_image = pygame.transform.scale(
                pygame.transform.rotate(
                    pygame.image.load(os.path.join("Assets", "destroyed_enemy.png")).convert_alpha(),180), (self.width, self.height))
            self.image = destroyed_image
            self.rect = destroyed_image.get_rect(topleft=(self.rect.x, self.rect.y))

    def update(self, all_enemies):
        if self.show_collision_image:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - self.destroyed_time
            if self.remaining_health == 0 and elapsed_time > self.collision_timer:
                all_enemies.remove(self)
