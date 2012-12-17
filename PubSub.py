class PubSub(object):
    def __init__(self):
        self.handlers = {}

    def on(self, event, fun):
        if not event in self.handlers:
            self.handlers[event] = []

        self.handlers[event].append(fun)

    def emit(self, event, args=[]):
        if event in self.handlers:
            for fun in self.handlers[event]:
                fun(self, event, args)
