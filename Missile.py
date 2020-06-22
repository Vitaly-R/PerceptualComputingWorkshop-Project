import pygame
import os


class Missile:

    def __init__(self, start_x, start_y):
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
        screen.blit(self.__image, (self.__x, self.__y))
        if self.__flying:
            screen.blit(self.__flame, (self.__flame_x, self.__flame_y))

    def move(self, dx=None, dy=None):
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
        self.__flying = True

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
    def x(self):
        return self.__x

    @property
    def radius(self):
        return (self.__width + self.__height) // 4
