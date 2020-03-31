#!/usr/bin/python3

# standard library
import random

# installed library
import pygame

# self-made modules
from object_position import PositionValueObject as pval

class Fruit:

    def __init__(self, window, v=1, size=(8,8), color=(200,0,0)):

        self.window = window
        self.position = pval((random.randint(0,self.window.get_width()),
                              random.randint(0,self.window.get_height())))

        self.nutritive_value = v #value
        self.size = size
        self.color = color

        self.surface = pygame.Surface((self.size))
        self.surface.fill(self.color)

        self.rect = self.surface.get_rect()
        self.rect.topleft = self.position.get()

    def show(self):

        self.window.blit(self.surface, self.rect)

class Apple(Fruit):
    def __init__(self, window):
        Fruit.__init__(self, window)

class Peer(Fruit):
    def __init__(self, window):
        Fruit.__init__(self, window, v=3, size=(12,12), color=(0,200,0))

class BlueBerry(Fruit):
    def __init__(self, window):
        Fruit.__init__(self, window, v=9, size=(16, 16), color=(0,0,200))

def random_fruit():
    P = [85,12,3]
    fruits = [Apple, Peer, BlueBerry]
    #choice = [p*[fruit] for p, fruit in zip(P, fruits)]
    choice = [item for sublist in [p*[fruit] for p, fruit in zip(P, fruits)] for item in sublist]
    return random.choice(choice)

