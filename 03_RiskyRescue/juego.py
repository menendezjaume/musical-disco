import pygame
import Risky_elements
import random
import pygame_menu

# Inicializamos el juego
pygame.init()

# Creamos la pantalla
tamaño = (1000, 800)
pantalla = pygame.display.set_mode(tamaño)


imagen_fondo_menu = pygame_menu.baseimage.BaseImage(
    image_path="fondo_menu.jpg",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
)

tema_menu = pygame_menu.themes.Theme(
    background_color=imagen_fondo_menu, 
    title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE,
    title_font=pygame_menu.font.FONT_8BIT,
    title_font_size=50,
    widget_padding=35,
    widget_font=pygame_menu.font.FONT_BEBAS,
    widget_font_size=35,
    widget_font_color = (255, 255, 255),
)

# Creamos un reloj
reloj = pygame.time.Clock()
FPS = 30

# Creamos una fuente para la pausa
font = pygame.font.Font(None, 30)
fuente_game_over = pygame.font.Font(None, 50)

# Variables globales
ultimo_enemigo_creado = 0
ultimo_astronauta_creado = 0
frecuencia_creacion_enemigo = 500  # Valor por defecto
frecuencia_creacion_astronauta = 1500  # Valor por defecto


def set_difficulty(value, difficulty):
    global frecuencia_creacion_enemigo
    frecuencia_creacion_enemigo = difficulty
    global frecuencia_creacion_astronauta
    frecuencia_creacion_astronauta = difficulty/2

def start_the_game():
    running = [True]
    global ultimo_enemigo_creado
    global ultimo_astronauta_creado
    global vidas 
    global puntuacion

    puntuacion = 0
    vidas = 3
    posicion = (650, 700)
    nave = Risky_elements.Nave(posicion , vidas , puntuacion)
    fondo = Risky_elements.Fondo()



    grupo_sprites_todos = pygame.sprite.Group()
    grupo_sprites_enemigos = pygame.sprite.Group()
    grupo_sprites_astronautas = pygame.sprite.Group()
    grupo_sprites_bala = pygame.sprite.Group()

    grupo_sprites_todos.add(fondo)
    grupo_sprites_todos.add(nave)

  

    pausado = False

    while running[0]:
        reloj.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = [False]

        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_ESCAPE]:
            running[0] = False

        if teclas[pygame.K_p]:
            pausado = not pausado

        if not pausado:
            momento_actual = pygame.time.get_ticks()

            if (momento_actual > ultimo_enemigo_creado + frecuencia_creacion_enemigo):
                cordX = random.randint(0, pantalla.get_width())
                cordY = -140
                enemigo = Risky_elements.Enemigo((cordX, cordY) , nave)
                grupo_sprites_todos.add(enemigo)
                grupo_sprites_enemigos.add(enemigo)
                ultimo_enemigo_creado = momento_actual

            if (momento_actual > ultimo_astronauta_creado + frecuencia_creacion_astronauta):
                cordX = random.randint(0, pantalla.get_width())
                cordY = -90
                astronauta = Risky_elements.Astronauta((cordX, cordY), nave)
                grupo_sprites_todos.add(astronauta)
                grupo_sprites_astronautas.add(astronauta)
                ultimo_astronauta_creado = momento_actual

            grupo_sprites_todos.update(teclas, grupo_sprites_todos, grupo_sprites_bala, grupo_sprites_enemigos,grupo_sprites_astronautas,
                                       running)
            
          
            grupo_sprites_todos.draw(pantalla)

        textoP = font.render(f"Puntuacion: {nave.getpuntuacion()}", True, "White")
        pantalla.blit(textoP, (10,10))
        textoV = font.render(f"Vidas: {nave.getvidas()}", True, "White")
        pantalla.blit(textoV, (10,30))

        vidas = nave.getvidas()
       


        if pausado:
            texto = font.render("PAUSA", True, "White")
            pantalla.blit(texto, (pantalla.get_width() / 2, pantalla.get_height() / 2))

        pygame.display.flip()

        
        if vidas <= 0:            
                    
                    pantalla.fill((0, 0, 0))
                    texto_game_over = pygame.image.load("game-over.jpg")
                    x = (pantalla.get_width() - texto_game_over.get_width()) // 2
                    y = (pantalla.get_height() - texto_game_over.get_height()) // 2
                    pantalla.blit(texto_game_over, (x, y))
                    textoP = fuente_game_over.render(f"Puntuacion: {nave.getpuntuacion()}", True, "White")
                    pantalla.blit(textoP, (pantalla.get_width()/2.75,pantalla.get_height()/1.3))
                    pygame.display.flip()
                    pygame.time.delay(2000)
                    
            
            

# Menú principal
     
menu = pygame_menu.Menu('Risky Rescue', 1000, 800, theme=tema_menu)

menu.add.text_input('Name :', default='')
menu.add.selector('Difficulty :', [('Hard', 400), ('Easy', 1500)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)


# Mostramos el menú y ejecutamos el juego
 
menu.mainloop(pantalla)

# Finalizamos el juego
pygame.quit()