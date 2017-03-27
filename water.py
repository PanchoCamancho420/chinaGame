from pyglet.gl import *


class Water(object):
    # self, x, y, z, x_size, y_size, texture, texture_scale=1.0
    def __init__(self, terrian, texture, texture_scale=1.0):
        shape_x, shape_y = terrian.size

        # x, y = terrian.convert_xy_to_location(shape_x, shape_y)

        self.x_skew = terrian.xyz[0]
        self.y_skew = terrian.xyz[1]
        self.z_skew = terrian.xyz[2] + 0.4

        self.x_size = shape_x
        self.y_size = shape_y

        self.texture = texture
        self.texture_scale = texture_scale

    def update(self, delta_time):
        pass

    def draw(self):
        glPushMatrix()
        glEnable(GL_TEXTURE_2D)

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
        glDisable(GL_TEXTURE_2D)
        glPopMatrix()
