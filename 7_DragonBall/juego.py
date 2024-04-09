import pygame
import elementos1
import pygame_menu
import random

#inicializamos el juego
pygame.init()

#Creamos pantalla y su tamaño
pantalla = pygame.display.set_mode((1366,768))

#creamos la frecuencia de creacion de esferas
ultimo_esferas_creado = 0
frecuencia_creacion_esferas = 10000

#creacion la creacion de enemigos
ultimo_enemigo_creado = 0
frecuencia_creacion_enemigo = 2000

#iniciamos la variable velocidad para picolo
velocidad = 3

#creamos un reloj 
reloj = pygame.time.Clock()

#fuente letras 
font= pygame.font.Font(pygame_menu.font.FONT_8BIT,20)

#crecion de la funcion dificultad para que en el menu se pueda elegir la dificultad del juego
def set_difficulty(value, difficulty):
    #cargamos los enemigos que se crearan mediante la dificultad
    global frecuencia_creacion_enemigo
    frecuencia_creacion_enemigo = difficulty

#funcion para inciar el juego con el menu
def start_the_game ():
    running = [True]
    global reloj
    global ultimo_esferas_creado
    global frecuencia_creacion_esferas
    global ultimo_enemigo_creado
    global frecuencia_creacion_enemigo

    #Cargamos personaje y su posicion
    posicion=(100 ,350)
    personaje = elementos1.Jugador(posicion,2)

    #Cargamos el fondo
    fondo = elementos1.Fondo()

    #cargamos picolo, su posicon y su velocidad inicial
    picolo = elementos1.Picolo((1200,500),velocidad)

    #creamos grupo de sprites de todo
    grupo_sprites_todos = pygame.sprite.Group()
    #creamos grupo de sprites del kame cada vez que dispare
    grupo_sprites_kame = pygame.sprite.Group()
    #creamos el grupo de sprites de las esferas que se iran creando
    grupo_sprites_esfera = pygame.sprite.Group()
    #creamos grupo de sprites de picolo
    grupo_sprites_picolo = pygame.sprite.Group()
    #grupo sprites de los rayos que dispara picolo
    grupo_sprites_rayos = pygame.sprite.Group()
    #creamos grupo sprites enemigos
    grupo_sprites_enemigos = pygame.sprite.Group()

    #añadimos el fondo al grupo sprites todos
    grupo_sprites_todos.add(fondo)
    #añadimos el personaje al grupo sprites todos
    grupo_sprites_todos.add(personaje)
    #añadimos picolo al grupo sprites todos
    grupo_sprites_todos.add(picolo)

    #añadimos el fondo al grupo sprites todos
    grupo_sprites_picolo.add(picolo)

    #creacion de la variable pausado con un booleano para alternar el juego entre pausado y no pausado
    pausado = False

    #cargmos la puntuacion de las esfreras con la clase Puntos de elementos1
    puntuacion_esferas = elementos1.Puntos()
    #cargmos las vidas de picolo con la clase Puntos de elementos1
    vidas_picolo = elementos1.Puntos()
    #cargmos las vidas del jugador con la clase Puntos de elementos1
    vidas_jugador = elementos1.Puntos()

    #bucle princiapl
    while running [0]:
        reloj.tick(90)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = [False]

        #capturamos teclas
        teclas = pygame.key.get_pressed()
        #la tecla ESC hace que el juego se pare y vuelva al menu
        if teclas[pygame.K_ESCAPE]:
          running[0] = False
        #la tecla b hace que el juego se pause
        if teclas[pygame.K_b]:
            pausado = not pausado

        #cuando no esta pausado realiza la funcion principal del juego
        if not pausado:
            #update funcion principal
            grupo_sprites_todos.update(teclas, grupo_sprites_todos, grupo_sprites_kame,grupo_sprites_esfera,grupo_sprites_picolo,puntuacion_esferas,vidas_picolo,running,grupo_sprites_enemigos,vidas_jugador,grupo_sprites_rayos)
            #obtenemos los ticks del juego para la creacion de esferas
            momento_actual = pygame.time.get_ticks()
            
            # creacion de esferas
            if momento_actual > ultimo_esferas_creado + frecuencia_creacion_esferas:
                    #cordenadas X de aparcicion esferas(no sobrepasan a picolo)
                    cordX = random.randint(0,1200)
                    cordY = random.randint(0,pantalla.get_height())
                    esfera = elementos1.Esferas((cordX, cordY))
                    grupo_sprites_todos.add(esfera)
                    grupo_sprites_esfera.add(esfera)
                    ultimo_esferas_creado = momento_actual

            #creacion enemigos
            if momento_actual > ultimo_enemigo_creado + frecuencia_creacion_enemigo:
                cordX = 1366
                cordY = random.randint(0,pantalla.get_height())
                enemigo = elementos1.Enemigos((cordX, cordY))
                grupo_sprites_todos.add(enemigo)
                grupo_sprites_enemigos.add(enemigo)
                ultimo_enemigo_creado = momento_actual

        #pintamos todo los sprites en la pantalla
        grupo_sprites_todos.draw(pantalla)

        #cuando esta pausado pintamos toda la informacion de las esfreas y barra de vidas, y un texto diciendo que esta pausado
        if pausado:
            texto = font.render("PAUSADO",True,"White")
            pantalla.blit(texto,(pantalla.get_width()//2 - texto.get_width()//2, pantalla.get_height()//2 - texto.get_height()//2))
            valor_puntuacion = font.render("Esferas del dragon " +str(puntuacion_esferas.getpuntuacion()),True,"Orange")
            pantalla.blit(valor_puntuacion, (0, 50))
            cuadrovida_goku = pygame.image.load("Imagenes/cuadrovidagoku.png")
            pantalla.blit(cuadrovida_goku,(0,10))
            pantalla.blit(personaje.barravida_goku.image, personaje.barravida_goku.rect)
            cuadrovida_picolo = pygame.image.load("Imagenes/cuadrovidapicolo.png")
            pantalla.blit(cuadrovida_picolo,(950,10))
            pantalla.blit(picolo.barravida_picolo.image, picolo.barravida_picolo.rect)

        #cuando no esta pausado pintamos toda la informacion de las esfreas y barra de vidas
        if not pausado : 
            valor_puntuacion = font.render("Esferas del dragon " +str(puntuacion_esferas.getpuntuacion()),True,"Orange")
            pantalla.blit(valor_puntuacion, (0, 50))
            cuadrovida_goku = pygame.image.load("Imagenes/cuadrovidagoku.png")
            pantalla.blit(cuadrovida_goku,(0,10))
            pantalla.blit(personaje.barravida_goku.image, personaje.barravida_goku.rect)
            cuadrovida_picolo = pygame.image.load("Imagenes/cuadrovidapicolo.png")
            pantalla.blit(cuadrovida_picolo,(950,10))
            pantalla.blit(picolo.barravida_picolo.image, picolo.barravida_picolo.rect)

        #si las vidas de picolo llegan a 0 el jugador gana 
        if vidas_picolo.getvidas_picolo() == 0:
            hasganado = pygame.image.load("Imagenes/hasganado.png")
            pantalla.blit(hasganado,(pantalla.get_width()//2 - hasganado.get_width()//2, pantalla.get_height()//2 - hasganado.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(3000)
        
        #si las vidas del jugador llegan a 0 el jugador pierde 
        if vidas_jugador.getvidas_jugador() == 0:
            hasperdido = pygame.image.load("Imagenes/hasperdido.png")
            pantalla.blit(hasperdido,(pantalla.get_width()//2 - hasperdido.get_width()//2, pantalla.get_height()//2 - hasperdido.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = [False]

        pygame.display.flip()

#imagen fondo menu
myimage = pygame_menu.baseimage.BaseImage(
    image_path="Imagenes/menu.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
)

#tema del menu
tema = pygame_menu.themes.Theme(
    background_color=myimage, 
    title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE,
    title_background_color=(255, 128, 0),
    title_font_shadow=True,
    title_font=pygame_menu.font.FONT_8BIT,
    title_font_size=50,
    widget_padding=35,
    widget_font=pygame_menu.font.FONT_8BIT,
    widget_font_size=35,
    widget_font_color = (255, 255, 255),
)
#creacion del menu
menu = pygame_menu.Menu('DragonBall Game', 1366,768, theme=tema)
#podemos seleccionar la dificultad del juego que queramos
menu.add.selector('Dificultad ', [('Facil', float('inf') ),('Dificil', 3000)], onchange=set_difficulty)
#boton para inciar el juego
menu.add.button('Jugar', start_the_game)
#boton para salir del juego
menu.add.button('Salir', pygame_menu.events.EXIT)

menu.mainloop(pantalla)

pygame.quit()