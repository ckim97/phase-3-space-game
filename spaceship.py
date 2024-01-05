import pygame
import os
from bullets import Bullets
from enemybullets import EnemyBullets

class Spaceship(pygame.sprite.Sprite):
    VEL = 10  
    WIDTH, HEIGHT = 1400, 700

    def __init__(self, x, y, health=100):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = 95
        self.height = 80
        self.vel_x = 0
        self.vel_y = 0
        self.image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "spaceship.png")).convert_alpha(), (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.starting_health = health
        self.remaining_health = health
        self.health_bar_width = 10
        self.health_bar_height = 50
        self.bullet_cooldown = 600  
        self.last_shot = pygame.time.get_ticks() 
        self.boost_duration = 20  
        self.boost_active = False
        self.boost_start_time = 0
        self.boost_value = 0

    def draw_health_bar(self, window):
        health_height = int((self.remaining_health / self.starting_health) * self.health_bar_height)
        green_health_rect = pygame.Rect(self.rect.x - 10, self.rect.y + 15 + self.health_bar_height - health_height, self.health_bar_width, health_height)
        red_health_rect = pygame.Rect(self.rect.x - 10, self.rect.y + 15, self.health_bar_width, self.health_bar_height - health_height)
        pygame.draw.rect(window, (0, 255, 0), green_health_rect)
        pygame.draw.rect(window, (255, 0, 0), red_health_rect)

    def heal(self, healing_amount):
        self.remaining_health = min(self.remaining_health + healing_amount, 100)

    def shooting_boost(self, speed_item):
        if not self.boost_active:
            self.boost_active = True
            self.boost_start_time = pygame.time.get_ticks()
            self.boost_value = speed_item

    def take_damage(self, damage):
        self.remaining_health -= damage
        if self.remaining_health < 0:
            self.remaining_health = 0

    def handle_enemy_bullets(self, enemy_bullets):
        for enemy_bullet in enemy_bullets:
            if self.rect.colliderect(enemy_bullet.rect):
                if isinstance(enemy_bullet, EnemyBullets):
                    self.take_damage(enemy_bullet.DAMAGE)
                    enemy_bullets.remove(enemy_bullet)

    def handle_movement(self, keys_pressed):
        bullet = None

        if self.boost_active:
            current_time = pygame.time.get_ticks()
            elapsed_time = (current_time - self.boost_start_time) / 1000  # Convert milliseconds to seconds
            if elapsed_time >= self.boost_duration:
                self.boost_active = False
                self.boost_start_time = 0
            else:
                self.bullet_cooldown = 500 - self.boost_value

        else:
            self.bullet_cooldown = 500  # Reset to the original value when boost is not active


        if keys_pressed[pygame.K_a] and self.rect.x - Spaceship.VEL > 0:
            self.vel_x = -Spaceship.VEL
        elif keys_pressed[pygame.K_d] and self.rect.x + Spaceship.VEL < Spaceship.WIDTH - self.width:
            self.vel_x = Spaceship.VEL
        else:
            self.vel_x = 0

        if keys_pressed[pygame.K_w] and self.rect.y - Spaceship.VEL > 0:
            self.vel_y = -Spaceship.VEL
        elif keys_pressed[pygame.K_s] and self.rect.y + Spaceship.VEL < Spaceship.HEIGHT - self.height:
            self.vel_y = Spaceship.VEL
        else:
            self.vel_y = 0
        
        if keys_pressed[pygame.K_w]:
            self.vel_y = -Spaceship.VEL
        if keys_pressed[pygame.K_s]:
            self.vel_y = Spaceship.VEL
        if keys_pressed[pygame.K_a]:
            self.vel_x = -Spaceship.VEL
        if keys_pressed[pygame.K_d]:
            self.vel_x = Spaceship.VEL

        if keys_pressed[pygame.K_9]:
            self.remaining_health = self.starting_health

        if keys_pressed[pygame.K_LSHIFT]:
            Spaceship.VEL = 15
        else:
            Spaceship.VEL = 10

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        self.rect.x = max(0, min(Spaceship.WIDTH - self.width, self.rect.x))
        self.rect.y = max(0, min(Spaceship.HEIGHT - self.height, self.rect.y))

        time_now = pygame.time.get_ticks()
        if keys_pressed[pygame.K_SPACE] and time_now - self.last_shot > self.bullet_cooldown:
            bullet = Bullets(self.rect.x + self.width, self.rect.y + self.height // 2)
            self.last_shot = time_now

        return bullet
