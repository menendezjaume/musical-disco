import pygame
import random


class Nave(pygame.sprite.Sprite):
    # Hacemos el contructor
    def __init__(self, posicion):
        super().__init__()
        self.naves = [pygame.image.load("navejuego.png"), pygame.image.load("navejuego3.png")]
        self.naves2 = [pygame.transform.scale(self.naves[0], (106.5 / 1.25, 110.5 / 1.25)),
                       pygame.transform.scale(self.naves[1], (106.5 / 1.25, 80 / 1.25))]
        self.indice_naves = 0
        self.image = self.naves2[self.indice_naves]
        self.contador_nave = 0
        # Rectangulo a partir de la nave
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
        self.ultimo_tiro = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.cooldown = 800  # Tiempo de cooldown en milisegundos (3 segundos)
        self.ultimo_disparo = pygame.time.get_ticks()
        self.cooldown_base = 800

    def set_cooldown(self, nuevo_cooldown):
        self.cooldown = nuevo_cooldown

    def disparar(self, grupo_sprites_todos, grupo_sprites_bala):
        actualidad = pygame.time.get_ticks()
        if actualidad - self.ultimo_disparo > self.cooldown:  # Verifica el cooldown
            bala = Bala((self.rect.x + self.image.get_width() / 2, self.rect.y + self.image.get_width() / 5))
            grupo_sprites_bala.add(bala)
            grupo_sprites_todos.add(bala)
            self.ultimo_disparo = actualidad  # Actualiza el tiempo del último disparo
    def update(self, *args, **kwargs) -> None:
        # miramos teclas
        teclas = args[0]
        # miramos la pantallla
        pantalla = pygame.display.get_surface()
        grupo_sprites_todos = args[1]
        # miarmos balas
        grupo_sprites_bala = args[2]
        # Capturar grupo sprites enemigos 3
        grupo_sprites_enemigos = args[3]
        # miramos el run
        running = args[4]
        # grupo sprites planeta
        grupo_sprites_planeta = args[5]
        # Grupo bala enemigo
        grupo_sprites_bala_enemigo = args[7]
        # grupo enemigo fuerte
        grupo_sprites_enemigos_fuertes = args[8]


        # planeta colision
        planeta_colision = pygame.sprite.spritecollideany(self, grupo_sprites_planeta, pygame.sprite.collide_mask)

        # Preparamos las teclas
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and not planeta_colision:
            self.rect.x -= 20
            self.rect.x = max(0, self.rect.x)
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and not planeta_colision:
            self.rect.x += 20
            self.rect.x = min(pantalla.get_width() - self.image.get_width(), self.rect.x)
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            self.rect.y -= 20
            self.rect.y = max(0, self.rect.y)
        if (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) and not planeta_colision:
            self.rect.y += 20
            self.rect.y = min(pantalla.get_width() - self.image.get_width(), self.rect.y)
        if teclas[pygame.K_SPACE]:
            self.disparar(grupo_sprites_todos, grupo_sprites_bala)

        # Hacemos la transicion de sprites
        self.contador_nave = (self.contador_nave + 5) % 40
        self.indice_naves = self.contador_nave // 30
        self.image = self.naves2[self.indice_naves]
        # detectar colisiones
        enemigo_colision = pygame.sprite.spritecollideany(self, grupo_sprites_enemigos, pygame.sprite.collide_mask)
        parametros = args[6]
        if enemigo_colision:
            enemigo_colision.kill()
            parametros.restarVida()
            parametros.restarPuntuacion()

        if parametros.getVidas() < 0:
            running[0] = False

        bala_enemigo_colision = pygame.sprite.spritecollideany(self, grupo_sprites_bala_enemigo,
                                                               pygame.sprite.collide_mask)
        parametros = args[6]
        if bala_enemigo_colision:
            bala_enemigo_colision.kill()
            parametros.restarVida()

        enemigo_fuerte_colision = pygame.sprite.spritecollideany(self, grupo_sprites_enemigos_fuertes,
                                                                 pygame.sprite.collide_mask)
        if enemigo_fuerte_colision:
            enemigo_fuerte_colision.kill()
            parametros.sumarPuntuacion(300)  # Sumar puntos al eliminar al enemigo fuerte

        bala_enemigo_colision = pygame.sprite.spritecollideany(self, grupo_sprites_bala_enemigo,
                                                               pygame.sprite.collide_mask)
        parametros = args[6]
        if bala_enemigo_colision:
            bala_enemigo_colision.kill()
            parametros.restarVida()


class Planeta(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        # Cargamos imagen imagen del planeta
        planeta = pygame.image.load("planet.png")
        self.image = pygame.transform.scale(planeta, (2200, 1250))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = posicion

def update(self, *args: any, **kwargs: any):
        grupo_sprites_enemigos = args[3]
        running = args[4]
        enemigo_colision = pygame.sprite.spritecollideany(self, grupo_sprites_enemigos, pygame.sprite.collide_mask)
        if enemigo_colision:
            enemigo_colision.kill()
            running[0] = False


class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posicion, velocidad_enemigo, grupo_sprites_planeta) -> None:
        super().__init__()
        # cargamos la imagen
        self.enemigos = [pygame.image.load("avion4.png"), pygame.image.load("avion5.png")]
        self.enemigos2 = [pygame.transform.scale(self.enemigos[0], (95 / 2, 181 / 2)),
                       pygame.transform.scale(self.enemigos[1], (85 / 2, 187 / 2))]
        self.manolos = [pygame.transform.rotate(self.enemigos2[0], 180), pygame.transform.rotate(self.enemigos2[1], 180)]
        self.indice_manolos = 0
        self.contador_manolos = 0
        self.image = self.manolos[self.indice_manolos]
        self.mask = pygame.mask.from_surface(self.image)
        # creamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        # actualizar la posición del rectangulo para que coincida con "posicion"
        self.rect = self.image.get_rect(topleft=posicion)
        self.velocidad_x = velocidad_enemigo
        self.velocidad = 70
        self.width = self.image.get_width()
        self.ultimo_disparo = 0
        self.frecuencia_disparo = 2000
        self.puede_disparar = random.random() > 0.55
        self.grupo_sprites_planeta = grupo_sprites_planeta

    def disparar(self, grupo_sprites_todos, grupo_sprites_bala_enemigo):
        actualidad = pygame.time.get_ticks()
        if self.puede_disparar and actualidad > self.ultimo_disparo + self.frecuencia_disparo:
            bala = BalaEnemigo((self.rect.x + self.image.get_width() / 2, self.rect.y + self.image.get_height()))
            grupo_sprites_bala_enemigo.add(bala)
            grupo_sprites_todos.add(bala)
            self.ultimo_disparo = actualidad

    def update(self, *args: any, **kwargs: any):
        pantalla = pygame.display.get_surface()
        actualidad = pygame.time.get_ticks()
        self.rect.x += self.velocidad_x
        if self.rect.right >= pantalla.get_width() or self.rect.left == 0:
            self.velocidad_x *= -1
            self.rect.y += self.velocidad
        self.contador_manolos = (self.contador_manolos + 3) % 20
        self.indice_manolos = self.contador_manolos // 10
        self.image = self.manolos[self.indice_manolos]
        grupo_sprites_todos = args[1]
        grupo_sprites_bala_enemigo = args[7]
        grupo_sprites_bala = args[2]
        grupo_sprites_todos = args[1]
        parametros = args[6]
        running = args[4]
        grupo_sprites_planeta = args[5]

        # Disparos de la bala
        self.disparar(grupo_sprites_todos, grupo_sprites_bala_enemigo)

        if random.random() < 0.02:
            self.disparar(grupo_sprites_todos, grupo_sprites_bala_enemigo)

        # capturar arg 2 bala
        bala_colision = pygame.sprite.spritecollideany(self, grupo_sprites_bala, pygame.sprite.collide_mask)
        if bala_colision:
            self.kill()
            bala_colision.kill()
            parametros.sumarPuntuacion()

        pantalla = pygame.display.get_surface()
        planeta_colision = pygame.sprite.spritecollideany(self, grupo_sprites_planeta, pygame.sprite.collide_mask)
        if planeta_colision:
            planeta_colision.kill()
            running[0] = False

        if not self.puede_disparar and actualidad > self.ultimo_disparo + self.frecuencia_disparo:
            self.puede_disparar = True

class Fondo(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        # cargamos la imagen
        imagen = pygame.image.load("fondo2.png")
        # pantalla
        pantalla = pygame.display.get_surface()
        self.image = pygame.transform.scale(imagen, (pantalla.get_width(), imagen.get_height() * 1.5))
        # creamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        # actualizar la posición del rectangulo para que coincida con "posicion"
        self.rect.topleft = (0, 0)


class Bala(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = posicion

    def update(self, *args: any, **kwargs: any) -> None:
        self.rect.y -= 10

class BalaEnemigo(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((0, 0, 255))  # Color azul para las balas de enemigos
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = posicion

    def update(self, *args: any, **kwargs: any) -> None:
        self.rect.y += 10  # Mueve la bala hacia abajo


class Parametros():
    def __init__(self):
        self.puntuacion = 0
        self.vidas = 3

    def restarVida(self):
        self.vidas -= 1

    def sumarVida(self):
        self.vidas += 1

    def restarPuntuacion(self):
        self.puntuacion -= 100

    def sumarPuntuacion(self, puntos = 50):
        self.puntuacion += puntos

    def getVidas(self):
        return self.vidas

    def getPuntuacion(self):
        return self.puntuacion