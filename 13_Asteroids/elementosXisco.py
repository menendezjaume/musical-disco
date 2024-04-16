import pygame
import pygame_menu
import math
import random

frecuenciaterminarBuff = 1500
puntuacion = 0
class Disparos(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        image = pygame. image.load("bola-de-fuego.png")
        self.image = pygame.transform.scale(image, (30, 30))
        self.rect = self.image.get_rect()
        self.pantalla = pygame.display.get_surface()
        self.rect.bottom = y
        self.rect.centerx = x
        self.bullet_speed = 5
        self.cooldown = 10
        self.angle = angle

    def update(self, *args: any, **kwargs: any):
        rad_angle = math.radians(self.angle)
        self.rect.x += 5 * math.sin(rad_angle)
        self.rect.y += 5 * math.cos(rad_angle)
        self.pantalla.blit(self.image, self.rect.topleft)
        if self.rect.x >= 990 or self.rect.x <= 0:
            print("Kill")
            self.kill()
        if self.rect.y >= 790 or self.rect.y <= 0:
            print("kill")
            self.kill()


class Nave(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        imagen = pygame.image.load("nave-espacial.png")
        self.image = pygame.transform.scale(imagen, (60, 60))
        image2 = pygame.image.load("StarBuff.png")
        self.image2 = pygame.transform.scale(image2, (60,60))
        self.image2 = pygame.transform.rotate(self.image2, 180)
        self.image = pygame.transform.rotate(self.image, 180)
        self.Imagen = self.image
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
        self.angle = 0
        self.ultimoDisparo = 0
        self.arrayBala = []
        self.balas = pygame.sprite.Group()  # Grupo para almacenar las balas
        #para que los enemigos te persigan
        self.naveX = self.rect.x
        self.naveY = self.rect.y

        self.velocidad = 0
        #VIDAS
        self.vida = 3

        #star
        self.star = -1500

    def movement(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += 4
        if keys[pygame.K_RIGHT]:
            self.angle -= 4
        if keys[pygame.K_UP]:
            Nave.movimiento(self)

            # if keys[pygame.K_SPACE]:
        #     self.disparar()


    def movimiento(self):
        self.rect.x += 4 * math.sin(self.angle * math.pi / 180)
        self.rect.y += 4 * math.cos(self.angle * math.pi / 180)

        self.naveX = self.rect.x
        self.naveY = self.rect.y

    def disparar(self, grupo_sprites_todos, grupo_sprites_balas):
        # Calcular la posición inicial de la bala en el centro del planeta
        momento_actual = pygame.time.get_ticks()
        if momento_actual > self.ultimoDisparo + 500:
            bala = Disparos(self.rect.centerx, self.rect.centery, self.angle)
            grupo_sprites_todos.add(bala)
            grupo_sprites_balas.add(bala)
            self.arrayBala.append(bala)
            self.balas.add(bala)
            bala.update()
            self.ultimoDisparo = momento_actual

    def update(self, *args: any, **kwargs: any):
        global puntuacion
        keys = args[0]
        # capturamos grupo sprites todos
        grupo_sprites_todos = args[1]
        # capturamos grupo sprites balas
        grupo_sprites_balas = args[2]
        # capturamos grupo sprites enemigos
        grupo_sprites_enemigos = args[3]
        grupo_sprites_stars = args[4]
        grupo_sprites_asteroides = args[5]
        if self.rect.bottom < 0:
            self.kill()
        rotated_image = pygame.transform.rotate(self.Imagen, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        self.image = rotated_image
        self.rect = new_rect
        # si las ponemos asi tambien se mueve (experimentos)
        keys = pygame.key.get_pressed()
        # self.angle += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5
        if keys[pygame.K_SPACE]:
            self.disparar(grupo_sprites_todos, grupo_sprites_balas)

        #estrella
        starColision = pygame.sprite.spritecollideany(self, grupo_sprites_stars)
        momento_actual = pygame.time.get_ticks()
        if starColision:
            print("colision estrella")
            starColision.kill()
            self.star = momento_actual

            momento_actual = pygame.time.get_ticks()
            # ultimo_star = 0

        buffTerminado = momento_actual > self.star + frecuenciaterminarBuff
        if (buffTerminado):
            pass
        else:
            self.image = pygame.transform.rotate(self.image2, self.angle)
            #self.image = la imagen amarilla

        grupo_sprites_asteroidesMinis = args[6]
        enemigoColision = pygame.sprite.spritecollideany(self, grupo_sprites_enemigos)
        asteroideColision = pygame.sprite.spritecollideany(self, grupo_sprites_asteroides)
        asteroideMiniColision = pygame.sprite.spritecollideany(self, grupo_sprites_asteroidesMinis)
        pantalla = pygame.display.get_surface()
        # ENEMIGOS COLISION
        if enemigoColision and not buffTerminado:
            print("colision star")
            puntuacion += 20
            enemigoColision.kill()
        if enemigoColision and buffTerminado:
            print("colision")
            enemigoColision.kill()
            self.vida -= 1
            print(self.vida)
            if self.vida == 0:
                self.kill()

        # ASTEROIDES COLISION
        if asteroideColision and not buffTerminado:
            print("colision star")
            puntuacion += 30
            asteroideColision.kill()
        if asteroideColision and buffTerminado:
            print("colision")
            asteroideColision.kill()
            self.vida -= 1
            print(self.vida)
            if self.vida == 0:
                self.kill()
        if asteroideMiniColision and not buffTerminado:
            print("colision star")
            puntuacion += 10
            asteroideMiniColision.kill()
        if asteroideMiniColision and buffTerminado:
            print("colision")
            asteroideMiniColision.kill()
            self.vida -= 1
            print(self.vida)
            if self.vida == 0:
                self.kill()


    def getX(self):
        return self.naveX

    def getY(self):
        return self.naveY

    def getAngle(self):
        return self.angle

    def getVida(self):
        return self.vida

class GameOver(pygame.sprite.Sprite):
    def __init__(self, posicion):
        super().__init__()
        image = pygame.image.load("gameOver.png")
        self.image = pygame.transform.scale(image, (1000, 800))
        self.rect = self.image.get_rect()
        self.rect.topleft = posicion
class Star(pygame.sprite.Sprite):
    def __init__(self, posicionStar):
        super().__init__()
        image = pygame.image.load("estrella.png")
        self.image = pygame.transform.scale(image, (40, 40))
        self.star = False
        self.ultimo_enemigo_creado = 0
        self.momento_actual = pygame.time.get_ticks()
        self.frecuenciaAparicion = 6000
        self.rect = self.image.get_rect()
        self.rect.topleft = posicionStar

    def update(self, *args, **kwargs):
        grupo_sprites_todos = args[1]
        grupo_sprites_stars = args[4]



class Enemigo(pygame.sprite.Sprite):
    def __init__(self, posicion, planeta):
        super().__init__()
        self.planeta = planeta
        imagen = pygame.image.load("nave-espacial.png")
        self.image = pygame.transform.scale(imagen, (60, 60))
        # esta es la imagen mirando hacia arriba
        self.imagenArriba = pygame.transform.rotate(self.image, 0)
        # esta es la imagen mirando hacia la derecha
        self.imagenDerecha = pygame.transform.rotate(self.image, 90)
        # esta es la imagen mirando hacia abajo
        self.imagenAbajo = pygame.transform.rotate(self.image, 180)
        # esta es la imagen mirando hacia la izuierda
        self.imagenIzq = pygame.transform.rotate(self.image, 270)
        #angulos medios
        self.imagenAbajoDerecha = pygame.transform.rotate(self.image, 225)
        self.imagenArribaDerecha = pygame.transform.rotate(self.image, 315)
        self.imagenArribaIzq = pygame.transform.rotate(self.image, 45)
        self.imagenAbajoIzq = pygame.transform.rotate(self.image, 135)
        #creamos el rect
        self.rect = self.image.get_rect()
        self.rect.center = posicion
        self.ultimo_rebote = 0

    def actualizador(self):
        naveX = self.planeta.getX()
        naveY = self.planeta.getY()
        return naveX, naveY

    def abajoDerecha(self):
        self.rect.y += 1
        self.rect.x += 1
        self.image = self.imagenAbajoDerecha
        # print(self.rect.y)
        # print(self.rect.x)
        # print(self.naveX)
        # print(self.naveY)

    def abajoIzquierda(self):
        self.rect.y += 1
        self.rect.x -= 1
        self.image = self.imagenAbajoIzq
        # print(self.rect.y)
        # print(self.rect.x)
        # print(self.naveX)
        # print(self.naveY)

    def arribaDerecha(self):
        self.image = self.imagenArribaDerecha
        self.rect.y -= 1
        self.rect.x += 1
        # print(self.rect.y)
        # print(self.rect.x)
        # print(self.naveX)
        # print(self.naveY)

    def arribaIzquierda(self):
        self.image = self.imagenArribaIzq
        self.rect.y -= 1
        self.rect.x -= 1
        # print(self.rect.y)
        # print(self.rect.x)
        # print(self.naveX)
        # print(self.naveY)

    def arriba(self):
        self.image = self.imagenArriba
        self.rect.y -= 1
        # print(self.rect.y)
        # print(self.rect.x)
        # print(self.naveX)
        # print(self.naveY)

    def izquierda(self):
        self.rect.x -= 1
        self.image = self.imagenDerecha
        # print(self.rect.y)
        # print(self.rect.x)
        # print(self.naveX)
        # print(self.naveY)

    def abajo(self):
        self.rect.y += 1
        self.image = self.imagenAbajo
        # print(self.rect.y)
        # print(self.rect.x)
        # print(self.naveX)
        # print(self.naveY)

    def derecha(self):
        self.image = self.imagenIzq
        self.rect.x += 1
        # print(self.rect.y)
        # print(self.rect.x)
        # print(self.naveX)
        # print(self.naveY)

    def update(self, *args: any, **kwargs: any):
        global puntuacion
        naveX, naveY = self.actualizador()
        #print(naveX)
        if naveX > self.rect.x and naveY > self.rect.y:
            Enemigo.abajoDerecha(self)
            self.actualizador()
        elif naveX < self.rect.x and naveY > self.rect.y:
            Enemigo.abajoIzquierda(self)
            self.actualizador()
        elif naveX > self.rect.x and naveY < self.rect.y:
            Enemigo.arribaDerecha(self)
            self.actualizador()
        elif naveX < self.rect.x and naveY < self.rect.y:
            Enemigo.arribaIzquierda(self)
            self.actualizador()
        elif naveX == self.rect.x and naveY < self.rect.y:
            self.arriba()
            self.actualizador()
        elif naveX == self.rect.x and naveY > self.rect.y:
            self.abajo()
            self.actualizador()
        elif naveX < self.rect.x and naveY == self.rect.y:
            self.izquierda()
            self.actualizador()
        elif naveX > self.rect.x and naveY == self.rect.y:
            self.derecha()
            self.actualizador()
        grupo_sprites_balas = args[2]
        # grupo_sprites_nave = args[3]
        bala_colision = pygame.sprite.spritecollideany(self, grupo_sprites_balas)
        if bala_colision:
            puntuacion += 20
            self.kill()
            bala_colision.kill()
        grupo_sprites_asteroides = args[5]
        asteroide_colision = pygame.sprite.spritecollideany(self, grupo_sprites_asteroides)
        if asteroide_colision:
            self.kill()

        grupo_sprites_asteroidesMini = args[6]
        asteroideMini_colision = pygame.sprite.spritecollideany(self, grupo_sprites_asteroidesMini)
        if asteroideMini_colision:
            self.kill()



class Asteroide(pygame.sprite.Sprite):
    def __init__(self, posicionAsteroide):
        super().__init__()
        image = pygame.image.load("asteroide.png")
        self.image = pygame.transform.scale(image, (160,160))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = posicionAsteroide
        self.pantalla = pygame.display.get_surface()
        self.inicioX = random.randint(1, 2) == 1
        self.inicioY = random.randint(1, 2) == 1
        self.posicionX = self.rect.x
        self.posicionY = self.rect.y

        self.ultimo_rebote = 0
        self.ultimo_rebote2 = 0

    def update(self, *args, **kwargs):
        global puntuacion
        pantalla = pygame.display.get_surface()
        grupo_sprites_asteroidesMinis = args[6]

        momento_actual = pygame.time.get_ticks()


        asteroideMiniColision = pygame.sprite.spritecollideany(self, grupo_sprites_asteroidesMinis)
        if self.inicioX:
            self.rect.x += 3
            self.posicionX = self.rect.x
            if self.rect.x >= pantalla.get_width() - 160 or asteroideMiniColision:
                if (momento_actual > self.ultimo_rebote + 1000):
                    self.inicioX = False
                    self.ultimo_rebote = momento_actual


        else:
            self.rect.x += -3
            self.posicionX = self.rect.x
            if self.rect.x <= 0 or asteroideMiniColision:
                if (momento_actual > self.ultimo_rebote + 1000):
                    self.inicioX = True
                    self.ultimo_rebote = momento_actual

        if self.inicioY:
            self.rect.y += 3
            self.posicionY = self.rect.y
            if self.rect.y >= pantalla.get_height() - 160 or asteroideMiniColision:
                if (momento_actual > self.ultimo_rebote2 + 1000):
                    self.inicioY = False
                    self.ultimo_rebote2 = momento_actual

        else:
            self.rect.y += -3
            self.posicionY = self.rect.y
            if self.rect.y <= 0 or asteroideMiniColision:
                if (momento_actual > self.ultimo_rebote2 + 1000):
                    self.inicioY = True
                    self.ultimo_rebote2 = momento_actual
        grupo_sprites_balas = args[2]
        grupo_sprites_todos = args[1]
        asteroideMini = AsteroideMini((self.posicionX, self.posicionY), True, False)
        asteroideMini2 = AsteroideMini((self.posicionX, self.posicionY), False, True)

        bala_colision = pygame.sprite.spritecollideany(self, grupo_sprites_balas)
        if bala_colision:
            grupo_sprites_asteroidesMinis.add(asteroideMini)
            grupo_sprites_asteroidesMinis.add(asteroideMini2)
            grupo_sprites_todos.add(asteroideMini)
            grupo_sprites_todos.add(asteroideMini2)
            puntuacion += 20
            self.kill()
            bala_colision.kill()

class AsteroideMini(pygame.sprite.Sprite):
    def __init__(self, posicion, X, Y):
        super().__init__()
        image = pygame.image.load("asteroide.png")
        self.image = pygame.transform.scale(image, (60, 60))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = posicion
        self.inicioMiniX = X
        self.inicioMiniY = Y
        self.ultimo_rebote = 0
        self.ultimo_rebote2 = 0


    def update(self, *args, **kwargs):
        global puntuacion
        grupo_sprites_asteroides = args[5]
        asteroide_colision = pygame.sprite.spritecollideany(self, grupo_sprites_asteroides, pygame.sprite.collide_mask)
        pantalla = pygame.display.get_surface()
        momento_actual = pygame.time.get_ticks()
        ultimo_rebote = 0
        if self.inicioMiniX:
            self.rect.x += 3
            if self.rect.x >= pantalla.get_width() - 60 or asteroide_colision:
                if (momento_actual > self.ultimo_rebote + 1000):
                    self.inicioMiniX = False
                    self.ultimo_rebote = momento_actual
        else:
            self.rect.x += -3
            if self.rect.x <= 0 or asteroide_colision:
                if (momento_actual > self.ultimo_rebote + 1000):
                    self.inicioMiniX = True
                    self.ultimo_rebote = momento_actual


        if self.inicioMiniY:
            self.rect.y += 3
            if self.rect.y >= pantalla.get_height() - 60 or asteroide_colision:
                if (momento_actual > self.ultimo_rebote2 + 1000):
                    self.inicioMiniY = False
                    self.ultimo_rebote2 = momento_actual

        else:
            self.rect.y += -3
            if self.rect.y <= 0 or asteroide_colision:
                if (momento_actual > self.ultimo_rebote2 + 1000):
                    self.inicioMiniY = True
                    self.ultimo_rebote2 = momento_actual
        grupo_sprites_balas = args[2]
        bala_colision = pygame.sprite.spritecollideany(self, grupo_sprites_balas)
        if bala_colision:
            puntuacion += 10
            self.kill()
            bala_colision.kill()


