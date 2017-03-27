import sprite
import math
import random


class Amphibian(sprite.Sprite):
    def __init__(self, *args, **kwargs):
        sprite.Sprite.__init__(self, *args, **kwargs)
        self.xy = [0.0, 0.0]

    def get_center(self):
        x, y, z = self.shape.get_xyz(self.xy[0], self.xy[1])
        if z <= 0.4:
            z = 0.4
        return x, y, z


class BeachAble(sprite.Sprite):
    def __init__(self, window, shape, random_xy=False, color=(0.0, 1.0, 0.0), scale=.1, max_velocity=5.0, xy=(0, 0)):
        if random_xy:
            distance = 2.0
            angle = random.uniform(0, 360)
            x_leg = math.cos(angle) * distance
            y_leg = math.sin(angle) * distance
            real_xy = x_leg, y_leg
        else:
            real_xy = xy

        sprite.Sprite.__init__(self, window=window, shape=shape, color=color,
                               scale=scale, max_velocity=max_velocity, xy=real_xy)
        self.is_beached = False
        self.beach_x = 0
        self.beach_z = 0

    def get_center(self):
        x, y, z = self.shape.get_xyz(self.xy[0], self.xy[1])
        if z <= 0.4:
            z = 0.4
        return x, y, z

    def update(self, delta_time):
        sprite.Sprite.update(self, delta_time)
        if not self.is_beached:
            center = self.get_center()
            if center[2] > 0.4:
                self.is_beached = True
                self.beach_x = center[0]
                self.beach_z = center[1]
        else:
            self.xy[0] = self.beach_x
            self.xy[1] = self.beach_z
