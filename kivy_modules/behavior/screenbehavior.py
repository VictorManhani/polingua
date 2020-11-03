
# OLD TODO
def transition_manager(self, **kwargs):
    screen = kwargs.get('screen', 'home')
    direction = kwargs.get('direction', "left") # left, right, up, down
    mode = kwargs.get('mode', "pop") #push, pop
    func = kwargs.get('func', None)
    args = kwargs.get('args', ())

    transition = kwargs.get('transition', 'NoTransition')
    self.root.transition = globals()[transition]()

    if transition == 'SlideTransition':
        self.root.transition.direction = direction
    elif transition == 'CardTransition':
        self.root.transition.direction = direction
        self.root.transition.mode = mode

    self.root.current = screen
    if func:
        getattr(self.root.get_screen(screen), func)(*args)