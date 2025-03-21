import pygame
import random
import math
import io

#Inicializa pygame
pygame.init()

#Crear la pantalla
pantalla = pygame.display.set_mode((800, 600))

#Título e icono
pygame.display.set_caption("Ataque de los saiyans")
icono = pygame.image.load("./recursos/bola.png")
pygame.display.set_icon(icono)

#Recursos de sonido
musica_fondo = pygame.mixer.music.load("./recursos/MusicaFondo.mp3")

#Imágen de fondo de pantalla
fondo = pygame.image.load("./recursos/escenario.jpg")

#Variables del jugador
img_jugador = pygame.image.load("./recursos/goku.png")
jugador_x = 368
jugador_y = 505
jugador_x_cambio = 0
velocidad_jugador = 0.2

def fuenteBytes(fuente):
    with open(fuente, 'rb') as f:
        ttf_bytes = f.read()

    return io.BytesIO(ttf_bytes)

#Variables de puntuación
puntuacion = 0
fuente_bytes = fuenteBytes("./recursos/FreeSansBold.ttf")
fuente = pygame.font.Font(fuente_bytes, 32)
texto_x = 10
texto_y = 10

#variables de disparo
disparo = pygame.image.load("./recursos/ataque.png")
disparo_x = 0
disparo_y = 505
disparo_y_cambio = 0.4
disparo_visible = False

#variables de enemigos
lista_enemigos = []
velocidad_enemigo = 0.3
cantidad_enemigos = 8



#Función que inicializa música de fondo
def iniciaMusicaFondo():
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

#Función para mostrar puntuación
def muestraPuntuacion(x, y):
    texto = fuente.render(f"Puntuación: {puntuacion}", True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

#Función jugador
def posicionaJugador(x, y):
    pantalla.blit(img_jugador, (x, y))

#Función enemigo
def posicionaEnemigo(x, y, img_enemigo):
    pantalla.blit(img_enemigo, (x, y))

def generaEnemigos(cantidad_enemigos):
    lista = []

    for itera in range(cantidad_enemigos):
        enemigo = {
            "img_enemigo": pygame.image.load("./recursos/saibaman.png"),
            "enemigo_x": random.randint(0, 736),
            "enemigo_y": random.randint(50, 200),
            "enemigo_x_cambio": velocidad_enemigo,
            "enemigo_y_cambio": 50
        }

        lista.append(enemigo)

    return lista

#Función para disparar ataque
def dispara(x, y):
    global disparo_visible
    disparo_visible = True
    pantalla.blit(disparo, (x + 16, y + 10))

#Función para detectar colisiones
def hayColision(x, y, x2, y2):
    distancia = math.sqrt(math.pow(x2 - x, 2) + math.pow(y2 - y, 2))

    if distancia < 27:
        return True
    else:
        return False

#Texto final del juego
fuente_final = pygame.font.Font(fuente_bytes, 40)

def textoFinal():
    mi_fuente_final = fuente_final.render(f"JUEGO TERMINADO", True, (240, 120, 40))
    pantalla.blit(mi_fuente_final, (200, 200))

#Loop del juego
se_ejecuta = True
partida_perdida = False

lista_enemigos = generaEnemigos(cantidad_enemigos)
iniciaMusicaFondo()

while se_ejecuta:
    #Imágen de fondo
    pantalla.blit(fondo, (0, 0))

    # Iterador de eventos
    for evento in pygame.event.get():
        # Evento salir del juego
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        # Evento presionar tecla
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio += velocidad_jugador
            elif evento.key == pygame.K_LEFT:
                jugador_x_cambio -= velocidad_jugador
            elif (evento.key == pygame.K_SPACE) and (not disparo_visible):
                sonido_disparo = pygame.mixer.Sound("./recursos/disparo.mp3")
                sonido_disparo.set_volume(0.2)
                sonido_disparo.play()
                disparo_x = jugador_x
                dispara(disparo_x, disparo_y)

        # Evento soltar tecla
        if evento.type == pygame.KEYUP:
            if (evento.key == pygame.K_RIGHT) or (evento.key == pygame.K_LEFT):
                jugador_x_cambio = 0

    if partida_perdida:
        textoFinal()
    else:
        #Modificar ubicación del jugador
        jugador_x += jugador_x_cambio

        #Mantener dento del borde al jugador
        if jugador_x <= 0:
            jugador_x = 0
        elif jugador_x >= 736:
            jugador_x = 736

        #Modificar ubicación del enemigo
        for enemigo in lista_enemigos:
            enemigo["enemigo_x"] += enemigo["enemigo_x_cambio"]

            if (enemigo["enemigo_y"] >= 430) and ((enemigo["enemigo_x"] + 60) >= jugador_x) and (enemigo["enemigo_x"] <= (jugador_x + 60)):
                lista_enemigos = []
                #Termina el juego (nos han matado)
                partida_perdida = True
                break
            else:
                #Mantener dento del borde al enemigo
                if enemigo["enemigo_x"] <= 0:
                    enemigo["enemigo_x_cambio"] = velocidad_enemigo
                    enemigo["enemigo_y"] += enemigo["enemigo_y_cambio"]
                elif enemigo["enemigo_x"] >= 736:
                    enemigo["enemigo_x_cambio"] = -velocidad_enemigo
                    enemigo["enemigo_y"] += enemigo["enemigo_y_cambio"]

                if hayColision(enemigo["enemigo_x"], enemigo["enemigo_y"], disparo_x, disparo_y):
                    disparo_x = 0
                    disparo_y = 505
                    disparo_visible = False
                    golpe = pygame.mixer.Sound("./recursos/golpe.mp3")
                    golpe.set_volume(0.2)
                    golpe.play()
                    puntuacion += 1
                    lista_enemigos.remove(enemigo)
                else:
                    posicionaEnemigo(enemigo["enemigo_x"], enemigo["enemigo_y"], enemigo["img_enemigo"])

        #Puntuación
        muestraPuntuacion(texto_x, texto_y)

        #Movimiento del ataque
        if disparo_y <= -32:
            disparo_y = 505
            disparo_visible = False

        if disparo_visible:
            dispara(disparo_x, disparo_y)
            disparo_y -= disparo_y_cambio

    posicionaJugador(jugador_x, jugador_y)

    #Actualizar pantalla
    pygame.display.update()