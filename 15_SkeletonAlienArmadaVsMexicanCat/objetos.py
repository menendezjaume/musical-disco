from typing import Any
import pygame
import pygame.mask
from pygame.locals import QUIT, KEYUP, K_SPACE

class Cat(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        self.derecha = pygame.image.load("derecha.png")
        self.izquierda = pygame.image.load("izquierda.png")

        scaled_width = 100
        scaled_height = 93
        self.derecha = pygame.transform.scale(self.derecha, (scaled_width, scaled_height))
        self.izquierda = pygame.transform.scale(self.izquierda, (scaled_width, scaled_height))
        self.images = [self.derecha, self.izquierda]

        self.image_index = 0
        self.tiempo_anterior_imagen = 0  # Inicializar a 0

        self.image = self.images[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
        self.puede_disparar = True  # Nuevo atributo para controlar si puede disparar
        
    def update(self, teclas, tiempo_actual, cambio_imagen_tiempo, enemigos, *args: Any, **kwargs: Any, ) -> None:
        pantalla = pygame.display.get_surface()
        limite = pantalla.get_width() - self.izquierda.get_width()
        self.rect.x = min(self.rect.x, limite)
        if teclas[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= 20
        if teclas[pygame.K_d]:
            self.rect.x = min(self.rect.x + 20, limite)
        if tiempo_actual - self.tiempo_anterior_imagen >= cambio_imagen_tiempo:
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]
            self.tiempo_anterior_imagen = tiempo_actual
        colision = pygame.sprite.spritecollideany(self, enemigos, pygame.sprite.collide_mask)
        if colision:
            # Eliminar tanto al gato como al enemigo en caso de colisión
            colision.kill()
            self.kill()
            
    # A partir de aqui codigo para disparar
    
    def disparar(self, teclas, proyectiles, todos_los_sprites):
        if teclas[pygame.K_SPACE] and self.puede_disparar:
            proyectil = Proyectil(self.rect.x + self.derecha.get_width() // 2, self.rect.y)
            todos_los_sprites.add(proyectil)
            proyectiles.add(proyectil)
            self.desactivar_disparo()
    def puede_disparar(self):
        return self.puede_disparar

    def desactivar_disparo(self):
        self.puede_disparar = False

    def activar_disparo(self):
        self.puede_disparar = True
class Background(pygame.sprite.Sprite):  # PUTOS SPRITES (Nota del dia siguiente: Efectivamente hermano) Ni me acuerdo de por que
    def __init__(self, velocidad, num_imagenes=3):
        super().__init__()

        self.imagenes = [pygame.image.load(f"background{i}.jpg") for i in range(1, num_imagenes + 1)]
        self.velocidad = velocidad
        self.num_imagenes = num_imagenes
        self.imagen_actual = 0

        # Redimensionar las imágenes al tamaño de la pantalla
        pantalla_info = pygame.display.Info()
        self.ancho_pantalla = pantalla_info.current_w
        self.alto_pantalla = pantalla_info.current_h
        self.imagenes = [pygame.transform.scale(imagen, (self.ancho_pantalla, self.alto_pantalla)) for imagen in self.imagenes]

        self.sprite1 = pygame.sprite.Sprite()
        self.sprite1.image = self.imagenes[(self.imagen_actual + 0)]
        self.sprite1.rect = self.sprite1.image.get_rect()
        self.sprite1.rect.y = 0 

        self.sprite2 = pygame.sprite.Sprite()
        self.sprite2.image = self.imagenes[(self.imagen_actual + 1)]
        self.sprite2.rect = self.sprite2.image.get_rect()
        self.sprite2.rect.y = -self.alto_pantalla 

        self.sprite3 = pygame.sprite.Sprite()
        self.sprite3.image = self.imagenes[(self.imagen_actual + 2)]
        self.sprite3.rect = self.sprite3.image.get_rect()  
        self.sprite3.rect.y = -2*self.alto_pantalla 

    def update(self):
        # Actualizar la posición vertical de ambos sprites hacia abajo
        self.sprite1.rect.y += self.velocidad
        self.sprite2.rect.y += self.velocidad
        self.sprite3.rect.y += self.velocidad

        # Para que funcione, en caso de añadir imagenes, se ha de multiplicar -self.alto_pantalla por el numero de imagenes - 1

        if self.sprite1.rect.y >= self.alto_pantalla:
            self.sprite1.rect.y = -2*self.alto_pantalla 

        if self.sprite2.rect.y >= self.alto_pantalla:
            self.sprite2.rect.y = -2*self.alto_pantalla
            
        if self.sprite3.rect.y >= self.alto_pantalla:
            self.sprite3.rect.y = -2*self.alto_pantalla

    def draw(self, screen):
        screen.blit(self.sprite1.image, self.sprite1.rect)
        screen.blit(self.sprite2.image, self.sprite2.rect)
        screen.blit(self.sprite3.image, self.sprite3.rect)
class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20))  # Tamaño del proyectil
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Epilepsia colores
        self.colores = [
            (255, 0, 0),
            (255, 165, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 0, 255),
            (75, 0, 130),
            (128, 0, 128)
        ]
        self.indice_color_actual = 0

    def update(self,  *args, **kwargs):
        
        self.rect.y -= 15  # Velocidad proyectil

        # Epilepsia
        self.image.fill(self.colores[self.indice_color_actual])
        self.indice_color_actual = (self.indice_color_actual + 1) % len(self.colores)

        # Borrar al salir de la pantalla
        if self.rect.bottom < 0:
            self.kill()
class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posicion, velocidad) -> None:
        super().__init__()
        
        # Cargar las imagenes
        self.enemigo_derecha = pygame.image.load("enemigoderecha.png")
        self.enemigo_izquierda = pygame.image.load("enemigoizquierda.png")
        
        #Escalado
        
        scaled_width = 200
        scaled_height = 100
        self.enemigo_derecha = pygame.transform.scale(self.enemigo_derecha, (scaled_width, scaled_height))
        self.enemigo_izquierda = pygame.transform.scale(self.enemigo_izquierda, (scaled_width, scaled_height))

        #El propio sprite del enemigo
        
        self.image = self.enemigo_izquierda
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion

        #Cosas
        
        self.velocidad = velocidad  # Speed
        self.direccion = 1  # 1 para derecha, -1 para izquierda
        self.descenso = 100  # Cuantos pixeles baja cada vez que choca con la pared
        
        # Crear máscara de colisión para el enemigo
        self.mask = pygame.mask.from_surface(self.image)
        
    def update(self, *args: Any, **kwargs: Any) -> None:
        pantalla = pygame.display.get_surface()
        limite_izquierdo = -200
        limite_derecho = pantalla.get_width()

        if self.direccion == 1:  # Mover hacia la derecha
            self.image = self.enemigo_derecha
            self.rect.x += self.velocidad
            if self.rect.x >= limite_derecho:
                self.rect.x = limite_derecho
                self.direccion = -1  # Cambiar dirección hacia la izquierda
                self.rect.y += self.descenso
        elif self.direccion == -1:  # Mover hacia la izquierda
            self.image = self.enemigo_izquierda
            self.rect.x -= self.velocidad
            if self.rect.x <= limite_izquierdo:
                self.rect.x = limite_izquierdo
                self.direccion = 1  # Cambiar dirección hacia la derecha
                self.rect.y += self.descenso

        # Colisión con proyectiles
        for proyectil in kwargs.get('proyectiles', []):
            # Crear máscara de colisión para el proyectil
            proyectil_mask = pygame.mask.from_surface(proyectil.image)

            # Obtener la posición relativa del proyectil con respecto al enemigo
            offset = (proyectil.rect.x - self.rect.x, proyectil.rect.y - self.rect.y)

            # Verificar la superposición de las máscaras
            if self.mask.overlap(proyectil_mask, offset):
                proyectil.kill()
                self.kill()
                break  # Salir del bucle al encontrar la primera colisión