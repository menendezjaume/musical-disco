import pygame
import pygame_menu
from objetos import Cat, Background, Enemigo

pygame.init()

#Pantalla

tamañopantalla = (1000,600) #Controla el tamaño de la pantalla
pantalla = pygame.display.set_mode(tamañopantalla)
pygame.display.set_caption("Skeleton Alien Armada Invasion Vs Mexican Cat Who Is Really Just A Cat With A Sombrero And Maracas Defending His Chimoles From Aliens That Are Actually Skeletons Wearing Sombreros And Trompetas The Videogame (Epilepsy Warning)")

#Tiempo/Ticks
velocidad_fondo = 15    #Wow, me pregunto que hará esto
cambio_imagen_tiempo = 150  # Cada cuantos frames cambia el sprite del jugador
tiempo_anterior_imagen = pygame.time.get_ticks() #Cosas de frames
image_index = 0 #Mas cosas de frames
clock = pygame.time.Clock() #Reloj, xd
FPS = 30 #Frames por segundo (No cambiar, juego diseñado a 30 FPS)
frames_enemigo = 15 #Cada cuantos frames aparece un enemigo   

#Fuente para pausa

font = pygame.font.Font(None,30)

def set_difficulty(value, difficulty):
    global frames_enemigo
    frames_enemigo = difficulty
    pass
def start_the_game():
    global salir
    salir = False
    contador_frames = 0 #Contador de frames para enemigos (MANTENER AQUI, SI NO PETA)

    #Clases Importadas

    cat = Cat((450,505)) #Posicion Inical Jugador
    background = Background(velocidad_fondo)

    # Sprites

    todos_los_sprites = pygame.sprite.Group()
    proyectiles = pygame.sprite.Group() #Más que los proyectiles, aquí está la mascara de colisión de los mismos
    enemigos = pygame.sprite.Group()  # Grupo para los enemigos
    todos_los_sprites.add(cat)
    
    #Menú de pausa
    
    pausado = False
    tiempo_pausa = pygame.time.get_ticks()
    
    # El juego
    
    while not salir:
        pantalla.fill((0,0,0))
        background.update()
        background.draw(pantalla)
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_ESCAPE]:
            salir = True
            
        # Control del tiempo entre pulsaciones para la pausa
        if teclas[pygame.K_p] and pygame.time.get_ticks() - tiempo_pausa > 200:  # Evitar múltiples pulsaciones rápidas
            pausado = not pausado
            tiempo_pausa = pygame.time.get_ticks()  # Actualizar el tiempo de la última pulsación
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                salir = True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                cat.activar_disparo()  # Activar el disparo cuando se suelta la barra espaciadora

        #Tiempo

        tiempo_actual = pygame.time.get_ticks()
        
        
        if not pausado:
            #Actualizar los sprites
            todos_los_sprites.update(teclas, tiempo_actual, cambio_imagen_tiempo, enemigos, proyectiles=proyectiles)
            
            #Controles
        
            cat.disparar(teclas, proyectiles, todos_los_sprites)
            
            #Creacion enemigos
            
            velocidad_enemigo = 30
            contador_frames += 1
            if contador_frames >= frames_enemigo:
                contador_frames = 0
                
                if frames_enemigo == 30:  # Dificultad Easy
                    velocidad_enemigo = 10
                elif frames_enemigo == 15:  # Dificultad Hard
                    velocidad_enemigo = 30  # Puedes ajustar este valor según lo que consideres adecuado
                    
                    
                nuevo_enemigo = Enemigo((-200, 0), velocidad_enemigo)
                todos_los_sprites.add(nuevo_enemigo)
                enemigos.add(nuevo_enemigo)

                nuevo_enemigo = Enemigo((1000, -100), velocidad_enemigo)
                todos_los_sprites.add(nuevo_enemigo)
                enemigos.add(nuevo_enemigo)

            colision_enemigo = pygame.sprite.spritecollide(cat, enemigos, False, pygame.sprite.collide_mask)
            if colision_enemigo:
                cat.kill()  # Eliminar al gato si hay colisión con algún enemigo
                salir = True
            
        
        if pausado:
            texto = font.render("PAUSA PARA TACOS COMPADRE", True, "White")
            text_rect = texto.get_rect(center=(pantalla.get_width() / 2, pantalla.get_height() / 2))
            pantalla.blit(texto, text_rect)

        # No idea really
        todos_los_sprites.draw(pantalla)
        pygame.display.flip()

        #FPS

        clock.tick(FPS)


    
#Menu
menu = pygame_menu.Menu("It's Morbin' Time", 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)
menu.add.selector('Difficulty :', [('Hard', 15), ('Easy', 30)], onchange=set_difficulty)
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(pantalla)


# Menu
# main_menu = True
# while main_menu:
#     events = pygame.event.get()
#     for event in events:
#         if event.type == pygame.QUIT:
#             main_menu = False
#             salir = True
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
#             main_menu = False

#     pantalla.fill((0, 0, 0))
#     background.update()
#     background.draw(pantalla)
#     menu.mainloop(pantalla, events)

#     pygame.display.flip()
pygame.quit()