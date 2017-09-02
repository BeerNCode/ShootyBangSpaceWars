import pygame
import os
from enum import Enum

class Sound(Enum):
    Fire = "Laser 9.wav"
    Thrust = "In Flight.wav"
    Impact = "Take Off.wav"
    #Thrust2 = "thrust.wav"

class Sounds():
    """ Mega beep"""

    _sound_library = {}
    _sound_voice = {}

    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.set_num_channels(10);
        for idx, sound in enumerate(Sound): 
            soundFile = pygame.mixer.Sound("..\\snd\\" + sound.value)
            self._sound_library[sound.name] = soundFile
            self._sound_voice[sound.name] = pygame.mixer.Channel(idx)

    def play(self, sound):
        if not self._sound_voice[sound.name].get_busy():
            self._sound_voice[sound.name].play(self._sound_library[sound.name])

    def stop(self, sound):
        self._sound_voice[sound.name].stop()