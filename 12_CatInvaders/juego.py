import pygame
import elements
import random
import pygame_menu




#Iniciamos el Juego
pygame.init()

#Tamaño de la Pantalla y posicion de la Nave
tamaño = (1920, 1080)
pantalla = pygame.display.set_mode((tamaño), pygame.FULLSCREEN)
#posicion = (960,550)
posicion = (710,480)
x = (710)
y = (480)

#Frecuencias del Enemigo
ultimo_enemigo_creado = 0
frecuencia_creacion_enemigo = 150
frecuencia_creacion_enemigo_Especial = 2

#Reloj del juego y FPS
reloj = pygame.time.Clock()
FPS = 60
#Puntuacion
score = [0]
scrx1, scry1 = 10, 10

#Vidas
vidas = 3
vrdx1 , vrdy1 = 10, 35

#Fuente para el texto
font = pygame.font.Font(None, 30)

def pintar_Puntos(scrx, scry): 
    score_texto = font.render("Score: " + str(score), True, "Green")
    pantalla.blit(score_texto, (scrx, scry))

def pintar_Vidas(vdx, vdy):
    vida_texto = font.render("Vidas: " + str(vidas), True, "Green")    
    pantalla.blit(vida_texto, (vdx, vdy))

def set_difficulty(value, difficulty):
    global frecuencia_creacion_enemigo
    frecuencia_creacion_enemigo = difficulty

def start_the_game():
    
    #Booleano de Control
    running = [True]
    
    #Globals
    global ultimo_enemigo_creado
    global reloj
    global FPS
    global frecuencia_creacion_enemigo
    global font
    global score
    global vidas

    #Grupo de Sprites
    grupo_sprites_todos = pygame.sprite.Group()
    grupo_sprites_enemigos = pygame.sprite.Group()
    grupo_sprites_balas = pygame.sprite.Group()

    #Añadimos las cosas a los sprites
    fondo = elements.Fondo()
    planeta = elements.Planeta((posicion))
    bala = elements.Bala((0,0),0)
    grupo_sprites_todos.add(fondo, planeta, bala)

    pausado = False
    reinicio = False

    #Bucle Principal
    while running[0]:
        #Limitamos los FrameRate
        reloj.tick(FPS)

        #Gestionamos la Salida
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running[0] = False

        #Capturamos la Teclas
        teclas = pygame.key.get_pressed()
        
        #Capturamos la posicion del Mouse
        pos = pygame.mouse.get_pos()
        dis = pygame.mouse.get_pressed()
        
        #KeyBinds
        if teclas[pygame.K_ESCAPE]:
            running[0] = False

        if teclas[pygame.K_SPACE]:
            pausado = not pausado
        
        if not pausado:
            
            #Aparicion  del enemigo
            if random.randint(0,1000) < frecuencia_creacion_enemigo:
                spawn = random.randint(1,4)
                if spawn == 1:
                    cordx1 = random.randint(-120, 0)
                    cordy1 = random.randint(0, 1080)
                    enemigo = elements.Enemigo((cordx1, cordy1))
                    grupo_sprites_todos.add(enemigo)
                    grupo_sprites_enemigos.add(enemigo)
                elif spawn == 2:
                    cordx2 = random.randint(0,1920)
                    cordy2 = random.randint(-120, 0)
                    enemigo = elements.Enemigo((cordx2, cordy2))
                    grupo_sprites_todos.add(enemigo)
                    grupo_sprites_enemigos.add(enemigo)
                elif spawn == 3:
                    cordx3 = random.randint(1920,2120)
                    cordy3 = random.randint(0, 1080)
                    enemigo = elements.Enemigo((cordx3, cordy3))
                    grupo_sprites_todos.add(enemigo)
                    grupo_sprites_enemigos.add(enemigo)
                elif spawn == 4:
                    cordx4 = random.randint(0,1920)
                    cordy4 = random.randint(1080, 1300)
                    enemigo = elements.Enemigo((cordx4, cordy4))
                    grupo_sprites_todos.add(enemigo)
                    grupo_sprites_enemigos.add(enemigo)
            
            #Aparicion enemigo Especial
            if random.randint(0,1000) < frecuencia_creacion_enemigo_Especial:
                spawn = random.randint(1,4)
                if spawn == 1:
                    cordx1 = random.randint(-120, 0)
                    cordy1 = random.randint(0, 1080)
                    enemigo = elements.Enemigo_Especial((cordx1, cordy1))
                    grupo_sprites_todos.add(enemigo)
                    grupo_sprites_enemigos.add(enemigo)
                elif spawn == 2:
                    cordx2 = random.randint(0,1920)
                    cordy2 = random.randint(-120, 0)
                    enemigo = elements.Enemigo_Especial((cordx2, cordy2))
                    grupo_sprites_todos.add(enemigo)
                    grupo_sprites_enemigos.add(enemigo)
                elif spawn == 3:
                    cordx3 = random.randint(1920,2120)
                    cordy3 = random.randint(0, 1080)
                    enemigo = elements.Enemigo_Especial((cordx3, cordy3))
                    grupo_sprites_todos.add(enemigo)
                    grupo_sprites_enemigos.add(enemigo)
                elif spawn == 4:
                    cordx4 = random.randint(0,1920)
                    cordy4 = random.randint(1080, 1300)
                    enemigo = elements.Enemigo_Especial((cordx4, cordy4))
                    grupo_sprites_todos.add(enemigo)
                    grupo_sprites_enemigos.add(enemigo)

            #Movemos a los enemigos
            for enemigo in grupo_sprites_enemigos:
                enemigo.movimiento_enemigo(planeta)

            #Colisiones con el Planeta
            for enemigo in grupo_sprites_enemigos:
                if pygame.sprite.collide_mask(enemigo, planeta):
                    vidas -= 1
                    grupo_sprites_enemigos.remove(enemigo)
                    grupo_sprites_todos.remove(enemigo)

            #Para poder volver a Jugar      
            if vidas <= 0:
                if not reinicio:
                    reinicio = pygame.time.get_ticks()
                    vidas = 3
                    score[0] = 0
                    for enemigo in grupo_sprites_enemigos:
                        enemigo.kill()
                    reinicio = False
                    menu.mainloop(pantalla)                   
                    
                    
            grupo_sprites_todos.update(teclas, grupo_sprites_todos, grupo_sprites_balas, grupo_sprites_enemigos, running, x,y,pos,posicion, dis, score)         
            
        #Pintamos la Pantalla
        pantalla.fill((80,80,80))
        grupo_sprites_todos.draw(pantalla)
        
        #Cuando esta Pausado
        if pausado:
            texto = font.render("PAUSA", True, "Green")
            pantalla.blit(texto, (pantalla.get_width() / 2.115, pantalla.get_height() / 3.15))
           
            
        #Pintamos la puntuacion
        pintar_Puntos(scrx1, scry1)
        #Pintamos las vidas
        pintar_Vidas(vrdx1, vrdy1)
        #Redibujamos la Pantalla
        pygame.display.flip()
        
    pass


menu = pygame_menu.Menu('Welcome', 400, 300, theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='Nombre')
menu.add.selector('Difficulty :', [('Hard', 100), ('Easy', 40)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(pantalla)


#Finalizamos el Juego
pygame.quit()