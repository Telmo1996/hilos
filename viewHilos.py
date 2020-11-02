import json
import math
import time

import pygame

if __name__ == '__main__':
    #################################################################

    fileName = 'evabyn128_1000'  # Sin .json
    saveExtension = '.png'

    width, height = 800, 800

    #################################################################

    # Read from
    loadDirectory = 'C:\\hilos\\save\\'

    # Write to
    saveDirectory = 'C:\\hilos\\view\\'
    saveFileName = fileName

    #################################################################

    loadFile = loadDirectory + fileName + '.json'
    saveFile = saveDirectory + saveFileName + saveExtension

    with open(loadFile) as json_file:
        hilosJson = json.load(json_file)

    n = hilosJson["info"]["n"]
    nHilos = hilosJson["info"]["nHilos"]

    hilos = hilosJson["hilos"]

    # iniciar pygane
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    screen.fill((255, 255, 255))
    pygame.display.update()

    # crear agujas
    agujas = [0] * n
    r = width / 2
    for i in range(0, n):
        alpha = 2 * math.pi / n * i
        x = width / 2 + r * math.cos(alpha)
        y = height / 2 - r * math.sin(alpha)
        agujas[i] = (int(x), int(y))
        screen.set_at(agujas[i], (255, 0, 0))
    pygame.display.update()

    for i in range(0, nHilos):
        x0, y0 = agujas[hilos[i]]
        x1, y1 = agujas[hilos[i + 1]]
        pygame.draw.line(screen, (255, 0, 0), (y0, x0), (y1, x1))
    pygame.display.update()

    # Esperar al SPACE para salir
    esperando = True
    while esperando:
        time.sleep(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                esperando = False
            if event.type == pygame.KEYDOWN:
                pulsados = pygame.key.get_pressed()
                if pulsados[pygame.K_SPACE]:
                    esperando = False