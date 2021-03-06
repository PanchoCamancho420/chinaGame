#!/usr/bin/env python
import os
import sys

import pyglet
from pyglet.gl import *

import terrainShape
from camera import Camera as FpsCamera
from terrain import Terrain


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class World(pyglet.window.Window):
    def __init__(self,
                 *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)
        self.scale = 1.0
        self.pos = (0, 0, 0)
        self.fov = 65
        self.render_distance = 100.0
        self.window_x = 1080
        self.window_y = 720
        self.on_resize(self.window_x, self.window_y)

        glClearColor(1.0, 1.0, 1.0, 0.0)
        glEnable(GL_DEPTH_TEST)

        self.file_path = resource_path('textureImages')
        self.textures = self.load_textures()

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        self.shape = terrainShape.TerrainShape(seed=11, island_location=(0, 0), size=15, height=1)
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        self.camera = FpsCamera(self)
        self.draw_number = 0  # the first rendered frame is 1

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def load_textures(self):
        img_dir = self.file_path
        textures = []
        img_paths = os.listdir(img_dir)
        print img_paths
        img_paths.sort()
        for image in img_paths:
            try:
                if not image == '.DS_Store':
                    image = pyglet.image.load(os.path.join(img_dir, image))
                else:
                    continue
            except pyglet.image.codecs.dds.DDSException:
                print '"%s" is not a valid image file' % image
                continue
            textures.append(image.get_texture())

            glEnable(textures[-1].target)
            glBindTexture(textures[-1].target, textures[-1].id)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.width, image.height,
                         0, GL_RGBA, GL_UNSIGNED_BYTE,
                         image.get_image_data().get_data('RGBA',
                                                         image.width * 4))
        if len(textures) == 0:
            print 'Found no textures to load. Exiting'
            sys.exit(0)
        return textures

    def update(self, delta_time):

        self.camera.update(delta_time)

    def on_draw(self):

        self.draw_number += 1

        glLoadIdentity()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.camera.draw()

        shape = self.shape
        terrain = Terrain(self.textures[0], shape)
        mat = terrain.get_example_mat(20, 20)

        import matTerrian
        matTerrian.draw(texture=terrain.sand_texture, mat=mat)

    def on_resize(self, width, height):
        self.window_x = width
        self.window_y = height
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), 0.1, self.render_distance)
        glMatrixMode(GL_MODELVIEW)


if __name__ == "__main__":
    window = World(width=800, height=600, caption='terrian Explorer', resizable=True, fullscreen=False)
    window.set_exclusive_mouse(True)
    pyglet.app.run()
