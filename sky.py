from pyglet.gl import *


class Sky(object):
    # self, x, y, z, x_size, y_size, texture, texture_scale=1.0
    def __init__(self, terrian, texture, texture_scale=1.0):
        self.size = 30

        # x, y = terrian.convert_xy_to_location(shape_x, shape_y)

        self.x_skew = terrian.xyz[0]
        self.y_skew = terrian.xyz[1] + 11.0
        self.z_skew = terrian.xyz[2]

        self.texture = texture
        self.texture_scale = texture_scale

    def update(self, delta_time):
        pass

    def draw(self):
        glPushMatrix()
        self._draw_one(-self.size, True)
        self._draw_one(self.size, True)
        self._draw_one(self.size, False)
        self._draw_one(-self.size, False)
        glPopMatrix()
        # self._draw_one(self.size, self.size, True)

    def _draw_one(self, d, turn):
        # type: (float, float, bool) -> None
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)

        glRotatef(-90.0, 1.0, 0.0, 0.0)
        if turn:
            glRotatef(-90.0, 0.0, 0.0, 1.0)

        glTranslatef(self.x_skew, self.z_skew + d, self.y_skew)

        glColor3f(1.0, 1.0, 1.0)
        glBindTexture(self.texture.target, self.texture.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)

        glBegin(GL_TRIANGLES)

        # 1
        # |\
        # 2-3

        glTexCoord2f(0.0, self.texture_scale)
        glVertex3f(-self.size, 0.0, self.size)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(-self.size, 0.0, -self.size)

        glTexCoord2f(self.texture_scale, 0.0)
        glVertex3f(self.size, 0.0, -self.size)

        glEnd()

        glBegin(GL_TRIANGLES)

        # 1-2
        #  \|
        #   3

        glTexCoord2f(0.0, self.texture_scale)
        glVertex3f(-self.size, 0.0, self.size)

        glTexCoord2f(self.texture_scale, self.texture_scale)
        glVertex3f(self.size, 0.0, self.size, )

        glTexCoord2f(self.texture_scale, 0.0)
        glVertex3f(self.size, 0.0, -self.size, )

        glEnd()
        glDisable(GL_TEXTURE_2D)

        glPopMatrix()
