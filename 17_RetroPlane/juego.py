
import random
import pygame, sys
from elements import Aircraft, Background, Enemy, EnemyBullet, bullet_group, enemy_bullet_group, enemy_group, aircraft_sprites, explosion_group, score

background = Background()
aircraft = Aircraft()
aircraft_sprites.add(aircraft)


start_time = pygame.time.get_ticks()
start_time_bullet = pygame.time.get_ticks()
pygame.init()


exit = False
clock = pygame.time.Clock()
FPS = 60

while not exit:
    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    def create_enemies():              
        enemy = Enemy(random.randint(70, 300), 10)
        enemy_group.add(enemy)
    
    
    current_time = pygame.time.get_ticks()
    current_time_bullet = pygame.time.get_ticks()
    
    lapsed_time = current_time - start_time
    lapsed_time_bullet = current_time_bullet - start_time_bullet
    cooldown_respawn = 5000
    cooldown_shot = 1000
    
    if score >= 10:
        cooldown_respawn = 2000
        cooldown_shot = 300
        
    if lapsed_time >= cooldown_respawn:
        create_enemies()
        start_time = current_time
    
    if lapsed_time_bullet >=  cooldown_shot:
        attacking_enemy = enemy_group.sprites()

        if attacking_enemy:
            attacking_enemies = attacking_enemy[0]
            enemy_bullet = EnemyBullet(attacking_enemies.rect.centerx, attacking_enemies.rect.bottom)
            enemy_bullet_group.add(enemy_bullet)
            start_time_bullet = current_time_bullet

     
   
    aircraft_sprites.update()
    bullet_group.update()
    enemy_group.update()
    enemy_bullet_group.update()
    explosion_group.update()
    background.scrollback()
    background.changebg()
    background.draw_score()
    background.draw_health()
    explosion_group.draw(background.screen)
    aircraft_sprites.draw(background.screen)
    bullet_group.draw(background.screen)
    enemy_group.draw(background.screen)
    enemy_bullet_group.draw(background.screen)
    
    pygame.display.flip()

pygame.quit()