import pygame
import os


class Bomb:
    def __init__(self, x, y, screen_height):
        """
        Constructor.
        :param x: x coordinate of the top left corner of the image.
        :param y: y coordinate of the top left corner of the image.
        :param screen_height: Height of the playing screen.
        """
        self.__image = pygame.image.load(os.path.join("Images", "Bomb.png")).convert_alpha()
        self.__width, self.__height = self.__image.get_size()
        self.__x = x
        self.__y = y
        self.__falling = False
        self.__to_destroy = False
        self.__speed_y = 5
        self.__threshold = screen_height

    def draw(self, screen):
        """
        Draws the bomb to the given screen.
        :param screen: The screen to draw to.
        """
        screen.blit(self.__image, (self.__x, self.__y))

    def move(self, dx=None, dy=None):
        """
        Moves the bomb.
        :param dx: Distance to move in the x axis.
        :param dy: Distance to move in the y axis.
        """
        if not self.__falling:
            self.__x += dx
            self.__y += dy
        else:
            self.__y += self.__speed_y
        if self.__threshold < self.__y:
            self.destroy()

    def launch(self):
        """
        Sets the launching flag of the bomb (used by the Enemy class).
        """
        self.__falling = True

    def destroy(self):
        """
        Sets the destruction flag of the bomb (used by the game managing class, and the Enemy class).
        """
        self.__to_destroy = True

    @property
    def to_destroy(self):
        return self.__to_destroy

    @property
    def cx(self):
        """
        :return: x coordinate of the center of mass of the bomb.
        """
        return self.__x + self.__width // 2

    @property
    def cy(self):
        """
        :return: y coordinate of the center of mass of the bomb.
        """
        return self.__y + self.__height // 2

    @property
    def radius(self):
        """
        :return: collision radius of the bomb.
        """
        return (self.__width + self.__height) // 4
