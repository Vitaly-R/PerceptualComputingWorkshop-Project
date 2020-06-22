import pygame
import os


class SoundPlayer:
    def __init__(self):
        """
        Constructor.
        """
        self.__laser_shot_sound = pygame.mixer.Sound(os.path.join("Sound", "Laser.wav"))
        self.__missile_shot_sound = pygame.mixer.Sound(os.path.join("Sound", "Missile.wav"))
        self.__explosion_sound = pygame.mixer.Sound(os.path.join("Sound", "Explosion.wav"))
        self.__bg = pygame.mixer.Sound(os.path.join("Sound", "StartScreenBackground.wav"))
        self.__mute = False

    def play_music(self):
        """
        Starts playing the background music.
        """
        self.__bg.play(-1)

    def shoot_laser(self):
        """
        Plays the sound of the laser shot.
        """
        self.__laser_shot_sound.play()

    def shoot_missile(self):
        """
        Plays the sound of the missile shot.
        """
        self.__missile_shot_sound.play()

    def explode(self):
        """
        Plays the sound of the explosion.
        """
        self.__explosion_sound.play()

    def mute(self):
        """
        Mutes all sounds.
        """
        self.__mute = True
        self.__bg.set_volume(0)
        self.__laser_shot_sound.set_volume(0)
        self.__missile_shot_sound.set_volume(0)
        self.__explosion_sound.set_volume(0)

    def unmute(self):
        """
        Unmutes all sounds.
        """
        self.__mute = False
        self.__bg.set_volume(1)
        self.__laser_shot_sound.set_volume(1)
        self.__missile_shot_sound.set_volume(1)
        self.__explosion_sound.set_volume(1)

    @property
    def is_mute(self):
        """
        :return: Weather the volume is muted.
        """
        return self.__mute
