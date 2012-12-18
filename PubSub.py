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

if __name__ == '__main__':
    def print_fun(x):
        print x
        
    pb = PubSub()
    pb.on('test', lambda x, *args: print_fun('one'))
    pb.on('test', lambda x, *args: print_fun('two'))
    pb.on('test', lambda x, *args: print_fun('three'))


    [pb.emit('test') for x in range(20)]
