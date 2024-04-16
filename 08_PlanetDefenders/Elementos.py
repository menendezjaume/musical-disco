from typing import Any
import pygame
import math
import random

class Fondo(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        pantalla = pygame.display.get_surface()
        self.image = pygame.image.load("./img/fondo.jpg")
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, pantalla.get_height()))
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, 0)


class Planeta(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.image = pygame.image.load("./img/planeta.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect(center=(320, 320))

class Anillo(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        self.imagen_original = pygame.image.load("./img/anillo.png")
        self.imagen_original = pygame.transform.scale(self.imagen_original, (165, 165))
        self.image = self.imagen_original.copy()
        self.rect = self.image.get_rect(center=(320, 320))
        self.angle = 0
        self.tiempo_ultimo_disparo = 0
        self.intervalo_disparo = 1000
        self.vida = 3
        self.puntos = 0
        # Variables necesarias para un powerup que te mejora los cañones al destruir a varios enemigos seguidos
        self.estaPowerupeado = False
        self.powerup = 0
        self.tiempo_powerup = 0
        self.duracion_powerup = 5000

    def update(self, *args: Any, **kwargs: Any) -> None:
        teclas = args[0]
        momento_actual = pygame.time.get_ticks()

        if teclas[pygame.K_RIGHT]:
            self.angle -= 2
            self.image = pygame.transform.rotate(self.imagen_original, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)
    
        if teclas[pygame.K_LEFT]:
            self.angle += 2
            self.image = pygame.transform.rotate(self.imagen_original, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

        if teclas[pygame.K_SPACE]:
            if momento_actual - self.tiempo_ultimo_disparo > self.intervalo_disparo:
                self.tiempo_ultimo_disparo = momento_actual
                self.disparar(args[1], args[2])

        # Lógica del powerup
        if self.powerup > 0 and not self.estaPowerupeado:   # EL powerup baja constantemente
            self.powerup -= 0.5

        if self.powerup >= 100 and not self.estaPowerupeado: # Si llega a 100 se inicia el powerup
            self.tiempo_powerup = momento_actual
            self.estaPowerupeado = True
            self.powerup = 100

        if self.estaPowerupeado: # Cambia el intervalo del disparo
            self.intervalo_disparo = 100
            self.powerup -= (100 / self.duracion_powerup) * 16.5 # Bajada del powerup para visualizar su duración
        else:
            self.intervalo_disparo = 1000
        
        if momento_actual - self.tiempo_powerup > self.duracion_powerup and self.estaPowerupeado: # Controla la duración del powerup
            self.powerup = 0
            self.tiempo_powerup = 0
            self.estaPowerupeado = False

    def disparar(self, grupo_sprites_todos, grupo_sprites_proyectiles):
        offsets = [(80, 0), (0, -80), (-80, 0), (0, 80)]

        for offset_x, offset_y in offsets:
            rotated_offset = pygame.math.Vector2(offset_x, offset_y).rotate(-self.angle)
            posicion_inicial = self.rect.center + rotated_offset
            nuevo_proyectil = Proyectil(posicion_inicial, self.angle + 90 * offsets.index((offset_x, offset_y)))
            grupo_sprites_todos.add(nuevo_proyectil)
            grupo_sprites_proyectiles.add(nuevo_proyectil)

    def restarVida(self):
        self.vida -= 1

    def sumarPuntos(self):
        self.puntos += 1
        if self.powerup <= 100 and not self.estaPowerupeado: # Subir el powerup por cada enemigo destruido
            self.powerup += 20


class Proyectil(pygame.sprite.Sprite):
    def __init__(self, posición, ángulo):
        super().__init__()

        self.radio = 5
        self.image = pygame.Surface((self.radio * 2, self.radio * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (0, 255, 85), (self.radio, self.radio), self.radio)
        self.rect = self.image.get_rect()
        self.rect.center = posición
        self.angle = ángulo
        self.velocidad = 7

    def update(self, *args: Any, **kwargs: Any):
        radianes = math.radians(self.angle)
        self.rect.x += self.velocidad * math.cos(radianes)
        self.rect.y -= self.velocidad * math.sin(radianes)

        if self.rect.left > 640 or self.rect.right < 0 or self.rect.top > 640 or self.rect.bottom < 0:
            self.kill()

        # Cambia el color y la velocidad de los proyectiles si está el powerup activo
        grupo_sprites_todos = args[1]
        if grupo_sprites_todos.sprites()[2].estaPowerupeado:
            pygame.draw.circle(self.image, (255, 255, 0), (self.radio, self.radio), self.radio)
            self.velocidad = 15


class Enemigo(pygame.sprite.Sprite):
    def __init__(self, pantalla):
        super().__init__()
        self.imagen_original = pygame.image.load("./img/enemigo.png")
        self.imagen_original = pygame.transform.scale(self.imagen_original, (50, 50))
        self.imagen_explosion = pygame.image.load("./img/explosión.png")
        self.imagen_explosion = pygame.transform.scale(self.imagen_explosion, (50, 50))
        self.image = self.imagen_original.copy()
        self.rect = self.image.get_rect()
        borde = random.choice([0, 1, 2, 3])

        if borde == 0:      # Aparece en la parte superior
            self.rect.topleft = (random.randint(0, pantalla.get_width() + self.rect.width), -self.rect.width)
        elif borde == 1:    # Aparece en la parte derecha
            self.rect.topleft = (pantalla.get_width() + self.rect.width, random.randint(0, pantalla.get_height() - self.rect.height))
        elif borde == 2:    # Aparece en la parte inferior
            self.rect.topleft = (random.randint(0, pantalla.get_width() - self.rect.width), pantalla.get_height() + self.rect.height)
        else:               # Aparece en la parte izquierda
            self.rect.topleft = (-self.rect.width, random.randint(0, pantalla.get_height() - self.rect.height))

        self.velocidad = 1

        self.explotando = False
        self.tiempo_explotando = 0
        self.duracion_explosion = 500

    def update(self, *args: Any, **kwargs: Any):
        grupo_sprites_todos = args[1]
        objetivo_x, objetivo_y = grupo_sprites_todos.sprites()[1].rect.center

        delta_x = objetivo_x - self.rect.centerx
        delta_y = objetivo_y - self.rect.centery

        radianes = math.atan2(delta_y, delta_x)
        self.rect.x += self.velocidad * math.cos(radianes)
        self.rect.y += self.velocidad * math.sin(radianes)
        self.image = pygame.transform.rotate(self.imagen_original, math.degrees(-radianes) - 90)
        self.rect = self.image.get_rect(center=self.rect.center)

        if not self.explotando:
            grupo_sprites_proyectiles = args[2]
            bala_collision = pygame.sprite.spritecollideany(self, grupo_sprites_proyectiles)
            if bala_collision:
                self.explotar()
                bala_collision.kill()
                grupo_sprites_todos.sprites()[2].sumarPuntos()

            anillo_collision = pygame.sprite.spritecollide(self, [grupo_sprites_todos.sprites()[2]], False, pygame.sprite.collide_mask)
            if anillo_collision:
                self.explotar()
                grupo_sprites_todos.sprites()[2].restarVida()

        elif pygame.time.get_ticks() - self.tiempo_explotando > self.duracion_explosion:
            self.kill()
        
        if self.explotando:
            self.image = self.imagen_explosion.copy()

    def explotar(self):
        self.explotando = True
        self.tiempo_explotando = pygame.time.get_ticks()
        self.velocidad = 0