import pygame
import elementos
import pygame_menu


pygame.init()

pygame.mixer.init()

#  Cargamos los sonidos de game over y disparo de nave
sonido_game_over = pygame.mixer.Sound("game-over-super-mario-made-with-Voicemod.mp3")
sonido_disparo = pygame.mixer.Sound("LaserZapsFastByRev PE431403.wav")
sonido_disparo.set_volume(0.20)

# Cargamos y ajustamos la música de fondo
pygame.mixer.music.load("cyberpunk-150207.mp3")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1) # El argumento -1 indica reproducción en bucle
# Creamos un reloj para los FPS
reloj = pygame.time.Clock()
FPS = 18
# Creamos la pantalla
espacio = (1920,1080)
screen = pygame.display.set_mode(espacio, pygame.FULLSCREEN)
posicion = (screen.get_width() / 2, screen.get_height() / 1.5)
nave = elementos.Nave(posicion)
font = pygame.font.Font(None, 30)
# fondo = eljuego.Fondo()
ultimo_enemigo_creado = 0
frecuencia_creacion_enemigo = 750
velocidad_enemigo = 22
screen_actual = False

def set_difficulty(value, difficulty):
    global frecuencia_creacion_enemigo
    global velocidad_enemigo
    global frecuencia_disparo_enemigo
    frecuencia_creacion_enemigo = difficulty

    if difficulty == 200:
        velocidad_enemigo = 23
        nave.set_cooldown(500)
    else:
        velocidad_enemigo = 20
        nave.set_cooldown(800)

def game_over(parametros):
    running = [True]
    while running[0]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = [False]

        sonido_game_over.play()
        pygame.mixer.music.pause()  # El argumento -1 indica reproducción en bucle

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            running[0] = False


        screen.fill((0, 0, 0))  # Fondo negro

        texto_game_over = font.render("¡Game Over!", True, "White")
        screen.blit(texto_game_over, (screen.get_width() / 2 - 100, screen.get_height() / 2 - 50))

        texto_puntuacion = font.render(f"Puntuación: {parametros.getPuntuacion()}", True, "White")
        screen.blit(texto_puntuacion, (screen.get_width() / 2 - 100, screen.get_height() / 2))

        texto_salir = font.render("Presiona ESC para salir", True, "White")
        screen.blit(texto_salir, (screen.get_width() / 2 - 100, screen.get_height() / 2 + 50))

        pygame.display.flip()

    pygame.mixer.music.play(-1)  # El argumento -1 indica reproducción en bucle
    sonido_game_over.stop()


def start_the_game():
    # Do the job here !

    running = [True]
    global ultimo_enemigo_creado
    global frecuencia_creacion_enemigo
    global FPS
    global reloj
    global nave

    # posicion = (screen.get_width() / 2, screen.get_height() / 1.5)
    posicionP = (screen.get_width() / 2.025, screen.get_height() * 1.5)
    # nave = elementos.Nave(posicion)
    fondo = elementos.Fondo()
    planeta = elementos.Planeta(posicionP)
    parametros = elementos.Parametros()

    grupo_sprites_todos = pygame.sprite.Group()
    grupo_sprites_enemigos = pygame.sprite.Group()
    grupo_sprites_bala = pygame.sprite.Group()
    grupo_sprites_planeta = pygame.sprite.Group()
    grupo_sprites_bala_enemigo = pygame.sprite.Group()
    grupo_sprites_enemigos_fuertes = pygame.sprite.Group()

    grupo_sprites_todos.add(fondo)
    grupo_sprites_todos.add(planeta)
    grupo_sprites_todos.add(nave)
    grupo_sprites_planeta.add(planeta)

    pausado = False

    # bucle principal
    while running[0]:
        # Limitamos el bucle al framrate definido
        reloj.tick(FPS)
        # gestionar la salida
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = [False]

        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            running[0] = False

        if teclas[pygame.K_p]:
            pausado = not pausado

        if teclas[pygame.K_SPACE]:
            sonido_disparo.play()


        if not pausado:
            # creacion de enemigos
            numero_enemigos = 1
            enemigos_por_fila = 1
            enemigos_creados = 0
            # creacion de enemigos
            momento_actual = pygame.time.get_ticks()
            if enemigos_creados < numero_enemigos and (
                    momento_actual > ultimo_enemigo_creado + frecuencia_creacion_enemigo):
                for i in range(enemigos_por_fila):
                    cordX = i * (screen.get_width() / enemigos_por_fila)
                    cordY = 0
                    enemigo = elementos.Enemigo((cordX, cordY), velocidad_enemigo, grupo_sprites_planeta)
                    grupo_sprites_enemigos.add(enemigo)
                    grupo_sprites_todos.add(enemigo)
                    enemigos_creados += 1
                    ultimo_enemigo_creado = momento_actual

                # Crear enemigo fuerte
            momento_actual = pygame.time.get_ticks()
            grupo_sprites_todos.update(teclas, grupo_sprites_todos, grupo_sprites_bala, grupo_sprites_enemigos,
                                           running, grupo_sprites_planeta, parametros, grupo_sprites_bala_enemigo, grupo_sprites_enemigos_fuertes)
        grupo_sprites_todos.draw(screen)

        vidas = font.render(f"Vidas: {parametros.getVidas()}", True, "White")
        screen.blit(vidas, (10, 20))
        puntos = font.render(f"Puntos: {parametros.getPuntuacion()} ", True, "White")
        screen.blit(puntos, (10, 40))

        planeta_colision = pygame.sprite.spritecollideany(nave, grupo_sprites_planeta, pygame.sprite.collide_mask)
        if planeta_colision:
            game_over(parametros)

        if parametros.getVidas() < 0:
            game_over(parametros)


        if pausado:
            texto = font.render("PAUSA", True, "White")
            screen.blit(texto, (screen.get_width() / 2, screen.get_height() / 2))
        # redibujar la pantala
        pygame.display.flip()
    pass

menu = pygame_menu.Menu('Buenas', 400, 300, theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('ID :', default='')
menu.add.selector('Dificultad :', [('Fácil', 2000), ('Difícil', 200)], onchange=set_difficulty)
menu.add.button('Jogar', start_the_game)
menu.add.button('Finalizar', pygame_menu.events.EXIT)

menu.mainloop(screen)
pygame.quit()