import collections


class InputHandler(object):
    def __init__(self):
        self.__pressed = collections.defaultdict(bool)
        self.__dx = 0
        self.__dy = 0

    def on_key_press(self, symbol, modifiers):
        del modifiers
        self.__pressed[symbol] = True

    def on_key_release(self, symbol, modifiers):
        del modifiers
        self.__pressed[symbol] = False

    def on_mouse_motion(self, x, y, dx, dy):
        del x
        del y
        self.__dx = dx
        self.__dy = dy

    def get_pressed(self):
        return self.__pressed

    def get_dx(self):
        store = self.__dx
        self.__dx = 0.0
        return store

    def get_dy(self):
        store = self.__dy
        self.__dy = 0.0
        return store

    def reset_mouse(self):
        self.__dy = 0.0
        self.__dx = 0.0
