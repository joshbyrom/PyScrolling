import pygame

from PubSub import *
from PyGameEngine import *


        
if __name__ == '__main__':
    def render_fun():
        def closure(engine, *args):
            event, surface = args

            surface.fill((0,0,0), (0,0,surface.get_width(), surface.get_height()))

            color = (232, 232, 232)
            
            surface.blit(
                engine.default_font.render(
                    "FPS: %.2f" % (engine.clock.get_fps()), 0, (color)),
                (10, 10)
            )
        return closure

    caption = 'Hello, World'
    def caption_fun(s):
        def closure(engine, *args):
            result = s + ' [' + args[0] + ': ' + args[1] + ']'
            engine.set_caption(result)

        return closure

    def caption_idle_fun(s):
        def closure(engine, *args):
            engine.set_caption(s)
        return closure
    
    engine = Engine()
    engine.set_caption(caption)
    engine.on('render', render_fun())
    engine.on('key_down', caption_fun(caption))
    engine.on('no_keys_down', caption_idle_fun(caption))
    engine.start()
