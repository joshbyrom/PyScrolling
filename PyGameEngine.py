import pygame

from PubSub import *

class Engine(PubSub):
    def __init__(self):
        PubSub.__init__(self)

    def init(self):
        if not hasattr(self, 'initialized'):
            self._init_pygame()
        
            self.init_font()
            self._init_clock()
            self.init_flow_controls()

            self.initialized = True
            self.emit('init')

    def init_flow_controls(self, value=False):
        self.active = value
        self.paused = value

    def _init_pygame(self, size=[854,480]):
        pygame.init()
        self.screen = pygame.display.set_mode(size)

    def init_font(self, fontsize=35):
        if not hasattr(self, 'fontsize'):
            self.fontsize = 0
            
        if not self.fontsize == fontsize:
            self.fontsize = fontsize
            self.default_font = pygame.font.SysFont("None", self.fontsize)
            self.emit('font_changed')

    def _init_clock(self, fps=30):
        self.fps = fps
        self.frame_count = 0

        self.clock = pygame.time.Clock()
        
    def set_caption(self, string):
        self.init()
        pygame.display.set_caption(string)

    def toggle_pause(self):
        self.set_paused(not self.paused)

    def set_paused(self, boolean):
        self.init()
        if not self.paused == boolean:
            self.paused = boolean
            self.emit('pause', [self.paused])

    def stop(self):
        self.init()
        
        if self.active:
            self.active = False
            self.emit('stopped')

    def start(self, start_paused = False):
        self.init()
        
        if not self.active:
            self.active = True
            self.paused = start_paused
            
            self.emit('started')
            self._loop()
            self._handle_stop()

    def _loop(self):
        elapsed = 0
        while self.active:
            if not self.paused:
                self._tick(elapsed)
            self._render()
            self._handle_pygame_events()
            elapsed = self.clock.tick(self.fps)

    def _tick(self, elapsed):
        self.emit('tick', elapsed)

    def _render(self):
        self.emit('render', self.screen)
        pygame.display.update()

    def _handle_stop(self):
        pygame.quit()

    def _handle_pygame_events(self):
        any_key_down = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                any_key_down = True
                if event.key == pygame.K_ESCAPE:
                    self.stop()
                else:
                    name = pygame.key.name(event.key)
                    self.emit('key_down', name)

                    # or you can listen for specific keys
                    self.emit(''.join([name, '_down']))

        if not any_key_down:
            self.emit('no_keys_down')
        
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
