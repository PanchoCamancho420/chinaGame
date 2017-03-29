from pyglet.gl import *
import random
import sys


random_fact_list = [
    'China was the first country to have vending machines',

    # 'China is the largest country by population',

    'As Nikola Tesla said:/'
    ' "coming back from China to America was like taking a time machine to 50 year older technology"',

    # 'The Chinese government owns the near side of the moon and helps all the other weak'
    # ' countries refuel their space ships',

    # '99.9% of the world economy is controlled by china',

    'Velcro, zippers, buttons and the belt buckle where all invented by a Chinese librarian',

    # 'On average China builds 2.6 new skyscrapers per day',

    # 'Only 0.23% of Chinese citizens are illiterate',

    # 'In every olympic event that China participated in for the last 30 years China earned either a gold or silver',

    'The Chinese Sunway TaihuLight super computer is more powerful than every computer in North America combined',

    # 'the Chinese Planet Colonization Mission (CEPCM) will have over 10 billion citizens within the next year',

    'The chinese government is extremely crafty, ounce they even made a thing called:/'
    '"Global Warming" just to make america fall further behind economically/'
    'they even made fake smog to make it seem like they where cleaning the air in China'
]

long_string_test_list = ['111111111111111111111111111111111111111111111111111111111111111111111111'
                         '222222222222222222222222222222222222222222222222222222222222222222222222'
                         '333333333333333333333333333333333333333333333333333333333333333333333333']


class Fact(object):
    def __init__(self, window):
        self.window = window
        self.fact_str = self.format_str(self.get_random_fact_str())

        self.message = pyglet.text.Label('Loading...', font_name='Arial', font_size=10,
                                         x=window.width * .25, y=30, anchor_x='left', anchor_y='bottom',
                                         color=(0, 0, 0, 255))
        self.load_bar = pyglet.text.Label('', font_name='Arial', font_size=10,
                                          x=window.width * .25, y=20, anchor_x='left', anchor_y='bottom',
                                          color=(0, 0, 0, 255))

    @staticmethod
    def get_random_fact_str():
        random_str = random.choice(random_fact_list)
        return random_str

    @staticmethod
    def clean():
        return False

    def update(self, delta_time):
        del delta_time
        float_complete = self.window.loading_time / self.window.loading_time_total
        total_tags = 50
        tags = int(total_tags * float_complete)
        self.load_bar.text = '#' * tags

    @staticmethod
    def format_str(string):
        # type: (str) -> str
        line_length = 45
        split = string.split('/')

        i = 0
        while i < len(split):
            if i >= 1000:
                print 'things got a little crazy during the fact drawing'
                sys.exit()
            if len(split[i]) > line_length:
                if ' ' in split[i][:line_length][::-1]:
                    index = split[i][:line_length][::-1].index(' ')

                    index = (len(split[i]) if (len(split[i]) < line_length) else line_length) - index
                else:
                    index = line_length

                new_line = '/' + split[i][index:]
                split[i] = ('' if ('/' in split[i][:index]) else '/') + split[i][:index]
                if len(new_line) > 0:
                    split.insert(i + 1, new_line)
            i += 1

        ret_str = ''
        for str_i in split:
            ret_str += str_i
        return ret_str

    def draw_fact(self):
        split = self.fact_str.split('/')
        for i in range(len(split)):
            line = pyglet.text.Label(split[i], font_name='Arial', font_size=30,
                                     x=10, y=self.window.height - 10 - (i * 30), anchor_x='left', anchor_y='top',
                                     color=(0, 0, 0, 255))
            line.draw()

    def draw(self):
        self.draw_fact()
        self.message.draw()
        self.load_bar.draw()
