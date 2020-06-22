import pygame
import os


class Laser:

    def __init__(self, start_x, start_y, start_speed):
        """
        Constructor.
        :param start_x: Initial x coordinate of the top of the laser.
        :param start_y: Initial y coordinate of the top of the laser.
        :param start_speed: Speed of the ship that fired the laser along the y axis.
        """
        self.__x = start_x
        self.__y = start_y
        self.__image = pygame.image.load(os.path.join("Images", "Laser.png")).convert_alpha()
        self.__width, self.__height = self.__image.get_size()
        self.__speed_y = -8
        if start_speed < 0:
            self.__speed_y += start_speed
        self.__to_destroy = False

    def draw(self, screen):
        """
        Draws the laser to the given screen.
        :param screen: The screen to draw to.
        """
        screen.blit(self.__image, (self.__x, self.__y))

    def move(self):
        """
        Moves the laser according to its speed and location.
        """
        self.__y += self.__speed_y
        if self.__y < -self.__height:
            self.destroy()

    def destroy(self):
        """
        Sets the destruction flag of the laser (used by the game managing class).
        """
        self.__to_destroy = True

    @property
    def to_destroy(self):
        return self.__to_destroy

    @property
    def cx(self):
        """
        :return: x coordinate of the center of the laser.
        """
        return self.__x + self.__width // 2

    @property
    def cy(self):
        """
        :return: y coordinate of the center of the laser.
        """
        return self.__y + self.__height // 2

    @property
    def radius(self):
        """
        :return: collision radius of the laser.
        """
        return (self.__width + self.__height) // 4
