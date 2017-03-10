from pyglet.gl import *
import numpy as np
import terrainShape


class Terrain(object):
    def __init__(self, sand_texture, terrain_shape, xyz=(0, 0, 0), texture_scale=1.0, size=(50, 50), resolution=50):
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

    '''Return the x y z location on the TerrainShape from mapping an x, y'''
    def get_xyz(self, x, y):
        pass

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

    '''create a matrix of heights use able by deprecated drawing methods'''
    def get_example_mat(self, x_size, y_size):

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

        mat_img = np.zeros([x_size, y_size])
        for x_mat in range(x_size):
            for y_mat in range(y_size):
                get_x, get_y = convert_xy_to_location(x_mat - (x_size / 2), y_mat - (y_size / 2))
                z_height = self.terrain_shape.get_height(get_x, get_y)
                mat_img[x_mat, y_mat] = z_height
        return mat_img

    '''Call OpenGL to create triangle based terrain'''
    def draw(self):
        pass
