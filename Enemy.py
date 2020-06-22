from Bomb import Bomb
import pygame
import os
import numpy as np


class Enemy:

    def __init__(self, screen_width, screen_height, speed_multiplier=1):
        self.__image = pygame.image.load(os.path.join("Images", "Enemy.png")).convert_alpha()
        self.__width, self.__height = self.__image.get_size()
        self.__x = np.random.randint(0, screen_width - self.__width + 1)
        self.__y = 0
        self.__bomb = Bomb(self.__x + 11, self.__y + 13, screen_height)
        self.__to_destroy = False
        self.__speed_x = speed_multiplier * np.random.randint(-2, 3)
        self.__speed_y = speed_multiplier * np.random.randint(3, 6)
        self.__threshold = int(0.6 * screen_height)
        self.__escape = False
        self.__to_launch = False

    def draw(self, screen):
        screen.blit(self.__image, (self.__x, self.__y))
        if self.__bomb is not None:
            self.__bomb.draw(screen)

    def move(self):
        if not self.__escape:
            self.__x += self.__speed_x
            self.__y += self.__speed_y
            self.__bomb.move(self.__speed_x, self.__speed_y)
            if self.__threshold <= self.__y and self.__bomb is not None:
                self.__to_launch = True
                self.__escape = True
        else:
            self.__x += self.__speed_x
            self.__y -= self.__speed_y
            if self.__y < (-self.__height):
                self.__to_destroy = True

    def drop_bomb(self):
        self.__bomb.launch()
        bomb = self.__bomb
        self.__bomb = None
        self.__to_launch = False
        return bomb

    def destroy(self):
        self.__to_destroy = True
        if self.__bomb is not None:
            self.__bomb.destroy()

    @property
    def to_launch(self):
        return self.__to_launch

    @property
    def to_destroy(self):
        return self.__to_destroy

    @property
    def cx(self):
        return self.__x + self.__width // 2

    @property
    def cy(self):
        return self.__y + self.__height // 2

    @property
    def radius(self):
        return (self.__width + self.__height) // 4
