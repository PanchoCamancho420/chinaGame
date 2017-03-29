from pyglet.gl import *
import inputHandler
import math


class Sprite(object):

    def __init__(self, window, shape, color=(0.0, 1.0, 0.0), scale=.1, max_velocity=5.0, xy=(0, 0)):
        self.xy = list(xy)
        self.x_velocity = 0.0
        self.y_velocity = 0.0
        self.acceleration = 1.0
        self.max_velocity = max_velocity
        self.shape = shape

        self.scale = scale
        self.color = color
        self.hp = 100

        self.input_handler = inputHandler.InputHandler()
        window.push_handlers(self.input_handler)

        self.keyboard_control = True

        self.last_pressed = 10000.0

    def push_x(self, amount):
        new_amount = amount

        # check if its being slowed down
        if (not ((self.x_velocity >= 0) is (new_amount >= 0))) and not self.x_velocity == 0:
            self.x_velocity = 0.0
        else:
            self.x_velocity += new_amount

        # check if its going to fast
        if math.fabs(self.x_velocity) > self.max_velocity:
            self.x_velocity = self.max_velocity

    def push_y(self, amount):
        new_amount = amount

        # check if its being slowed down
        if (not ((self.y_velocity >= 0) is (new_amount >= 0))) and not self.y_velocity == 0:
            self.y_velocity = 0.0
        else:
            self.y_velocity += new_amount

        # check if its going to fast
        if math.fabs(self.y_velocity) > self.max_velocity:
            self.y_velocity = self.max_velocity

    def slow(self, friction, delta_time):
        self.x_velocity = self._slow_val(self.x_velocity, friction, delta_time)
        self.y_velocity = self._slow_val(self.y_velocity, friction, delta_time)

    @staticmethod
    def _slow_val(speed, friction, delta_time):
        if speed > friction * delta_time:
            new_speed = speed - (friction * delta_time)
        elif speed < -friction * delta_time:
            new_speed = speed + (friction * delta_time)
        else:
            new_speed = 0
        return new_speed

    def attack(self, damage):
        self.hp -= damage

    def heal(self, healing):
        if self.hp > 0:
            self.hp += healing

    def get_hp(self):
        return self.hp

    def clean(self):
        return self.hp <= 0  # if the building has got no hp, git rid of it

    def update(self, delta_time):
        self.xy[0] += delta_time * self.x_velocity
        self.xy[1] += delta_time * self.y_velocity

        if self.keyboard_control is True:
            keymap = {
                'forward': pyglet.window.key.W,
                'backward': pyglet.window.key.S,
                'left': pyglet.window.key.A,
                'right': pyglet.window.key.D,
                'up': pyglet.window.key.SPACE,
                'down': pyglet.window.key.LSHIFT
            }

            if self.input_handler.get_pressed()[keymap['forward']]:
                self.push_x(delta_time * self.acceleration)

            if self.input_handler.get_pressed()[keymap['backward']]:
                self.push_x(-delta_time * self.acceleration)

            if self.input_handler.get_pressed()[keymap['left']]:
                self.push_y(-delta_time * self.acceleration)

            if self.input_handler.get_pressed()[keymap['right']]:
                self.push_y(delta_time * self.acceleration)

            if self.input_handler.get_pressed()[keymap['down']]:
                self.x_velocity = 0.0
                self.y_velocity = 0.0
                self.xy = [0.0, 0.0]

        if all(value is False for value in self.input_handler.get_pressed().values()):
            self.last_pressed += delta_time
        else:
            self.last_pressed = 0.0

        if self.last_pressed >= .25:
            self.slow(2.0, delta_time)

    def set_control(self, mouse, key_board):
        del mouse
        self.keyboard_control = key_board
        # do this because never want mouse control
        return False, key_board

    def get_center(self):
        return self.shape.get_xyz(self.xy[0], self.xy[1])

    def draw(self):
        x, y, z = self.get_center()
        glPushMatrix()
        
        glTranslatef(x, z, y)
        glColor3f(*self.color)

        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, self.scale)
        glVertex3f(self.scale, self.scale, self.scale)
        glVertex3f(-self.scale, self.scale, self.scale)
        glVertex3f(-self.scale, -self.scale, self.scale)

        glEnd()

        # Purple
        glBegin(GL_POLYGON)

        glVertex3f(2 * self.scale, -self.scale, -self.scale)
        glVertex3f(2 * self.scale, self.scale, -self.scale)
        glVertex3f(2 * self.scale, self.scale, self.scale)
        glVertex3f(2 * self.scale, -self.scale, self.scale)

        glEnd()

        # Green
        glBegin(GL_POLYGON)

        glVertex3f(2 * -self.scale, -self.scale, self.scale)
        glVertex3f(2 * -self.scale, self.scale, self.scale)
        glVertex3f(2 * -self.scale, self.scale, -self.scale)
        glVertex3f(2 * -self.scale, -self.scale, -self.scale)

        glEnd()

        # Blue
        glBegin(GL_POLYGON)

        glVertex3f(2 * self.scale, self.scale, self.scale)
        glVertex3f(2 * self.scale, self.scale, -self.scale)
        glVertex3f(2 * -self.scale, self.scale, -self.scale)
        glVertex3f(2 * -self.scale, self.scale, self.scale)

        glEnd()

        # Red
        glBegin(GL_POLYGON)

        glVertex3f(2 * self.scale, -self.scale, -self.scale)
        glVertex3f(2 * self.scale, -self.scale, self.scale)
        glVertex3f(2 * -self.scale, -self.scale, self.scale)
        glVertex3f(2 * -self.scale, -self.scale, -self.scale)

        glEnd()

        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        glPopMatrix()
