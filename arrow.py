from pyglet.gl import *
import math


class Arrow(object):
    def __init__(self, location=(0.0, 0.0, 0.0), color=(0.0, 0.0, 0.0), scale=.25):
        self.__scale = scale
        self.__x_loc = location[0]
        self.__y_loc = location[1]
        self.__z_loc = location[2]

        self.color = color

        self.__direction = 0.0
        self.__angle = 0.0

        self.__direction_getter = None
        self.__is_pointing = False

    def __point_void(self):
        center = self.__direction_getter.get_center()
        x_diff = center[0] - self.__x_loc
        z_diff = center[1] - self.__z_loc

        if z_diff == 0:
            z_diff = .0001
        direction = math.degrees(math.atan(x_diff / z_diff))
        if z_diff > 0:
            direction += 180.0
        self.__direction = direction

        xz_diff = (((center[0] - self.__x_loc) ** 2) + ((center[1] - self.__z_loc) ** 2)) ** .5  # euler distance easy
        y_diff = center[2] - self.__y_loc

        if y_diff == 0:
            y_diff = .0001
        if xz_diff == 0:
            xz_diff = .0001
        angle = math.degrees(math.atan(y_diff / xz_diff))
        # if y_diff > 0:
        #     angle += 180.0
        self.__angle = angle

    def update(self, delta_time):
        del delta_time
        # self.direction += 1.0 * delta_time
        # self.angle += 1.0 * delta_time
        if self.__is_pointing:
            self.__point_void()
        # self.z_loc += 0.1 * delta_time
        # self.x_loc += .5 * delta_time

    def point_at(self, direction):
        self.__direction_getter = direction
        self.__is_pointing = True

    def cancel_pointing(self):
        self.__direction_getter = None
        self.__is_pointing = False

    def set_xyz(self, x, y, z):
        self.__x_loc = x
        self.__y_loc = y
        self.__z_loc = z

    def draw(self):
        glPushMatrix()

        glTranslatef(self.__x_loc, self.__y_loc, self.__z_loc)

        glRotatef(self.__direction, 0.0, 1.0, 0.0)
        glRotatef(self.__angle, 1.0, 0.0, 0.0)

        # draws cube don't really want that
        if False:
            glColor3f(0.7, 0.3, 0.3)
            # wierd color z
            glBegin(GL_POLYGON)

            glVertex3f(self.__scale, -self.__scale, self.__scale)
            glVertex3f(self.__scale, self.__scale, self.__scale)
            glVertex3f(-self.__scale, self.__scale, self.__scale)
            glVertex3f(-self.__scale, -self.__scale, self.__scale)

            glEnd()

            # Purple
            # x
            glColor3f(1.0, .3, 1.0)
            glBegin(GL_POLYGON)

            glVertex3f(self.__scale, -self.__scale, -self.__scale)
            glVertex3f(self.__scale, self.__scale, -self.__scale)
            glVertex3f(self.__scale, self.__scale, self.__scale)
            glVertex3f(self.__scale, -self.__scale, self.__scale)

            glEnd()

            # Blue
            # anti x
            glColor3f(0.3, 0.3, 1.0)
            glBegin(GL_POLYGON)

            glVertex3f(-self.__scale, -self.__scale, self.__scale)
            glVertex3f(-self.__scale, self.__scale, self.__scale)
            glVertex3f(-self.__scale, self.__scale, -self.__scale)
            glVertex3f(-self.__scale, -self.__scale, -self.__scale)

            glEnd()

            # white
            # top
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_POLYGON)

            glVertex3f(self.__scale, self.__scale, self.__scale)
            glVertex3f(self.__scale, self.__scale, -self.__scale)
            glVertex3f(-self.__scale, self.__scale, -self.__scale)
            glVertex3f(-self.__scale, self.__scale, self.__scale)

            glEnd()

            # bottom
            # black
            glColor3f(0.0, 0.0, 0.0)
            glBegin(GL_POLYGON)

            glVertex3f(self.__scale, -self.__scale, -self.__scale)
            glVertex3f(self.__scale, -self.__scale, self.__scale)
            glVertex3f(-self.__scale, -self.__scale, self.__scale)
            glVertex3f(-self.__scale, -self.__scale, -self.__scale)

            glEnd()

            # green anti y
            glColor3f(0.3, 1.0, 0.3)
            glBegin(GL_POLYGON)

            glVertex3f(self.__scale, -self.__scale, -self.__scale)
            glVertex3f(self.__scale, self.__scale, -self.__scale)
            glVertex3f(-self.__scale, self.__scale, -self.__scale)
            glVertex3f(-self.__scale, -self.__scale, -self.__scale)

            glEnd()

        pointed_ness = 2.5

        glColor3f(*self.color)
        glBegin(GL_TRIANGLES)

        glVertex3f(0.0, self.__scale / pointed_ness, self.__scale)
        glVertex3f(0.0, 0.0, -self.__scale)  # point
        glVertex3f(0.0, -self.__scale / pointed_ness, self.__scale)

        glVertex3f(self.__scale / pointed_ness, 0.0, self.__scale)
        glVertex3f(0.0, 0.0, -self.__scale)  # point
        glVertex3f(-self.__scale / pointed_ness, 0.0, self.__scale)

        glEnd()

        glPopMatrix()
