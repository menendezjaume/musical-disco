import pygame
import math

#Fondo
class Fondo (pygame.sprite.Sprite):
    def __init__(self, posicion, imagen) -> None:
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion

    def update(self, *args: any, **kwargs: any):
        self.rect.x -= 2
        pantalla = pygame.display.get_surface()
        if self.rect.x <= - pantalla.get_width():
            self.rect.x = pantalla.get_width()      

#Pajaro
class Pajaro(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        imagen = [pygame.image.load("Imagenes/pajaro-abajo.PNG"), pygame.image.load("Imagenes/pajaro-arriba.PNG")]
        self.imagen_pajaro=[pygame.transform.scale(imagen[0],(55,40)), pygame.transform.scale(imagen[1],(55,40))]
        self.indice_imagenes = 0
        self.image = self.imagen_pajaro[self.indice_imagenes]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.topleft = (20,200)
        self.contador = 0

    def update(self, *args: any, **kwargs: any):
        self.contador =(self.contador+1) % 40
        self.indice_imagenes = self.contador // 20
        self.image = self.imagen_pajaro[self.indice_imagenes]


        teclas = args[2]
        if teclas[pygame.K_SPACE]:
            Pajaro.moverArriba(self)
        else:
            Pajaro.moverAbajo(self)
        self.mask = pygame.mask.from_surface(self.image)
            
    def moverArriba(self):
        self.rect.y -= 2
        # pantalla = pygame.display.get_surface()
        # limite = pantalla.get_height()
        # self.rect.y = max(self.rect.y, limite-self.image.get_height())
        self.image = pygame.transform.rotate(self.image, 25)

    def moverAbajo(self):
        self.rect.y += 1
        self.image = pygame.transform.rotate(self.image, -25)

#Tubo
class Tubo(pygame.sprite.Sprite):
    def __init__(self, posicion, imagen) -> None:
        super().__init__()
        self.image = imagen
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
        self.mask = pygame.mask.from_surface(self.image)
    def update(self, *args: any, **kwargs: any):
        self.rect.x -= 2
        pantalla = pygame.display.get_surface()
        if self.rect.x <= - pantalla.get_width():
            self.rect.x = pantalla.get_width()