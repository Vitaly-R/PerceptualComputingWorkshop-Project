import pygame
import os


class SoundPlayer:
    def __init__(self, mute=False):
        self.__laser_shot_sound = pygame.mixer.Sound(os.path.join("Sound", "Laser.wav"))
        self.__missile_shot_sound = pygame.mixer.Sound(os.path.join("Sound", "Missile.wav"))
        self.__explosion_sound = pygame.mixer.Sound(os.path.join("Sound", "Explosion.wav"))
        self.__bg = pygame.mixer.Sound(os.path.join("Sound", "StartScreenBackground.wav"))
        self.__playing = False
        self.__mute = mute

    def play_music(self):
        self.__bg.play(-1)
        self.__playing = True

    def shoot_laser(self):
        self.__laser_shot_sound.play()

    def shoot_missile(self):
        self.__missile_shot_sound.play()

    def explode(self):
        self.__explosion_sound.play()

    def mute(self):
        self.__mute = True
        self.__bg.set_volume(0)
        self.__laser_shot_sound.set_volume(0)
        self.__missile_shot_sound.set_volume(0)
        self.__explosion_sound.set_volume(0)

    def unmute(self):
        self.__mute = False
        self.__bg.set_volume(1)
        self.__laser_shot_sound.set_volume(1)
        self.__missile_shot_sound.set_volume(1)
        self.__explosion_sound.set_volume(1)

    @property
    def is_mute(self):
        return self.__mute

    @property
    def playing(self):
        return self.__playing
