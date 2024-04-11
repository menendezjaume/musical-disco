import pygame

class Nave(pygame.sprite.Sprite):
    
    def __init__(self, posicion,tamaño):
        super().__init__()
        self.nave=[pygame.transform.scale( pygame.image.load("nave1.png"),(tamaño,tamaño)),pygame.transform.scale( pygame.image.load("nave2.png"),(tamaño,tamaño))]
        self.indice=0
        self.contador=0
        self.image=self.nave[self.indice]
        self.contador_imagen=0
        self.rect=self.image.get_rect() 
        self.rect.topleft=posicion
        self.mask=pygame.mask.from_surface(self.image)


    def update(self, *args: any, **kwargs: any):

        teclas=args[0]
        self.tamaño = kwargs.get('tamaño', 0)
        
        pantalla=pygame.display.get_surface()
        self.contador=(self.contador+7)%40
        self.indice=self.contador//20
        self.image=self.nave[self.indice]
        if teclas[pygame.K_LEFT]:
            self.rect.x -=4
            self.rect.x = max(0,self.rect.x )
        if teclas[pygame.K_RIGHT]:
            self.rect.x +=4
            self.rect.x=min(pantalla.get_width()-self.tamaño,self.rect.x)
        if teclas[pygame.K_UP]:
            self.rect.y -=4
            self.rect.y=max(0,self.rect.y)
        if teclas[pygame.K_DOWN]:
            self.rect.y +=4
            self.rect.y=min(pantalla.get_height()-self.tamaño,self.rect.y)
        self.mask=pygame.mask.from_surface(self.image)
        

class Fondo(pygame.sprite.Sprite):
    def __init__(self,posicion):
        super().__init__()
        self.image=pygame.image.load("fondito.png")
         
        pantalla=pygame.display.get_surface()
        self.fondo=pygame.transform.scale(self.image, (pantalla.get_width(), pantalla.get_height()))
        self.rect=self.image.get_rect()
    
    def update(self, *args: any, **kwargs: any) -> None:
        pantalla=pygame.display.get_surface()
        pantalla.blit(self.fondo,((0,0))) 
        

class Meteorito(pygame.sprite.Sprite):
     
    def __init__(self, posicion):
        super().__init__()
        self.image=pygame.transform.scale( pygame.image.load("meteoro.png"),(40,40))
        self.rect=self.image.get_rect()
        self.rect.topleft=posicion
        self.mask=pygame.mask.from_surface(self.image)
        

    def update(self, *args: any, **kwargs: any):
        self.rect.y += 1
        pantalla = pygame.display.get_surface()
        if self.rect.y > pantalla.get_height():
            self.kill()
            running = args
        
      
class Astronauta(pygame.sprite.Sprite):
     
    def __init__(self, posicion):
        super().__init__()
        self.image=pygame.transform.scale( pygame.image.load("astronauta.png"),(60,60))
        self.rect=self.image.get_rect()
        self.rect.topleft=posicion

    def update(self, *args: any, **kwargs: any):
        self.rect.y += 1
        pantalla = pygame.display.get_surface()
        if self.rect.y > pantalla.get_height():
            self.kill()
            running = args

