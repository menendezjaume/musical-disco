from typing import Any
import pygame
from pygame.sprite import  Group
import math

class Planeta(pygame.sprite.Sprite):
    #Constructor de la Nave
    def __init__(self, posicion, *args):
        super().__init__()
        #cargamos las imagenes
        self.ricardo = pygame.image.load("PlanetaF1.png")
        self.ricardo2 = pygame.transform.scale(self.ricardo, (140,140)).convert_alpha()
        self.image = self.ricardo2
        #Añadimos una mascara
        self.mask = pygame.mask.from_surface(self.image)
        #Rectangulo para la imagen
        self.rect = self.image.get_rect()
        #Actualizamos el rectangulo para que coincida con la imagen
        self.rect.center = posicion
        #Disparos
        self.ultimo_disparo = 0
        
        
    def update(self, *args: any, **kwargs: any):
        #Capturamos running
        running = args[4]
        #Capturamos X e Y
        x = args[5]
        y = args[6]
        #Capturamos las teclas y el raton
        teclas = args[0]
        click_izdo, click_central, click_dcho = args[9]
        #Capturamos a Todos
        grupo_sprites_todos = args[1]
        #Capturamos las Balas
        grupo_sprites_balas = args[2]
        #Capturamos los Enemigos
        grupo_sprites_enemigos = args[3]
        #Capturamos la posicion del mouse
        pos = args[7]
        #Calculamos el angulo del planeta
        x_dist = pos[0] - x
        y_dist = -(pos[1] - y)
        self.angulo = math.degrees(math.atan2(y_dist, x_dist))
        #Rotacion del Planeta
        self.mask =  pygame.mask.from_surface(self.image)
        self.image = pygame.transform.rotate(self.ricardo2, self.angulo - 90)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center = self.rect.center)
        #Video del movimiento de raton
        #https://www.youtube.com/watch?v=WnIycS9Gf_c
        #Gestionamos el Raton y las teclas
        if click_izdo:
            #Disparar
            self.disparar(grupo_sprites_todos,grupo_sprites_balas)
        
    def disparar(self, grupo_sprites_todos, grupo_sprites_balas,):
        momento_actual = pygame.time.get_ticks()
        if momento_actual > self.ultimo_disparo + 200:     
            nueva_bala = Bala((self.rect.centerx, self.rect.centery), self.angulo + 90)
            grupo_sprites_balas.add(nueva_bala)
            grupo_sprites_todos.add(nueva_bala)
            self.ultimo_disparo = momento_actual 
            
class Fondo(pygame.sprite.Sprite):
    
    def __init__(self,) -> None:
        super().__init__()
        #Cargamos la imagen del Fondo
        paco = pygame.image.load("fondoF.png")
        #Capturamos la Pantalla
        pantalla = pygame.display.get_surface()
        self.image = pygame.transform.scale(paco,(pantalla.get_width(), pantalla.get_height()))
        #Creamos un Rectangulo
        self.rect = self.image.get_rect()
        #Actualizamos su posición
        self.rect.topleft = (0,0)

class Bala(pygame.sprite.Sprite):
    
    def __init__(self, posicion, angulo) -> None:
        super().__init__()
        #Añadimos la imagen de la bala
        bala_imagen = pygame.image.load("BalaF.png")
        self.image = pygame.transform.scale(bala_imagen, (20,20))
        self.image = pygame.transform.rotate(self.image, angulo + 180)
        #Añadimos una mascara
        self.mask = pygame.mask.from_surface(self.image)
        #Añadimos el rectangulo
        self.rect = self.image.get_rect()
        self.rect.center = posicion
        self.angulo = angulo
        
        
    def update(self, *args: Any, **kwargs: Any) -> None:
        rad_angle = math.radians(self.angulo)
        self.rect.x += 6 * math.sin(rad_angle)
        self.rect.y += 6 * math.cos(rad_angle)
        
  
class Enemigo(pygame.sprite.Sprite):
    
    def __init__(self,posicion) -> None:
        super().__init__()
        #Cargamos la imagen del Enemigo
        messi = pygame.image.load("enemigoM.png")
        self.image = pygame.transform.scale(messi, (120,120))
        #Creamos el Rectangulo
        self.rect = self.image.get_rect()
        #Actualizamos su posicion 
        self.rect.topleft = posicion
        #Añadimos el angulo
        self.angle = 0
        self.velocidad = 1.75

            
    
    def movimiento_enemigo(self, planeta):
        #Calculamos el angulo de los enemigos
        angle = math.atan2(planeta.rect.centery - self.rect.centery, planeta.rect.centerx - self.rect.centerx)
        #Actualizamos las coordenadas
        self.rect.x += self.velocidad * math.cos(angle)
        self.rect.y += self.velocidad * math.sin(angle)
        
    
    def update(self, *args: Any, **kwargs: Any) :
        self.mask =  pygame.mask.from_surface(self.image)
        self.image = pygame.transform.rotate(self.image, +self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.rect.center)
        score = args[10]
        grupo_sprites_balas = args[2]
        bala_colision = pygame.sprite.spritecollideany(self, grupo_sprites_balas, pygame.sprite.collide_mask)
        if bala_colision:
            self.kill()
            bala_colision.kill()
            score[0] += 10
    
class Enemigo_Especial(pygame.sprite.Sprite):

    def __init__(self,posicion) -> None:
        super().__init__()
        #Cargamos la Imagen
        cristiano = pygame.image.load("EnemigoEspeF.png")
        self.image = pygame.transform.scale(cristiano, (120,120))
        #Creamos el Rectangulo
        self.rect = self.image.get_rect()
        #Actualizamos su posicion 
        self.rect.topleft = posicion
        #Añadimos el angulo
        self.angle = 0
        self.velocidad = 2
    
    def movimiento_enemigo(self, planeta):
        #Calculamos el angulo de los enemigos
        angle = math.atan2(planeta.rect.centery - self.rect.centery, planeta.rect.centerx - self.rect.centerx)
        #Actualizamos las coordenadas
        self.rect.x += self.velocidad * math.cos(angle)
        self.rect.y += self.velocidad * math.sin(angle)

    def update(self, *args: Any, **kwargs: Any) :
        self.mask =  pygame.mask.from_surface(self.image)
        self.image = pygame.transform.rotate(self.image, +self.angle)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=self.rect.center)
        score = args[10]
        grupo_sprites_balas = args[2]
        bala_colision = pygame.sprite.spritecollideany(self, grupo_sprites_balas, pygame.sprite.collide_mask)
        if bala_colision:
            self.kill()
            bala_colision.kill()
            score[0] += 100