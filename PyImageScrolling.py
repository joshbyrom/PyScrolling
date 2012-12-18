import pygame

from PubSub import *
from PyGameEngine import *
from PyImageModel import *

class ImageScrollView(PubSub):
    def __init__(self, x, y, width, height):
        PubSub.__init__(self)
        
        self.x = x
        self.y = y

        self.scroll_x = 0
        self.scroll_y = 0
        self.width = width
        self.height = height

    def handle(self, engine, model):
        self.engine = engine
        self.model = model

        if self.model.loaded:
            self._handle_model()
        else:
            self.model.on('loaded', lambda _, *__: self._handle_model())

    def _handle_model(self):
        self.image_width = self.model.width()
        self.image_height = self.model.height()

        assert(self.width <= self.image_width and self.height <= self.image_height)
        
        self.engine.on('render', lambda engine, *args: self.render(engine, args[1]))

    def render(self, engine, surface):
        dx = (self.scroll_x + self.width) - self.image_width
        dy = (self.scroll_y + self.height) - self.image_height

        over_x, over_y = dx > 0, dy > 0

        width = min(self.width, self.image_width - self.scroll_x)
        height = min(self.height, self.image_height - self.scroll_y)

        # blit the normal surface
        self._blit(surface, (self.scroll_x, self.scroll_y, width, height), (self.x, self.y))

        if over_x:
            next_x = self.x + width
            self._blit(surface, (0, self.scroll_y, dx, height), (next_x, self.y))

        if over_y:
            next_y = self.y + height
            self._blit(surface, (self.scroll_x, 0, width,  dy), (self.x, next_y))

        if over_y and over_x:
            self._blit(surface, (0, 0, dx, dy),(next_x, next_y))

    def _blit(self, surface, rect, xy):
        x, y, w, h = rect
        surface.blit(self.model.get_surface(x, y, w, h), (xy[0], xy[1]))

    def scroll(self, x, y=0):
        self.scroll_x += x
        self.scroll_y += y

        self.scroll_x = self.scroll_x % self.image_width
        self.scroll_y = self.scroll_y % self.image_height

        if self.scroll_x < 0:
            self.scroll_x += self.image_width

        if self.scroll_y < 0:
            self.scroll_y += self.image_height
            
        self.emit('scroll', [x, y])

        
if __name__ == '__main__':
    import sys, os

    to_scroll = [
        ('clouds.png', 1),
        ('mountains.png', 2.5),
        ('cloudy_day.png', 4),
    ]

    def init(engine, event, *args):
        for pair in to_scroll:
            def load_scroll_view(key = pair[0], value = pair[1]):
                filepath = os.path.join(sys.path[0], key)
                
                model = ImageModel(filepath)
                scroll_view = ImageScrollView(0, 0, engine.width, engine.height)

                model.on('loaded', lambda x, e, *a: scroll_view.handle(engine, model))
                model.load()

                engine.on('tick', lambda x, e, *a: scroll_view.scroll(value, 0))
            load_scroll_view()


    engine = Engine()
    engine.on('init', init)
    engine.start()
