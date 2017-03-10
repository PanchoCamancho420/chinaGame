from pyglet.gl import *


class Building(object):
    def __init__(self, x, y, scale):
        self.x = x
        self.y = y
        self.scale = scale

    def draw_xyz(self, x, y, z):
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

        # Red
        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale, -self.scale, self.scale)
        glVertex3f(-self.scale, -self.scale, self.scale)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        glPopMatrix()
