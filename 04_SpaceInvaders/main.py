import pygame
import pygame_menu
import elementos3
import random

pygame.init()
tamanyo=(800,600)
pantalla=pygame.display.set_mode(tamanyo)
font=pygame.font.Font(None,40)
reloj=pygame.time.Clock()
FPS=60
frecuencia_caida=1000
frecuencia_astronautas=5000

def set_difficulty(value, difficulty):
    global frecuencia_caida
    frecuencia_caida=difficulty

def start_the_game():
    running=True
    tamaño=90
    nave=elementos3.Nave((200,500),tamaño)
    fondo=elementos3.Fondo((0,0))
    grupo_sprites_todos=pygame.sprite.Group()
    grupo_sprites_meteoritos=pygame.sprite.Group()
    grupo_sprites_astronautas=pygame.sprite.Group()
    vidas=3
    astronautasrecogidos=0
    tiempo_transcurrido = 0
    grupo_sprites_todos.add(nave)
   

    ultimo_objeto_creado=0
    ultimo_meteorito_creado=0
    while running:
        
        reloj.tick(FPS) 
        tiempo_pasado = reloj.get_time() 
        tiempo_transcurrido += tiempo_pasado / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False

    
        teclas=pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            running=False

        grupo_sprites_todos.update(teclas)
        momento_actual=pygame.time.get_ticks()
        if (momento_actual>ultimo_meteorito_creado+frecuencia_caida):
            meteorito=elementos3.Meteorito((random.randint(0, pantalla.get_width()),-100))
            grupo_sprites_todos.add(meteorito)
            grupo_sprites_meteoritos.add(meteorito)


            ultimo_meteorito_creado=momento_actual
        if(frecuencia_caida!=100):
            
            if (momento_actual>ultimo_objeto_creado+frecuencia_astronautas):
                astronauta=elementos3.Astronauta((random.randint(0, pantalla.get_width()),-100))
                grupo_sprites_todos.add(astronauta)
                grupo_sprites_astronautas.add(astronauta)
                ultimo_objeto_creado=momento_actual
            tamaño=90
        else:
            tamaño=40
            nave.image = pygame.transform.scale(nave.nave[nave.indice], (tamaño, tamaño))
            nave.mask = pygame.mask.from_surface(nave.image)

        colisiones_nave_meteoritos = pygame.sprite.spritecollideany(nave, grupo_sprites_meteoritos,pygame.sprite.collide_mask)
        colisiones_nave_astronautas = pygame.sprite.spritecollideany(nave, grupo_sprites_astronautas, pygame.sprite.collide_mask)
        
        if (colisiones_nave_meteoritos):
            vidas-=1
            colisiones_nave_meteoritos.kill()
        if(vidas<=0):
            running=False
        if(colisiones_nave_astronautas):
           colisiones_nave_astronautas.kill()
           astronautasrecogidos+=1

       
       
            
        fondo.update()
        grupo_sprites_todos.draw(pantalla)
        if frecuencia_caida != 100:
            texto_vidas = font.render("Vidas: " + str(vidas), True, (255, 0, 0))
            pantalla.blit(texto_vidas, (10, 10))
            texto_astronauta = font.render("Astronautas rescatados: " + str(astronautasrecogidos), True, (0, 255, 0))
            pantalla.blit(texto_astronauta, (10, 40))
        else:
            texto_tiempo = font.render("Tiempo: {:.2f} segundos".format(tiempo_transcurrido), True, (255, 255, 255))
            pantalla.blit(texto_tiempo, (10, 40))
            texto_vidas = font.render("Vidas: " + str(vidas), True, (255, 0, 0))  # Incluido en modo "Dodge"
            pantalla.blit(texto_vidas, (10, 10))
        
        pygame.display.flip()
menu = pygame_menu.Menu('Welcome', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='Jugador')
menu.add.selector('Difficulty :', [('Hard', 200), ('Easy', 2000),('Dodge', 100)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

menu.mainloop(pantalla)
pygame.quit()