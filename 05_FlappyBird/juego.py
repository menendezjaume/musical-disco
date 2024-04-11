import pygame
import constructor
import pygame_menu
import random

pygame.init()

#icono
icono = pygame.image.load("Imagenes/pajaro-abajo.png")
pygame.display.set_icon(icono)

#Pantalla
tamanyo = (850, 478)
pantalla = pygame.display.set_mode(tamanyo)

#Reloj
reloj = pygame.time.Clock()
FPS = 60
#Juego
def pause():
    loop = 1
    # write("PAUSED", 500, 150)
    # write("Press Space to continue", 500, 250)
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = 0
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_RETURN:
                    loop = 0
                if event.type == pygame.K_RETURN:
                    pantalla.fill((0, 0, 0))
                    loop = 0
        pygame.display.update()
        # screen.fill((0, 0, 0))
        reloj.tick(60)

def set_difficulty(value, set_difficulty):
    tubo_dificil = pygame.image.load("Imagenes/tubo1.png")
    tubo_dificil = pygame.transform.scale(tubo_dificil, (300,478))
    tubo1_dificil_sprite = constructor.Tubo((600,0), tubo_dificil)
def start_the_game():
    running = [True]
    global todos
    global pantalla
    global reloj
    global FPS

    tamanyo = pygame.sprite.Group()
    tamanyo = (850, 478)
    #Pajaro
    posicion = (200, 239)
    pajaro = constructor.Pajaro(posicion)
    #Pantalla con sol
    con_sol = pygame.image.load("Imagenes/Fondo.jpg")
    con_sol = pygame.transform.scale(con_sol, (pantalla.get_width(), con_sol.get_height()))
    #Pantalla sin sol
    sin_sol = pygame.image.load("Imagenes/Fondo2.png")
    sin_sol = pygame.transform.scale(con_sol, (pantalla.get_width(), con_sol.get_height()))
    #Tubo1
    tubo1 = pygame.image.load("Imagenes/tubo1.png")
    tubo1 = pygame.transform.scale(tubo1, (600,478))
    tubo1_facil_sprite = constructor.Tubo((600,0), tubo1)
    #Tubo2
    tubo2 = pygame.image.load("Imagenes/tubo2.png")
    tubo2 = pygame.transform.scale(tubo2, (600,478))
    tubo2_facil_sprite = constructor.Tubo((1000,0), tubo2)
    #Tubo3
    tubo3 = pygame.image.load("Imagenes/tubo3.png")
    tubo3 = pygame.transform.scale(tubo3, (600,478))
    tubo3_facil_sprite = constructor.Tubo((1400,0), tubo3)
    #Tubo 4
    tubo4_facil_sprite = constructor.Tubo((1800,0), tubo2)

    #Sprites
    #todos
    todos = pygame.sprite.Group()
    # grupo_sprites_pajaro = pygame.sprite.Group()
    todos.add(constructor.Fondo((0,0),con_sol))
    todos.add(constructor.Fondo((pantalla.get_width(),0), sin_sol))
    todos.add(tubo1_facil_sprite)
    todos.add(tubo2_facil_sprite)
    todos.add(tubo3_facil_sprite)
    todos.add(tubo4_facil_sprite)
    todos.add(pajaro)
    #Tubos
    tubos = pygame.sprite.Group()
    tubos.add(tubo1_facil_sprite)
    tubos.add(tubo2_facil_sprite)
    tubos.add(tubo3_facil_sprite)
    tubos.add(tubo4_facil_sprite)


    while running[0]:
        teclas = pygame.key.get_pressed()
        reloj.tick(FPS)
        # if event.type == pygame.K_RETURN:
        #             pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #Coli ion
        tubo_colision = pygame.sprite.spritecollideany(pajaro, tubos, pygame.sprite.collide_mask)
        if tubo_colision:
            running[0]= False
            

        pantalla.fill((255,255,255))
        todos.update(todos, running, teclas)
        todos.draw(pantalla)

        pygame.display.flip()

# mymenu = pygame_menu.widgets.MENUBAR_STYLE_NONE
myimage = pygame_menu.baseimage.BaseImage(
    image_path = "Imagenes/Fondo.jpg",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

# todos.draw(pantalla)
pygame.display.flip()
myfont = pygame_menu.font.FONT_8BIT
mytheme = widget_font=myfont
mytheme = pygame_menu.themes.THEME_GREEN
mytheme.background_color= myimage
# mytheme.widgets = mymenu
mytheme.font = myfont
menu = pygame_menu.Menu('Flappy Bird', pantalla.get_width(), pantalla.get_height(), theme=mytheme) #theme = pygame_menu.themes.THEME_GREEN)
# menu.add.text_input('Nombre: ', default='Jugador 1')
# menu.add.selector('Dificulad: ', [('Facil', 0), ('Dificil', 1)], onchange= set_difficulty)
menu.add.button('Jugar', start_the_game)
menu.add.button('Salir', pygame_menu.events.EXIT)

menu.mainloop(pantalla)

pygame.quit()