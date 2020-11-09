#!/usr/bin/env python3
import pygame
import numpy as np
import random
import tensorflow as tf

model = tf.keras.models.load_model("model.model")

WIDTH = 560
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("NumRec - mrmalac")
GREY = (128, 128, 128)
WHITE = (255,255,255)
BLACK = (0,0,0)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = BLACK
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        
    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, (self.x, self.y, self.width, self.width))

    def make_square(self):
        self.color = WHITE

    def reset(self):
        self.color = BLACK

def predict(array, model):
    x_test = tf.keras.utils.normalize(array)
    prediction = model.predict([x_test])
    pygame.display.set_caption("NumRec - mrmalac - Prediction: " + str(np.argmax(prediction[0])))

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)

    return grid

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

def main(win, width):
    ROWS = 28
    grid = make_grid(ROWS, width)
    arr = np.zeros((10, 28, 28), dtype=int)

    running = True
    while running:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.make_square()
                arr[0][col][row] = 1
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                arr[0][col][row] = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    predict(arr, model)
                if event.key == pygame.K_r:
                    pygame.display.set_caption("NumRec - mrmalac")
                    arr = np.zeros((10, 28, 28))
                    grid = make_grid(ROWS, width)
                if event.key == pygame.K_q:
                    running = False
    pygame.quit()

main(WIN, WIDTH) 
