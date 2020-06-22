import pygame
import os


class Missile:

    def __init__(self, start_x, start_y):
        """
        Constructor.
        :param start_x: Initial x coordinate of the top left corner of the missile.
        :param start_y: Initial y coordinate of the top left corner of the missile.
        """
        self.__image = pygame.image.load(os.path.join("Images", "Missile.png")).convert_alpha()
        self.__flame = pygame.image.load(os.path.join("Images", "MissileFlame.png")).convert_alpha()
        self.__flying = False
        self.__width, self.__height = self.__image.get_size()
        self.__x = start_x - self.__width // 2
        self.__y = start_y - self.__height // 2
        flame_width, flame_height = self.__flame.get_size()
        self.__flame_x = start_x - flame_width // 2
        self.__flame_y = start_y + self.__height // 2 + 1
        self.__speed_y = -6
        self.__to_destroy = False

    def draw(self, screen):
        """
        Draws the missile to the given screen.
        If the missile is in flight, draws the tail flame as well.
        :param screen: The screen to draw to.
        """
        screen.blit(self.__image, (self.__x, self.__y))
        if self.__flying:
            screen.blit(self.__flame, (self.__flame_x, self.__flame_y))

    def move(self, dx=None, dy=None):
        """
        Moves the laser according to its speed and location.
        :param dx: Distance to move the missile along the x axis (used when attached to a ship).
        :param dy: Distance to move the missile along the y axis (used when attached to a ship).
        """
        if self.__flying:
            self.__y += self.__speed_y
            self.__flame_y += self.__speed_y
        else:
            self.__x += dx
            self.__flame_x += dx
            self.__y += dy
            self.__flame_y += dy
        if self.__y < -self.__height:
            self.destroy()

    def launch(self):
        """
        Sets the flying flag of the missile (used by the ship it's attached to).
        """
        self.__flying = True

    def destroy(self):
        """
        Sets the destruction flag of the missile (used by the game managing class).
        """
        self.__to_destroy = True

    @property
    def to_destroy(self):
        return self.__to_destroy

    @property
    def cx(self):
        """
        :return: x coordinate of the center of the missile.
        """
        return self.__x + self.__width // 2

    @property
    def cy(self):
        """
        :return: y coordinate of the center of the missile.
        """
        return self.__y + self.__height // 2

    @property
    def radius(self):
        """
        :return: collision radius of the missile.
        """
        return (self.__width + self.__height) // 4
