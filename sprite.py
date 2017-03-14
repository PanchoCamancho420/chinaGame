from pyglet.gl import *
import inputHandler


class Sprite(object):

    def __init__(self, window, shape, scale=.1, max_velocity=10, xy=(0, 0), xy_velocity=(0.0, 0.0)):
        self.xy = list(xy)
        self.xy_velocity = list(xy_velocity)
        self.acceleration = 1.0
        self.max_velocity = max_velocity
        self.shape = shape
        self.scale = scale

        self.input_handler = inputHandler.InputHandler()
        window.push_handlers(self.input_handler)

        self.keyboard_control = True

        self.last_pressed = 10000.0

    def give_gas(self, amount_xy):
        self.xy_velocity[0] += amount_xy[0]
        if self.xy_velocity[0] > self.max_velocity:
            self.xy_velocity = self.max_velocity
        self.xy_velocity[1] += amount_xy[1]
        if self.xy_velocity[1] > self.max_velocity:
            self.xy_velocity[1] = self.max_velocity

    def push_x(self, amount):
        self.xy_velocity[0] += amount
        if self.xy_velocity[0] > self.max_velocity:
            self.xy_velocity = self.max_velocity

    def push_y(self, amount):
        self.xy_velocity[1] += amount
        if self.xy_velocity[1] > self.max_velocity:
            self.xy_velocity[1] = self.max_velocity

    def slow(self, friction):
        if self.xy_velocity[0] > friction:
            self.xy_velocity[0] -= friction
        elif self.xy_velocity[0] < -friction:
            self.xy_velocity[0] += friction
        else:
            self.xy_velocity[0] = 0

        if self.xy_velocity[1] > friction:
            self.xy_velocity[1] -= friction
        elif self.xy_velocity[1] < -friction:
            self.xy_velocity[1] += friction
        else:
            self.xy_velocity[1] = 0

    def update(self, delta_time):
        self.xy[0] += delta_time * self.xy_velocity[0]
        self.xy[1] += delta_time * self.xy_velocity[1]

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

        if all(value is False for value in self.input_handler.get_pressed().values()):
            self.last_pressed += delta_time
        else:
            self.last_pressed = 0.0

        if self.last_pressed >= 1:
            self.slow(.1)

    def set_control(self, mouse, key_board):
        del mouse
        self.keyboard_control = key_board
        # do this because never want mouse control
        return False, key_board

    def draw(self):
        x, y, z = self.shape.get_xyz(self.xy[0], self.xy[1])
        glPushMatrix()
        glTranslatef(x, z, y)
        glColor3f(.7, 1.0, 0.7)

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
