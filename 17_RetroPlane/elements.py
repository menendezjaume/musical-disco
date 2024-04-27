import random
import pygame

bullet_group = pygame.sprite.Group()
enemy_group =  pygame.sprite.Group()
enemy_bullet_group =  pygame.sprite.Group()
aircraft_sprites = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()

score = 0
font_name = pygame.font.match_font('arial')
def increment_score(points):
    global score
    score += points
    return score

class Aircraft(pygame.sprite.Sprite):
    def __init__(self):# alien_group
        super().__init__()
        
        self.sprites_movement = [
            pygame.transform.scale(pygame.image.load("17_RetroPlane/aircraft_img/avion-left.png"), (95,90)),
            pygame.transform.scale(pygame.image.load("17_RetroPlane/aircraft_img/avion-right.png"), (95,90))]
    
    
        self.sprites = [
            pygame.image.load("17_RetroPlane/aircraft_img/avion1.png"),
            pygame.image.load("17_RetroPlane/aircraft_img/avion2.png")
        ]
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = (200, 800)
        self.health = 3
        self.final_shot = pygame.time.get_ticks()
        
           
    def update(self):
        keys = pygame.key.get_pressed()
        pantalla = pygame.display.get_surface()
        speed = 3
        cooldown = 1000
        
        self.mask = pygame.mask.from_surface(self.image) 
        
        if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.animate()
        
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
            self.image = self.sprites_movement[0]
        
        if keys[pygame.K_RIGHT] and self.rect.x + self.image.get_width() < pantalla.get_width():
            self.rect.x += speed
            self.image = self.sprites_movement[1]
        
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= speed
            self.animate()
            
        if keys[pygame.K_DOWN] and self.rect.y + self.image.get_height() < pantalla.get_height():
            self.rect.y += speed
            self.animate()
        time_now = pygame.time.get_ticks()
        if score >= 10:
            cooldown = 200
        if keys[pygame.K_SPACE] and time_now - self.final_shot > cooldown: 
            bullet = Bullet(self.rect.centerx, self.rect.top) 
            bullet_group.add(bullet)
            self.final_shot = time_now 
            bullet.update() 
    
        if pygame.sprite.spritecollide(self, enemy_group, True,  pygame.sprite.collide_mask):
              self.kill()
              explosion = Explosion(self.rect.centerx, self.rect.centery)
              explosion_group.add(explosion)
              self.health = 0
            
        self.mask = pygame.mask.from_surface(self.image)
        if score == 10:
            self.sprites.clear()
    def animate(self):
        if score >= 10 and score < 20:
            self.sprites = [
                pygame.image.load("17_RetroPlane/aircraft_img/player.png"),
                pygame.image.load("17_RetroPlane/aircraft_img/player1.png")
            ]
            self.sprites_movement = [
                pygame.transform.scale(pygame.image.load("17_RetroPlane/aircraft_img/player3.png"), (95,90)),
                pygame.transform.scale(pygame.image.load("17_RetroPlane/aircraft_img/player2.png"), (95,90))
            ]
        if score == 20:
            self.sprites = [
                pygame.image.load("17_RetroPlane/aircraft_img/e1.png"),
                pygame.image.load("17_RetroPlane/aircraft_img/e2.png")
            ]
            self.sprites_movement = [
                pygame.transform.scale(pygame.image.load("17_RetroPlane/aircraft_img/e4.png"), (95,90)),
                pygame.transform.scale(pygame.image.load("17_RetroPlane/aircraft_img/e3.png"), (95,90))
            ]
            
        self.current_sprite += 1
        if self.current_sprite > 1:
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.image = pygame.transform.scale(self.image, (95, 90))
        
    def create_bullet(self):
        return Bullet(self.rect.x,self.rect.y)
        
aircraft = Aircraft()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("17_RetroPlane/aircraft_img/bullet.png"), (20, 30))
        if score >= 10 and score < 13:
            self.image = pygame.transform.scale(pygame.image.load("17_RetroPlane/aircraft_img/avion-bullet.png"), (70, 70))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        

    def update(self):
        self.rect.y -= 5
        if self.rect.y < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, enemy_group, True,  pygame.sprite.collide_mask):
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            explosion_group.add(explosion)
            increment_score(1) 
                
                
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()       
        self.image = pygame.transform.scale(pygame.image.load("17_RetroPlane/enemy_img/e"+ str(random.randint(1, 2))+".png"),(110, 100))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.speed = 2
        if score >= 10:
            self.speed = 4
        self.ticks_final = pygame.time.get_ticks()
    def update(self):
        self.rect.y += 3
        self.rect.x += self.speed
        self.mask = pygame.mask.from_surface(self.image)
        pantalla = pygame.display.get_surface()
        self.ticks = pygame.time.get_ticks()
        self.cooldown = 900

        if self.rect.left < 0 or self.rect.right - self.image.get_width() > random.randint(300,482) and self.ticks - self.ticks_final >= self.cooldown:
            self.speed *= -1
            self.ticks = self.ticks_final
        if self.rect.x  + self.image.get_width()< 0 or self.rect.y + self.image.get_height() > pantalla.get_height() + 30:
            self.kill()
    
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self,x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("17_RetroPlane/enemy_img/enemy_bullet.png"), (20, 30))
        if score >= 10:
            self.image = pygame.transform.scale(pygame.image.load("17_RetroPlane/aircraft_img/bullet2.png"), (20, 30))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y] 
        
        
    def update(self):
        pantalla = pygame.display.get_surface()
        self.rect.y += 7
        if self.rect.y > pantalla.get_height():
            self.kill()
        if pygame.sprite.spritecollide(self, aircraft_sprites, False, pygame.sprite.collide_mask):
            self.kill()
            explosion = Explosion(self.rect.centerx, self.rect.centery)
            explosion_group.add(explosion)
            aircraft.health -= 1
            print(aircraft.health)
          
class Explosion(pygame.sprite.Sprite):
    def __init__(self,x, y):
        super().__init__()
        self.images = []
        for n in range(1, 10):
            img = pygame.image.load(f"17_RetroPlane/explosion/Circle_explosion{n}.png")
            self.images.append(img)
            self.count = 0
        self.image = self.images[self.count]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
    
    def update(self):
        speed = 3
        
        self.counter += 1
        if self.counter >= speed and self.count < len(self.images) - 1:
            self.counter = 0
            self.count += 1
            self.image =self.images[self.count]

        if self.count >= len(self.images) - 1 and  self.counter >= speed:
            self.kill()
     
class Background:
    
    def __init__(self) -> None:
        width = 482
        height = 892
        self.screen = pygame.display.set_mode((width,height))
        self.bg = pygame.image.load("17_RetroPlane/frame.png").convert()
        self.bg_height = self.bg.get_height()
        self.scroll = 0

    def scrollback(self):
        self.scroll += 1.5
        if self.scroll > self.bg_height:
            self.scroll = 0
        self.screen.blit(self.bg, (0, self.scroll - self.bg_height))
        self.screen.blit(self.bg, (0, self.scroll))
    def draw_score(self):
        font = pygame.font.Font(font_name, 36)
        text_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 10)
        self.screen.blit(text_surface, text_rect)

    def draw_health(self):
        font = pygame.font.Font(font_name, 36)
        text_surface = font.render(f"Health: {aircraft.health}", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (10, 60)
        self.screen.blit(text_surface, text_rect)
        if  aircraft.health == 0:
            pygame.quit()

    
    def changebg(self):
        if score == 10: 
            self.bg = pygame.image.load("17_RetroPlane/frame2.png").convert()
        if score == 20: 
            self.bg = pygame.image.load("17_RetroPlane/frame3.png").convert()