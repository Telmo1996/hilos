import json

import pygame
import time
from numpy import math
from PIL import Image
from numpy import asarray
from bresenham import bresenham


def intensidad(linea, data):
    inten=0
    for i in range(0, len(linea)):
        x, y = linea[i]
        inten += 255 - data[x-1][y-1]
    return inten


def blanquear(linea, data):
    for i in range(0, len(linea)):
        x, y = linea[i]
        data[x-1][y-1] = 255
    return data


if __name__ == '__main__':
    ##################################################

    n = 128
    nHilos = 1000

    imgName = "eva800.png"
    coolSaveName = "eva800"

    ##################################################

    imgDir = "C:\\hilos\\img\\"
    saveDir = "C:\\hilos\\save\\"

    saveName = coolSaveName + str(n) + "_" + str(nHilos) + ".json"

    saveFile = saveDir + saveName
    imgPath = imgDir + imgName

    image = Image.open(imgPath)

    # print(image.format)
    width, height = image.size
    # print(image.mode)
    # show the image
    # image.show()

    img = asarray(image)
    data = img.copy()
    # print(type(data))
    # summarize shape
    # print(data.shape)

    # iniciar pygane
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    for i in range(0, width):
        for j in range(0, height):
            color = data[i][j], data[i][j], data[i][j]
            screen.set_at((j, i), color)
    pygame.display.update()

    # crear agujas
    agujas = [0]*n
    r = width/2
    for i in range(0, n):
        alpha = 2 * math.pi / n * i
        x = width/2 + r * math.cos(alpha)
        y = height/2 - r * math.sin(alpha)
        agujas[i] = (int(x), int(y))
        screen.set_at(agujas[i], (255, 0, 0))
    pygame.display.update()

    # Bucle principal
    currAguja = 0
    hilos = [0] * (nHilos + 1)
    hilos[0] = 0
    # hilos[0]=currAguja
    for i in range(0, nHilos):
        maxIntensidad=0
        nextAguja=currAguja
        for j in range(0, n):   # TODO maybe considerar aguja actual
            x0, y0 = agujas[currAguja]
            x1, y1 = agujas[j]
            linea = list(bresenham(x0, y0, x1, y1))
            inten = intensidad(linea, data)
            if inten > maxIntensidad:
                maxIntensidad = inten
                nextAguja = j
        x0, y0 = agujas[currAguja]
        x1, y1 = agujas[nextAguja]
        linea = list(bresenham(x0, y0, x1, y1))
        data = blanquear(linea, data)
        currAguja = nextAguja
        hilos[i+1] = currAguja

        x0, y0 = agujas[hilos[i]]
        x1, y1 = agujas[hilos[i + 1]]
        pygame.draw.line(screen, (255, 0, 0), (y0, x0), (y1, x1))
        pygame.display.update()

    print(hilos)
    print("DONE!!")

    # Guardar la matriz de iteraciones a disco
    mandelbrotJson = {"info": {"n": n, "nHilos": nHilos},
                      "hilos": hilos}
    with open(saveFile, 'w') as outfile:
        json.dump(mandelbrotJson, outfile)
        print("Matriz guardada en: " + saveFile)

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
