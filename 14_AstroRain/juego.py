import pygame
import elementos
import random
import sys
# Iniciamos juego y pantalla

pygame.init()
tamanyo_pantalla = (900, 800)
pantalla = pygame.display.set_mode(tamanyo_pantalla)
pantalla.fill((4,6,6))

# Configuramos reloj y FPS

running = True
FPS = 60
reloj = pygame.time.Clock()
ultimo_meteorito_creado = 0
ultimo_astronauta_creado = 0
# Creamos un numero aleatorio para la generacion de meteoritos y astronautas

numero_aleatorio = random.randint(1, pantalla.get_width())


# Ponemos posiciones

posicion = (200, 300)
posicion_spawn = (numero_aleatorio, 0)
posicion_vacio = (0, 900)

# Creamos grupos

grupo_sprites_todos = pygame.sprite.Group() 
grupo_sprites_nave = pygame.sprite.Group()
grupo_sprites_meteoritos = pygame.sprite.Group()
grupo_sprites_astronautas = pygame.sprite.Group()
# Añadimos los sprites

grupo_sprites_todos.add(elementos.Fondo())
plataforma = elementos.Plataforma((posicion))
grupo_sprites_todos.add(plataforma)
grupo_sprites_nave.add(plataforma)
meteorito = elementos.Meteorito(posicion_spawn) 
astronauta = elementos.Atronauta(posicion_spawn)
vacio = elementos.Vacio(posicion_vacio)

# Creamos los contadores de vida y puntos
puntos = 0
vidas = 3


# Bucle principal del juego

while running:

    # Marcar los FPS

    reloj.tick(FPS)

    # Detectar que cierras el juego

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
     
    momento_actual = pygame.time.get_ticks()
    #   Capturamos teclas
    teclas = pygame.key.get_pressed()
    grupo_sprites_todos.update(teclas)

    # Hacemos que caigan asteroides
    
    momento_actual_meteoritos = momento_actual
    if (momento_actual_meteoritos > ultimo_meteorito_creado + 600):
        numero_aleatorio = random.randint(1, pantalla.get_width())
        posicion_spawn = (numero_aleatorio, -100)
        meteorito = elementos.Meteorito(posicion_spawn) 
        grupo_sprites_meteoritos.add(meteorito)
        grupo_sprites_todos.add(meteorito)
        ultimo_meteorito_creado = momento_actual_meteoritos

    # Hacemos que caigan astronautas
    momento_actual_astronautas = momento_actual
    if (momento_actual_astronautas > ultimo_astronauta_creado + 1500):
        numero_aleatorio = random.randint(1, pantalla.get_width())
        posicion_spawn = (numero_aleatorio, -100)
        astronauta = elementos.Atronauta(posicion_spawn)  
        grupo_sprites_astronautas.add(astronauta)
        grupo_sprites_todos.add(astronauta)
        ultimo_astronauta_creado = momento_actual_astronautas
        
   # Detectamos que los astronautas choquen con la nave, si choca matamos el sprite
    
    colision_astronautas = pygame.sprite.spritecollideany(plataforma, grupo_sprites_astronautas, pygame.sprite.collide_mask)

    if (colision_astronautas):
        colision_astronautas.kill()
        puntos += 1
    
    # Detectamos meteoritos que choquen con la nave, si choca se acaba el juego.
    
    colision_meteorito = pygame.sprite.spritecollideany(plataforma, grupo_sprites_meteoritos, pygame.sprite.collide_mask)
    
    if (colision_meteorito):
        colision_meteorito.kill()
        vidas -= 1

    # Si las vidas llegan a 0 perdemos.
    if (vidas == 0):
        running = False
    # Detectamos que los astronautas que caen choquen con el final de la pantalla.
       
    colision_vacio_astronautas = pygame.sprite.spritecollideany(vacio, grupo_sprites_astronautas, pygame.sprite.collide_rect)

    if (colision_vacio_astronautas):
       colision_vacio_astronautas.kill()
       puntos -= 5
    
    # Detectamos que los meteoritos caen al vacio y los borramos para ahorrar memoria.
    
    colision_vacio_meteoritos = pygame.sprite.spritecollideany(vacio, grupo_sprites_meteoritos, pygame.sprite.collide_rect)

    if (colision_vacio_meteoritos):
        colision_vacio_meteoritos.kill()
    
    
    # añadimos textos
    
    texto_puntos = str(puntos) 
    contador_puntos = elementos.Texto("Puntos: " + texto_puntos, puntos, 450, 100, color=(255, 255, 255), tamaño=20)
    texto_vidas = str(vidas)
    contador_vidas = elementos.Texto("Vidas restantes: " + texto_vidas, vidas, 450, 120, color=(255, 0, 0), tamaño=20)
    # Pintamos pantalla y grupos de sprites y pasamos frame

    pantalla.fill((24,5,5))
    grupo_sprites_todos.draw(pantalla)
    pantalla.blit(contador_puntos.surface, contador_puntos.rect)
    pantalla.blit(contador_vidas.surface, contador_vidas.rect)
    pygame.display.flip()

    
  
         
pygame.quit()

