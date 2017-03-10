from pyglet.gl import *


class Water(object):
    # self, x, y, z, x_size, y_size, texture, texture_scale=1.0
    def __init__(self, terrian, texture, texture_scale=1.0):
        shape_x, shape_y = terrian.get_mat().shape

        x, y = terrian.convert_xy_to_location((shape_x, shape_y))

        self.x_skew = x
        self.y_skew = y
        self.z_skew = terrian.z_skew + (0.4 * terrian.scale)

        self.x_size = shape_x
        self.y_size = shape_y

        self.texture = texture
        self.texture_scale = texture_scale

    def update(self):
        pass

    def draw(self):
        glPushMatrix()

        glTranslatef(self.x_skew, self.z_skew, self.y_skew)

        glColor3f(1.0, 1.0, 1.0)
        glBindTexture(self.texture.target, self.texture.id)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)

        glBegin(GL_TRIANGLES)

        # 1
        # |\
        # 2-3

        glTexCoord2f(0.0, self.texture_scale)
        glVertex3f(-self.x_size, 0.0, self.y_size)

        glTexCoord2f(0.0, 0.0)
        glVertex3f(-self.x_size, 0.0, -self.y_size)

        glTexCoord2f(self.texture_scale, 0.0)
        glVertex3f(self.x_size, 0.0, -self.y_size)

        glEnd()

        glBegin(GL_TRIANGLES)

        # 1-2
        #  \|
        #   3

        glTexCoord2f(0.0, self.texture_scale)
        glVertex3f(-self.x_size, 0.0, self.y_size)

        glTexCoord2f(self.texture_scale, self.texture_scale)
        glVertex3f(self.x_size, 0.0, self.y_size,)

        glTexCoord2f(self.texture_scale, 0.0)
        glVertex3f(self.x_size, 0.0, -self.y_size,)

        glEnd()

        glPopMatrix()
