import pygame
import sys
from typing import Any





# Creamos la plataforma, o nave.

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        imagenes_cargadas = pygame.image.load("imagenes/nave.png")
        self.image = pygame.transform.scale(imagenes_cargadas, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
        self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, *args: Any, **kwargs: Any):
        teclas = args[0]
        pantalla = pygame.display.get_surface()
        
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 7
            self.rect.x = max(0, self.rect.x)
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 7
            self.rect.x = min(pantalla.get_width()-self.image.get_width(), self.rect.x)
        if teclas[pygame.K_UP]:
            self.rect.y -= 7
            self.rect.y = max(0, self.rect.y)
        if teclas[pygame.K_DOWN]:
            self.rect.y += 7
            self.rect.y = min(pantalla.get_height()-self.image.get_height(), self.rect.y)
        self.mask = pygame.mask.from_surface(self.image)

     
# Creamos el fondo
        
class Fondo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        imagen = pygame.image.load("imagenes/cielo.jpg")
        pantalla = pygame.display.get_surface()
        self.image = pygame.transform.scale(imagen, (pantalla.get_width(), pantalla.get_height()))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0,0)

# Creamos meteoritos 
        
class Meteorito(pygame.sprite.Sprite):
    def __init__(self, posicion_spawn):
        super().__init__()
        imagen = pygame.image.load("imagenes/meteoro.png")
        posicion_spawn = posicion_spawn
        self.image = imagen
        self.image = pygame.transform.rotate(imagen, (-42))
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion_spawn
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, *args: Any, **kwargs: Any):
        self.rect.y += 4

# Creamos Astronautas

class Atronauta(pygame.sprite.Sprite):
    def __init__(self, posicion_spawn):
        super().__init__()
        imagen = pygame.image.load("imagenes/astronauta.png")
        posicion_spawn = posicion_spawn
        self.imagen_escalada = pygame.transform.scale(imagen, (80, 80))
        self.image = self.imagen_escalada
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion_spawn
        self.rotacion = 0
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, *args: Any, **kwargs: Any):
        self.rotacion += 2
        self.image = pygame.transform.rotate(self.imagen_escalada, (self.rotacion))
        self.rect.y += 2
        self.rect = self.image.get_rect(center=self.rect.center)

class Vacio(pygame.sprite.Sprite):
    def __init__(self, posicion_vacio):
        super().__init__()
        self.rect = pygame.Rect(posicion_vacio, (900, 50))
        
class Texto:
    def __init__(self, contenido, contador, x, y, color=(255, 255, 255), tamaño=10):
        self.contenido = contenido
        self.contador = contador
        self.color = color
        self.tamaño = tamaño
        self.font = pygame.font.Font(None, tamaño) 
        self.surface = self.font.render(contenido, True, color)
        self.rect = self.surface.get_rect()
        self.rect.center = (x, y)