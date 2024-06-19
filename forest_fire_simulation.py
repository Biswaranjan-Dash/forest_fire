# forest_fire_simulation.py

import numpy as np

EMPTY, TREE, FIRE = 0, 1, 2

class ForestFireSimulation:
    def __init__(self, Nx=100, Ny=100, p=0.02, f=0.001):
        self.Nx = Nx
        self.Ny = Ny
        self.p = p
        self.f = f
        self.forest = self.initialize_forest(full_green=True)

    def initialize_forest(self, full_green=False):
        if full_green:
            return np.ones((self.Nx, self.Ny), dtype=int) * TREE
        else:
            return np.zeros((self.Nx, self.Ny), dtype=int)

    def step(self):
        new_forest = self.forest.copy()
        for x in range(self.Nx):
            for y in range(self.Ny):
                if self.forest[x, y] == EMPTY and np.random.random() <= self.p:
                    new_forest[x, y] = TREE
                elif self.forest[x, y] == TREE:
                    if np.random.random() <= self.f:
                        new_forest[x, y] = FIRE
                    elif (self.forest[(x - 1) % self.Nx, y] == FIRE or
                          self.forest[(x + 1) % self.Nx, y] == FIRE or
                          self.forest[x, (y - 1) % self.Ny] == FIRE or
                          self.forest[x, (y + 1) % self.Ny] == FIRE):
                        new_forest[x, y] = FIRE
                elif self.forest[x, y] == FIRE:
                    new_forest[x, y] = EMPTY
        self.forest = new_forest
        return self.forest.tolist()
