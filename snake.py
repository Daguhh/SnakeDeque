#!/usr/bin/python3

import sys
import random
from collections import deque

import pygame

from object_position import PositionValueObject as pval

#DIR_EVENT = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP)
DIR_EVENT_DICT = {pygame.K_RIGHT : (1,0),
                  pygame.K_LEFT : (-1,0),
                  pygame.K_DOWN : (0,1),
                  pygame.K_UP : (0,-1)}
GAME_WINDOW_OFFSET = pval((30,30))
GAME_WINDOW_SIZE = pval((800,600))


def random_fruit():
    P = [85,12,3]
    fruits = [Apple, Peer, BlueBerry]
    #choice = [p*[fruit] for p, fruit in zip(P, fruits)]
    choice = [item for sublist in [p*[fruit] for p, fruit in zip(P, fruits)] for item in sublist]
    return random.choice(choice)

class MainWindow:
    def __init__(self):

        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Snake game")

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color("#222222"))

        self.game_surf_pos = GAME_WINDOW_OFFSET.get()
        game_surf_size = (GAME_WINDOW_SIZE - 2 * GAME_WINDOW_OFFSET).get()
        rect = pygame.Rect(self.game_surf_pos, game_surf_size)
        self.game_surface = pygame.Surface(game_surf_size)

        pygame.draw.rect(
            self.game_surface,
            (255, 255, 255),
            self.game_surface.get_rect(),
            5
        )

        self.snake = Snake(self.game_surface)
        self.fruits = (Apple, Peer)
        self.fruit = Apple(self.game_surface)

        self.clock = pygame.time.Clock()

        self.update_rect_list = []

        self.window.blit(self.background, (0, 0))
        self.window.blit(self.game_surface, self.game_surf_pos)
        pygame.display.flip()

    def loop(self):

        is_running = True
        while is_running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in DIR_EVENT_DICT.keys():
                        self.snake.change_direction(DIR_EVENT_DICT[event.key])

            if self.snake.head.rect.colliderect(self.fruit.rect):
                self.snake.eat(self.fruit)
                self.fruit = random_fruit()(self.game_surface)

            self.snake.move()

            self.update_game_window()


    def update_game_window(self):

        self.window.blit(self.background, (0, 0))
        self.window.blit(self.game_surface, self.game_surf_pos)
        self.snake.show()
        self.fruit.show()

        self.clock.tick(15)
        pygame.display.flip()
        #pygame.display.update(self.snake.body_parts)

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

class BodyPart:
    def __init__(self, size=10, color=(200,200,200)):

        self.surface = pygame.Surface((size, size))
        self.color = color
        self.surface.fill(color)
        self.rect = pygame.Rect(0,0,size,size)

class Snake:
    def __init__(self, window):

        self.window = window
        self.speed = 1
        self.direction = pval((0, 1))
        self.head_pos = pval((0,0))

        self.length = 5
        self.body_parts = deque(maxlen=self.length)
        for i in range(5):
            self.body_parts.append(BodyPart())
        self.eaten_fruits = []

    def change_direction(self, direction):
        if pval.dot(self.direction, direction) == 0:
            self.direction = pval(direction) * 10# self.body_part_size

    def move(self):

        for s in range(self.speed):
            #rect = self.body_parts[-1].rect.copy()
            next_head_pos = self.head_pos + self.direction
            next_rect = self.head.rect.copy()
            next_rect.topleft = next_head_pos.get()

            if not self.window.get_rect().colliderect(next_rect):
                next_rect = self.go_trough(next_rect)
                next_head_pos = pval(next_rect.topleft)
            if any(next_rect.colliderect(part.rect) for part in [b for b in self.body_parts][:-3]): #self.body_parts[:-3]):
                print("You're dead")

            if self.eaten_fruits :
                if any(self.tail.rect.colliderect(f.rect) for f in self.eaten_fruits) :
                    self.grow(self.eaten_fruits.pop(0).nutritive_value)

            self.head_pos = next_head_pos
            new_part = BodyPart()
            new_part.rect = next_rect
            self.body_parts.append(new_part)

    @property
    def head(self):
        return self.body_parts[-1]

    @head.setter
    def head(self, bodypart):
        self.body_parts[-1] = bodypart

    @property
    def tail(self):
        return self.body_parts[0]

    def go_trough(self, rect):

        rect = self.head.rect
        x,y = self.direction

        if x > 0:
            rect.x = 0
        elif x < 0:
            rect.x = self.window.get_width()
        elif y > 0:
            rect.y = 0
        elif y < 0:
            rect.y = self.window.get_height()
        return rect

    def eat(self, fruit) :

        fruit.rect = self.head.rect
        self.eaten_fruits.append(fruit)

        head = BodyPart()
        head.rect.topleft = self.head.rect.topleft
        s = round(fruit.nutritive_value/2)+1
        head.rect = head.rect.inflate(s,s)

        self.head = head
        self.head.surface = pygame.Surface(self.head.rect.size)
        self.head.surface.fill(self.head.color)

    def grow(self, value):

        self.length += value #1
        self.body_parts = deque(self.body_parts, maxlen=self.length)

    def show(self):

        self.window.fill((20, 20, 20))
        pygame.draw.rect(self.window, (255, 255, 255), self.window.get_rect(), 5)
        for part in self.body_parts:
            self.window.blit(part.surface, part.rect)

if __name__ == "__main__":
    game = MainWindow()
    game.loop()
    #pass
