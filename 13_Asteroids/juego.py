import pygame
import pygame_menu
import Fondo
import elementosXisco
import random

# Iniciar pygame, método Main
pygame.init()

# Crear la pantalla
tamaño = (1000, 800)
pantalla = pygame.display.set_mode(tamaño)
# pygame.display.set_caption("Trabajo de clase")

# Crear grupos de sprites
grupo_sprites_stars = pygame.sprite.Group()
grupo_sprites_todos = pygame.sprite.Group()
grupo_sprites_enemigos = pygame.sprite.Group()
grupo_sprites_balas = pygame.sprite.Group()
grupo_sprites_asteroides = pygame.sprite.Group()
grupo_sprites_asteroidesMinis = pygame.sprite.Group()
grupo_sprites_GameOver = pygame.sprite.Group()
# Añadir objetos al grupo de sprites
grupo_sprites_todos.add(Fondo.Fondo((0,0)))


# Creacion de planeta
posicion = (320, 360)
planeta = elementosXisco.Nave(posicion)

# Añadir el planeta al grupo de sprites
grupo_sprites_todos.add(planeta)
# grupo_sprites_nave.add(planeta)

font_score = pygame.font.Font(None, 32)
font_vida = pygame.font.Font(None, 32)

# dificultad
frecuenciaAparicionEnemigos = 4000
frecuenciaAparicionasteroide = 3500
frecuenciaAparicionStar = 6000
def set_difficulty(value, difficulty):
    global frecuenciaAparicionEnemigos
    global frecuenciaAparicionasteroide
    global frecuenciaAparicionStar
    if difficulty == 1:
        frecuenciaAparicionEnemigos = 4000
        frecuenciaAparicionasteroide = 3500
        frecuenciaAparicionStar = 6000
    else:
        frecuenciaAparicionEnemigos = 5000
        frecuenciaAparicionasteroide = 4500
        frecuenciaAparicionStar = 4500

def puntuacion(x, y):
    score = font_score.render("Puntuación: " + str(elementosXisco.puntuacion), True, (255, 255, 255))
    pantalla.blit(score, (x, y))

def vidas(x, y):
    vidas = font_vida.render("Vidas: " + str(elementosXisco.Nave.getVida(planeta)), True, (255, 255, 255))
    pantalla.blit(vidas, (x, y))
def vidasAmarilla(x, y):
    vidas = font_vida.render("Vidas: " + str(elementosXisco.Nave.getVida(planeta)), True, (255, 255, 0))
    pantalla.blit(vidas, (x, y))
def vidasRoja(x, y):
    vidas = font_vida.render("Vidas: " + str(elementosXisco.Nave.getVida(planeta)), True, (255, 0, 0))
    pantalla.blit(vidas, (x, y))


def start_the_game():

    # Inicializar reloj y FPS controlamos la velocidad del juego
    reloj = pygame.time.Clock()
    FPS = 60
    running = True
    ultimo_enemigo_creado = 0
    ultimo_star_creado = 0
    ultimo_asteroide_creado = 0
    # global vidas_restantes
    # vidas_restantes = 3
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # creacion de enemigos
        randomAparicion = random.randint(1, 4)
        if randomAparicion == 1:
            coordY = 900
            coordX = random.randint(100,600)
        if randomAparicion == 2:
            coordY = random.randint(100,600)
            coordX = 1050
        if randomAparicion == 3:
            coordY = random.randint(100,700)
            coordX = -50
        if randomAparicion == 4:
            coordY = 900
            coordX = random.randint(100,600)

        momento_actual = pygame.time.get_ticks()
        if (momento_actual > ultimo_enemigo_creado + frecuenciaAparicionEnemigos):
            # X = random.randint(200, 400)
            enemigo = elementosXisco.Enemigo((coordX, coordY), planeta)
            grupo_sprites_todos.add(enemigo)
            grupo_sprites_enemigos.add(enemigo)
            ultimo_enemigo_creado = momento_actual

        if (momento_actual > ultimo_star_creado + frecuenciaAparicionStar):
            starX = random.randint(100, 900)
            starY = random.randint(100,700)
            star = elementosXisco.Star((starX, starY))
            grupo_sprites_todos.add(star)
            grupo_sprites_stars.add(star)
            ultimo_star_creado = momento_actual

        if (momento_actual > ultimo_asteroide_creado + frecuenciaAparicionasteroide):
            asteroide = elementosXisco.Asteroide((coordX, coordY))
            grupo_sprites_todos.add(asteroide)
            grupo_sprites_asteroides.add(asteroide)
            ultimo_asteroide_creado = momento_actual
        if (elementosXisco.Nave.getVida(planeta) <= 0):
            gameOver = elementosXisco.GameOver((0, 0))
            pantalla.fill((255, 255, 255))
            grupo_sprites_todos.add(gameOver)
            grupo_sprites_GameOver.add(gameOver)

        # # teclas
        keys = pygame.key.get_pressed()
        planeta.movement(keys)

        # Crear y actualizar balas
        # if keys[pygame.K_SPACE]:
        #     planeta.disparar()



        # Actualizar y dibujar los sprites
        grupo_sprites_todos.update(keys, grupo_sprites_todos, grupo_sprites_balas, grupo_sprites_enemigos, grupo_sprites_stars, grupo_sprites_asteroides, grupo_sprites_asteroidesMinis)
        grupo_sprites_todos.draw(pantalla)

        # Eliminar las balas fuera de la pantalla
        for bala in planeta.balas:
            if bala.rect.bottom < 0:
                bala.kill()

        # Redibujar la pantalla
        if elementosXisco.Nave.getVida(planeta) > 2:
            vidas(10, 40)
        if elementosXisco.Nave.getVida(planeta) == 2:
            vidasAmarilla(10, 40)
        if elementosXisco.Nave.getVida(planeta) == 1:
            vidasRoja(10, 40)

        puntuacion(10, 10)
        pygame.display.flip()
        # Limitar el bucle a los FPS definidos
        reloj.tick(FPS)
# Crea el menú
menu = pygame_menu.Menu('Welcome', 900, 700, theme=pygame_menu.themes.THEME_ORANGE)

# Agrega un cuadro de texto, un selector y dos botones como en tu código original
menu.add.text_input('Name:', default='Player 1')
menu.add.selector('Difficulty:', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

# Ejecuta el menú
menu.mainloop(pantalla)

# Salir del juego
pygame.quit()

