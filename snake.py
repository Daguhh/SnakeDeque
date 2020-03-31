#!/usr/bin/python3

# standard library
from collections import deque

# installed library
import pygame

# self-made modules : object to store and perform math on tuple like positions
# value
from object_position import PositionValueObject as pval

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

