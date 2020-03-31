#!/usr/bin/python3

# standard library
import sys
import random
from collections import deque

# installed library
import pygame

# self-made modules
from snake import Snake
from fruit import random_fruit
from object_position import PositionValueObject as pval

# local var
DIR_EVENT_DICT = {pygame.K_RIGHT : (1,0),
                  pygame.K_LEFT : (-1,0),
                  pygame.K_DOWN : (0,1),
                  pygame.K_UP : (0,-1)}
GAME_WINDOW_OFFSET = pval((30,30))
GAME_WINDOW_SIZE = pval((800,600))

class MainWindow:
    def __init__(self):

        # create a new window
        self.window = pygame.display.set_mode((800, 600))
        # set game window name
        pygame.display.set_caption("Snake game")

        # create a grey background
        self.background = pygame.Surface((800, 600))
        self.background.fill(pygame.Color("#222222"))

        # make a surface/game area inside main window
        self.game_surf_pos = GAME_WINDOW_OFFSET.get()
        game_surf_size = (GAME_WINDOW_SIZE - 2 * GAME_WINDOW_OFFSET).get()
        rect = pygame.Rect(self.game_surf_pos, game_surf_size)
        self.game_surface = pygame.Surface(game_surf_size)

        # create the snake and store it
        self.snake = Snake(self.game_surface)
        # create a random fruit and store it
        self.fruit = random_fruit()(self.game_surface)

        self.clock = pygame.time.Clock()

    def loop(self):

        is_running = True
        while is_running:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    sys.exit()

                # loop for arrow key event
                if event.type == pygame.KEYDOWN:
                    if event.key in DIR_EVENT_DICT.keys():
                        self.snake.change_direction(DIR_EVENT_DICT[event.key])

            # test if snake head collide with a fruit
            if self.snake.head.rect.colliderect(self.fruit.rect):
                self.snake.eat(self.fruit)
                # create a new fruit, old one is deleted as it's not referenced anymore
                self.fruit = random_fruit()(self.game_surface)

            self.snake.move()

            # update screen
            self.update_game_window()


    def update_game_window(self):

        self.window.blit(self.background, (0, 0))
        self.window.blit(self.game_surface, self.game_surf_pos)
        self.snake.show()
        self.fruit.show()

        self.clock.tick(15)
        pygame.display.flip()
        #pygame.display.update(self.snake.body_parts)

if __name__ == "__main__":
    game = MainWindow()
    game.loop()
    #pass
