import pygame
import pygame_menu
import Elementos
from Elementos import Enemigo

pygame.init()

pygame.display.set_caption('Planet Defenders')

pantalla = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()
FPS = 60

# Elementos
fondo = Elementos.Fondo()
planeta = Elementos.Planeta()
anillo = Elementos.Anillo()

# Grupos de sprites
grupo_sprites_todos = pygame.sprite.Group(fondo, planeta, anillo)
grupo_sprites_enemigos = pygame.sprite.Group()
grupo_sprites_proyectiles = pygame.sprite.Group()

dificultad = 1
def mostrar_menu():
    global dificultad
    dificultad = 1
    menu = pygame_menu.Menu('Planet Defenders', 640, 640, theme=pygame_menu.themes.THEME_DARK)
    menu.add.selector('Dificultad :', [('Normal', 1), ('Difícil', 2)], onchange=establecer_dificultad)
    menu.add.button('Jugar', reiniciar_juego)
    menu.add.button('Salir', pygame_menu.events.EXIT)
    menu.mainloop(pantalla)

def establecer_dificultad(valor, dificultad_elegida):
    global dificultad
    if dificultad_elegida == 2:
        dificultad = 2
    else:
        dificultad = 1

def reiniciar_juego():
    grupo_sprites_todos.empty()
    grupo_sprites_enemigos.empty()
    grupo_sprites_proyectiles.empty()

    fondo = Elementos.Fondo()
    planeta = Elementos.Planeta()
    anillo = Elementos.Anillo()

    grupo_sprites_todos.add(fondo, planeta, anillo)

    iniciar_juego()

def iniciar_juego():
    salir = False
    tiempo = 0
    tiempo_ultimo_enemigo = 0
    fuente = pygame.font.Font(None, 36)
    demora_enemigos = 1000
    if dificultad == 2:
        demora_enemigos = 700
    else:
        demora_enemigos = 1500

    while not salir:
        tiempo += clock.get_time()
        clock.tick(FPS)

        # Gestionar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir = True

        if grupo_sprites_todos.sprites()[2].vida == 0:
            salir = True
            mostrar_menu()

        teclas = pygame.key.get_pressed()

        # Generación de enemigos
        tiempo_ultimo_enemigo += clock.get_time()

        if tiempo_ultimo_enemigo > demora_enemigos:
            nuevo_enemigo = Enemigo(pantalla)
            grupo_sprites_todos.add(nuevo_enemigo)
            grupo_sprites_enemigos.add(nuevo_enemigo)
            tiempo_ultimo_enemigo = 0
            if demora_enemigos > 150:   # Por cada enemigo que aparezca, la demora de aparición de enemigos se reduce por 5ms
                demora_enemigos -= 5

        # Gestionar cambios
        grupo_sprites_todos.update(teclas, grupo_sprites_todos, grupo_sprites_proyectiles, grupo_sprites_enemigos)
        grupo_sprites_todos.draw(pantalla)

        vidas_texto = fuente.render(f"Vidas: {grupo_sprites_todos.sprites()[2].vida}", True, (255, 255, 255))
        puntos_texto = fuente.render(f"Puntos: {grupo_sprites_todos.sprites()[2].puntos}", True, (255, 255, 255))
        powerup_texto = fuente.render(f"Powerup: {round(grupo_sprites_todos.sprites()[2].powerup, 1)}%", True, (255, 255, 255))
        pantalla.blit(vidas_texto, (10, 10))
        pantalla.blit(puntos_texto, (630 - puntos_texto.get_width(), 610))
        pantalla.blit(powerup_texto, (10, 610))

        # Redibujar el juego
        pygame.display.flip()

    pygame.quit()

mostrar_menu()