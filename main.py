import pygame
import os
import math
from enemy import Enemy
from spaceship import Spaceship
from bullets import Bullets
from enemybullets import EnemyBullets
from health import Health
from shooting import Shooting 

WIDTH, HEIGHT = 1400, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

FPS = 60
VEL = 5

BACKGROUND_IMAGE = pygame.image.load(os.path.join("Assets", "stars.png")).convert()
BACKGROUND_IMAGE_WIDTH = BACKGROUND_IMAGE.get_width()



pygame.font.init()
font = pygame.font.Font(None, 36)


def draw_window(spaceship, enemies, bullets, enemy_bullets, scroll, phase, phase_timer, score, health_items, speed_items):
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

    for health_item in health_items:
        WIN.blit(health_item.image, health_item.rect)

    for speed_item in speed_items:
        WIN.blit(speed_item.image, speed_item.rect)

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
    health_items = []
    speed_items = []

    health_item_created = False
    shooting_item_created = False
    

    phase = 1
    phase_timer = 20
    enemy_spawn_timer = 0
    enemy_spawn_interval = 50
    enemies_per_phase = 15  
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
            if event.type == pygame.QUIT:
                pygame.quit()
        



        phase_timer -= 1 / FPS  

        if not health_item_created and 9 <= phase_timer <= 10:
            health_items.append(Health.create_random_health())
            health_item_created = True 
        
        


        if phase_timer <= 0:
            phase += 1
            phase_timer = 20  
            enemies_per_phase += 3  
            enemies_spawned = 0  
            health_item_created = False
            shooting_item_created = False

            if not shooting_item_created and phase % 2 == 0:
                speed_items.append(Shooting.create_random_speed())
                shooting_item_created = True

            
            if phase % 3 == 0:
                EnemyBullets.base_speed += 2  

        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval and enemies_spawned < enemies_per_phase:
            enemies.append(Enemy.create_random_enemy())
            enemy_spawn_timer = 0
            enemies_spawned += 1

        keys_pressed = pygame.key.get_pressed()
        bullet = spaceship.handle_movement(keys_pressed)



        scroll -= 5
        if abs(scroll) > BACKGROUND_IMAGE_WIDTH:
            scroll = 0


        if bullet:
            bullets.append(bullet)

        for bullet in bullets:
            for speed_item in speed_items:
                if bullet.rect.colliderect(speed_item.rect):
                    spaceship.shooting_boost(speed_item.speed_boost)
                    speed_items.remove(speed_item)
                    bullets.remove(bullet)
                    break
        
        for speed_item in speed_items:
            speed_item.update()
     
        
        for bullet in bullets:  
            for health_item in health_items:
                if bullet.rect.colliderect(health_item.rect):
                    spaceship.heal(health_item.healing)
                    health_items.remove(health_item)
                    bullets.remove(bullet)
                    break  
            bullet.update()

        for health_item in health_items:
                health_item.update()

        for enemy_bullet in enemy_bullets:
            enemy_bullet.update()

        
        for enemy in enemies:
            enemy.handle_shooting(enemy_bullets)
            enemy.handle_player_bullets(bullets)
            enemy.update(enemies)
            enemy.rect.x -= VEL * 2

            if enemy.rect.right < 0:
                spaceship.take_damage(enemy.DAMAGE)
                enemies.remove(enemy)


            if enemy.is_destroyed:
                current_time = pygame.time.get_ticks()
                elapsed_time = current_time - enemy.destroyed_time

                if elapsed_time > 200:
                    score += 1
                
 
        spaceship.handle_enemy_bullets(enemy_bullets)

        
        draw_window(spaceship, enemies, bullets, enemy_bullets, scroll, phase, phase_timer, score, health_items, speed_items)

        if spaceship.remaining_health <= 0:
            draw_game_over()
            pygame.display.update()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                        game_over = True
                        pygame.quit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            main()  
                        elif event.key == pygame.K_q:
                            pygame.quit()

    pygame.quit()


if __name__ == "__main__":
    main()
