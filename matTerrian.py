import numpy as np
from pyglet.gl import *


def right_up_func((x, y)):
    is_even = (0 == y % 2)
    if is_even:
        return x, y - 1
    else:
        return x - 1, y - 1


def right_func((x, y)):
    return x - 1, y


def right_down_func((x, y)):
    is_even = (0 == y % 2)
    if is_even:
        return x, y + 1
    else:
        return x - 1, y + 1


def left_up_func((x, y)):
    is_even = (0 == y % 2)
    if is_even:
        return x, y - 1
    else:
        return x + 1, y - 1


def left_func((x, y)):
    return x + 1, y


def left_down_func((x, y)):
    is_even = (0 == y % 2)
    if is_even:
        return x, y + 1
    else:
        return x + 1, y + 1


def convert_xy_to_location((x, y)):
    y_const = np.sin(np.radians([-360/6])[0])
    x_const = 0.5  # np.cos(np.radians([-360/6])[0])

    is_even = (0 == y % 2)
    ret_x = x
    if not is_even:
        ret_x -= x_const

    ret_y = y_const * y
    return ret_x, ret_y


def get_example():
    h = 1.0
    l = 0.0

    terrian_map = np.array([[l, l, l, l, l, l, l, l, l, l],
                            [l, l, l, l, l, l, l, l, l, l],
                            [l, l, l, l, l, l, l, l, l, l],
                            [l, l, l, l, l, l, l, l, l, l],
                            [l, l, l, l, l, l, l, l, l, l],
                            [l, l, l, l, l, h, h, l, l, l],
                            [l, l, l, l, h, h, h, l, l, l],
                            [l, l, l, l, h, h, l, l, l, l],
                            [l, l, l, l, l, l, l, l, l, l],
                            [l, l, l, l, l, l, l, l, l, l],
                            [l, l, l, l, l, l, l, l, l, l],
                            [l, l, l, l, l, l, l, l, l, l]])

    return terrian_map


def get_example_2():
    h = 1.0
    m = 0.5
    l = 0.0

    terrian_map = np.array([[l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l],
                            [l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l],
                            [l, l, m, m, m, m, m, m, l, l, l, l, l, l, l, l, l],
                            [l, l, m, h, h, h, h, m, l, l, l, l, l, l, l, l, l],
                            [l, l, m, h, h, h, h, m, l, l, l, l, l, l, l, l, l],
                            [l, l, m, h, h, h, h, m, l, l, l, l, l, l, l, l, l],
                            [l, l, m, h, h, h, h, m, m, l, l, l, l, l, l, l, l],
                            [l, l, m, h, m, m, h, m, m, m, m, l, l, l, l, l, l],
                            [l, l, m, h, m, m, h, m, m, m, m, m, m, l, l, l, l],
                            [l, l, m, m, m, m, m, m, l, l, l, m, m, m, l, l, l],
                            [l, l, m, m, m, m, m, m, l, l, l, l, l, m, m, l, l],
                            [l, l, m, m, m, m, m, m, l, l, l, l, l, m, m, l, l],
                            [l, l, m, m, m, m, m, m, l, l, l, l, l, l, l, l, l],
                            [l, l, m, m, m, m, m, m, l, l, l, l, l, l, l, l, l],
                            [l, l, m, m, m, m, m, m, l, l, l, l, l, l, l, l, l],
                            [l, l, l, m, m, m, m, m, l, l, l, l, l, l, l, l, l],
                            [l, l, l, l, l, l, m, m, l, l, l, m, m, l, l, l, l],
                            [l, l, l, l, l, l, m, m, m, m, m, m, m, m, l, l, l],
                            [l, l, l, l, l, l, l, m, m, m, m, l, l, l, l, l, l],
                            [l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l],
                            [l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l, l]])

    return terrian_map


# really watch out cuz the x and y draw a FLAT, not what the x,y,z actally looks like
def draw(texture, mat=get_example(), (x_skew, y_skew, z_skew)=(0, 0, 0), scale=1.0, tex_scale=1.0):
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glLoadIdentity()

    x_size, y_size = mat.shape
    for x in range(0, x_size, 1):
        for y in range(1, y_size - 1, 1):
            dual_tri(texture, mat, x, y, x_skew, y_skew, z_skew, scale, tex_scale)

    glFlush()


def dual_tri(texture, mat, x, y, x_skew, y_skew, z_skew, scale, tex_scale):
    # first point: left
    l_x, l_y = convert_xy_to_location((x, y))
    l_x += x_skew
    l_y += y_skew
    l_z = mat[x, y] + z_skew
    left_point = np.array([l_x, l_z, l_y])

    # second point: top
    t_xy = right_up_func((x, y))
    t_x, t_y = convert_xy_to_location(t_xy)
    t_x += x_skew
    t_y += y_skew
    t_z = mat[t_xy[0], t_xy[1]] + z_skew
    top_point = np.array([t_x, t_z, t_y])

    # third point: right
    r_xy = right_func((x, y))
    r_x, r_y = convert_xy_to_location(r_xy)
    r_x += x_skew
    r_y += y_skew
    r_z = mat[r_xy[0], r_xy[1]] + z_skew
    right_point = np.array([r_x, r_z, r_y])

    # fourth point
    b_xy = right_down_func((x, y))
    b_x, b_y = convert_xy_to_location(b_xy)
    b_x += x_skew
    b_y += y_skew
    b_z = mat[b_xy[0], b_xy[1]] + z_skew
    bottom_point = np.array([b_x, b_z, b_y])

    top_tri = np.array([left_point, top_point, right_point])
    draw_tri(top_tri, scale, texture, tex_scale)

    bottom_tri = np.array([left_point, bottom_point, right_point])
    draw_tri(bottom_tri, scale, texture, tex_scale)


def draw_tri(mat, scale, texture, tex_scale=1.0):
    numpy_mat = np.array(mat)
    tri_point_0 = numpy_mat[0]
    tri_point_1 = numpy_mat[1]
    tri_point_2 = numpy_mat[2]

    # glBindTexture(texture.target, texture.id)

    glBegin(GL_TRIANGLES)  # Begin drawing the pyramid with 4 triangles
    glColor3f(1.0, 0.8, 0.8)  # Red
    glTexCoord2f(0.0, 0.0)
    glVertex3f(tri_point_0[0] * scale, tri_point_0[1] * scale, tri_point_0[2] * scale)

    glColor3f(0.8, 1.0, 0.8)  # Green
    glTexCoord2f(0.5 * tex_scale, 1.0 * tex_scale)
    glVertex3f(tri_point_1[0] * scale, tri_point_1[1] * scale, tri_point_1[2] * scale)

    glColor3f(0.8, 0.8, 1.0)  # Blue
    glTexCoord2f(1.0 * tex_scale, 0.0)
    glVertex3f(tri_point_2[0] * scale, tri_point_2[1] * scale, tri_point_2[2] * scale)

    glEnd()


class Terrain(object):
    def __init__(self, mat, x, y, z, scale, texture, texture_scale):
        self.mat = mat
        self.x_skew = x
        self.y_skew = y
        self.z_skew = z
        self.scale = scale
        self.texture = texture
        self.texture_scale = texture_scale

    def get_mat(self):
        return self.mat

    def update(self):
        pass

    def convert_xy_to_location(self, (x, y)):
        y_const = np.sin(np.radians([-360 / 6])[0])
        x_const = 0.5  # np.cos(np.radians([-360/6])[0])

        is_even = (0 == y % 2)
        ret_x = x
        if not is_even:
            ret_x -= x_const

        ret_y = y_const * y
        return ret_x + self.x_skew, ret_y + self.y_skew

    def get_xyz(self, x, y):
        ret_z = self.mat[x, y]
        ret_x, ret_y = self.convert_xy_to_location((x, y))
        return ret_x, ret_y, ret_z

    def draw(self):
        draw(self.texture, self.mat, (self.x_skew, self.y_skew, self.z_skew), self.scale, self.texture_scale)
