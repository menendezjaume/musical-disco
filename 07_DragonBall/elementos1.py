import pygame
import time

#creamos la clase jugador para el jugador
class Jugador (pygame.sprite.Sprite):
    def __init__(self,posicion,velocidad):
        super().__init__()
        #creacion de array de las imagenes
        self.imagenes = [
            pygame.image.load("Imagenes/kid.png"),  # normal
            pygame.image.load("Imagenes/kid1.png"),  # arriba
            pygame.image.load("Imagenes/kid2.png"),  # abajo
            pygame.image.load("Imagenes/kid3.png"),  # derecha
            pygame.image.load("Imagenes/kid4.png"),  # izquierda
            pygame.image.load("Imagenes/kidkame.png")  # kame
        ]
        self.image = self.imagenes[0]
        #creamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        #actualizar la posición del rectangulo para que coincida con "posicion"
        self.rect.topleft = posicion
        #creamos la variable velocidad para cuando sse recolecte esfera aumente la velocidad durante un tiempo y luego vuelva a su velocidad original
        self.velocidad = velocidad
        self.velocidad_original = velocidad
        #creamos la barra de vida del jugador con su posicion y la cantidad de vidas que tiene
        self.barravida_goku = Barravida_goku((18, 14), 3)
        #variable del ultimo kame que ha disparado el jugador 
        self.ultimo_disparo = 0
        #creamos la variable puntuacion para que cada vez que se recolecte una esfera la puntuacion aumente 
        self.puntuacion = 0
        #tiempo de creacion de esferas
        self.tiempo_esfera = 0

    #funcion para que jugador dispare kame
    def disparar(self, grupo_sprites_todos, grupo_sprites_kame):
        #creamos la variable que recoge los ticks del juego
        momento_actual = pygame.time.get_ticks()
        if momento_actual > self.ultimo_disparo + 500 :
            #creacion de la bala con la clase kamehameha, y la posicion desde donde saldra la bala (centro de la imagen jugador)
            bala = Kamehameha((self.rect.x + self.image.get_width() / 2, self.rect.y + self.image.get_width() / 2))
            #añadimos la bala al grupo sprites kame
            grupo_sprites_kame.add(bala)
            #añadimos la bala al grupo sprites todos
            grupo_sprites_todos.add(bala)
            self.ultimo_disparo = momento_actual

    def update(self, *args):
        #capturamos teclas
        teclas = args[0]
        #capturamos todos
        grupo_sprites_todos = args[1]
        #capturamos kames
        grupo_sprites_kame = args[2]
        #capturamos esferas
        grupo_sprites_esfera = args[3]
        #capturamos puntuacion esferas
        puntuacion = args[5]
        #capturamos running
        running = args[7]
        #capturamos las vidas jugador
        vidas_jugador = args[9]

        #movimiento hacia arriba
        if teclas[pygame.K_UP]:
            self.image = self.imagenes[1]
            self.rect.y -= self.velocidad
            self.rect.y = max(0, self.rect.y)
        #movimiento hacia abajo
        elif teclas[pygame.K_DOWN]:
            self.image = self.imagenes[2]
            self.rect.y += self.velocidad
            pantalla = pygame.display.get_surface()
            self.rect.y = min(pantalla.get_height() - self.image.get_height(), self.rect.y)
        #movimiento hacia la izquierda
        if teclas[pygame.K_LEFT]:
            self.image = self.imagenes[4]
            self.rect.x -= self.velocidad
            self.rect.x = max(0,self.rect.x)
        #movimiento hacia la derecha
        elif teclas[pygame.K_RIGHT]:
            self.image = self.imagenes[3]
            self.rect.x += self.velocidad
            pantalla = pygame.display.get_surface()
            self.rect.x = min(pantalla.get_width ()- self.image.get_width(),self.rect.x)
        #jugador dispara con la barra espaciadora
        if teclas[pygame.K_SPACE]:
            self.image = self.imagenes[5]
            self.disparar(grupo_sprites_todos, grupo_sprites_kame)
        #si no se mueve la imagen sera normal
        if not any(teclas):
            self.image = self.imagenes[0]
        
        # verificar si han pasado 5 segundos desde que se recogió la esfera
        if self.tiempo_esfera and time.time() - self.tiempo_esfera > 5:
            self.velocidad = self.velocidad_original
            self.tiempo_esfera = 0

        #colisiones del jugador con las esferas
        esfera_colison  = pygame.sprite.spritecollideany(self,grupo_sprites_esfera,pygame.sprite.collide_mask)
        if esfera_colison : 
            #cuando colisine la esfera desaparece
            esfera_colison.kill()
            #se suma la puntuacion con la funcion sumar puntuacion
            puntuacion.sumarpuntuacion()
            # cuando colisione se duplicara la velocidad
            self.velocidad *= 2
            #Registra el momento en que se recogió la esfera  
            self.tiempo_esfera = time.time()  

        #cargamos el grupo de sprites de enemigos
        grupo_sprites_enemigos = args[8]
        #colisiones del jugador con los enemigos
        enemigos_colison= pygame.sprite.spritecollideany(self,grupo_sprites_enemigos,pygame.sprite.collide_mask)
        if enemigos_colison:
            #cuando colisine el enemigo desaparece
            enemigos_colison.kill()
            #se restara una vida al jugador si se colisione con un enemigo
            vidas_jugador.restarvidas_jugador()
            #se actualiza la barra de vida por cada colision con el enemigo con la funcion de actualizar la barra de vida
            self.actualizar_barravida_goku(vidas_jugador.getvidas_jugador()) 
            #el juego se detendra si la vida del jugador llega a 0
            if vidas_jugador.getvidas_picolo() == 0 :
                running[0] = False
        
        #cargamos el grupo de sprites de rayo   
        grupo_sprites_rayo = args[10]
        #colisiones del jugador con los rayos que dispara picolo
        rayo_colision = pygame.sprite.spritecollideany(self,grupo_sprites_rayo,pygame.sprite.collide_mask)
        if rayo_colision :
            #cuando colisine el enemigo desaparece
            rayo_colision.kill()
            #se restara una vida al jugador si se colisione con el rayo que dispara picolo
            vidas_jugador.restarvidas_jugador()
            #se actualiza la barra de vida por cada colision con el enemigo con la funcion de actualizar la barra de vida
            self.actualizar_barravida_goku(vidas_jugador.getvidas_jugador())
            #el juego se detendra si la vida del jugador llega a 0
            if vidas_jugador.getvidas_picolo() == 0 :
                running[0] = False

    #funcion para poder actualizar la barra de vida del jugador, utiliza el metodo update para actualizar las vidas del jugador y poder pasarlas a la barra de vida de goku
    def actualizar_barravida_goku(self, vidas):
        self.barravida_goku.update(vidas)

#creamos la clase kamehameha para el disparo del jugador        
class Kamehameha(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        #cargamos la imagen
        self.image = pygame.image.load("Imagenes/kame.png")
        self.mask = pygame.mask.from_surface(self.image)
        #creamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        #actualizar la posición del rectangulo para que coincida con "posicion"
        self.rect.center = posicion

    def update(self, *args: any, **kwargs: any) -> None:
        #velocidad y direccion a la que avanza el kame
        self.rect.x +=5
        #cuando el kame se salga de la pantalla se elimina 
        if self.rect.bottom < 0:
            self.kill()

        #cargamos grupo de sprites enemigos
        grupo_sprites_enemigos = args[8]
        #colision del kame con los enemigos
        enemigos_colison= pygame.sprite.spritecollideany(self,grupo_sprites_enemigos,pygame.sprite.collide_mask)
        if enemigos_colison:
            #cuando colisione los enemigos desaparecen
            enemigos_colison.kill()
            #cuando colisione el kame desaparece
            self.kill()

#creamos la clase picolo que sera el enemigo del jugador a vencer        
class Picolo (pygame.sprite.Sprite):
    def __init__(self,posicion,velocidad) -> None:
        super().__init__()
        #cargamos imagen
        self.image = pygame.image.load("Imagenes/boss.png")
        #creamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        #actualizar la posición del rectangulo para que coincida con "posicion"
        self.rect.center = posicion
        #creamos variable de velocidad para que se mueva de arriba abajo
        self.velocidad = velocidad
        #variable del disparo rayo
        self.ultimo_disparo = 0
        #creamos la barra de vida de picolo con su posicion y la cantidad de vidas que tiene
        self.barravida_picolo = Barravida_picolo((954,14), 10)  # Asegúrate de usar la imagen correcta aquí

    def update(self, *args: any, **kwargs: any):
        #creamos la funcion para que cada vez que choque con el max y el min de la y de la pantalla picolo se mueva de arriba hacia abajo
        pantalla = pygame.display.get_surface()
        self.rect.y -= self.velocidad
        if self.rect.y < 0:
            self.velocidad = -self.velocidad
        elif self.rect.y > pantalla.get_height() - self.image.get_height():
            self.velocidad = -self.velocidad

        #cargamos grupo sprites del kame
        grupo_sprites_kame = args[2]
        #cargamos las vidas de picolo
        vidas_picolo = args[6]
        #cargamos el running
        running = args[7]
        #colision de picolo con el kame del jugador
        colision = pygame.sprite.spritecollideany(self,grupo_sprites_kame,pygame.sprite.collide_mask)
        if colision:
            #cuando colisione el kame desaparece
            colision.kill()
            #se resta una vida por cada colision
            vidas_picolo.restarvida_picolo()
            #actualizamos la barra de vida de pciolo con la funcion actualizar barra vida de picolo
            self.actualizar_barravida_picolo(vidas_picolo.getvidas_picolo())
            #si las vidas de picolo llegan a 0 el juego se detiene
            if vidas_picolo.getvidas_picolo() <= 0 :
                running[0] = False

        #cargamos grupo de sprites de todos
        grupo_sprites_todos = args[1]
        #cargamos grupo de sprites de l rayo que dispara
        grupo_sprites_rayos = args[10]
        #cargamos los ticks del juego
        momento_actual = pygame.time.get_ticks()
        #cada segundo  ira disparando rayos
        if momento_actual > self.ultimo_disparo + 1000:  
            self.disparar(grupo_sprites_todos, grupo_sprites_rayos) 
            self.ultimo_disparo = momento_actual

    #funcion para actualizar la barra de vida de picolo 
    def actualizar_barravida_picolo(self, vidas):
        self.barravida_picolo.update(vidas)

    #funcion para que jugador dispare rayo
    def disparar(self, grupo_sprites_todos, grupo_sprites_balas_picolo):
        #creacion de la bala con la clase rayo, y la posicion desde donde saldra la bala (centro de la imagen picolo)
        bala = Rayo((self.rect.x + self.image.get_width() / 2, self.rect.y + self.image.get_width() / 2))
        #aladimos la bala al grupo spritee de picolo
        grupo_sprites_balas_picolo.add(bala)
        #añadimos la bala al grupo sprites de todos
        grupo_sprites_todos.add(bala)

#creamos la clase rayoparala bala de picolo
class Rayo(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        #cargamos iamgen
        self.image = pygame.image.load("Imagenes/rayo.png")
        self.mask = pygame.mask.from_surface(self.image)
        #creamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        #actualizar la posición del rectangulo para que coincida con "posicion"
        self.rect.center = posicion
        #creamos variable de velocidad para que se mueva de arriba abajo

    def update(self, *args: any, **kwargs: any) -> None:
        #velocidad y direccion a la que avanza el kame
        self.rect.x -=5
        #cuando el kame se salga de la pantalla se elimina 
        if self.rect.bottom < 0:
            self.kill()

#creamos la clase enemigos
class Enemigos(pygame.sprite.Sprite):
    def __init__(self,posicion) -> None:
        super().__init__()
        #cargamos iamgen
        self.image = pygame.image.load("Imagenes/picolo.png")
        #creamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        #actualizar la posición del rectangulo para que coincida con "posicion"
        self.rect.center = posicion
        #creamos variable de velocidad para que se mueva de arriba abajo

    #funcion para que se creen enemigos, se muevan hacia la izquierda y si llegan a la izquierda (x=0) de la pantalla se mueran  
    def update(self, *args: any, **kwargs: any):
        pantalla = pygame.display.get_surface()
        self.rect.x -=1
        self.rect.x = max(0, self.rect.x)
        self.rect.x = min(pantalla.get_width() - self.image.get_width(), self.rect.x)
        self.rect.y = max(0, self.rect.y)
        self.rect.y = min(pantalla.get_height() - self.image.get_height(), self.rect.y)
        if (self.rect.x == 0):
            self.kill()

#creacion de la clase esferas 
class Esferas(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        #cargamos imagen
        self.image = pygame.image.load("Imagenes/esfera.png")
        self.mask = pygame.mask.from_surface(self.image)
        #creamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        #actualizar la posición del rectangulo para que coincida con "posicion"
        self.rect.topleft = posicion
        #cargamos los ticks del juego para la creacion del tiempo de lacreacion de esferas
        self.tiempo_inicial = pygame.time.get_ticks()

    #update para capturar max y min de pantalla y cuando las esferas se salgan se mueran
    def update(self, *args: any, **kwargs: any):
        pantalla = pygame.display.get_surface()
        self.rect.x = max(0, self.rect.x)
        self.rect.x = min(pantalla.get_width() - self.image.get_width(), self.rect.x)
        if (self.rect.y > pantalla.get_height()):
            self.kill()

#creacion de la clase fondo
class Fondo(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()
        # cargamos la imagen
        imagen = pygame.image.load("Imagenes/fondo1.png")
        #pantalla
        pantalla = pygame.display.get_surface()
        self.image = pygame.transform.scale(imagen, (pantalla.get_width(), imagen.get_height()))
        # creamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        # actualizar la posición del rectangulo para que coincida con "posicion"
        self.rect.topleft = (0, 0)

#creamos la clase puntos para obtener la puntuacion y las vidas del jugador y picolo 
class Puntos ():
    def __init__(self) -> None:
        #inicio variable puntuacion
        self.puntuacion = 0
        #inicio variable de las vidas de picolo
        self.vidas_picolo = 10
        #inicio variable de las vidas del jugador 
        self.vidas_jugador = 3
    
    #funcion para capturar las vidas de picolo
    def getvidas_picolo (self) :
        return self.vidas_picolo
    #funcion para restar vidas de picolo por cada colision con el kame del jugador
    def restarvida_picolo(self):
        self.vidas_picolo-=1

    #funcion para capturar las vidas del jugador
    def getvidas_jugador(self):
        return self.vidas_jugador
    #funcion para restar vidas del jugador por cada colision con el rayo de picolo o enemigos
    def restarvidas_jugador(self):
        self.vidas_jugador-=1

    #funcion para capturar la puntuacion
    def getpuntuacion (self):
        return self.puntuacion
    #funcion para sumar puntuacion cada vez que se recolecte una esfera
    def sumarpuntuacion(self):
        self.puntuacion +=1

#creacion de clase barra de vida de goku (jugador)
class Barravida_goku(pygame.sprite.Sprite):
    def __init__(self, posicion, vida_maxima):
        super().__init__()
        #cargamos imagen
        self.image = pygame.image.load("Imagenes/barravidagoku.png")
        #creamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        #actualizar la posición del rectangulo para que coincida con "posicion"
        self.rect.topleft = posicion
        #creamos la variable de la vida maxima que del jugador al iniciar el juego
        self.vida_maxima = vida_maxima
        #creamos la variable de las vidas que tendra el jugador durante el desarrollo del juego
        self.vida_actual = vida_maxima

    #funcion para ir actualizando la barra de vida del jugador
    def update(self, vida):
        #hacemos el porcentaje de la vida del jugador con las vida actuales que tiene y la vida maxima que tiene al principio
        porcentaje_vida = vida / self.vida_maxima
        #hacemos que la imagen se recorte con el porcentaje  de vida
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * porcentaje_vida), self.rect.height))
        self.vida_actual = vida

#creacion de clase barra de vida de pciolo
class Barravida_picolo(pygame.sprite.Sprite):
    def __init__(self, posicion, vida_maxima):
        super().__init__()
        #cargamos imagen
        self.image = pygame.image.load("Imagenes/barravidapicolo.png")
        #creamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        #actualizar la posición del rectangulo para que coincida con "posicion"
        self.rect.topleft = posicion
        #creamos la variable de la vida maxima que del jugador al iniciar el juego
        self.vida_maxima = vida_maxima
        #creamos la variable de las vidas que tendra el jugador durante el desarrollo del juego
        self.vida_actual = vida_maxima

    #funcion para ir actualizando la barra de vida de picolo
    def update(self, vida):
        #hacemos el porcentaje de la vida del jugador con las vida actuales que tiene y la vida maxima que tiene al principio
        porcentaje_vida = vida / self.vida_maxima
        #hacemos que la imagen se recorte con el porcentaje  de vida
        self.image = pygame.transform.scale(self.image, (int(self.rect.width * porcentaje_vida), self.rect.height))
        self.vida_actual = vida