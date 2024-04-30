import pygame
import pygame_menu
import random
import subprocess
import os

pygame.init()

# icono
icono = pygame.image.load("logo.png")
pygame.display.set_icon(icono)

# Pantalla
tamanyo = (1920, 1080)
pantalla = pygame.display.set_mode(tamanyo, pygame.RESIZABLE)

# Funciones para acceder a los juegos


def astroRescue():
    wd = os.getcwd()
    os.chdir("./01_AstroRescue")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def marioBros():
    wd = os.getcwd()
    os.chdir("./02_MarioBros")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def riskyRescue():
    wd = os.getcwd()
    os.chdir("./03_RiskyRescue")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def spaceInvaders():
    wd = os.getcwd()
    os.chdir("./04_SpaceInvaders")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def flappyBird():
    wd = os.getcwd()
    os.chdir("./05_FlappyBird")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def rescateEspacial():
    wd = os.getcwd()
    os.chdir("./06_RescateEspacial")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def dragonBall():
    wd = os.getcwd()
    os.chdir("./07_DragonBall")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def planetDefenders():
    wd = os.getcwd()
    os.chdir("./08_PlanetDefenders")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)

# def 9():
#     wd = os.getcwd()
#     os.chdir("./09_")
#     subprocess.Popen("ls")
#     subprocess.Popen(["python3", "juego.py"])
#     os.chdir(wd)
# def 10():
#     wd = os.getcwd()
#     os.chdir("./10_")
#     subprocess.Popen("ls")
#     subprocess.Popen(["python3", "juego.py"])
#     os.chdir(wd)


def spaceShooter():
    wd = os.getcwd()
    os.chdir("./11_SpaceShooter")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def catInvaders():
    wd = os.getcwd()
    os.chdir("./12_CatInvaders")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def asteroids():
    wd = os.getcwd()
    os.chdir("./13_Asteroids")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def astroRain():
    wd = os.getcwd()
    os.chdir("./14_AstroRain")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def skeletonAlienArmadaVsMexicanCat():
    wd = os.getcwd()
    os.chdir("./15_SkeletonAlienArmadaVsMexicanCat")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def PlanetDefender():
    wd = os.getcwd()
    os.chdir("./16_PlanetDefender")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


def RetroPlane():
    wd = os.getcwd()
    os.chdir("./17_RetroPlane")
    subprocess.Popen("ls")
    subprocess.Popen(["python3", "juego.py"])
    os.chdir(wd)


pantalla.fill((255, 255, 255))

pygame.display.flip()

myimage = pygame_menu.baseimage.BaseImage(
    image_path="logo.png",
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL,
)

mytheme = pygame_menu.Theme(background_color=(myimage),
                            title_background_color=(0, 0, 0),
                            )


pygame.display.flip()
menu = pygame_menu.Menu('', pantalla.get_width(),
                        pantalla.get_height(), theme=mytheme)
menu.add.button('Astro Rescue', astroRescue)
menu.add.button('Mario Bros', marioBros)
menu.add.button('Risky Rescue', riskyRescue)
menu.add.button('Space Invaders', spaceInvaders)
menu.add.button('Flappy Bird', flappyBird)
menu.add.button('Rescate Espacial', rescateEspacial)
menu.add.button('Dragon Ball', dragonBall)
menu.add.button('Planet Defenders', planetDefenders)
# menu.add.button('9', )
# menu.add.button('10', )
menu.add.button('Space Shooter', spaceShooter)
menu.add.button('Cat Invaders', catInvaders)
menu.add.button('Asteroids', asteroids)
menu.add.button('Astro Rain', astroRain)
menu.add.button('Skeleton Alien Armada VS Mexican Cat', skeletonAlienArmadaVsMexicanCat)
menu.add.button('Planet Defender', PlanetDefender)
menu.add.button('RetroPlane', RetroPlane)


menu.mainloop(pantalla)

pygame.quit()
