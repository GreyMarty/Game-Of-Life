import pygame as pg
import numpy as np
from time import time

from config import *


class GameOfLife:
    def __init__(self):
        pg.init()
        pg.display.set_caption("Game Of Life")
        self.main_surface = pg.display.set_mode(WINDOW_SIZE)

        self.grid = np.zeros(tuple(map(lambda x: x // CELL_SIZE, WINDOW_SIZE)))
        self.paused = True

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.paused = not self.paused
                if event.key == pg.K_c:
                    self.grid = np.zeros(self.grid.shape)

        if pg.mouse.get_pressed()[0]:
            self.grid[tuple(map(lambda x: x // CELL_SIZE, pg.mouse.get_pos()))] = 1
        elif pg.mouse.get_pressed()[2]:
            self.grid[tuple(map(lambda x: x // CELL_SIZE, pg.mouse.get_pos()))] = 0

    def render(self):
        self.main_surface.fill(BG_COLOR)

        for y in range(self.grid.shape[1]):
            for x in range(self.grid.shape[0]):
                if self.grid[x, y]:
                    rect = [
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    ]
                    pg.draw.rect(self.main_surface, CELL_COLOR, rect)

        self.draw_grid()

        pg.display.update()

    def draw_grid(self):
        for y in range(CELL_SIZE, WINDOW_SIZE[1], CELL_SIZE):
            start_pos = (0, y)
            end_pos = (WINDOW_SIZE[0], y)
            pg.draw.line(self.main_surface, GRID_COLOR, start_pos, end_pos)

        for x in range(CELL_SIZE, WINDOW_SIZE[0], CELL_SIZE):
            start_pos = (x, 0)
            end_pos = (x, WINDOW_SIZE[1])
            pg.draw.line(self.main_surface, GRID_COLOR, start_pos, end_pos, 2)

    def logic(self):
        if not self.paused:
            new_grid = np.zeros(self.grid.shape)

            for y in range(self.grid.shape[1]):
                for x in range(self.grid.shape[0]):
                    neighbors = tuple(self.get_neighbors((x, y)))
                    alive = neighbors.count(1)

                    if alive == 3:
                        new_grid[x, y] = 1
                    elif 2 <= alive < 3:
                        new_grid[x, y] = self.grid[x, y]
                    else:
                        new_grid[x, y] = 0

            self.grid = new_grid.copy()

    def get_neighbors(self, pos):
        for act_y in (-1, 0, 1):
            for act_x in (-1, 0, 1):
                if 0 <= pos[0] + act_x < self.grid.shape[0] and 0 <= pos[1] + act_y < self.grid.shape[1]:
                    if not act_x == act_y == 0:
                        yield self.grid[pos[0] + act_x, pos[1] + act_y]

    def mainloop(self):
        last_refresh = time()
        while True:
            start = time()

            self.check_events()
            if time() - last_refresh >= 1 / REFRESH_RATE:
                self.logic()
                last_refresh = time()
            self.render()

            time_delta = time() - start


GameOfLife().mainloop()