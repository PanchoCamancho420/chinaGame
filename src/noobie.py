import terrain
import main
from pyglet.gl import *
import sprite
import math


class Noob(sprite.Sprite):
    def __init__(self, window, shape, pointer_pointer, color=(0.0, 1.0, 0.0),
                 scale=.05, max_velocity=5.0, xy=(0.0, 0.0)):
        # type: (main.window, terrain.Terrain, list, tuple(float), float, float, [float]) -> None
        sprite.Sprite.__init__(self, window, shape, color=color, scale=scale, max_velocity=max_velocity, xy=xy)
        self.pointer_pointer = pointer_pointer
        self.punch_distance = 0.25
        self.attack_speed = 1.0
        self.rotate_speed = 20.0
        self.punch_damage = 10

    def set_control(self, mouse, key_board):
        del mouse
        del key_board
        return False, False  # never want control

    def get_target(self):  # returns the closest
        self_center = self.get_center()

        def get_distance(pot_sprite):
            sprite_center = pot_sprite.get_center()
            x_diff = self_center[0] - sprite_center[0]
            z_diff = self_center[2] - sprite_center[2]
            direct_distance = ((x_diff ** 2) + (z_diff ** 2)) ** 0.5
            return direct_distance

        min_distance_index = 0
        min_distance = get_distance(self.pointer_pointer[min_distance_index])
        for i in range(len(self.pointer_pointer)):
            distance = get_distance(self.pointer_pointer[i])
            if distance <= min_distance:
                min_distance_index = i
                min_distance = distance

        return self.pointer_pointer[min_distance_index]

    def update(self, delta_time):
        target = self.get_target()
        target_center = target.get_center()
        self_center = self.get_center()

        x_diff = target_center[0] - self_center[0]
        if x_diff == 0.0:
            x_diff = 0.001
        z_diff = target_center[2] - self_center[1]
        if z_diff == 0.0:
            z_diff = 0.001

        angle = math.degrees(math.atan(x_diff / z_diff))
        if x_diff >= 0:
            angle += 180.0

        print 'angle', angle

        self.xy[0] -= delta_time * math.cos(math.radians(angle)) * self.attack_speed
        self.xy[1] -= delta_time * math.sin(math.radians(angle)) * self.attack_speed

        sprite_center = target.get_center()
        x_diff = self_center[0] - sprite_center[0]
        z_diff = self_center[2] - sprite_center[2]
        direct_distance = ((x_diff ** 2) + (z_diff ** 2)) ** 0.5

        if direct_distance <= self.punch_distance:
            target.attack(self.punch_damage)
            print 'i punched'

        # if in_range:
        #     target.attack(self.punch_damage)

        print
        print
        print

    def draw(self):
        x, y, z = self.get_center()
        glPushMatrix()

        glTranslatef(x, z, y)
        glColor3f(0.7, 0.3, 0.3)
        # weird color z
        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, self.scale)
        glVertex3f(self.scale, self.scale, self.scale)
        glVertex3f(-self.scale, self.scale, self.scale)
        glVertex3f(-self.scale, -self.scale, self.scale)

        glEnd()

        # Purple
        # x
        glColor3f(1.0, .3, 1.0)
        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale, self.scale, -self.scale)
        glVertex3f(self.scale, self.scale, self.scale)
        glVertex3f(self.scale, -self.scale, self.scale)

        glEnd()

        # Blue
        # anti x
        glColor3f(0.3, 0.3, 1.0)
        glBegin(GL_POLYGON)

        glVertex3f(-self.scale, -self.scale, self.scale)
        glVertex3f(-self.scale, self.scale, self.scale)
        glVertex3f(-self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        # white
        # top
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_POLYGON)

        glVertex3f(self.scale, self.scale, self.scale)
        glVertex3f(self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, self.scale, self.scale)

        glEnd()

        # bottom
        # black
        glColor3f(0.0, 0.0, 0.0)
        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale, -self.scale, self.scale)
        glVertex3f(-self.scale, -self.scale, self.scale)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        # green anti y
        glColor3f(0.3, 1.0, 0.3)
        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        glPopMatrix()
