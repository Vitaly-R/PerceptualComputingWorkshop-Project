from abc import ABC, abstractmethod
from Parameters import KEYBOARD, RIGHT
from WebcamReader import WebcamThread
from HandDetector import HandDetector
from GestureEngine import GestureEngine
import pygame


NO_ACTION = GestureEngine.NO_GESTURE
MOVE = GestureEngine.OPEN_HAND
SHOOT_MISSILE = GestureEngine.METAL
SHOOT_LASER = SHOOT_MISSILE + 1
ACCELERATE = SHOOT_LASER + 1
PLAYERS = list()


class Player(ABC):

    def start(self):
        """
        Initialization method for any players that require some initialization before the start of a game.
        """
        pass

    def set_hand(self, hand):
        """
        Sets which hand the player uses, if any.
        :param hand: Value for the hand (one of RIGHT, LEFT from the parameters file).
        """
        pass

    @abstractmethod
    def get_action(self):
        """
        :return: The action for the round from the player.
        """
        pass


class WebcamPlayer(Player):
    def __init__(self, hand):
        """
        Constructor.
        Initializes webcam and hand detection objects for playing.
        :param hand: Which hand to play with (RIGHT or LEFT from parameters file)
        """
        self.__capture = WebcamThread()
        self.__hand_detector = HandDetector(self.__capture, hand)
        self.__gesture_engine = GestureEngine(hand)
        self.__started = False

    def start(self):
        if not self.__started:
            self.__capture.start()
            self.__started = True

    def set_hand(self, hand):
        self.__hand_detector.set_hand(hand)
        self.__gesture_engine.set_hand(hand)

    def get_action(self):
        frame = self.__capture.grab_frame()
        if frame is not None:
            handKeypoints = self.__hand_detector.detect(frame)
            handKeypoints[:, 0] -= self.__capture.top_left_x
            gesture, _, _, dx, dy = self.__gesture_engine.analyze(handKeypoints)
            return gesture, dx, dy, self.__gesture_engine.THRESHOLD < handKeypoints[0, 2]
        return NO_ACTION, 0, 0, False


class KeyboardPlayer(Player):

    def get_action(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            return ACCELERATE, 0, -5, False
        if keys[pygame.K_DOWN]:
            return ACCELERATE, 0, 5, False
        if keys[pygame.K_RIGHT]:
            return ACCELERATE, 5, 0, False
        if keys[pygame.K_LEFT]:
            return ACCELERATE, -5, 0, False
        if keys[pygame.K_SPACE]:
            return SHOOT_LASER, 0, 0, False
        if keys[pygame.K_n]:
            return SHOOT_MISSILE, 0, 0, False
        return NO_ACTION, 0, 0, False


def init(hand):
    """
    Initializes the players available for the game.
    :param hand:
    :return:
    """
    global PLAYERS
    PLAYERS = [KeyboardPlayer(), WebcamPlayer(hand)]


def get_player(mode, hand=RIGHT):
    """
    :param mode: Playing mode (KEYBOARD or WEBCAM from parameters file)
    :param hand: Hand to play with (RIGHT or LEFT from parameters file)
    :return: A player for the requested mode, with the requested hand.
    """
    global PLAYERS
    if not len(PLAYERS):
        init(hand)
    if mode == KEYBOARD:
        return PLAYERS[0]
    return PLAYERS[1]
