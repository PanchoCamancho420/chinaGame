import sprite
import math
import random
from pyglet.gl import *


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
    def __init__(self, window, shape, random_xy=False, color=(0.0, 0.7, 0.0), scale=.1, max_velocity=5.0, xy=(0, 0)):
        if random_xy:
            distance = 11.0  # should be 11
            self.angle = random.uniform(0, 360)
            x_leg = math.sin(math.radians(self.angle)) * distance
            y_leg = math.cos(math.radians(self.angle)) * distance
            real_xy = x_leg, y_leg
        else:
            real_xy = xy
            self.angle = 0

        sprite.Sprite.__init__(self, window=window, shape=shape, color=color,
                               scale=scale, max_velocity=max_velocity, xy=real_xy)

        self.attack_speed = 0.5
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
                self.xy[0] -= delta_time * math.sin(math.radians(self.angle)) * self.attack_speed
                self.xy[1] -= delta_time * math.cos(math.radians(self.angle)) * self.attack_speed

        else:
            self.xy[0] = self.beach_x
            self.xy[1] = self.beach_z

    def draw(self):
        x, y, z = self.get_center()
        glPushMatrix()

        glTranslatef(x, z, y)

        glRotatef(self.angle + 90.0, 0.0, 1.0, 0.0)

        glColor3f(*self.color)

        proportion_big = 3.0
        proportion_small = 2.0
        proportion_medium = 2.5
        proportion_extreme = 4.0

        glBegin(GL_POLYGON)  # side right

        glVertex3f(-self.scale * proportion_big, self.scale, -self.scale * proportion_small)
        glVertex3f(-self.scale * proportion_big, -self.scale, -self.scale)
        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale * proportion_big, self.scale, -self.scale * proportion_small)  # point

        glEnd()

        glBegin(GL_POLYGON)  # side left

        glVertex3f(-self.scale * proportion_big, self.scale, self.scale * proportion_small)
        glVertex3f(-self.scale * proportion_big, -self.scale, self.scale)
        glVertex3f(self.scale, -self.scale, self.scale)
        glVertex3f(self.scale * proportion_big, self.scale, self.scale * proportion_small)  # point

        glEnd()

        # glColor3f(1.0, 1.0, 1.0)

        # glBegin(GL_POLYGON)  # center

        # glVertex3f(-self.scale * proportion_big, self.scale, 0.0)
        # glVertex3f(-self.scale * proportion_big, -self.scale, 0.0)
        # glVertex3f(self.scale * proportion_medium, -self.scale, 0.0)
        # glVertex3f(self.scale * proportion_extreme, self.scale, 0.0)  # point

        # glEnd()

        # glColor3f(1.0, 0.0, 0.0)

        glBegin(GL_TRIANGLES)  # lower front side right lower

        glVertex3f(self.scale * proportion_big, self.scale, self.scale * proportion_small)
        glVertex3f(self.scale * proportion_medium, -self.scale, 0.0)
        glVertex3f(self.scale, -self.scale, self.scale)

        glEnd()

        # glColor3f(0.5, 0.5, 1.0)

        glBegin(GL_TRIANGLES)  # lower front side right lower

        glVertex3f(self.scale * proportion_extreme, self.scale, 0.0)
        glVertex3f(self.scale * proportion_big, self.scale, self.scale * proportion_small)
        glVertex3f(self.scale * proportion_medium, -self.scale, 0.0)

        glEnd()

        # glColor3f(1.0, 0.0, 0.0)

        glBegin(GL_TRIANGLES)  # lower front side left lower

        glVertex3f(self.scale * proportion_big, self.scale, -self.scale * proportion_small)
        glVertex3f(self.scale * proportion_medium, -self.scale, 0.0)
        glVertex3f(self.scale, -self.scale, -self.scale)

        glEnd()

        # glColor3f(0.5, 0.5, 1.0)

        glBegin(GL_TRIANGLES)  # lower front side left lower

        glVertex3f(self.scale * proportion_extreme, self.scale, 0.0)
        glVertex3f(self.scale * proportion_big, self.scale, -self.scale * proportion_small)
        glVertex3f(self.scale * proportion_medium, -self.scale, 0.0)

        glEnd()

        # glColor3f(0.0, 0.0, 0.0)

        glBegin(GL_POLYGON)  # back

        glVertex3f(-self.scale * proportion_big, self.scale, -self.scale * proportion_small)
        glVertex3f(-self.scale * proportion_big, -self.scale, -self.scale)

        glVertex3f(-self.scale * proportion_big, -self.scale, self.scale)
        glVertex3f(-self.scale * proportion_big, self.scale, self.scale * proportion_small)

        glEnd()

        glBegin(GL_POLYGON)  # top

        glVertex3f(self.scale * proportion_extreme, self.scale, 0.0)  # point
        glVertex3f(self.scale * proportion_big, self.scale, -self.scale * proportion_small)
        glVertex3f(-self.scale * proportion_big, self.scale, -self.scale * proportion_small)
        glVertex3f(-self.scale * proportion_big, self.scale, self.scale * proportion_small)
        glVertex3f(self.scale * proportion_big, self.scale, self.scale * proportion_small)

        glEnd()

        glPopMatrix()
