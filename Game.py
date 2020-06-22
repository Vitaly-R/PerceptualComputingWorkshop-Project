from Asteroid import Asteroid
from Base import Base
from Enemy import Enemy
from GUI import GUI
from Parameters import KEYBOARD, WEBCAM, RIGHT, LEFT
from Player import get_player, MOVE, ACCELERATE, SHOOT_LASER, SHOOT_MISSILE
from Ship import Ship
from SoundPlayer import SoundPlayer
import pygame
import numpy as np


class Game:

    """ Game Constants. """
    __LASER_DELAY_FRAMES = 10
    __MISSILE_DELAY_FRAMES = 60
    __RELOAD_FRAMES = 300
    __ASTEROID_GENERATION_FRAMES = 45
    __ENEMY_GENERATION_FRAMES = 80
    __SHIP_RECOVERY_FRAMES = 600
    __RESPECT_TIME = 2000
    __MAX_SCORE = 30
    __HOW_TO_PLAY_PAGES = 2
    __HOW_TO_PLAY_START_PAGE = 1
    __INITIALIZATION_DELAY = 10
    __TOTAL_NUM_OF_ENEMIES = 20
    __ENEMY_DIFFICULTY_INCREASE_STEP = 5

    def __init__(self, mode, hand=RIGHT):
        """
        Constructor.
        :param mode: Mode value (KEYBOARD or WEBCAM from the parameters file).
        :param hand: Hand value (LEFT or RIGHT from the parameters file).
        """
        self.__mode = mode
        self.__hand = hand
        self.__gui = GUI()
        self.__sound_player = SoundPlayer()
        self.__player = get_player(self.__mode, self.__hand)
        self.__initialize_game_objects()
        self.__events = list()

    def __initialize_game_objects(self):
        """
        Initializes all flags, values, objects and data structures for the game.
        """
        self.__base = Base(self.__gui.window_width, self.__gui.window_height)
        self.__ship = Ship(self.__gui.window_width // 2, 3 * self.__gui.window_height // 4, self.__gui.window_width, self.__gui.window_height)
        self.__asteroids = list()
        self.__bombs = list()
        self.__enemies = list()
        self.__lasers = list()
        self.__missiles = list()
        self.__laser_delay = 0
        self.__missile_delay = 0
        self.__missile_reload_delay = self.__RELOAD_FRAMES
        self.__generate_asteroid_delay = self.__ASTEROID_GENERATION_FRAMES
        self.__generate_enemy_delay = self.__ENEMY_GENERATION_FRAMES
        self.__recovery_delay = self.__SHIP_RECOVERY_FRAMES
        self.__running = True
        self.__start_screen = True
        self.__settings_screen = False
        self.__how_to_play_screen = False
        self.__initialize_hand_tracking_screen = False
        self.__playing = False
        self.__paused = False
        self.__game_over = False
        self.__game_won = False
        self.__hand_in_screen = False
        self.__next_increase = self.__ENEMY_DIFFICULTY_INCREASE_STEP
        self.__how_to_play_page = 1
        self.__initialization_frame = 0
        self.__eliminated_enemies = 0
        self.__generated_enemies = 0
        self.__reset_difficulty()

    def __reset_difficulty(self):
        """
        Resets the difficulty level of the game.
        """
        if self.__mode == KEYBOARD:
            self.__enemy_difficulty_level = 1
            self.__asteroid_difficulty_level = 1
        else:
            self.__enemy_difficulty_level = 1.5
            self.__asteroid_difficulty_level = 1.5

    def play(self):
        """
        Runs a complete game.
        (Since there is an option for restarting the game within the game loop itself,
        after this method ends, this method cannot be called again)
        """
        self.__sound_player.play_music()
        while self.__running:
            self.__events = pygame.event.get()
            self.__check_mute()
            if self.__start_screen:
                self.__do_start_screen_loop()
            elif self.__settings_screen:
                self.__do_settings_loop()
            elif self.__how_to_play_screen:
                self.__do_how_to_play_loop()
            elif self.__initialize_hand_tracking_screen:
                self.__do_hand_tracking_initialization_loop()
            elif self.__playing:
                self.__do_game_loop()
            elif self.__game_won:
                self.__do_win_loop()
            else:
                self.__do_game_over_loop()
        self.__gui.end()

    def __do_start_screen_loop(self):
        """ Runs the loop of the start screen. """
        self.__gui.show_start_screen()
        for event in self.__events:
            if event.type == pygame.QUIT:
                self.__running = False
                self.__start_screen = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.__mode == WEBCAM:
                        self.__initialize_hand_tracking_screen = True
                    else:
                        self.__playing = True
                    self.__start_screen = False
                    self.__player.start()
                elif event.key == pygame.K_s:
                    self.__settings_screen = True
                    self.__start_screen = False
                elif event.key == pygame.K_h:
                    self.__how_to_play_screen = True
                    self.__start_screen = False

    def __do_settings_loop(self):
        """ Runs the loop of the settings screen. """
        self.__gui.show_settings(self.__mode, self.__hand)
        for event in self.__events:
            if event.type == pygame.QUIT:
                self.__running = False
                self.__settings_screen = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.__start_screen = True
                    self.__settings_screen = False
                elif event.key == pygame.K_k:
                    self.__mode = KEYBOARD if self.__mode == WEBCAM else WEBCAM
                    self.__player = get_player(self.__mode)
                    self.__reset_difficulty()
                elif event.key == pygame.K_h:
                    self.__hand = LEFT if self.__hand == RIGHT else RIGHT
                    self.__player.set_hand(self.__hand)

    def __do_how_to_play_loop(self):
        """ Runs the loop of the 'how to play' screen. """
        self.__gui.show_how_to_play_screen(self.__how_to_play_page)
        for event in self.__events:
            if event.type == pygame.QUIT:
                self.__running = False
                self.__how_to_play_screen = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.__start_screen = True
                    self.__how_to_play_screen = False
                    self.__how_to_play_page = self.__HOW_TO_PLAY_START_PAGE
                elif event.key == pygame.K_RIGHT:
                    self.__how_to_play_page += 1
                    self.__how_to_play_page = min(self.__how_to_play_page, self.__HOW_TO_PLAY_PAGES)
                elif event.key == pygame.K_LEFT:
                    self.__how_to_play_page -= 1
                    self.__how_to_play_page = max(self.__how_to_play_page, self.__HOW_TO_PLAY_START_PAGE)

    def __do_hand_tracking_initialization_loop(self):
        """ Runs the loop of the hand tracking initialization screen. """
        self.__gui.screen.fill((0, 0, 0))
        gesture, dx, dy, _ = self.__player.get_action()
        if gesture == MOVE:
            self.__initialization_frame += 1
            if self.__initialization_frame == self.__INITIALIZATION_DELAY:
                self.__playing = True
                self.__initialize_hand_tracking_screen = False
        else:
            self.__initialization_frame = 0
        self.__gui.show_initialize_tracking_screen(self.__hand, self.__initialization_frame)
        for event in self.__events:
            if event.type == pygame.QUIT:
                self.__running = False
                self.__initialize_hand_tracking_screen = False

    def __do_game_loop(self):
        """ Runs the main loop of the game. """
        self.__check_end_game()
        if self.__running and not self.__game_over:
            self.__check_pause()
            if not self.__paused:
                self.__check_collisions()
                self.__update_asteroids()
                self.__update_enemies()
                self.__update_ship()
                self.__update_lasers()
                self.__update_missiles()
                self.__update_bombs()
            self.__gui.show_current_game_screen(self.__base, self.__ship, self.__lasers, self.__missiles, self.__asteroids, self.__enemies, self.__bombs,
                                                self.__paused, self.__LASER_DELAY_FRAMES - self.__laser_delay, self.__hand_in_screen, self.__eliminated_enemies,
                                                self.__MAX_SCORE, self.__TOTAL_NUM_OF_ENEMIES)

    def __check_end_game(self):
        """ Checks weather any condition for the end of the game is met, and if so, updates the required parameters. """
        for event in self.__events:
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.__playing = False
                    self.__start_screen = True
                    self.__initialize_game_objects()
        if 0 in [self.__ship.hp, self.__base.hp]:
            self.__playing = False
            self.__game_over = True
        elif (self.__ship.score == self.__MAX_SCORE) or (self.__eliminated_enemies == self.__TOTAL_NUM_OF_ENEMIES):
            self.__playing = False
            self.__game_won = True

    def __check_pause(self):
        """ Checks weather the game needs to be paused / unpaused. """
        for event in self.__events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.__paused = not self.__paused

    def __check_mute(self):
        """ Checks weather the game needs to be muted / unmuted. """
        for event in self.__events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    if self.__sound_player.is_mute:
                        self.__sound_player.unmute()
                    else:
                        self.__sound_player.mute()

    def __check_collisions(self):
        """ Checks all possible collisions in the game. """
        self.__check_asteroids_collisions()
        self.__check_enemy_collisions()
        self.__check_bomb_collisions()

    def __check_asteroids_collisions(self):
        """ Checks collisions of asteroids with lasers, missiles, the ship, and the base. """
        for asteroid in self.__asteroids:
            if not asteroid.to_destroy:
                self.__check_collisions_with_lasers(asteroid)
            if not asteroid.to_destroy:
                self.__check_collisions_with_missiles(asteroid)
            if not asteroid.to_destroy:
                self.__check_collisions_with_ship(asteroid)
            if not asteroid.to_destroy:
                self.__check_collisions_with_base(asteroid)

    def __check_enemy_collisions(self):
        """ Checks collisions of enemies with lasers, missiles, and the ship. """
        for enemy in self.__enemies:
            if not enemy.to_destroy:
                self.__check_collisions_with_lasers(enemy)
            if not enemy.to_destroy:
                self.__check_collisions_with_missiles(enemy)
            if not enemy.to_destroy:
                self.__check_collisions_with_ship(enemy)

    def __check_bomb_collisions(self):
        """ Checks collisions of bombs with lasers, missiles, the ship, and the base. """
        for bomb in self.__bombs:
            if not bomb.to_destroy:
                self.__check_collisions_with_lasers(bomb)
            if not bomb.to_destroy:
                self.__check_collisions_with_missiles(bomb)
            if not bomb.to_destroy:
                self.__check_collisions_with_ship(bomb)
            if not bomb.to_destroy:
                self.__check_collisions_with_base(bomb)

    def __check_collisions_with_lasers(self, other):
        """ Checks collision of a given object with the lasers. """
        for laser in self.__lasers:
            if not laser.to_destroy:
                if self.__check_collisions_between_flying_objects(other, laser):
                    self.__ship.get_score()

    def __check_collisions_with_missiles(self, other):
        """ Checks collision of a given object with the flying missiles. """
        for missile in self.__missiles:
            if not missile.to_destroy:
                if self.__check_collisions_between_flying_objects(other, missile):
                    self.__ship.get_score()

    def __check_collisions_between_flying_objects(self, obj1, obj2):
        """ Checks collision between two flying objects. """
        distance = np.sqrt((obj1.cx - obj2.cx) ** 2 + (obj1.cy - obj2.cy) ** 2)
        collision_distance = obj1.radius + obj2.radius
        if distance < collision_distance:
            obj1.destroy()
            obj2.destroy()
            self.__sound_player.explode()
            return True
        return False

    def __check_collisions_with_ship(self, other):
        """ Checks collision of a given object with the ship. """
        distance = np.sqrt((other.cx - self.__ship.cx) ** 2 + (other.cy - self.__ship.cy) ** 2)
        collision_distance = other.radius + self.__ship.radius
        if distance < collision_distance:
            other.destroy()
            self.__ship.hit()
            self.__sound_player.explode()

    def __check_collisions_with_base(self, other):
        """ Checks collision of a given object with the base. """
        if self.__base.check_collision(other.cx, other.cy, other.radius):
            other.destroy()
            self.__base.hit()
            self.__sound_player.explode()

    def __update_asteroids(self):
        """ Updates the asteroid objects in the game. Moves and destroys the existing ones as necessary, and if needed, generates more. """
        asteroids_to_destroy = list()
        for asteroid in self.__asteroids:
            if not asteroid.to_destroy:
                asteroid.move()
            else:
                asteroids_to_destroy.append(asteroid)
        for asteroid in asteroids_to_destroy:
            self.__asteroids.remove(asteroid)
        if not self.__generate_asteroid_delay:
            self.__asteroids.append(Asteroid(self.__gui.window_width, self.__gui.window_height, self.__asteroid_difficulty_level))
            self.__generate_asteroid_delay = self.__ASTEROID_GENERATION_FRAMES
        else:
            self.__generate_asteroid_delay -= 1

    def __update_enemies(self):
        """ Updates the enemy objects in the game. Moves and destroys the existing ones as necessary, and if needed, generates more. """
        if self.__eliminated_enemies == self.__next_increase:
            self.__enemy_difficulty_level += 0.3
            self.__next_increase += self.__ENEMY_DIFFICULTY_INCREASE_STEP
        enemies_to_destroy = list()
        for enemy in self.__enemies:
            if not enemy.to_destroy:
                enemy.move()
                if enemy.to_launch:
                    self.__bombs.append(enemy.drop_bomb())
            else:
                enemies_to_destroy.append(enemy)
        for enemy in enemies_to_destroy:
            self.__enemies.remove(enemy)
            self.__eliminated_enemies += 1
        if (not self.__generate_enemy_delay) and (self.__generated_enemies < self.__TOTAL_NUM_OF_ENEMIES):
            self.__enemies.append(Enemy(self.__gui.window_width, self.__gui.window_height, self.__enemy_difficulty_level))
            self.__generate_enemy_delay = self.__ENEMY_GENERATION_FRAMES
            self.__generated_enemies += 1
        else:
            self.__generate_enemy_delay -= 1
            self.__generate_enemy_delay = max(self.__generate_enemy_delay, 0)

    def __update_ship(self):
        """ Receives information as to which action to take with the ship from the player object. Then, applies the received action. If the game is in webcam mode,
        then the lasers are shot automatically. If the game is in keyboard mode, the ship moves automatically (the player accelerates in the desired direction). """
        action, dx, dy, self.__hand_in_screen = self.__player.get_action()
        if action == ACCELERATE:
            self.__ship.accelerate(dx, dy)
        elif action == SHOOT_LASER:
            self.__shoot_laser()
        elif action == SHOOT_MISSILE:
            if not self.__missile_delay:
                missile = self.__ship.shoot_missile()
                if missile is not None:
                    self.__missiles.append(missile)
                    self.__missile_delay = self.__MISSILE_DELAY_FRAMES
                    self.__sound_player.shoot_missile()
        if self.__mode == KEYBOARD:
            self.__ship.move()
            pygame.time.wait(60)
        else:
            self.__ship.move(dx, dy)
            self.__shoot_laser()
        if not self.__recovery_delay:
            self.__ship.recover()
            self.__recovery_delay = self.__SHIP_RECOVERY_FRAMES
        else:
            self.__recovery_delay -= 1

    def __shoot_laser(self):
        """ Asks the ship to shoot a laser, if possible. """
        if not self.__laser_delay:
            self.__lasers.append(self.__ship.shoot_laser())
            self.__laser_delay = self.__LASER_DELAY_FRAMES
            self.__sound_player.shoot_laser()

    def __update_lasers(self):
        """ Updates the laser objects in the game. Moves and destroys them as necessary, and charges the ships laser cannon. """
        lasers_to_erase = list()
        for laser in self.__lasers:
            if not laser.to_destroy:
                laser.move()
            else:
                lasers_to_erase.append(laser)
        for laser in lasers_to_erase:
            self.__lasers.remove(laser)
        if self.__laser_delay:
            self.__laser_delay -= 1

    def __update_missiles(self):
        """ Updates the flying missile objects in the game. Moves and destroys them as necessary, and charges the ships missiles. """
        missiles_to_erase = list()
        for missile in self.__missiles:
            if not missile.to_destroy:
                missile.move()
            else:
                missiles_to_erase.append(missile)
        for missile in missiles_to_erase:
            self.__missiles.remove(missile)
        if self.__missile_delay:
            self.__missile_delay -= 1
            if self.__missile_delay and self.__mode == WEBCAM:
                self.__missile_delay -= 1
        if self.__missile_reload_delay:
            self.__missile_reload_delay -= 1
            if self.__mode == WEBCAM and self.__missile_reload_delay:
                self.__missile_reload_delay -= 1
        else:
            self.__ship.reload_missile()
            self.__missile_reload_delay = self.__RELOAD_FRAMES

    def __update_bombs(self):
        """ Updates the falling bomb objects in the game. Moves and destroys them as necessary. """
        bombs_to_destroy = list()
        for bomb in self.__bombs:
            if not bomb.to_destroy:
                bomb.move()
            else:
                bombs_to_destroy.append(bomb)
        for bomb in bombs_to_destroy:
            self.__bombs.remove(bomb)

    def __do_game_over_loop(self):
        """ Runs the 'game over' loop of the game. """
        self.__gui.show_game_over_screen()
        for event in self.__events:
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.__restart()
                elif event.key == pygame.K_f:
                    self.__pay_respects()
                elif event.key == pygame.K_RETURN:
                    self.__initialize_game_objects()

    def __do_win_loop(self):
        """ Runs the victory loop of the game. """
        self.__gui.show_win_screen()
        for event in self.__events:
            if event.type == pygame.QUIT:
                self.__running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.__restart()
                elif event.key == pygame.K_RETURN:
                    self.__initialize_game_objects()

    def __restart(self):
        """ Restarts the game. """
        self.__initialize_game_objects()
        self.__player.start()
        self.__start_screen = False
        self.__playing = True

    def __pay_respects(self):
        """ Shows the selected meme for a certain amount of time. """
        self.__gui.show_respects_screen()
        pygame.time.wait(self.__RESPECT_TIME)


def init(mode=KEYBOARD):
    """
    Initializes a new game object.
    :param mode: Playing mode value (KEYBOARD or WEBCAM from parameters file)
    :return: If the given mode is legal, a new Game object, None otherwise.
    """
    if mode in [KEYBOARD, WEBCAM]:
        return Game(mode)
    return None
