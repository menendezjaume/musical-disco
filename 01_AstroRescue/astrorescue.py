import pygame
import rescElementos
import random
import pygame_menu

# Iniciamos el juego
pygame.init()

# Creamos la pantalla
tamaño = (800, 600)
pantalla = pygame.display.set_mode(tamaño)

def set_difficulty(value, difficulty):
    global frecuencia_creacion_enemigos
    global frecuencia_creacion_paracaidistas

    if difficulty == 1:  # Difícil
        frecuencia_creacion_enemigos = 500
        frecuencia_creacion_paracaidistas = 6000
    elif difficulty == 2:  # Fácil
        frecuencia_creacion_enemigos = 3000
        frecuencia_creacion_paracaidistas = 4000

def start_the_game():
    
    # Creamos la puntuacion
    puntuacion = 0

    # Creamos un reloj para limitar el framerate
    reloj = pygame.time.Clock()
    FPS = 60

    # Booleano de control
    running = True

    # Creamos la nave
    posicion = (360,540)
    nave = rescElementos.Nave(posicion)

    # Creamos un grupo de sprites
    grupo_sprite_todos = pygame.sprite.Group()
    grupo_sprite_enemigos = pygame.sprite.Group()
    grupo_sprite_balas = pygame.sprite.Group()
    grupo_sprite_paracaidistas = pygame.sprite.Group()

    grupo_sprite_todos.add(rescElementos.Fondo((0,0)))
    grupo_sprite_todos.add(nave)  

    paracaidista = rescElementos.Paracaidista((100, 50))
    enemigo = rescElementos.Enemigo((50,50))
    grupo_sprite_enemigos.add(enemigo)
    grupo_sprite_paracaidistas.add(paracaidista)
    # Creamos una variable que almacena la ultima vez que se creo un enemigo
    ultimo_enemigo_creado = 0
    frecuencia_creacion_enemigos = 1000

    # Creamos una variable que almacena la ultima vez que se creo un paracaidista
    ultimo_paracaidista_creado = 0
    frecuencia_creacion_paracaidistas = 4000

    # Creamos el bucle principal
    while running:
        
        # Limitamos el bucle al framerate que hemos definido
        reloj.tick(FPS)
        
        # Gestionamos la salida
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # teclas = pygame.key.get_pressed()

        # Detectar colisiones entre la nave y los enemigos + paracaidistas
        nave.detectar_colisiones_nave_enemigos(grupo_sprite_enemigos)
        nave.detectar_colisiones_nave_paracaidistas(grupo_sprite_paracaidistas)

        colisiones_nave_paracaidistas = pygame.sprite.spritecollideany(nave, grupo_sprite_paracaidistas)
        if colisiones_nave_paracaidistas:
            # Eliminar al paracaidista al colisionar con la nave
            colisiones_nave_paracaidistas.kill() 
            puntuacion += 100
        
        # Detectar colisiones entre enemigos y nave
        colisiones_nave_enemigos = pygame.sprite.spritecollideany(nave, grupo_sprite_enemigos)
        if colisiones_nave_enemigos:
            # Reducir vida a la nave al colisionar con el enemigo
            nave.vida -= 1

        # Detectar colisiones entre balas y enemigos
        colisiones_balas_enemigos = pygame.sprite.groupcollide(grupo_sprite_balas, grupo_sprite_enemigos, True, True)
        for bala, enemigos in colisiones_balas_enemigos.items():
            puntuacion += len(enemigos) * 50

        # Si nos eliminan, acaba la partida automaticamente
        if nave.vida <= 0:
            running = False

        # Creacion de enemigos
        momento_actual_enemigos = pygame.time.get_ticks()
        if (momento_actual_enemigos > ultimo_enemigo_creado + frecuencia_creacion_enemigos):
            cordX = random.randint(0, pantalla.get_width())
            cordY = -200
            # Creamos el enemigo y lo añadimos a los grupos
            enemigo = rescElementos.Enemigo((cordX, cordY))
            grupo_sprite_todos.add(enemigo)
            grupo_sprite_enemigos.add(enemigo)
            # Actualizamos el momento del ultimo enemigo creado
            ultimo_enemigo_creado = momento_actual_enemigos
            
        # Creacion de paracaidistas
        momento_actual_paracaidistas = pygame.time.get_ticks()
        if (momento_actual_paracaidistas > ultimo_paracaidista_creado + frecuencia_creacion_paracaidistas):
            cordX = random.randint(0, pantalla.get_width())
            cordY = -100
            # Creamos el paracaidista y lo añadimos a los grupos
            paracaidista = rescElementos.Paracaidista((cordX, cordY))
            grupo_sprite_todos.add(paracaidista)
            grupo_sprite_paracaidistas.add(paracaidista)

            # Actualizamos el momento del ultimo paracaidista creado
            ultimo_paracaidista_creado = momento_actual_paracaidistas

        # Capturamos las teclas
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_SPACE]:
            nave.disparar(grupo_sprite_todos, grupo_sprite_balas)
        
        # Pintamos
        pantalla.fill((255, 255, 255))
        grupo_sprite_todos.update(teclas, grupo_sprite_todos, grupo_sprite_balas, grupo_sprite_enemigos, grupo_sprite_paracaidistas)
        grupo_sprite_todos.draw(pantalla)

        # Dibujar la puntuacion en la pantalla
        fuente = pygame.font.Font(None, 36)
        texto_puntuacion = fuente.render("Puntuación: " + str(puntuacion), True, (255, 255, 255))
        pantalla.blit(texto_puntuacion, (10, 10))  

        # Redibujar la pantalla
        pygame.display.flip()

menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='John Doe')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(pantalla)

    # Finalizamos el juego
pygame.quit()