import json
import math
import os
import time
from bresenham import bresenham

import pygame

#################################################################

fileName = 'evaV3180_5000'  # Sin .json
saveFileNameBase = "evaV3"
saveExtension = '.png'

tamano = 800
width, height = tamano, tamano

# dibujarHasta = 250
incremento = 250
dibujarHasta = incremento

multIntensidad = 25

#################################################################

# iniciar pygane
pygame.init()
screen = pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))
pygame.display.update()


def shade(i):
    intensidad = 255 - i*multIntensidad
    if intensidad < 0:
        intensidad = 0
    return intensidad, intensidad, intensidad


def pintar(data):
    screen.fill((255, 255, 255))
    for i in range(0, width):
        for j in range(0, height):
            color = shade(data[i][j])
            screen.set_at((i, height-j-1), color)
    pygame.display.update()


if __name__ == '__main__':

    # Read from
    loadDirectory = 'C:\\hilos\\save\\'

    # Write to
    saveDirectory = 'C:\\hilos\\capturas\\'
    # saveFileName = fileName

    #################################################################

    # saveFileName = saveFileNameBase + str(dibujarHasta)

    loadFile = loadDirectory + fileName + '.json'
    # saveFile = saveDirectory + saveFileName + saveExtension

    with open(loadFile) as json_file:
        hilosJson = json.load(json_file)

    n = hilosJson["info"]["n"]
    nHilos = hilosJson["info"]["nHilos"]

    if dibujarHasta > nHilos:
        dibujarHasta = nHilos
    if dibujarHasta == 0:
        dibujarHasta = nHilos

    hilos = hilosJson["hilos"]

    # crear agujas
    agujas = [0] * n
    r = width / 2
    for i in range(0, n):
        alpha = (2 * math.pi / n * i) + math.pi / 2
        x = width / 2 + r * math.cos(alpha)
        y = height / 2 - r * math.sin(alpha)
        agujas[i] = (int(x), int(y))
        # screen.set_at(agujas[i], (255, 0, 0))
    # pygame.display.update()

    # crear matriz data
    data = [0] * height
    for i in range(0, height):
        data[i] = [0] * width

    # Bucle principal
    # SPACE: salir
    # izq der: menos, mas hilos
    # s: guardar
    esperando = True
    actualizar = True
    while esperando:
        time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esperando = False
            if event.type == pygame.KEYDOWN:
                pulsados = pygame.key.get_pressed()
                if pulsados[pygame.K_SPACE]:    # Salir
                    esperando = False
                if pulsados[pygame.K_RIGHT]:
                    dibujarHasta += incremento
                    if dibujarHasta > nHilos:
                        dibujarHasta = nHilos
                    print("dibujar hasta: " + str(dibujarHasta))
                    actualizar = True
                if pulsados[pygame.K_LEFT]:
                    dibujarHasta -= incremento
                    if dibujarHasta < incremento:
                        dibujarHasta = incremento
                    print("dibujar hasta: " + str(dibujarHasta))
                    actualizar = True
                if pulsados[pygame.K_s]:  # Guardar imagen
                    print()
                    saveFileName = saveFileNameBase + str(dibujarHasta)
                    saveFile = saveDirectory + saveFileName + saveExtension
                    if os.path.isfile(saveFile):
                        numFile = 1
                        while os.path.isfile(
                                "{0}\\{1} ({2}){3}".format(saveDirectory, saveFileName, numFile, saveExtension)):
                            numFile += 1
                        pygame.image.save(screen,
                                          "{0}\\{1} ({2}){3}".format(saveDirectory, saveFileName, numFile,
                                                                     saveExtension))
                        print("Imagen guardada en: " + "{0}\\{1} ({2}){3}".format(saveDirectory, saveFileName, numFile,
                                                                                  saveExtension))
                    else:
                        pygame.image.save(screen, saveFile)
                        print("Imagen guardada en: " + saveFile)

        if actualizar:
            actualizar = False

            data = [0] * height
            for i in range(0, height):
                data[i] = [0] * width
            # calcular data
            for i in range(0, dibujarHasta):
                x0, y0 = agujas[hilos[i]]
                x1, y1 = agujas[hilos[i + 1]]
                linea = list(bresenham(x0, y0, x1, y1))
                for j in range(0, len(linea)):
                    x, y = linea[j]
                    data[x - 1][y - 1] += 1

            pintar(data)
