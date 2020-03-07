#!/usr/bin/python3

import sys
import random
from collections import deque

import pygame

from object_position import PositionMathTool as pmt
from object_position import PositionValueObject as pval


# DIR_EVENT = zip((pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP),
#                ((1,0),(-1,0),(0,1),(0,-1)))

DIR_EVENT = (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP)


class MainWindow:
    def __init__(self):

        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Snake game")

        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color("#222222"))

        self.game_surf_pos = (30, 30)
        game_surf_size = (740, 540)
        rect = pygame.Rect(self.game_surf_pos, game_surf_size)
        self.game_surface = pygame.Surface(game_surf_size)

        pygame.draw.rect(
            self.game_surface, (255, 255, 255), self.game_surface.get_rect(), 5
        )

        self.snake = Snake(self.game_surface)
        self.apple = Fruit(self.game_surface, 1)

        self.clock = pygame.time.Clock()

        self.update_rect_list = []

    def loop(self):

        is_running = True
        last_huge_meal = 2
        time_before_roasted = 10*1000
        tic = pygame.time.get_ticks()
        toc = 0
        while is_running:

            self.update_rect_list = [part.rect for part in self.snake.body_parts]
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:

                    if event.key in DIR_EVENT:
                        self.change_snake_direction(event.key)

            if self.snake.body_parts[-1].rect.colliderect(self.apple.rect):
                self.snake.eat(self.apple)
                last_huge_meal -= 1
                if last_huge_meal > 0 :
                    self.apple = Fruit(self.game_surface, 1 )
                else :
                    tic = pygame.time.get_ticks()
                    toc = 0
                    last_huge_meal = 5
                    self.apple = Fruit(self.game_surface, 20 )

            if toc > time_before_roasted and self.apple.value > 1 :
                tic = pygame.time.get_ticks()
                self.apple = Fruit(self.game_surface, 1 )

            self.snake.move()
            test = [part.rect for part in self.snake.body_parts]
            print('------------------')
            print(test)
            #self.update_rect_list = set(self.update_rect_list).union([part.rect for part in self.snake.body_parts])
            #self.update_rect_list.append(self.apple.rect)
            #list1 + [elmt for i, elmt in enumerate(list2) if elmt not in list1+list2[:i]]

            self.window.blit(self.background, (0, 0))
            self.window.blit(self.game_surface, self.game_surf_pos)
            self.snake.show()
            self.apple.show()

            toc = pygame.time.get_ticks() - tic
            self.clock.tick(15)
            pygame.display.flip()
            #pygame.display.update(self.update_rect_list)

    def change_snake_direction(self, key):

        if key == pygame.K_RIGHT:
            self.snake.change_direction((1, 0))

        elif key == pygame.K_LEFT:
            self.snake.change_direction((-1, 0))

        elif key == pygame.K_DOWN:
            self.snake.change_direction((0, 1))

        elif key == pygame.K_UP:
            self.snake.change_direction((0, -1))

class Fruit:
    def __init__(self, window, value):

        self.window = window

        self.value = value
        s = 10 + 3*(value-1)
        self.size=(s,s)
        self.surface = pygame.Surface((self.size))

        self.position = pval((random.randint(0,self.window.get_width()),
                              random.randint(0,self.window.get_height())))
        self.rect = self.surface.get_rect()
        self.rect.topleft = self.position.get()

        self.surface.fill((200, 0, 0))

    def show(self):

        self.window.blit(self.surface, self.rect)

class BodyPart:
    def __init__(self, window, size=10, color=(200,200,200)):

        self.window = window

        self.size = size
        self.surface = pygame.Surface((self.size,self.size))
        self.surface.fill(color)
        self.rect = pygame.Rect(0,0,self.size,self.size)


class Snake:
    def __init__(self, window):

        self.window = window
        self.speed = 1
        self.direction = pval((0, 1))

        self.length = 5
        self.body_parts = deque(maxlen=self.length)
        self.body_parts.append(self.gen())

#        self.body_part_size = 10
#
#        self.body_rect = deque(maxlen=self.length)
#        self.body_rect.append(pygame.Rect(0,0,10,10))
#
#        self.body_part_surface = pygame.Surface(
#            (self.body_part_size-1, self.body_part_size-1)
#        )

    def gen(self, kind='thin'):
        if kind == 'thin':
            return BodyPart(self.window)
        elif kind == 'thick':
            return BodyPart(self.window, 12)

    def change_direction(self, direction):
        if pmt.dot(self.direction, direction) == 0:
            self.direction = pval(direction) * 10# self.body_part_size

    def move(self):

        for s in range(self.speed):
            rect = self.body_parts[-1].rect.copy()

            rect.x +=  self.direction[0]
            rect.y +=  self.direction[1]

            if not self.window.get_rect().colliderect(rect):
                rect = self.go_trough(rect)
            elif any(rect.colliderect(part.rect) for part in self.body_parts):
                print("You're dead")

            new_part = self.gen()
            new_part.rect = rect
            self.body_parts.append(new_part)

    def go_trough(self, rect):

        head_rect = self.body_parts[-1].rect

        if self.direction[0] > 0:
            head_rect.x = 0

        elif self.direction[0] < 0:
            head_rect.x = self.window.get_width()

        elif self.direction[1] > 0:
            head_rect.y = 0

        elif self.direction[1] < 0:
            head_rect.y = self.window.get_height()

        return head_rect

    def eat(self, fruit):

        for i in range(fruit.value) :
            self.grow()

        new_part = self.gen('thick')
        new_part.rect.center = self.body_parts[-1].rect.center
        self.body_parts.append(new_part)

    def grow(self):

        self.length += 1
        self.body_parts = deque(self.body_parts, maxlen=self.length)


    def show(self):

        self.window.fill((20, 20, 20))
        pygame.draw.rect(self.window, (255, 255, 255), self.window.get_rect(), 5)
        for part in self.body_parts:
            self.window.blit(part.surface, part.rect)

if __name__ == "__main__":
    game = MainWindow()
    game.loop()
