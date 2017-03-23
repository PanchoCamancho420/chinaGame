from pyglet.gl import *
import random


class Fact(object):
    def __init__(self, window):
        self.base_fact_str = self.get_random_fact_str()
        self.label = pyglet.text.Label('fun fact', font_name='Arial', font_size=40,
                                       x=window.width * .25, y=window.height - 10, anchor_x='left', anchor_y='top',
                                       color=(0, 0, 0, 255))

    @staticmethod
    def get_random_fact_str():
        random_str = 'not so random' + str(random.randrange(0, 1000))
        return random_str

    def update(self, delta_time):
        pass

    def draw(self):
        self.label.draw()
