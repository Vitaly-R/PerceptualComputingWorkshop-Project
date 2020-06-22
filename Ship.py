import pygame
import os
from Laser import Laser
from Missile import Missile


class Ship:

    __MAX_HP = 7

    def __init__(self, start_x, start_y, screen_width, screen_height):
        """
        Constructor.
        :param start_x: Initial x coordinate of the center of the ship.
        :param start_y: Initial y coordinate of the center of the ship.
        :param screen_width: Width of the playing screen.
        :param screen_height: Height of the playing screen.
        """
        self.__x = start_x
        self.__y = start_y
        self.__screen_width = screen_width
        self.__screen_height = screen_height
        self.__image = pygame.image.load(os.path.join("Images", "Ship.png")).convert_alpha()
        self.__width, self.__height = self.__image.get_size()
        self.__speed_x = 0
        self.__speed_y = 0
        self.__cannon = 0
        self.__cannons = 4
        self.__missiles = [Missile(self.__x - 16, self.__y - 4), Missile(self.__x + 16, self.__y - 4)]
        self.__right_missile = True
        self.__left_missile = True
        self.__num_missiles = len(self.__missiles)
        self.__max_missiles = 2
        self.__hp = self.__MAX_HP
        self.__score = 0

    def draw(self, screen):
        """
        Draws the ship to the given screen.
        If any missiles are attached to it, draws them too.
        :param screen: The screen to draw to.
        """
        for missile in self.__missiles:
            missile.draw(screen)
        screen.blit(self.__image, (self.__x - self.__width // 2, self.__y - self.__height // 2))

    def move(self, dx=None, dy=None):
        """
        Moves the ship according to its speed and direction, or a given distance along the x and y axes.
        If any missiles are attached to the ship, they are moved as well.
        :param dx: Distance to move the ship along the x axis.
        :param dy: Distance to move the ship along the y axis.
        """
        if dx is None:
            dx = self.__speed_x
        if dy is None:
            dy = self.__speed_y
        if not ((self.__width // 2) <= (self.__x + dx) <= (self.__screen_width - self.__width // 2)):
            self.__speed_x = 0
            dx = self.__speed_x
        if not ((self.__height // 2) <= (self.__y + dy) <= (self.__screen_height - self.__height // 2)):
            self.__speed_y = 0
            dy = self.__speed_y
        self.__y += dy
        self.__x += dx
        for missile in self.__missiles:
            missile.move(dx, dy)

    def accelerate(self, dx, dy):
        """
        Accelerates the ship along the x and y axes.
        :param dx: Acceleration along the x axis.
        :param dy: Acceleration along the y axis.
        """
        self.__speed_x += dx
        self.__speed_y += dy

    def shoot_laser(self):
        """
        Shoots a laser from the current cannon.
        :return: A laser object representing the laser shot.
        """
        if self.__cannon == 0:
            laser = Laser(self.__x - 24, self.__y - (self.__height // 2) + 3, self.__speed_y)
        elif self.__cannon == 1:
            laser = Laser(self.__x - 7, self.__y - (self.__height // 2), self.__speed_y)
        elif self.__cannon == 2:
            laser = Laser(self.__x + 7, self.__y - (self.__height // 2), self.__speed_y)
        else:
            laser = Laser(self.__x + 24, self.__y - (self.__height // 2) + 3, self.__speed_y)
        self.__cannon += 1
        self.__cannon %= self.__cannons
        return laser

    def shoot_missile(self):
        """
        Shoots a missile from the attached missiles.
        :return: The last attached missile object if any exist, None otherwise.
        """
        if self.__num_missiles:
            missile = self.__missiles.pop()
            if self.__x < missile.cx:
                self.__right_missile = False
            else:
                self.__left_missile = False
            missile.launch()
            self.__num_missiles -= 1
            return missile
        return None

    def reload_missile(self):
        """
        Adds a new attached missile object to the ship.
        """
        if self.__num_missiles < self.__max_missiles:
            if self.__num_missiles == 0:
                self.__missiles.append(Missile(self.__x - 16, self.__y - 4))
                self.__left_missile = True
            else:
                self.__missiles.append(Missile(self.__x + 16, self.__y - 4))
                self.__right_missile = True
            self.__num_missiles += 1

    def hit(self):
        """
        Registers a hit on the ship.
        """
        self.__hp -= 1
        self.__hp = max(self.__hp, 0)

    def recover(self):
        """
        Recovers a hit point.
        """
        self.__hp += 1
        self.__hp = min(self.__hp, self.__MAX_HP)

    def get_score(self):
        """
        Adds a point to the score of the ship.
        """
        self.__score += 1

    @property
    def right_missile(self):
        """
        :return: Weather a missile is attached on the right of the ship (used to draw indication of missile to the menu).
        """
        return self.__right_missile

    @property
    def left_missile(self):
        """
        :return: Weather a missile is attached on the left of the ship (used to draw indication of missile to the menu).
        """
        return self.__left_missile

    @property
    def hp(self):
        """
        :return: Ship HP.
        """
        return self.__hp

    @property
    def score(self):
        """
        :return: Ship score.
        """
        return self.__score

    @property
    def cx(self):
        """
        :return: x coordinate of the center of the ship.
        """
        return self.__x

    @property
    def cy(self):
        """
        :return: y coordinate of the center of the ship.
        """
        return self.__y

    @property
    def radius(self):
        """
        :return: Collision radius of the ship.
        """
        return (self.__width + self.__height) // 4
