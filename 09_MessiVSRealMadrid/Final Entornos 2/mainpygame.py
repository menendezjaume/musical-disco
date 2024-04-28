import pygame
import Elementos2
import random
import pygame_menu
#inicialicamos el juego
pygame.init()

#creamos la pantalla
tamanio = (800,960)
pantalla = pygame.display.set_mode(tamanio)

# Cargar la imagen del fondo del menú
imagen_fondo_menu = pygame_menu.baseimage.BaseImage(
    image_path="fondo.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
)

# Crear el tema del menú
tema_menu = pygame_menu.themes.Theme(
    background_color=imagen_fondo_menu,
    title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
    title_font=pygame_menu.font.FONT_8BIT,
    title_font_size=40,
    title_offset=(170, 260),
    widget_padding=20,
    widget_font=pygame_menu.font.FONT_8BIT,
    widget_font_size=30,
    widget_font_color=(220, 220, 220),  
)


#creamos un reloj
reloj = pygame.time.Clock()
FPS = 18

# creamos una fuente para la pausa
font = pygame.font.Font(None, 30)

#booleano de control
# posicion = (650,700)
# nave = Elementos2.Nave(posicion)
# fondo = Elementos2.Fondo()
# #crear un grupo de sprites
# #grupo_sprites = pygame.sprite.Group(fondo)
# #grupo_sprites.add(nave)
#
# #grupo_sprites.add(Elementos2.Nave((400,200)))
# #grupo_sprites.add(Elementos2.Nave((500,100)))
# #grupo_sprites.add(Elementos2.Nave((100,300)))
#
# grupo_sprites_todos = pygame.sprite.Group()
# grupo_sprites_enemigos = pygame.sprite.Group()
# grupo_sprites_bala = pygame.sprite.Group()
#
# # grupo_sprites_todos.add(Elementos2.Fondo, (0, ))
# grupo_sprites_todos.add(fondo)
# grupo_sprites_todos.add(nave)
# enemigo = Elementos2.Enemigo((50,50))
# grupo_sprites.add(Elementos2.Enemigo((70, 70)))

#crear u na variable que almacene la última creacion de enemigo
ultimo_enemigo_creado = 0
frecuencia_creacion_enemigo = 750

contador_balondeoro = 0
contador_enemigo2 = 0
contador_enemigo3 = 0
limite_enemigo2 = 5
limite_enemigo3 = 5
limite_balondeoro = 1

frecuencia_creacion_enemigo1 = 0
frecuencia_creacion_enemigo2 = 0
frecuencia_creacion_enemigo3 = 0
frecuencia_creacion_balondeoro = 0


def set_difficulty(value, difficulty):
    global frecuencia_creacion_enemigo
    frecuencia_creacion_enemigo = difficulty
    

def start_the_game():
    running = [True]
    global ultimo_enemigo_creado
    global frecuencia_creacion_enemigo
    global frecuencia_creacion_enemigo1
    global frecuencia_creacion_enemigo2
    global frecuencia_creacion_enemigo3
    global frecuencia_creacion_balondeoro
    global FPS
    global reloj
    
    
    posicion_nave = (650, 700)
    nave = Elementos2.Nave(posicion_nave)

    fondo = Elementos2.Fondo()

    # grupo_sprites.add(Elementos2.Nave((400,200)))
    # grupo_sprites.add(Elementos2.Nave((500,100)))
    # grupo_sprites.add(Elementos2.Nave((100,300)))

    grupo_sprites_todos = pygame.sprite.Group()
    grupo_sprites_enemigos = pygame.sprite.Group()
    grupo_sprites_bala = pygame.sprite.Group()
    grupo_sprites_balon = pygame.sprite.Group()

     # grupo_sprites_todos.add(Elementos2.Fondo, (0, - ))
    grupo_sprites_todos.add(fondo)
    grupo_sprites_todos.add(nave)

    pausado = False

    # capturamos las teclas

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

        if teclas[pygame.K_SPACE]:
            nave.disparar(grupo_sprites_todos, grupo_sprites_bala)


        if not pausado:
            #controlar la aparicion de enemigos
            tiempo_transcurrido = pygame.time.get_ticks() / 1000
            if tiempo_transcurrido < 5:
                frecuencia_creacion_enemigo1 = 700
            elif tiempo_transcurrido < 8:
                frecuencia_creacion_enemigo1 = 1000
                frecuencia_creacion_enemigo2 = 700
            else:
                frecuencia_creacion_enemigo1 = 1300
                frecuencia_creacion_enemigo2 = 1000
                frecuencia_creacion_enemigo3 = 900
                frecuencia_creacion_balondeoro = 8000
            
            # creacion de enemigos
            momento_actual = pygame.time.get_ticks()
            if (momento_actual > ultimo_enemigo_creado + frecuencia_creacion_enemigo):
                cordX = random.randint(0, pantalla.get_width())
                cordY = 0
                enemigo = Elementos2.Enemigo((cordX, cordY))
                grupo_sprites_todos.add(enemigo)
                grupo_sprites_enemigos.add(enemigo)
                ultimo_enemigo_creado = momento_actual

                if tiempo_transcurrido >= 5 and contador_enemigo2 < limite_enemigo2:
                    cordX2 = random.randint(0, pantalla.get_width())
                    cordY2 = 0
                    enemigo2 = Elementos2.Enemigo2((cordX2, cordY2))
                    grupo_sprites_todos.add(enemigo2)
                    grupo_sprites_enemigos.add(enemigo2)
                    ultimo_enemigo_creado = momento_actual
                    contador_enemigo2 +=1
                    contador_balondeoro +=1
                else:
                    contador_enemigo2 = 0
                    contador_balondeoro = 0

                if tiempo_transcurrido >= 8 and contador_enemigo3 < limite_enemigo3 and contador_balondeoro < limite_balondeoro: 
                    cordX3 = random.randint(0, pantalla.get_width())
                    cordY3 = 0
                    enemigo3 = Elementos2.Enemigo3((cordX3, cordY3))
                    grupo_sprites_todos.add(enemigo3)
                    grupo_sprites_enemigos.add(enemigo3)
                    ultimo_enemigo_creado = momento_actual
                    contador_enemigo3 +=1
                    contador_balondeoro += 1
                else:
                    contador_enemigo3 = 0
                    contador_balondeoro = 0

                if tiempo_transcurrido >= 15: 
                    cordX3 = random.randint(0, pantalla.get_width())
                    cordY3 = 0
                    balondeoro = Elementos2.BalonDeOro((cordX3, cordY3))
                    grupo_sprites_todos.add(balondeoro)
                    grupo_sprites_enemigos.add(balondeoro)
                    ultimo_enemigo_creado = momento_actual
            
            grupo_sprites_todos.update(teclas, grupo_sprites_todos, grupo_sprites_bala, grupo_sprites_enemigos, grupo_sprites_balon,
                                          running)

        # capturamos las teclas

        # pintaremos:
        # pantalla.fill((255,255,255))
        # grupo_sprites_todos.update(teclas, grupo_sprites_todos, grupo_sprites_bala, grupo_sprites_enemigos, running)
        grupo_sprites_todos.draw(pantalla)

        nave.mostrar_contadores(pantalla)

        # if pausado:
        #     texto = font.render("PAUSA", True, "White")
        #     pantalla.blit(texto, (pantalla.get_width() / 2, pantalla.get_height() / 2))

        # redibujar la pantala
        pygame.display.flip()
    pass

menu = pygame_menu.Menu('getBalonDor()', 800, 960, theme=tema_menu)

menu.add.text_input('Name :', default='')
menu.add.selector('Difficulty :', [('Hard', 200), ('Easy', 2000)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(pantalla)
#finalizamos el juego
pygame.quit()