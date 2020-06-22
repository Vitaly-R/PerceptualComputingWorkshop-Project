import pygame
import os
import numpy as np

""" Image names of the different asteroids. """
IMAGE_NAMES = ["Asteroid1.png", "Asteroid2.png", "Asteroid3.png", "Asteroid4.png", "Asteroid5.png"]


class Asteroid:

    def __init__(self, screen_width, screen_height, speed_multiplier=1):
        """
        Constructor.
        :param screen_width: Width of the playing screen.
        :param screen_height: Height of the playing screen.
        :param speed_multiplier: A multiplier factor for the speed of the asteroid.
        """
        image_index = np.random.randint(0, len(IMAGE_NAMES))
        self.__image = pygame.image.load(os.path.join("Images", IMAGE_NAMES[image_index]))
        self.__width, self.__height = self.__image.get_size()
        self.__x = np.random.randint(0, screen_width)
        self.__y = np.random.randint(-10, 10)
        self.__speed_x = speed_multiplier * np.random.randint(-3, 4)
        self.__speed_y = speed_multiplier * np.random.randint(2, 5)
        self.__to_destroy = False
        self.__threshold_y = screen_height
        self.__threshold_x = -self.__width if self.__speed_x < 0 else screen_width

    def draw(self, screen):
        """
        Draws the asteroid to the given screen.
        :param screen: The screen to draw to.
        """
        screen.blit(self.__image, (self.__x, self.__y))

    def move(self):
        """
        Moves the asteroid according to its speed and location.
        """
        self.__x += self.__speed_x
        self.__y += self.__speed_y
        if self.__threshold_y < self.__y:
            self.destroy()
        elif self.__speed_x < 0 and (self.__x < self.__threshold_x):
            self.destroy()
        elif 0 < self.__speed_x and (self.__threshold_x < self.__x):
            self.destroy()

    def destroy(self):
        """
        Sets the destruction flag of the asteroid (used by the game managing class).
        """
        self.__to_destroy = True

    @property
    def to_destroy(self):
        return self.__to_destroy

    @property
    def cx(self):
        """
        :return: x coordinate of the center of mass of the asteroid.
        """
        return self.__x + self.__width // 2

    @property
    def cy(self):
        """
        :return: y coordinate of the center of mass of the asteroid.
        """
        return self.__y + self.__height // 2

    @property
    def radius(self):
        """
        :return: collision radius of the asteroid.
        """
        return (self.__width + self.__height) // 4
