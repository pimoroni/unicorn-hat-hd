#!/usr/bin/env python

import random
from sys import exit

try:
    import numpy
except ImportError:
    exit('This script requires the numpy module\nInstall with: sudo pip install numpy')

import unicornhathd


print("""Unicorn HAT HD: Forest Fire

This example simulates a forest fire.

Press Ctrl+C to exit!

""")

scale = 3

unicornhathd.rotation(0)
unicornhathd.brightness(0.6)
width, height = unicornhathd.get_shape()

forest_width = width * scale
forest_height = height * scale

hood_size = 3
avg_size = scale


def get_neighbours(x, y, z):
    return [(x2, y2) for x2 in range(x - (z - 1), x + z) for y2 in range(y - (z - 1), y + z) if (-1 < x < forest_width and -1 < y < forest_height and (x != x2 or y != y2) and (0 <= x2 < forest_width) and (0 <= y2 < forest_height))]


initial_trees = 0.55
p = 0.01
f = 0.0005

tree = [0, 255, 0]
burning = [255, 0, 0]
space = [0, 0, 0]


def initialise():
    forest = [[tree if random.random() <= initial_trees else space for x in range(forest_width)] for y in range(forest_height)]
    return forest


def update_forest(forest):
    new_forest = [[space for x in range(forest_width)] for y in range(forest_height)]
    for x in range(forest_width):
        for y in range(forest_height):
            if forest[x][y] == burning:
                new_forest[x][y] = space
            elif forest[x][y] == space:
                new_forest[x][y] = tree if random.random() <= p else space
            elif forest[x][y] == tree:
                neighbours = get_neighbours(x, y, hood_size)
                new_forest[x][y] = (burning if any([forest[n[0]][n[1]] == burning for n in neighbours]) or random.random() <= f else tree)
    return new_forest


def average_forest(forest):
    avg_forest = [[space for x in range(width)] for y in range(height)]

    for i, x in enumerate(range(1, forest_width, scale)):
        for j, y in enumerate(range(1, forest_height, scale)):
            neighbours = get_neighbours(x, y, avg_size)
            red = int(numpy.mean([forest[n[0]][n[1]][0] for n in neighbours]))
            green = int(numpy.mean([forest[n[0]][n[1]][1] for n in neighbours]))
            blue = int(numpy.mean([forest[n[0]][n[1]][2] for n in neighbours]))
            avg_forest[i][j] = [red, green, blue]

    return avg_forest


def show_forest(forest):
    avg_forest = average_forest(forest)

    for x in range(width):
        for y in range(height):
            r, g, b = avg_forest[x][y]
            unicornhathd.set_pixel(x, y, int(r), int(g), int(b))

    unicornhathd.show()


def main():
    forest = initialise()

    while True:
        show_forest(forest)
        forest = update_forest(forest)


try:
    main()

except KeyboardInterrupt:
    unicornhathd.off()
