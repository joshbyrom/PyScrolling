import pygame

from PubSub import *
from PyGameEngine import *

class ImageModel(PubSub):
    def __init__(self, filepath):
        PubSub.__init__(self)

        self.filepath = filepath
        self.loaded = False

    def load(self):
        if self.loaded:
            return
        
        self._image = pygame.image.load(self.filepath)

        def closure(x = 0, y = 0, w = self._image.get_width(), h = self._image.get_height()):
            return self._image.subsurface([x, y, w, h])

        self.get_surface = closure

        self.loaded = True
        self.emit('loaded')

    def width(self):
        if self.loaded:
            return self._image.get_width()
        else:
            return 0

    def height(self):
        if self.loaded:
            return self._image.get_height()
        else:
            return 0
