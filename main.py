import pygame
import os
import math
import random
from enemy import Enemy
from spaceship import Spaceship
from bullets import Bullets
from enemybullets import EnemyBullets

WIDTH, HEIGHT = 1400, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

FPS = 60
VEL = 5

BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets", "stars.png")).convert()
BACKGROUND_IMAGE_WIDTH = BACKGROUND_IMAGE.get_width()



pygame.font.init()
font = pygame.font.Font(None, 36)


def draw_window(spaceship, enemies, bullets, enemy_bullets, scroll, phase, phase_timer, score):
    for i in range(0, math.ceil(WIDTH / BACKGROUND_IMAGE_WIDTH) + 1):
        WIN.blit(BACKGROUND_IMAGE, (i * BACKGROUND_IMAGE_WIDTH + scroll, 0))

    WIN.blit(spaceship.image, spaceship.rect)

    spaceship.draw_health_bar(WIN)

    for enemy in enemies:
        WIN.blit(enemy.image, enemy.rect)

    for bullet in bullets:
        WIN.blit(bullet.image, bullet.rect)

    for enemy_bullet in enemy_bullets:
        WIN.blit(enemy_bullet.image, enemy_bullet.rect)

    phase_text = font.render(f"Phase {phase}", True, (255, 255, 255))
    WIN.blit(phase_text, (700, 10))

    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    WIN.blit(score_text, (10, 10))

    timer_text = font.render(f"Timer: {int(phase_timer)} seconds", True, (255, 255, 255))
    WIN.blit(timer_text, (10, 50))

    pygame.display.update()

def draw_game_over():
    game_over = font.render("Game Over", True, (255, 255, 255))
    WIN.blit(game_over, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
    play_again = font.render("Press 'P' to play again", True, (255, 255, 255))
    WIN.blit(play_again, (WIDTH // 2 - 140, HEIGHT // 2 + 20))
    exit_text = font.render("Press 'Q' to exit", True, (255, 255, 255))
    WIN.blit(exit_text, (WIDTH // 2 - 100, HEIGHT // 2 + 60))

def main():
    spaceship = Spaceship(100, 300)
    enemies = []
    bullets = []
    enemy_bullets = []
    

    phase = 1
    phase_timer = 20
    enemy_spawn_timer = 0
    enemy_spawn_interval = 50
    enemies_per_phase = 3  
    enemies_spawned = 0

    score = 0

    clock = pygame.time.Clock()
    scroll = 0

    run = True
    game_over = False

    while run and not game_over:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        phase_timer -= 1 / FPS  
        if phase_timer <= 0:
            phase += 1
            phase_timer = 20  
            enemies_per_phase += 3  
            enemies_spawned = 0  

            
            if phase % 3 == 0:
                EnemyBullets.base_speed += 2  

        keys_pressed = pygame.key.get_pressed()
        bullet = spaceship.handle_movement(keys_pressed)

        scroll -= 5
        if abs(scroll) > BACKGROUND_IMAGE_WIDTH:
            scroll = 0

        if bullet:
            bullets.append(bullet)

        
        for bullet in bullets:
            bullet.update()

        for enemy_bullet in enemy_bullets:
            enemy_bullet.update()

        
        for enemy in enemies:
            enemy.handle_shooting(enemy_bullets)
            enemy.handle_player_bullets(bullets)
            enemy.update(enemies)
            enemy.rect.x -= VEL * 2

            if enemy.is_destroyed:
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - enemy.destroyed_time

                if elapsed_time > 200:
                    score += 1
                
 
        spaceship.handle_enemy_bullets(enemy_bullets)

        
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval and enemies_spawned < enemies_per_phase:
            enemies.append(Enemy.create_random_enemy())
            enemy_spawn_timer = 0
            enemies_spawned += 1

        
        draw_window(spaceship, enemies, bullets, enemy_bullets, scroll, phase, phase_timer, score)

        if spaceship.remaining_health <= 0:
            draw_game_over()
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        game_over = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            main()  
                        elif event.key == pygame.K_q:
                            pygame.quit()

    pygame.quit()


if __name__ == "__main__":
    main()
