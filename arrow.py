from pyglet.gl import *
import math


class Arrow(object):
    def __init__(self):
        self.scale = 0.25
        self.x_loc = 0.0
        self.y_loc = 0.0
        self.z_loc = 0.0

        self.direction = 0.0
        self.angle = 0.0

        self.direction_getter = None
        self.is_pointing = False

    def calc_direction(self):
        center = self.direction_getter.get_center()
        x_diff = center[0] - self.x_loc
        z_diff = center[1] - self.z_loc

        if z_diff == 0:
            z_diff = .0001
        direction = math.degrees(math.atan(x_diff / z_diff))
        if z_diff > 0:
            direction += 180.0
        self.direction = direction

        xz_diff = (((center[0] - self.x_loc) ** 2) + ((center[1] - self.z_loc) ** 2)) ** .5  # euler distance easy
        y_diff = center[2] - self.y_loc

        if y_diff == 0:
            y_diff = .0001
        if xz_diff == 0:
            xz_diff = .0001
        angle = math.degrees(math.atan(y_diff / xz_diff))
        # if y_diff > 0:
        #     angle += 180.0
        self.angle = angle

    def update(self, delta_time):
        del delta_time
        # self.direction += 1.0 * delta_time
        # self.angle += 1.0 * delta_time
        if self.is_pointing:
            self.calc_direction()
        # self.z_loc += 0.1 * delta_time
        # self.x_loc += .5 * delta_time

    def point_at(self, direction):
        self.direction_getter = direction
        self.is_pointing = True

    def cancel_pointing(self):
        self.direction_getter = None
        self.is_pointing = False

    def draw(self):
        glPushMatrix()

        glTranslatef(self.x_loc, self.y_loc, self.z_loc)

        glRotatef(self.direction, 0.0, 1.0, 0.0)
        glRotatef(self.angle, 1.0, 0.0, 0.0)

        # glTranslatef(self.x_loc, self.y_loc, self.z_loc)

        glColor3f(0.7, 0.3, 0.3)
        # wierd color z
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

        # blue anti y
        glColor3f(0.3, 1.0, 0.3)
        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        glPopMatrix()
