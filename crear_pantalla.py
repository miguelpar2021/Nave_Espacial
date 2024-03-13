import pygame
import random
import math
from pygame import mixer

#Iniciarlizar Pygame
pygame.init()

#Crear la pantalla
pantalla = pygame.display.set_mode((800,600))

#Titulo e Icono
pygame.display.set_caption("Invasion Espacial")
icono= pygame.image.load('icono_img.png')
pygame.display.set_icon(icono)
fondo = pygame.image.load("fondo_ok.png")

#Agregar Musica
mixer.music.load('fondo.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)


#Jugador y sus variables
img_jugador= pygame.image.load('nave.png')
jugador_x = 368
jugador_y = 500
jugador_x_cambio=0



#Variable del Enemigo
img_enemigo= []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio= []
enemigo_y_cambio=[]
cantida_enemigos= 8


for e in range(cantida_enemigos):
    img_enemigo.append(pygame.image.load('alien.png'))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)



#Variable de la bala
balas = []
img_bala = pygame.image.load("bala.png")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 1
bala_visible = False

#Puntaje
puntaje=0
fuente = pygame.font.Font('Transcorner.ttf',32)
texto_x=10
texto_y=10

#Texto Final
fuente_final= pygame.font.Font('Transcorner.ttf',42)

def texto_final():
    mi_fuente_final=fuente_final.render("FIN DE JUEGO",True,(255,255,255))
    pantalla.blit(mi_fuente_final,(250,200))

#funcion de mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f'Puntaje: {puntaje}',True,(255,255,255))
    pantalla.blit(texto,(x,y))


#Funcion para llamar al jugador
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))


#Funcion para llamar al Enemigp
def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x,y))


#Funcion Disparar bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible=True
    pantalla.blit(img_bala,(x+16,y+10))

#Funcion para Colisiones
def hay_colision(x_1,y_1,x_2,y_2):
    distancia=math.sqrt(math.pow(x_1-x_2,2)+math.pow(y_1-y_2,2))
    if distancia < 27 :
        return True
    else:
        return False



#Loop del juego
se_ejecuta =True
while se_ejecuta:


    # Imagen de fondo
    pantalla.blit(fondo,(0,0))


    #Evento de cerrar
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        #Evento de presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                sonido_disparo=mixer.Sound('laser.mp3')
                sonido_disparo.set_volume(0.1)
                sonido_disparo.play()
                nueva_bala = {
                    "x": jugador_x,
                    "y": jugador_y,
                    "velocidad": -2
                }
                balas.append(nueva_bala)


        #Evento de soltar tecla
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or  evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0


    #modificar ubicacion del jugador
    jugador_x += jugador_x_cambio

    #Mantener dentro del borde al jugador
    if jugador_x <= 0:
        jugador_x=0
    elif jugador_x >= 736:
        jugador_x=736



    # modificar ubicacion del Enemigo
    for e in range(cantida_enemigos):

        #Fin del juego
        if enemigo_y[e]>500:
            for k in range(cantida_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        # Mantener dentro del borde al Enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        for bala in balas:
            colision = hay_colision(enemigo_x[e], enemigo_y[e], bala["x"], bala["y"])
            if colision:
                sonido_colision=mixer.Sound('muerte_e.mp3')
                sonido_colision.set_volume(0.3)
                sonido_colision.play()
                bala_y = 500
                bala_visible = False
                puntaje += 1

                enemigo_x[e] = random.randint(0, 736)
                enemigo_y[e] = random.randint(50, 200)
                break

        enemigo(enemigo_x[e], enemigo_y[e],e)


    #Movimiento de Bala
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)
    for bala in balas:
        bala["y"] += bala["velocidad"]
        pantalla.blit(img_bala, (bala["x"] + 16, bala["y"] + 10))
        if bala["y"] < 0:
            balas.remove(bala)



    jugador(jugador_x,jugador_y)
    mostrar_puntaje(texto_x,texto_y)

    #Actualizar
    pygame.display.update()