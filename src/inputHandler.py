import collections


class Bumped(object):
    def __init__(self, key):
        self.__key = key
        self.__is_bumped = False
        self.__is_un_released = False

    def is_key(self, key):
        return self.__key == key

    def release(self):
        self.__is_un_released = False

    def press(self):
        if not self.__is_un_released:
            self.__is_bumped = True
        self.__is_un_released = True

    def get_bumped(self):
        store = self.__is_bumped
        self.__is_bumped = False
        return store


class InputHandler(object):
    def __init__(self):
        self.__pressed = collections.defaultdict(bool)
        self.__dx = 0
        self.__dy = 0
        self.bumpers = []

    def on_key_press(self, symbol, modifiers):
        del modifiers
        self.__pressed[symbol] = True
        for bumper in self.bumpers:
            if bumper.is_key(symbol):
                bumper.press()

    def on_key_release(self, symbol, modifiers):
        del modifiers
        self.__pressed[symbol] = False
        for bumper in self.bumpers:
            if bumper.is_key(symbol):
                bumper.release()

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

    def add_bumped(self, key):
        bumper = Bumped(key)
        self.bumpers.append(bumper)
        return bumper
