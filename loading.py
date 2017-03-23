from pyglet.gl import *
import random


random_fact_list = [
    
]


class Fact(object):
    def __init__(self, window):
        self.window = window
        fact_str = self.get_random_fact_str()
        self.fact = pyglet.text.Label(fact_str, font_name='Arial', font_size=40,
                                      x=window.width * .25, y=window.height - 10, anchor_x='left', anchor_y='top',
                                      color=(0, 0, 0, 255))
        self.message = pyglet.text.Label('Loading...', font_name='Arial', font_size=20,
                                         x=window.width * .25, y=50, anchor_x='left', anchor_y='bottom',
                                         color=(0, 0, 0, 255))
        self.load_bar = pyglet.text.Label('', font_name='Arial', font_size=20,
                                          x=window.width * .25, y=20, anchor_x='left', anchor_y='bottom',
                                          color=(0, 0, 0, 255))

    @staticmethod
    def get_random_fact_str():
        random_str = 'not so random ' + str(random.randrange(1000, 9999))
        return random_str

    def update(self, delta_time):
        del delta_time
        print self.fact.text
        self.load_bar.text = '#' * int(40 - (self.window.laoding_time * 8))
        print self.fact.text

    def draw(self):
        self.fact.draw()
        self.message.draw()
        self.load_bar.draw()
