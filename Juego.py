import pygame
import random
import math
from pygame import mixer 
# Inicializar pygame
pygame.init()


# Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

# Título e Icono
pygame.display.set_caption("Invasión Espacial")
icono = pygame.image.load("C:/Users/josue/OneDrive/Desktop/Python/new/ovni.png")
pygame.display.set_icon(icono)


#agregar musica
mixer.music.load("C:/Users/josue/OneDrive/Desktop/Python/new/Musicafondo.mp3")
mixer.music.set_volume(0.3)
mixer.music.play(-1)



# Fondo
fondo = pygame.image.load("C:/Users/josue/OneDrive/Desktop/Python/new/Fondo.jpg")

# Variables del Jugador
img_jugador = pygame.image.load("C:/Users/josue/OneDrive/Desktop/Python/new/cohete.png")
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0

# Variables de los enemigos
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("C:/Users/josue/OneDrive/Desktop/Python/new/enemigo.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

# Variables de las balas
img_bala = pygame.image.load("C:/Users/josue/OneDrive/Desktop/Python/new/bala.png")
bala_x = 0
bala_y = 500
bala_y_cambio = 1
bala_visible = False

# Puntaje
puntaje = 0
fuente = pygame.font.SysFont(None, 32)  # fuente del sistema
texto_x = 10
texto_y = 10

# texto final de juego

fuente_final = pygame.font.SysFont(None, 32)  # Usa fuente del sistema

def texto_final():
    mi_fuente_final = fuente_final.render("Game Over", True, (255, 255, 255))
    pantalla.blit(mi_fuente_final,(75,200))


# Funciones
def mostrar_puntaje(x, y):
    texto = fuente.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

def enemigo(x, y, ene):
    pantalla.blit(img_enemigo[ene], (x, y))

def disparar_bala(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

def hay_colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    return distancia < 27

# Loop del juego
se_ejecuta = True

while se_ejecuta:
    pantalla.blit(fondo, (0, 0))

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x, bala_y)

        # Evento soltar teclas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Movimiento del jugador
    jugador_x += jugador_x_cambio
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736

    # Movimiento del enemigo
    for e in range(cantidad_enemigos):
        #fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y [k] = 1000

            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 0.5
            enemigo_y[e] += enemigo_y_cambio[e]
        elif enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -0.5
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colisión
        colision = hay_colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if colision:
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento de la bala
    if bala_visible:
        disparar_bala(bala_x, bala_y)
        bala_y -= bala_y_cambio

        if bala_y <= 0:
            bala_y = 500
            bala_visible = False

    jugador(jugador_x, jugador_y)
    mostrar_puntaje(texto_x, texto_y)

    pygame.display.update()
