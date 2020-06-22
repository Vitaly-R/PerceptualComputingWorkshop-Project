import pygame
import os


class Base:

    __MAX_HP = 10

    def __init__(self, screen_width, screen_height):
        self.__image = pygame.image.load(os.path.join("Images", "Base.png")).convert_alpha()
        self.__shield_1 = pygame.image.load(os.path.join("Images", "Shield1.png")).convert_alpha()
        self.__shield_2 = pygame.image.load(os.path.join("Images", "Shield2.png")).convert_alpha()
        self.__shield_3 = pygame.image.load(os.path.join("Images", "Shield3.png")).convert_alpha()
        self.__shield_4 = pygame.image.load(os.path.join("Images", "Shield4.png")).convert_alpha()
        image_width, image_height = self.__image.get_size()
        self.__x = (screen_width - image_width) // 2
        self.__y = screen_height - image_height
        self.__hp = self.__MAX_HP
        self.__sections = [(self.__x + 51, self.__y + 83, self.__y + 57),
                           (self.__x + 151, self.__y + 57, self.__y + 23),
                           (self.__x + 185, self.__y + 23, self.__y + 5),
                           (self.__x + 374, self.__y + 5, self.__y - image_height),
                           (self.__x + 410, self.__y + 23, self.__y + 5),
                           (self.__x + 477, self.__y + 53, self.__y + 23),
                           (self.__x + 513, self.__y + 23, self.__y - image_height),
                           (self.__x + 559, self.__y + 72, self.__y + 23)]
        self.__shield_offset = 7

    def draw(self, screen):
        screen.blit(self.__image, (self.__x, self.__y))
        if (int(0.8 * self.__MAX_HP)) < self.__hp:
            screen.blit(self.__shield_1, (self.__x, self.__y))
        elif (int(0.6 * self.__MAX_HP)) < self.__hp:
            screen.blit(self.__shield_2, (self.__x, self.__y))
        elif (int(0.4 * self.__MAX_HP)) < self.__hp:
            screen.blit(self.__shield_3, (self.__x, self.__y))
        elif (int(0.2 * self.__MAX_HP)) < self.__hp:
            screen.blit(self.__shield_4, (self.__x, self.__y))

    def hit(self):
        self.__hp -= 1
        self.__hp = max(self.__hp, 0)

    def check_collision(self, cx, cy, radius):
        if (int(0.2 * self.__MAX_HP)) < self.__hp:
            for section_x, section_y_lower, section_y_higher in self.__sections:
                if self.__x <= cx <= section_x:
                    if section_y_higher <= cy:
                        if section_y_lower <= (cy + radius):
                            return True
                    break
            return False
        else:
            for section_x, section_y_lower, section_y_higher in self.__sections:
                if self.__x <= cx <= section_x:
                    if section_y_higher <= cy:
                        if section_y_lower <= (cy + radius + self.__shield_offset):
                            return True
                    break
            return False

    @property
    def hp(self):
        return self.__hp
