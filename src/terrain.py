from pyglet.gl import *
import numpy as np
# import terrainShape


class _HexOperation(object):
    @staticmethod
    def right_up_func((x, y)):
        is_even = (0 == y % 2)
        if is_even:
            return x, y - 1
        else:
            return x - 1, y - 1

    @staticmethod
    def right_func((x, y)):
        return x - 1, y

    @staticmethod
    def right_down_func((x, y)):
        is_even = (0 == y % 2)
        if is_even:
            return x, y + 1
        else:
            return x - 1, y + 1

    @staticmethod
    def left_up_func((x, y)):
        is_even = (0 == y % 2)
        if is_even:
            return x, y - 1
        else:
            return x + 1, y - 1

    @staticmethod
    def left_func((x, y)):
        return x + 1, y

    @staticmethod
    def left_down_func((x, y)):
        is_even = (0 == y % 2)
        if is_even:
            return x, y + 1
        else:
            return x + 1, y + 1


class Terrain(object):
    def __init__(self, sand_texture, terrain_shape, xyz=(0, 0, 0), texture_scale=1.0, size=(50, 50), resolution=5):
        self.sand_texture = sand_texture
        self.texture_scale = texture_scale

        self.xyz = xyz
        self.size = size
        self.resolution = resolution

        self.terrain_shape = terrain_shape
        # xyz location
        # sand texture
        # sand texture scale
        # sample rate (triangle size)
        # x size
        # y size
        # terrainShape

    '''where its being drawn to where it is on the map'''
    def draw_xy_to_terrain_xy(self, x, y):
        ret_x = x / self.resolution + self.xyz[0]
        ret_y = y / self.resolution + self.xyz[1]
        return ret_x, ret_y

    '''Return the z location on the TerrainShape from mapping an x, y'''
    def get_z(self, x, y):
        loc = self.draw_xy_to_terrain_xy(x, y)
        height = self.terrain_shape.get_height(loc[0], loc[1])
        return height

    '''Return the x y z location on the TerrainShape from mapping an x, y'''
    def get_xyz(self, x, y):
        x_loc, y_loc = self.draw_xy_to_terrain_xy(x, y)
        height = self.terrain_shape.get_height(x_loc, y_loc)
        return x_loc, y_loc, height

    '''Converts a matrix xy to a sample location'''
    def __mat_xy_to_map_xy(self, x, y):
        y_const = np.sin(np.radians([-360 / 6])[0])
        x_const = 0.5  # np.cos(np.radians([-360/6])[0])

        is_even = (0 == y % 2)
        ret_x = x
        if not is_even:
            ret_x -= x_const

        ret_y = y_const * y
        return ret_x, ret_y

    @staticmethod
    def convert_xy_to_location(mat_x, mat_y):
        y_const = np.sin(np.radians([-360 / 6])[0])
        x_const = 0.5  # np.cos(np.radians([-360/6])[0])

        is_even = (0 == mat_y % 2)
        ret_x = mat_x
        if not is_even:
            ret_x -= x_const

        ret_y = y_const * mat_y
        ret = ret_x, ret_y
        return ret

    '''create a matrix of heights use able by deprecated drawing methods'''
    def get_example_mat(self, x_size, y_size):

        mat_img = np.zeros([x_size, y_size])
        for x_mat in range(x_size):
            for y_mat in range(y_size):
                get_x, get_y = self.convert_xy_to_location(x_mat - (x_size / 2), y_mat - (y_size / 2))
                z_height = self.terrain_shape.get_height(get_x, get_y)
                mat_img[x_mat, y_mat] = z_height
        return mat_img

    '''Call OpenGL to create triangle based terrain'''
    def draw(self):
        self._draw()

    def update(self, delta_time):
        pass

    # ~~~~~~~~~~ DRAWING FUNCTION ~~~~~~~~~~~~~~~~~~~~~~~~
    def _draw(self):

        x_size, y_size = self.size
        for x in range(0, x_size, 1):
            for y in range(1, y_size - 1, 1):
                self.dual_tri(x - int(x_size / 2), y - int(y_size / 2))

        glFlush()

    def dual_tri(self, x, y):
        # first point: left
        l_x, l_y = self.convert_xy_to_location(x, y)
        l_x += self.xyz[0]
        l_y += self.xyz[1]
        l_z = self.get_z(l_x, l_y) + self.xyz[2]
        left_point = np.array([l_x, l_z, l_y])

        # second point: top
        t_xy = _HexOperation.right_up_func((x, y))
        t_x, t_y = self.convert_xy_to_location(t_xy[0], t_xy[1])
        t_x += self.xyz[0]
        t_y += self.xyz[1]
        t_z = self.get_z(t_x, t_y) + self.xyz[2]
        top_point = np.array([t_x, t_z, t_y])

        # third point: right
        r_xy = _HexOperation.right_func((x, y))
        r_x, r_y = self.convert_xy_to_location(r_xy[0], r_xy[1])
        r_x += self.xyz[0]
        r_y += self.xyz[1]
        r_z = self.get_z(r_x, r_y) + self.xyz[2]
        right_point = np.array([r_x, r_z, r_y])

        # fourth point
        b_xy = _HexOperation.right_down_func((x, y))
        b_x, b_y = self.convert_xy_to_location(b_xy[0], b_xy[1])
        b_x += self.xyz[0]
        b_y += self.xyz[1]
        b_z = self.get_z(b_x, b_y) + self.xyz[2]
        bottom_point = np.array([b_x, b_z, b_y])

        top_tri = np.array([left_point, top_point, right_point])
        self.draw_tri(top_tri)

        bottom_tri = np.array([left_point, bottom_point, right_point])
        self.draw_tri(bottom_tri)

    def draw_tri(self, triangle_as_mat):
        numpy_mat = np.array(triangle_as_mat)
        tri_point_0 = numpy_mat[0]
        tri_point_1 = numpy_mat[1]
        tri_point_2 = numpy_mat[2]

        def above_water(point):
            ret = point[1] >= 0.4
            return ret

        above_0 = above_water(tri_point_0)
        above_1 = above_water(tri_point_1)
        above_2 = above_water(tri_point_2)

        if (not above_0) and (not above_1) and (not above_2):
            return
        glEnable(GL_TEXTURE_2D)
        glBindTexture(self.sand_texture.target, self.sand_texture.id)

        glColor3f(1.0, 1.0, 1.0)

        glBegin(GL_TRIANGLES)  # Begin drawing the pyramid with 4 triangles
        # glColor3f(1.0, 0.8, 0.8)  # Red
        glTexCoord2f(0.0, 0.0)
        glVertex3f(tri_point_0[0] * self.resolution, tri_point_0[1] * self.resolution, tri_point_0[2] * self.resolution)

        # glColor3f(0.8, 1.0, 0.8)  # Green
        glTexCoord2f(0.5 * self.texture_scale, 1.0 * self.texture_scale)
        glVertex3f(tri_point_1[0] * self.resolution, tri_point_1[1] * self.resolution, tri_point_1[2] * self.resolution)

        # glColor3f(0.8, 0.8, 1.0)  # Blue
        glTexCoord2f(1.0 * self.texture_scale, 0.0)
        glVertex3f(tri_point_2[0] * self.resolution, tri_point_2[1] * self.resolution, tri_point_2[2] * self.resolution)

        glEnd()
        glDisable(GL_TEXTURE_2D)
