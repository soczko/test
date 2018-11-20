import pygame
import math
import numpy as np


def move_right(vel, map):
    for row in range(len(map)):
        for col in range(len(map[row])):
            if (col == 0 or col == 3):
                map[row][col] -= vel


def move_left(vel, map):
    for row in range(len(map)):
        for col in range(len(map[row])):
            if (col == 0 or col == 3):
                map[row][col] += vel


def move_up(vel, map):
    for row in range(len(map)):
        for col in range(len(map[row])):
            if (col == 1 or col == 4):
                map[row][col] -= vel


def move_down(vel, map):
    for row in range(len(map)):
        for col in range(len(map[row])):
            if (col == 1 or col == 4):
                map[row][col] += vel


def move_forward(vel, map):
    for row in range(len(map)):
        for col in range(len(map[row])):
            if (col == 2 or col == 5):
                map[row][col] -= vel


def move_backward(vel, map):
    for row in range(len(map)):
        for col in range(len(map[row])):
            if (col == 2 or col == 5):
                map[row][col] += vel


def turn_OX2(angle, map):
    X = np.array([0, 0, 0, 0, 0, 0])
    for row in range(len(map)):
        for col in range(len(map[row])):
            if (col == 1 or col == 4):
                # AY, BY
                X[col] = map[row][col] * math.cos(angle) - map[row][col + 1] * math.sin(angle)
            if (col == 2 or col == 5):
                # AZ, BZ
                X[col] = map[row][col - 1] * math.sin(angle) + map[row][col] * math.cos(angle)
            if (col == 5):
                map[row][1] = X[1]
                map[row][2] = X[2]
                map[row][4] = X[4]
                map[row][5] = X[5]


def turn_OY2(angle, map):
    X = np.array([0, 0, 0, 0, 0, 0])
    for row in range(len(map)):
        for col in range(len(map[row])):
            if (col == 0 or col == 3):
                # AX, BX
                X[col] = map[row][col] * math.cos(angle) + map[row][col + 2] * math.sin(angle)
            if (col == 2 or col == 5):
                # AY, BY
                X[col] = (-1) * map[row][col - 2] * math.sin(angle) + map[row][col] * math.cos(angle)
            if (col == 5):
                map[row][0] = X[0]
                map[row][2] = X[2]
                map[row][3] = X[3]
                map[row][5] = X[5]


def turn_OZ2(angle, map):
    X = np.array([0, 0, 0, 0, 0, 0])
    for row in range(len(map)):
        for col in range(len(map[row])):
            if (col == 0 or col == 3):
                # AX, BX
                X[col] = map[row][col] * math.cos((-1) * (angle)) - map[row][col + 1] * math.sin((-1) * (angle))
            if (col == 1 or col == 4):
                # AY, BY
                X[col] = map[row][col - 1] * math.sin((-1) * (angle)) + map[row][col] * math.cos((-1) * (angle))
            if (col == 5):
                map[row][0] = X[0]
                map[row][1] = X[1]
                map[row][3] = X[3]
                map[row][4] = X[4]


def zoomIN(step, focal):
    focal += step
    return focal


def zoomOUT(step, focal):
    if (focal > 0):
        focal -= step
    return focal


def count_map_2D(map, map_2D):
    for row in range(len(map)):
        coefficient1 = focal / (map[row][2] - vcam)
        coefficient2 = focal / (map[row][5] - vcam)
        x1 = coefficient1 * map[row][0] + window_w / 2
        y1 = window_h * (2 / 3) - coefficient1 * map[row][1]
        x2 = coefficient2 * map[row][3] + window_w / 2
        y2 = window_h * (2 / 3) - coefficient2 * map[row][4]
        map_row = [x1, y1, x2, y2]
        if (len(map_2D) < len(map)):
            map_2D.append(map_row)
        else:
            map_2D[row] = map_row


def draw_image(map_2D):
    for row in range(len(map_2D)):
        pygame.draw.aaline(window, (0, 0, 0), (map_2D[row][0], map_2D[row][1]), (map_2D[row][2], map_2D[row][3]))


pygame.init()

file = "mapa2.txt"
vel = 10
angle = math.pi / 18
map = []
focal = 500
vcam = 0
step = 50
window_w = 800
window_h = 600
map_2D = []

with open(file, "r") as plik:
    for linia in plik.readlines():
        linia = linia.split(',')
        linia.pop()
        linia = [int(x) for x in linia]
        map.append(linia)

window = pygame.display.set_mode((window_w, window_h))
window.fill((255, 255, 255))
pygame.display.set_caption("Grafika komputerowa 1")

count_map_2D(map, map_2D)
draw_image(map_2D)

run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        move_forward(vel, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_s]:
        move_backward(vel, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_a]:
        move_left(vel, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_d]:
        move_right(vel, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_q]:
        move_up(vel, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_z]:
        move_down(vel, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_UP]:
        turn_OX2(angle, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_DOWN]:
        turn_OX2(-angle, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_LEFT]:
        turn_OY2(-angle, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_RIGHT]:
        turn_OY2(angle, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_n]:
        turn_OZ2(angle, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_m]:
        turn_OZ2(-angle, map)
        count_map_2D(map, map_2D)
    if keys[pygame.K_c]:
        focal = zoomIN(step, focal)
        count_map_2D(map, map_2D)
    if keys[pygame.K_v]:
        focal = zoomOUT(step, focal)
        count_map_2D(map, map_2D)

    window.fill((255, 255, 255))
    draw_image(map_2D)
    pygame.display.update()

pygame.quit()
