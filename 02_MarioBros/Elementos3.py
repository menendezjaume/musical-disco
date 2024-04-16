from typing import Any
import pygame
import math

class Nave(pygame.sprite.Sprite,):
    def __init__(self, posicion) -> None:
        super().__init__()
        self.x=650
        self.y=650
        self.imagen=pygame.transform.scale( pygame.image.load("nave.png"),(70,90))
        self.contador_imagen = 0
        self.image = self.imagen

        self.mask=pygame.mask.from_surface(self.imagen)
        self.rect=self.imagen.get_rect()
        self.rect.topleft=posicion
        self.ultimo_disparo=0
    def update(self, *args: any, **kwargs: any):
        #capturamos teclas
        teclas=args[0]
        #capturamos pantalla
        pantalla=pygame.display.get_surface()
        self.mask=pygame.mask.from_surface(self.imagen)
        #gestionamos teclas
        limite_x = pantalla.get_width() - self.rect.width
        limite_y = pantalla.get_height() - self.rect.height
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 3
            limite = 0
            self.rect.x = max(self.rect.x, limite)
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 3
            pantalla = pygame.display.get_surface()
            limite = pantalla.get_width() - self.rect.width
            self.rect.x = min(self.rect.x, limite)
        if teclas[pygame.K_UP]:
            self.rect.y -= 3
            limite = 0
            self.rect.y = max(self.rect.y, limite)
        if teclas[pygame.K_DOWN]:
            self.rect.y += 3
            pantalla = pygame.display.get_surface()
            limite = pantalla.get_height() - self.rect.height
            self.rect.y = min(self.rect.y, limite)
        self.image = self.imagen

    def disparar(self,grupo_sprites):
        momento_actual=pygame.time.get_ticks()
        if momento_actual>self.ultimo_disparo+200:
            self.ultimo_disparo=momento_actual
        
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        
        self.imagen=pygame.transform.scale( pygame.image.load("roca.png"),(70,70))
        self.image=self.imagen
        self.mask=pygame.mask.from_surface(self.imagen)
        #creamos un rectangulo a partir de la imagen
        self.rect=self.image.get_rect()
        #actualizar posicion del rectangulo para que coincida con "posicion"
        self.rect.topleft=posicion
    def update(self, *args: any, **kwargs: any):
        self.rect.y +=1
        pantalla = pygame.display.get_surface()
        self.mask=pygame.mask.from_surface(self.imagen)
        self.image = self.imagen  
        if self.rect.y > pantalla.get_height():
            self.kill()
        #capturamos running
            running=args
class Astronauta(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        
        self.imagen=pygame.transform.scale( pygame.image.load("astro.png"),(65,90))
        self.image=self.imagen
        self.mask=pygame.mask.from_surface(self.imagen)
        
        self.rect=self.image.get_rect()
       
        self.rect.topleft=posicion
    def update(self, *args: any, **kwargs: any):
        self.rect.y +=1
        self.mask=pygame.mask.from_surface(self.imagen)
        pantalla = pygame.display.get_surface()
        self.image = self.imagen  
        if self.rect.y > pantalla.get_height():
            self.kill()
            running=args

class Fondo(pygame.sprite.Sprite):
    def __init__(self,posicion) -> None:
        super().__init__()
        self.image=pygame.image.load("fondo.png")
        pantalla=pygame.display.get_surface()
        self.fondo=pygame.transform.scale(
        self.image, (pantalla.get_width(), self.image.get_height()))
        self.rect=self.image.get_rect()
      
        self.rect.topleft=posicion
        
    def update(self, *args: Any, **kwargs: Any) -> None:
        pantalla=pygame.display.get_surface()
        pantalla.blit(self.fondo,((0,0)))  