from pyglet.gl import *


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
