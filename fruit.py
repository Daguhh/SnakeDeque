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

        # create fruit on a random position
        self.position = pval((random.randint(0,self.window.get_width()),
                              random.randint(0,self.window.get_height())))

        self.nutritive_value = v # = v will be added to snake size
        self.size = size # size on the screen
        self.color = color

        # what will be drawn on the screen
        self.surface = pygame.Surface((self.size))
        self.surface.fill(self.color)

        # store fruit size and position
        self.rect = self.surface.get_rect()
        self.rect.topleft = self.position.get()

    def show(self):

        # add to the image to be added on the screen
        self.window.blit(self.surface, self.rect)

class Apple(Fruit):
    # inherit from Fruit class
    def __init__(self, window):
        Fruit.__init__(self, window)

class Peer(Fruit):
    # inherit from Fruit class but with alternate init values
    def __init__(self, window):
        Fruit.__init__(self, window, v=3, size=(12,12), color=(0,200,0))

class BlueBerry(Fruit):
    def __init__(self, window):
        Fruit.__init__(self, window, v=9, size=(16, 16), color=(0,0,200))

def random_fruit():
    """ return a Fruit object with P propobility """
    P = [85,12,3]
    fruits = [Apple, Peer, BlueBerry]
    # an unnecessary complex function :
    # (create list of elementwise P * fruits elements and put it in a simple list
    choice = [item for sublist in [p*[fruit] for p, fruit in zip(P, fruits)] for item in sublist]
    # return a random item(=Fruiti class) in the list
    return random.choice(choice)

