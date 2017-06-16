#!/usr/bin/env python

import os
import random
import time

import pygame

import unicornhathd


class Snake:
    def __init__(self, canvas, x=5, y=5):
        self.position = (x, y)
        self.velocity = (1, 0)

        self.length = 1
        self.score = 0
        self.tail = []
        self.colour_head = (128,0,255)
        self.colour_tail = (32,0,64)
        self.canvas = canvas
        self.eaten = []

        self.grow_speed = 1

    def poo(self):
        self.eaten = []
        self.tail = []
        self.length = 1
        self.grow_speed += 1

    def shrink(self):
        if self.length > 1:
            self.length -= 1
            self.tail = self.tail[-self.length:] 
        if len(self.eaten) > 0:
            self.eaten.pop(0)

    def get_colour(self, x, y):
        if (x, y) == self.position:
            return self.colour_head
        elif (x, y) in self.tail:
            return self.colour_tail

    def draw(self):
        for position in [self.position] + self.tail:
            x, y = position
            r, g, b = self.get_colour(x, y)
            self.canvas.set_pixel(x, y, r, g, b)

        for idx, colour in enumerate(self.eaten):
            r, g, b = colour
            self.canvas.set_pixel(idx, 14, r >> 1, g >> 1, b >> 1)

    def num_eaten(self):
        return len(self.eaten)

    def update(self, apples):
        keys = pygame.key.get_pressed()
        pygame.event.pump()

        x, y = self.position

        if keys[pygame.K_LEFT] and self.velocity != (1, 0):
            self.velocity = (-1, 0)
            
        if keys[pygame.K_RIGHT] and self.velocity != (-1, 0):
            self.velocity = (1, 0)

        if keys[pygame.K_UP] and self.velocity != (0, -1):
            self.velocity = (0, 1)

        if keys[pygame.K_DOWN] and self.velocity != (0, 1):
            self.velocity = (0, -1)

        v_x, v_y = self.velocity
        x += v_x
        y += v_y
        c_x, c_y = self.canvas.get_shape()
        c_y -= 3 # 3 pixels along the top for score
        x %= c_x
        y %= c_y

        if (x, y) in self.tail:
            return False

        self.tail.append(self.position)
        self.tail = self.tail[-self.length:]
        self.position = (x, y)

        for apple in apples:
            if apple.position == self.position:
                score = apple.eat()
                if score > 0:
                    self.score += score
                    self.length += self.grow_speed
                    self.eaten.append(apple.get_colour())

        return True


class Apple:
    colours = [(128,0,0), (0,128,0), (96,96,0)]
    def __init__(self, canvas):
        self.canvas = canvas

        self.reset()

    def get_colour(self):
        return self.colours[self.score]

    def reset(self):
        c_x, c_y = self.canvas.get_shape()
        c_y -= 3

        self.position = (random.randint(0, c_x-1), random.randint(0, c_y-1))

        self.score = random.randint(0, len(self.colours)-1)

        self.eaten = False

    def eat(self):
        if self.eaten:
            return 0

        self.eaten = True
        return self.score + 1

    def update(self):
        pass # What's an apple 'gon do?

    def draw(self):
        if self.eaten:
            return

        x, y = self.position
        r, g, b = self.get_colour()
        self.canvas.set_pixel(x, y, r, g, b)


if __name__ == "__main__":
    os.putenv("DISPLAY", ":0.0")
    pygame.init()
    screen = pygame.display.set_mode((160,160))

    #unicornhathd.rotation(-90)

    width, height = unicornhathd.get_shape()

    step = 0

    running = True

    num_apples = 16

    snake = Snake(unicornhathd, 5, 5)

    apples = [Apple(unicornhathd) for x in range(num_apples)]

    t_start = time.time()

    hit = False

    try:
        while running:
            unicornhathd.clear()

            for x in range(16):
                for y in range(3):
                    unicornhathd.set_pixel(x, 15-y, 10, 10, 10)


            if hit:
                if snake.length == 1:
                    hit = False
                    for apple in apples:
                        apple.reset()
                    continue

                snake.shrink()
                snake.draw()                

            else:
                
                for apple in apples:
                    apple.update()
                    apple.draw()

                hit = not snake.update(apples)

                if snake.num_eaten() == num_apples:
                    snake.poo()
                    for apple in apples:
                        apple.reset()
                        apple.draw()

                snake.draw()

            unicornhathd.show()
            step += 1
            time.sleep(0.1)

        t_time = time.time() - t_start
        print("You scored: {}".format(snake.score))

    except KeyboardInterrupt:
        pass
