from opensimplex import OpenSimplex
import random
import numpy as np


class _NoiseGetter(object):
    def __init__(self, sample_rate, inverse_weight, seed):
        self.sample_rate = sample_rate
        self.noise = OpenSimplex(seed)
        self.inverse_weight = inverse_weight

    '''spikey value in range -1 to 1'''
    def get_fractal_value(self, x, y):
        sample_x = float(x) / self.sample_rate
        sample_y = float(y) / self.sample_rate
        val = self.noise.noise2d(sample_x, sample_y)
        new_val = ((-(np.abs(val))) + .5) * 2  # basically abs and then some math to get it facing up
        weighted_val = new_val / self.inverse_weight
        return weighted_val

    '''spikey value in range 0 to 1'''
    def get_height(self, x, y):
        sample_x = float(x) / self.sample_rate
        sample_y = float(y) / self.sample_rate
        val = self.noise.noise2d(sample_x, sample_y)
        new_val = -np.abs(val) + 1.0  # basically abs, invert and push up
        weighted_val = new_val * self.inverse_weight
        return weighted_val

    '''return simple value between 0 and 1, un-waited'''

    def get_simple_height(self, x, y):
        sample_x = float(x) / self.sample_rate
        sample_y = float(y) / self.sample_rate
        val = self.noise.noise2d(sample_x, sample_y)
        new_val = -np.abs(val) + 1.0  # basically abs, invert and push up
        return new_val

    '''returns weight'''
    def get_weight(self):
        return self.inverse_weight


class TerrainShape2(object):
    def __init__(self, seed=None, island_location=(0.0, 0.0), size=1.0, height=5.0):

        if seed is None:
            self.seed = random.randrange(0, 10000)
        else:
            self.seed = seed
        r = random.Random()
        r.seed(seed)

        self.getters = []
        self.getters.append(_NoiseGetter(256, 1, r.randrange(0, 10000)))
        self.getters.append(_NoiseGetter(24, 4, r.randrange(0, 10000)))
        self.getters.append(_NoiseGetter(10, 8, r.randrange(0, 10000)))
        self.getters.append(_NoiseGetter(6, 16, r.randrange(0, 10000)))

        self.island_x = island_location[0]
        self.island_y = island_location[1]
        self.island_height = height
        self.island_size = size

        self._plateau_accuracy = 10

    '''weight value based on a distance'''
    @staticmethod
    def _plateau(d, accuracy):
        if d >= 50:
            return 0
        return (-(d ** 2) + accuracy) / (2 ** (d ** 2))

    '''Euler distance between two points, scale changes so that n scale equals one'''
    @staticmethod
    def _distance(x_1, y_1, x_2, y_2, scale=1):
        x_dis = ((float(x_1) / scale) - (float(x_2) / scale)) ** 2
        y_dis = ((float(y_1) / scale) - (float(y_2) / scale)) ** 2
        dis = (x_dis + y_dis) ** .5
        return dis

    '''Returns the height of the terrain at that point'''
    def get_height(self, x, y):
        fractal_sum = 0
        weight_sum = 0
        for getter in self.getters:
            fractal_sum += getter.get_height(x, y)
            weight_sum += getter.get_weight()
        weighted_average = fractal_sum / weight_sum

        distance = self._distance(x, y, self.island_x, self.island_y)

        plat_o_d = self._plateau(distance * (1.0 / self.island_size), self._plateau_accuracy)\
            * self.island_height / self._plateau_accuracy

        transformed_plat = plat_o_d * 5

        weighted_value = transformed_plat * weighted_average
        # print transformed_sum, transformed_plat, weighted_value
        return weighted_value
