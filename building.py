from pyglet.gl import *
import arrow


class Building(object):
    def __init__(self, shape, x, y, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.shape = shape
        self.x_loc, self.y_loc, self.z_loc = shape.get_xyz(self.x, self.y)

    def get_center(self):
        return self.x_loc, self.y_loc, self.y_loc

    def draw(self):
        self._draw_xyz(self.x_loc, self.z_loc, self.y_loc)

    def _draw_xyz(self, x, y, z):
        glPushMatrix()

        glTranslatef(x, y, z)
        glColor3f(0.3, 0.3, 0.3)

        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, self.scale)
        glVertex3f(self.scale, self.scale, self.scale)
        glVertex3f(-self.scale, self.scale, self.scale)
        glVertex3f(-self.scale, -self.scale, self.scale)

        glEnd()

        # Purple
        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale, self.scale, -self.scale)
        glVertex3f(self.scale, self.scale, self.scale)
        glVertex3f(self.scale, -self.scale, self.scale)

        glEnd()

        # Green
        glBegin(GL_POLYGON)

        glVertex3f(-self.scale, -self.scale, self.scale)
        glVertex3f(-self.scale, self.scale, self.scale)
        glVertex3f(-self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        # Blue
        glBegin(GL_POLYGON)

        glVertex3f(self.scale, self.scale, self.scale)
        glVertex3f(self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, self.scale, self.scale)

        glEnd()

        #bottom
        # Red
        # glBegin(GL_POLYGON)

        # glVertex3f(self.scale, -self.scale, -self.scale)
        # glVertex3f(self.scale, -self.scale, self.scale)
        # glVertex3f(-self.scale, -self.scale, self.scale)
        # glVertex3f(-self.scale, -self.scale, -self.scale)

        # glEnd()

        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        glPopMatrix()


class Turret(Building):
    def __init__(self, shape, x, y, scale, color=(0.3, 0.3, 0.3)):
        self.color = color
        Building.__init__(self, shape=shape, x=x, y=y, scale=scale)

        self.arrow = arrow.Arrow(location=(self.x_loc, self.y_loc+self.scale, self.z_loc), color=(1.0, 0.0, 0.0),
                                 scale=self.scale / 2)

    def point_at(self, direction):
        self.arrow.point_at(direction)

    def cancel_pointing(self):
        self.arrow.cancel_pointing()

    def update(self, delta_time):
        self.arrow.update(delta_time)

    def draw(self):
        self.arrow.draw()

        glPushMatrix()

        glTranslatef(self.x_loc, self.y_loc, self.z_loc)
        # print self.x_loc, self.y_loc, self.z_loc

        glColor3f(*self.color)

        glBegin(GL_POLYGON)

        h = 2.0

        glVertex3f(self.scale, -self.scale, self.scale)
        glVertex3f(self.scale / 2, self.scale / h, self.scale / 2)
        glVertex3f(-self.scale / 2, self.scale / h, self.scale / 2)
        glVertex3f(-self.scale, -self.scale, self.scale)

        glEnd()

        # Purple
        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(self.scale / 2, self.scale / h, self.scale / 2)
        glVertex3f(self.scale, -self.scale, self.scale)

        glEnd()

        # Green
        glBegin(GL_POLYGON)

        glVertex3f(-self.scale, -self.scale, self.scale)
        glVertex3f(-self.scale / 2, self.scale / h, self.scale / 2)
        glVertex3f(-self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        # Blue
        glBegin(GL_POLYGON)

        glVertex3f(self.scale / 2, self.scale / h, self.scale / 2)
        glVertex3f(self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(-self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(-self.scale / 2, self.scale / h, self.scale / 2)

        glEnd()

        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(-self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        glPopMatrix()
