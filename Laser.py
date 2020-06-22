import pygame
import os


class Laser:

    def __init__(self, start_x, start_y, start_speed):
        self.__x = start_x
        self.__y = start_y
        self.__image = pygame.image.load(os.path.join("Images", "Laser.png")).convert_alpha()
        self.__width, self.__height = self.__image.get_size()
        self.__speed_y = -8
        if start_speed < 0:
            self.__speed_y += start_speed
        self.__to_destroy = False

    def draw(self, screen):
        screen.blit(self.__image, (self.__x, self.__y))

    def move(self):
        self.__y += self.__speed_y
        if self.__y < -self.__height:
            self.destroy()

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
