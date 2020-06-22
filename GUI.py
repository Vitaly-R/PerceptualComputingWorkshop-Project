from Parameters import KEYBOARD, RIGHT, LEFT
import pygame
import os


class GUI:

    __GAME_TITLE = "Base Defender"
    __PAGE_MAIN_TEXT_SIZE = 50
    __PAGE_MAIN_TEXT_COLOR = (255, 255, 255)
    __PAGE_TEXT_SIZE = 30
    __PAGE_TEXT_COLOR = (150, 150, 150)
    __BACKGROUND_COLOR = (0, 0, 0)
    __WINDOW_WIDTH = 750
    __WINDOW_HEIGHT = 750
    __BOTTOM_MENU_HEIGHT = 100

    def __init__(self):
        """
        Constructor. Calls initialization methods for pygame, the display, all required images and texts to show, and their positions.
        """
        pygame.init()
        pygame.font.init()
        self.__main_text_font = pygame.font.Font(pygame.font.get_default_font(), self.__PAGE_MAIN_TEXT_SIZE)
        self.__text_font = pygame.font.Font(pygame.font.get_default_font(), self.__PAGE_TEXT_SIZE)
        self.__initialize_images()
        self.__initialize_image_positions()
        self.__initialize_image_parameters()
        self.__initialize_paused_text()
        self.__screen = pygame.display.set_mode((self.__WINDOW_WIDTH, self.__WINDOW_HEIGHT + self.__BOTTOM_MENU_HEIGHT))
        pygame.display.set_caption(self.__GAME_TITLE)

    def __initialize_images(self):
        """
        Loads the images that are part of the GUI to show.
        """
        self.__numbers = {"0": pygame.image.load(os.path.join("Images", "0.png")),
                          "1": pygame.image.load(os.path.join("Images", "1.png")),
                          "2": pygame.image.load(os.path.join("Images", "2.png")),
                          "3": pygame.image.load(os.path.join("Images", "3.png")),
                          "4": pygame.image.load(os.path.join("Images", "4.png")),
                          "5": pygame.image.load(os.path.join("Images", "5.png")),
                          "6": pygame.image.load(os.path.join("Images", "6.png")),
                          "7": pygame.image.load(os.path.join("Images", "7.png")),
                          "8": pygame.image.load(os.path.join("Images", "8.png")),
                          "9": pygame.image.load(os.path.join("Images", "9.png"))}
        self.__start_screen = pygame.image.load(os.path.join("Images", "StartScreen.png"))
        self.__settings_screen = pygame.image.load(os.path.join("Images", "SettingsScreen.png"))
        self.__keyboard_mode = pygame.image.load(os.path.join("Images", "KeyboardMode.png"))
        self.__webcam_mode = pygame.image.load(os.path.join("Images", "WebcamMode.png"))
        self.__right_hand = pygame.image.load(os.path.join("Images", "RightHand.png"))
        self.__left_hand = pygame.image.load(os.path.join("Images", "LeftHand.png"))
        self.__init_hand_tracking_screen = {RIGHT: [pygame.image.load(os.path.join("Images", "InitHandTrackingRight.png")),
                                                    pygame.image.load(os.path.join("images", "InitHandTrackingRightLoading.png"))],
                                            LEFT: [pygame.image.load(os.path.join("Images", "InitHandTrackingLeft.png")),
                                                   pygame.image.load(os.path.join("Images", "InitHandTrackingLeftLoading.png"))]}
        self.__how_to_play_pages = {1: pygame.image.load(os.path.join("Images", "HowToPlay01.png")),
                                    2: pygame.image.load(os.path.join("Images", "HowToPlay02.png"))}
        self.__bottom_menu = pygame.image.load(os.path.join("Images", "BottomMenu.png"))
        self.__bottom_menu_side = pygame.image.load(os.path.join("Images", "BottomMenuSide.png"))
        self.__hp_unit = pygame.image.load(os.path.join("Images", "HPUnit.png"))
        self.__respects = pygame.image.load(os.path.join("Images", "F.png"))
        self.__laser_unit = pygame.image.load(os.path.join("Images", "LaserUnit.png"))
        self.__missile_unit = pygame.image.load(os.path.join("Images", "MissileUnit.png"))
        self.__game_over_screen = pygame.image.load(os.path.join("Images", "GameOver.png"))
        self.__victory_screen = pygame.image.load(os.path.join("Images", "VictoryScreen.png"))
        self.__hand_frame = pygame.image.load(os.path.join("Images", "HandFrame.png"))

    def __initialize_image_positions(self):
        """
        Initializes the positions of all images loaded as part of the GUI.
        """
        self.__mode_position = (200, 170)
        self.__hand_position = (240, 237)
        self.__bottom_menu_position = ((self.__WINDOW_WIDTH - self.__bottom_menu.get_width()) // 2, self.__WINDOW_HEIGHT)
        self.__bottom_menu_side_position1 = (0, self.__WINDOW_HEIGHT)
        self.__bottom_menu_side_position2 = (self.__bottom_menu.get_width() + self.__bottom_menu_side.get_width(), self.__WINDOW_HEIGHT)
        self.__first_digit_score_position = (self.__bottom_menu_position[0] + 119, self.__bottom_menu_position[1] + 57)
        self.__first_digit_max_score_position = (self.__bottom_menu_position[0] + 177, self.__bottom_menu_position[1] + 57)
        self.__first_digit_enemies_position = (self.__bottom_menu_position[0] + 339, self.__bottom_menu_position[1] + 57)
        self.__first_digit_total_enemies_position = (self.__bottom_menu_position[0] + 401, self.__bottom_menu_position[1] + 57)
        self.__ship_hp_initial_position = (self.__bottom_menu_position[0] + 131, self.__bottom_menu_position[1] + 12)
        self.__base_hp_initial_position = (self.__bottom_menu_position[0] + 131, self.__bottom_menu_position[1] + 35)
        self.__respects_position = ((self.__WINDOW_WIDTH - self.__respects.get_width()) // 2, (self.__WINDOW_HEIGHT - self.__respects.get_height()) // 2)
        self.__laser_unit_bottom_position = (self.__bottom_menu_position[0] + 540, self.__bottom_menu_position[1] + 77)
        self.__missile_unit_position_left = (self.__bottom_menu_position[0] + 484, self.__bottom_menu_position[1] + 50)
        self.__missile_unit_position_right = (self.__bottom_menu_position[0] + 503, self.__bottom_menu_position[1] + 50)

    def __initialize_image_parameters(self):
        """
        Initializes parameters related to displaying the images loaded to the GUI.
        """
        self.__digit_width = self.__numbers['0'].get_width() + 2
        self.__hp_unit_width = self.__hp_unit.get_width() + 2
        self.__laser_unit_height = self.__laser_unit.get_height() + 1

    def __initialize_paused_text(self):
        """
        Initializes the text appearing on the screen when the game is paused.
        """
        paused_text = "Paused"
        paused_center = (self.__WINDOW_WIDTH // 2, self.__WINDOW_HEIGHT // 2)
        self.__paused_text, self.__paused_center = self.__initialize_text(paused_text, paused_center, self.__main_text_font, self.__PAGE_MAIN_TEXT_COLOR)

        unpause_text = "press \'p\' to unpause"
        unpause_center = (self.__WINDOW_WIDTH // 2, self.__WINDOW_HEIGHT // 2 + self.__PAGE_TEXT_SIZE * 2)
        self.__unpause_text, self.__unpause_center = self.__initialize_text(unpause_text, unpause_center, self.__text_font, self.__PAGE_TEXT_COLOR)

    @staticmethod
    def __initialize_text(text, center_position, font, color):
        """
        Initializes the text surface and position rectangle for a given main text centered at a given position.
        :param text: Text to initialize.
        :param center_position: Center position of the text.
        :return: A tuple (text surface, rectangle), where rectangle represents where the text surface will be shown.
        """
        text_surface = font.render(text, True, color)
        rectangle = text_surface.get_rect()
        rectangle.center = center_position
        return text_surface, rectangle

    def show_start_screen(self):
        """ Shows the start screen of the game. """
        self.__screen.blit(self.__start_screen, (0, 0))
        pygame.display.flip()

    def show_settings(self, mode, hand):
        """ Shows the settings screen of the game. """
        self.__screen.blit(self.__settings_screen, (0, 0))
        if mode == KEYBOARD:
            self.__screen.blit(self.__keyboard_mode, self.__mode_position)
        else:
            self.__screen.blit(self.__webcam_mode, self.__mode_position)
        if hand == RIGHT:
            self.__screen.blit(self.__right_hand, self.__hand_position)
        else:
            self.__screen.blit(self.__left_hand, self.__hand_position)
        pygame.display.flip()

    def show_how_to_play_screen(self, page):
        """ Shows the 'how to play' screen of the game. """
        self.__screen.blit(self.__how_to_play_pages[page], (0, 0))
        pygame.display.flip()

    def show_initialize_tracking_screen(self, hand, loading):
        """ Shows the hand tracking initialization screen of the game. """
        if loading:
            self.__screen.blit(self.__init_hand_tracking_screen[hand][1], (0, 0))
        else:
            self.__screen.blit(self.__init_hand_tracking_screen[hand][0], (0, 0))
        pygame.display.flip()

    def show_current_game_screen(self, base, ship, lasers, missiles, asteroids, enemies, bombs, paused, laser_charge, hand_in_screen, eliminated_enemies, max_score, num_enemies):
        """
        Shows the current state of the main game screen.
        :param base: Base object.
        :param ship: Ship object.
        :param lasers: List of laser objects
        :param missiles: List of flying missile objects.
        :param asteroids: List of asteroid object.
        :param enemies: List of enemy objects.
        :param bombs: List of falling bomb objects.
        :param paused: A flag of weather the game is paused.
        :param laser_charge: Current value of the laser charge.
        :param hand_in_screen: A flag of weather the hand is registered in the screen.
        :param eliminated_enemies: Number of eliminated enemies.
        :param max_score: Max score of the game.
        :param num_enemies: Total number of enemies.
        """
        self.__screen.fill(self.__BACKGROUND_COLOR)
        base.draw(self.__screen)
        ship.draw(self.__screen)
        self.__show_lasers(lasers)
        self.__show_missiles(missiles)
        self.__show_asteroids(asteroids)
        self.__show_enemies(enemies)
        self.__show_bombs(bombs)
        self.__show_bottom_menu(ship, base, laser_charge, max_score, eliminated_enemies, num_enemies)
        self.__show_paused(paused)
        self.__show_hand_in_screen(hand_in_screen)
        pygame.display.flip()

    def __show_lasers(self, lasers):
        """ Shows the lasers on the screen. """
        for laser in lasers:
            laser.draw(self.__screen)

    def __show_missiles(self, missiles):
        """ Shows the missiles flying on the screen. """
        for missile in missiles:
            missile.draw(self.__screen)

    def __show_asteroids(self, asteroids):
        """ Shows the asteroid on the screen. """
        for asteroid in asteroids:
            asteroid.draw(self.__screen)

    def __show_enemies(self, enemies):
        """ Shows the enemies on the screen. """
        for enemy in enemies:
            enemy.draw(self.__screen)

    def __show_bombs(self, bombs):
        """ Shows the falling bombs on the screen. """
        for bomb in bombs:
            bomb.draw(self.__screen)

    def __show_bottom_menu(self, ship, base, laser_charge, max_score, eliminated_enemies, num_enemies):
        """
        Shows the menu below the playing screen, which shows the current base and ship HP, the laser charge status, missile charge indicators,
        the number of eliminated enemies (out of total), the score (out of max score), and button instructions to pause and exit the game.
        """
        self.__screen.blit(self.__bottom_menu_side, self.__bottom_menu_side_position1)
        self.__screen.blit(self.__bottom_menu, self.__bottom_menu_position)
        self.__screen.blit(self.__bottom_menu_side, self.__bottom_menu_side_position2)
        for i in range(ship.hp):
            self.__screen.blit(self.__hp_unit, (self.__ship_hp_initial_position[0] + i * self.__hp_unit_width, self.__ship_hp_initial_position[1]))
        for i in range(base.hp):
            self.__screen.blit(self.__hp_unit, (self.__base_hp_initial_position[0] + i * self.__hp_unit_width, self.__base_hp_initial_position[1]))
        for i in range(laser_charge):
            self.__screen.blit(self.__laser_unit, (self.__laser_unit_bottom_position[0], self.__laser_unit_bottom_position[1] - self.__laser_unit_height * i))
        if ship.right_missile:
            self.__screen.blit(self.__missile_unit, self.__missile_unit_position_right)
        if ship.left_missile:
            self.__screen.blit(self.__missile_unit, self.__missile_unit_position_left)
        score = str(ship.score)
        for i in range(len(score)):
            self.__screen.blit(self.__numbers[score[i]], (self.__first_digit_score_position[0] + i * self.__digit_width, self.__first_digit_score_position[1]))
        max_score = str(max_score)
        for i in range(len(max_score)):
            self.__screen.blit(self.__numbers[max_score[i]], (self.__first_digit_max_score_position[0] + i * self.__digit_width, self.__first_digit_max_score_position[1]))
        eliminated = str(eliminated_enemies)
        for i in range(len(eliminated)):
            self.__screen.blit(self.__numbers[eliminated[i]], (self.__first_digit_enemies_position[0] + i * self.__digit_width, self.__first_digit_enemies_position[1]))
        total_enemies = str(num_enemies)
        for i in range(len(total_enemies)):
            self.__screen.blit(self.__numbers[total_enemies[i]], (self.__first_digit_total_enemies_position[0] + i * self.__digit_width, self.__first_digit_total_enemies_position[1]))

    def __show_paused(self, paused):
        """ Shows paused text if necessary. """
        if paused:
            self.__screen.blit(self.__paused_text, self.__paused_center)
            self.__screen.blit(self.__unpause_text, self.__unpause_center)

    def __show_hand_in_screen(self, hand_in_screen):
        """ Shows a frame indicating that the hand of the player is registered in the screen, if necessary. """
        if hand_in_screen:
            self.__screen.blit(self.__hand_frame, (0, 0))

    def show_game_over_screen(self):
        """ Shows 'game over' screen. """
        self.__screen.blit(self.__game_over_screen, (0, 0))
        pygame.display.flip()

    def show_win_screen(self):
        """ Shows victory screen. """
        self.__screen.blit(self.__victory_screen, (0, 0))
        pygame.display.flip()

    def show_respects_screen(self):
        """ Shows a meme to pay respects. """
        self.__screen.fill(self.__BACKGROUND_COLOR)
        self.__screen.blit(self.__respects, self.__respects_position)
        pygame.display.flip()

    @staticmethod
    def end():
        """ Quits pygame. """
        pygame.font.quit()
        pygame.quit()

    @property
    def screen(self):
        return self.__screen

    @property
    def window_width(self):
        return self.__WINDOW_WIDTH

    @property
    def window_height(self):
        return self.__WINDOW_HEIGHT
