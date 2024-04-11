import pygame
import Elementos3
import random
import pygame_menu
pygame.init()

#icono
icono = pygame.image.load("nave.png")
pygame.display.set_icon(icono)

tamanyo=(800,600)
pantalla=pygame.display.set_mode(tamanyo)

reloj=pygame.time.Clock()
FPS = 325

font=pygame.font.Font(None,30)

#almacen del ultimo enemigo
ultimo_enemigo_creado=0
frecuencia_creacion_enemigo=3000

ultimo_astronauta_creado=0
frecuencia_creacion_astronauta=3500
vidas = 3
astronautas_recogidos = 0
def restart_game():
    global vidas
    global astronautas_recogidos
    vidas = 3
    astronautas_recogidos = 0
def restar_vida():
    global vidas
    vidas -= 1

fondo=Elementos3.Fondo((0,0))
nave = Elementos3.Nave((350,350))
def set_difficulty(value, difficulty):
    global frecuencia_creacion_enemigo
    global frecuencia_creacion_astronauta
    frecuencia_creacion_enemigo = difficulty
    frecuencia_creacion_astronauta = difficulty
    
pausado= False
def start_the_game():
    running=True
    global ultimo_enemigo_creado
    global frecuencia_creacion_enemigo
    global frecuencia_creacion_astronauta
    global FPS
    global grupo_sprites_enemigos
    global grupo_sprites_astronauta
    global grupo_sprites_todos
    global reloj
    global pausado
    global vidas
    global astronautas_recogidos
    grupo_sprites_todos=pygame.sprite.Group()
    grupo_sprites_enemigos=pygame.sprite.Group()
    grupo_sprites_astronauta=pygame.sprite.Group()
    ultimo_enemigo_creado = 0
    ultimo_astronauta_creado = 0


    grupo_sprites_todos.add(fondo)
    grupo_sprites_todos.add(nave)
    
    restart_game()
    while running:
        reloj.tick(FPS)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
                
        teclas=pygame.key.get_pressed()
        if teclas[pygame.K_o]:
            running=False
        
        if not pausado:
            momento_actual=pygame.time.get_ticks()
            if(momento_actual>ultimo_enemigo_creado+frecuencia_creacion_enemigo):
                coordX=random.randint(0,pantalla.get_width())
                coordY=-200
                #creacion enemigo
                enemigo=Elementos3.Enemigo((coordX,coordY))
                grupo_sprites_todos.add(enemigo)
                grupo_sprites_enemigos.add(enemigo)
                ultimo_enemigo_creado=momento_actual
            if(momento_actual>ultimo_astronauta_creado+frecuencia_creacion_astronauta):
                coordX=random.randint(0,pantalla.get_width())
                coordY=-200
                #creacion enemigo
                astronauta=Elementos3.Astronauta((coordX,coordY))
                grupo_sprites_todos.add(astronauta)
                grupo_sprites_astronauta.add(astronauta)
                ultimo_astronauta_creado=momento_actual
                
            colisiones_astronautas=pygame.sprite.spritecollideany(nave,grupo_sprites_astronauta,pygame.sprite.collide_mask)
            colisiones_nave=pygame.sprite.spritecollideany(nave,grupo_sprites_enemigos,pygame.sprite.collide_mask)
            
            if colisiones_nave:
                restar_vida()
                nave.rect.topleft = (350, 350)
            if vidas <= 0:
                running = False
            if colisiones_astronautas:
                colisiones_astronautas.kill() 
                astronautas_recogidos += 1
        
        pantalla.fill((255,255,255))

        grupo_sprites_todos.update(teclas, grupo_sprites_todos, grupo_sprites_enemigos,grupo_sprites_todos)
        grupo_sprites_todos.draw(pantalla)
        

        
        texto_vidas = font.render("Vidas: " + str(vidas), True, (255, 0, 0))
        pantalla.blit(texto_vidas, (10, 10))
        
        texto_astronautas = font.render("Princesas: " + str(astronautas_recogidos), True, (0, 255, 0))
        pantalla.blit(texto_astronautas, (10, 40))
        
            
        pygame.display.flip()
menu = pygame_menu.Menu('Welcome', 400, 300,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='Name')
menu.add.selector('Difficulty :', [('Hard', 500), ('Easy', 1000)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(pantalla)
pygame.quit()