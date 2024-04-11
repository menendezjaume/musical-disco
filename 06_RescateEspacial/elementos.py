import pygame
import pygame_menu
score = 0
class Nave(pygame.sprite.Sprite):
    #Aqui ceamos el costructor
    def __init__(self, posicion) -> None:
        super().__init__()
        #Cargamos la imagen
        images = [pygame.image.load("astronave.png")]
        self.images = [pygame.transform.scale(images[0],(60,60))]
        self.indice_images = 0
        self.image = self.images[self.indice_images]
        self.contador_image = 0
        self.mask = pygame.mask.from_surface(self.image)

        #Cremamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        #Actualizamos la posicion del rectangulo
        self.rect.topleft=posicion
        self.ultimo_disparo = 0
        self.font = pygame.font.Font(None, 30)
        
        #Las vidas
        self.vidas = 3
        
    
    def update (self,*args: any,**kwargs: any):
        #Capturamos las teclas
        teclas = args[0]
        #Capturamos grupo_sprite_todos
        grupo_sprite_todos = args[1]
        #Capturamos grupo_sprite_balas
        grupo_sprite_balas = args[2]
        #Capturamos la pantalla
        pantalla = pygame.display.get_surface()
        
        global score
        
        #Gestionamos las teclas
        if teclas[pygame.K_LEFT]:
            self.rect.x -= 5
            self.rect.x = max(0, self.rect.x)
        #Aqui disparamos.
        if teclas[pygame.K_SPACE]:
            self.disparar(grupo_sprite_todos, grupo_sprite_balas)
        
        if teclas[pygame.K_RIGHT]:
            self.rect.x += 5
            pantalla = pygame.display.get_surface()
            self.rect.x = min(pantalla.get_width()-self.image.get_width(), self.rect.x)
            
            
        if teclas[pygame.K_UP]:
            self.rect.y -= 2
            self.rect.y = max(0, self.rect.y)
            
        if teclas[pygame.K_DOWN]:
            self.rect.y += 5
            pantalla = pygame.display.get_surface()
            self.rect.y = min(pantalla.get_height()-self.image.get_height(), self.rect.y)
            
        self.contador_image = (self.contador_image + 1) % 40
        self.indice_images = self.contador_image // 20
        #Capturar grupo sprite enemgios
        grupo_sprite_enemigos = args[3]
        #Capturamos la variable de control running
        running = args[4]

        grupo_sprite_aliados = args[5]
        aliado_colision = pygame.sprite.spritecollideany(self, grupo_sprite_aliados, pygame.sprite.collide_mask)
        if aliado_colision:
            aliado_colision.kill()
            score += 50

        enemigoColision = pygame.sprite.spritecollideany(self, grupo_sprite_enemigos)
        if enemigoColision:
            enemigoColision.kill()
            score -= 50
            self.vidas = self.vidas -1
            print(self.vidas)
            if self.vidas == 0:
                self.kill()
                running[0] = False
                
    def getvidas(self):
        return self.vidas 
    

    def disparar(self, grupo_sprite_todos, grupo_sprite_balas):
        momento_actual = pygame.time.get_ticks()
        if momento_actual >  self.ultimo_disparo +200:
            bala = Bala((self.rect.x + self.image.get_width() /2, self.rect.y))
            grupo_sprite_todos.add(bala)
            grupo_sprite_balas.add(bala)
            self.ultimo_disparo = momento_actual
    
class Enemigo(pygame.sprite.Sprite):
    #Aqui ceamos el costructor
    def __init__(self, posicion) -> None:
        super().__init__()
        #Cargamos la imagen
        imagen = pygame.image.load("roca.png")
        self.image = pygame.transform.scale(imagen,(60,40))
        # self.image = pygame.transform.rotate(self.image, 180)
        self.mask = pygame.mask.from_surface(self.image)
        #Cremamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        #Actualizamos la posicion del rectangulo
        self.rect.topleft = posicion
        
    def update (self,*args: any,**kwargs: any) -> None:
        global score
        self.rect.y += 3
        #Capturamos el argumento 2 -> grupo_sprite_balas
        grupo_sprite_balas = args[2]
        bala_colision = pygame.sprite.spritecollideany(self, grupo_sprite_balas, pygame.sprite.collide_mask)
        if bala_colision:
            score += 20
            self.kill()
            bala_colision.kill()

class Aliado(pygame.sprite.Sprite):
    #Aqui ceamos el costructor
    def __init__(self, posicion) -> None:
        super().__init__()
        #Cargamos la imagen
        imagen = pygame.image.load("astronauta.png")
        self.image = pygame.transform.scale(imagen,(60,40))
        # self.image = pygame.transform.rotate(self.image, 180)
        self.mask = pygame.mask.from_surface(self.image)
        #Cremamos un rectangulo a partir de la imagen
        self.rect = self.image.get_rect()
        #Actualizamos la posicion del rectangulo
        self.rect.topleft = posicion
        
    def update (self,*args: any,**kwargs: any) -> None:
        self.rect.y += 3
        #Capturamos el argumento 2 -> grupo_sprite_balas
        grupo_sprite_balas = args[2]
        bala_colision = pygame.sprite.spritecollideany(self, grupo_sprite_balas, pygame.sprite.collide_mask)
        if bala_colision:
            self.kill()
            bala_colision.kill()
            

class Fondo(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        images = pygame.image.load("Fondo3.jpg")
        pantalla = pygame.display.get_surface()
        self.image = pygame.transform.scale(images, (pantalla.get_width(), pantalla.get_height()))
        self.rect = self.image.get_rect()
        self.rect.topleft = (posicion)
        
    def update (self,*args: any,**kwargs: any) -> None:
        self.rect.y += 1
        #Capturamos la pantalla
        pantalla = pygame.display.get_surface()
        if self.rect.y >= pantalla.get_height():
            self.rect.y = - pantalla.get_height()
        
class Bala(pygame.sprite.Sprite):
    def __init__(self, posicion) -> None:
        super().__init__()
        image = pygame.image.load("./bola-de-fuego.png")
        self.image = pygame.transform.scale(image,(30,30))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = posicion
        
    def update (self,*args: any,**kwargs: any) -> None:
        self.rect.y -=5