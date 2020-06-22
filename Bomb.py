import pygame
import os


class Bomb:
    def __init__(self, x, y, screen_height):
        self.__image = pygame.image.load(os.path.join("Images", "Bomb.png")).convert_alpha()
        self.__width, self.__height = self.__image.get_size()
        self.__x = x
        self.__y = y
        self.__falling = False
        self.__to_destroy = False
        self.__speed_y = 5
        self.__threshold = screen_height

    def draw(self, screen):
        screen.blit(self.__image, (self.__x, self.__y))

    def move(self, dx=None, dy=None):
        if not self.__falling:
            self.__x += dx
            self.__y += dy
        else:
            self.__y += self.__speed_y
        if self.__threshold < self.__y:
            self.destroy()

    def launch(self):
        self.__falling = True

    def destroy(self):
        self.__to_destroy = True

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
