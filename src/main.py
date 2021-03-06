#!/usr/bin/env python
import os
import sys

import pyglet
from pyglet.gl import *

import boat
import noobie
import building
import inputHandler
import loading
import map
import selector
import sky
from camera import Camera as FpsCamera
from terrain import Terrain
from terrainShape import TerrainShape


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(relative_path)


class World(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(World, self).__init__(*args, **kwargs)
        self.scale = 1.0
        self.pos = (0, 0, 0)
        self.fov = 75
        self.render_distance = 100.0
        self.window_x = 1080
        self.window_y = 720
        self.on_resize(self.window_x, self.window_y)

        glClearColor(1.0, 1.0, 1.0, 0.0)
        glEnable(GL_DEPTH_TEST)

        self.file_path = resource_path('textureImages')
        self.textures = self.load_textures()

        import random
        seed = random.randrange(1000, 9999)
        print 'seed ', seed
        shape = TerrainShape(seed=seed, island_location=(0, 0), size=4, height=.5)
        sand = Terrain(self.textures[0], shape, size=(20, 20), resolution=1)
        self.sand = sand

        self.draw_ables = []
        self.update_ables = []
        self.control_ables = []
        self.point_ables = []
        self.draw_ables_2d = []

        self.loading = loading.Fact(self)
        self.update_ables.append(self.loading)
        self.loading_time_total = 10.0
        self.loading_time = 0.0

        fort = building.Building(sand, 1, 1, .1)
        fort_2 = building.Building(sand, 2, 1, .1)
        fort_3 = building.Building(sand, 1, 2, .2)
        fort_4 = building.Building(sand, 2, 2, .1)
        fort_outpost = building.Building(sand, -2, -2, .07)
        fort_king = building.Building(sand, 0, 0, .25)

        self.map = map.Map(self.textures[1], sand)
        self.update_ables.append(self.map)
        self.map.add_building(fort)
        self.map.add_building(fort_2)
        self.map.add_building(fort_3)
        self.map.add_building(fort_4)
        self.map.add_building(fort_outpost)
        self.map.add_building(fort_king)

        self.sky = sky.Sky(self.sand, self.textures[4])
        self.draw_ables.append(self.sky)

        self.control_able_index = 0
        self.default_controllable_index = 0

        self.camera = FpsCamera(self, self.sand)
        self.control_ables.append(self.camera)

        noob = noobie.Noob(self, self.sand, self.map.get_buildings())
        self.draw_ables.append(noob)
        self.update_ables.append(noob)

        # self.sprite = sprite.Sprite(self, self.map.land)
        # self.control_ables.append(self.sprite)
        # self.draw_ables.append(self.sprite)
        # self.update_ables.append(self.sprite)
        # self.point_ables.append(self.sprite)

        self.selector = selector.Selector(shape=sand, window=self)
        self.draw_ables.append(self.selector)
        self.update_ables.append(self.selector)

        self.input_handler = inputHandler.InputHandler()
        self.push_handlers(self.input_handler)
        self.c_bumped = self.input_handler.add_bumped(pyglet.window.key.C)
        self.v_bumped = self.input_handler.add_bumped(pyglet.window.key.V)
        self.b_bumped = self.input_handler.add_bumped(pyglet.window.key.B)
        self.n_bumped = self.input_handler.add_bumped(pyglet.window.key.N)
        self.b_switch = False
        self.period_bumped = self.input_handler.add_bumped(pyglet.window.key.PERIOD)
        self.comma_bumped = self.input_handler.add_bumped(pyglet.window.key.COMMA)

        self.reset_control()

        self.draw_number = 0  # the first rendered frame is 1

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

    def load_textures(self):
        img_dir = self.file_path
        textures = []
        if not os.path.isdir(img_dir):
            print 'Could not find directory "%s" under "%s"' % (img_dir,
                                                                os.getcwd())
            sys.exit(1)
        for image in os.listdir(img_dir):
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
            sys.exit(0)
        return textures

    def reset_control(self):
        for control in self.control_ables:
            control.set_control(False, False)

        self.control_ables[self.default_controllable_index].set_control(True, True)

    def increment_control(self):
        for control in self.control_ables:
            control.set_control(False, False)

        self.control_able_index += 1
        if len(self.control_ables) <= self.control_able_index:
            self.control_able_index = 0
        mouse, key_board = self.control_ables[self.control_able_index].set_control(True, True)
        if not self.control_able_index == self.default_controllable_index:
            self.control_ables[self.default_controllable_index].set_control(not mouse, not key_board)

    def set_3d(self):
        """ Configure OpenGL to draw in 3d.
        """
        width, height = self.get_size()
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(self.fov, width / float(height), 0.01, self.render_distance)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def set_2d(self):
        width, height = self.get_size()
        glDisable(GL_DEPTH_TEST)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def update(self, delta_time):

        if self.loading_time <= self.loading_time_total:
            self.loading_time += delta_time
            self.loading.update(delta_time)
            return

        if self.v_bumped.get_bumped():
            self.increment_control()
        if self.c_bumped.get_bumped():
            self.reset_control()
        if self.b_bumped.get_bumped():
            self.b_switch = not self.b_switch
            if self.b_switch:
                self.camera.point_at(self.sprite)
            else:
                self.camera.cancel_pointing()
        if self.n_bumped.get_bumped():
            insert_sprite = boat.BeachAble(self, self.map.land, random_xy=True)
            self.control_ables.append(insert_sprite)
            self.draw_ables.append(insert_sprite)
            self.update_ables.append(insert_sprite)
            self.point_ables.append(insert_sprite)

        if self.period_bumped.get_bumped():
            x, y = self.selector.get_mat_selection()
            if self.map.try_delete(x, y):
                pass
            else:
                import building
                import random
                scale = random.uniform(.05, .15)
                insert_building = building.Building(scale=scale, shape=self.sand, x=x, y=y)
                self.map.add_building(insert_building)

        if self.comma_bumped.get_bumped():
            x, y = self.selector.get_mat_selection()
            if self.map.try_delete(x, y):
                pass
            else:
                import building
                import random
                scale = random.uniform(.2, .35)
                insert_building = building.Turret(self.sand, x, y, scale, pointer_pointer=self.point_ables)
                self.map.add_building(insert_building)

        self.camera.update(delta_time)

        i = 0  # looks through each element and deletes or updates
        while i < len(self.update_ables):
            if self.update_ables[i].clean():
                del self.update_ables[i]
            else:
                self.update_ables[i].update(delta_time)
                i += 1
        i = 0  # looks through other list
        while i < len(self.point_ables):
            if self.point_ables[i].clean():
                del self.point_ables[i]
            else:
                i += 1

    def on_draw(self):

        if self.loading_time_total >= self.loading_time:
            glLoadIdentity()
            glClearColor(1.0, 1.0, 1.0, 0.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.set_2d()
            self.loading.draw()
            return

        self.set_3d()

        self.draw_number += 1

        glLoadIdentity()
        glClearColor(0.3, 0.8, 1.0, 0.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.camera.draw()
        self.map.draw()

        i = 0  # looks through each element and deletes or updates
        while i < len(self.draw_ables):
            if self.draw_ables[i].clean():
                del self.draw_ables[i]
            else:
                self.draw_ables[i].draw()
                i += 1

        self.set_2d()

        # self.set_info_string()
        for drawable_2d in self.draw_ables_2d:
            drawable_2d.draw()

    def on_resize(self, width, height):
        self.window_x = width
        self.window_y = height
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(65.0, width / float(height), .01, self.render_distance)
        glMatrixMode(GL_MODELVIEW)


if __name__ == "__main__":
    window = World(width=1080, height=720, caption='MAKE CHINA GREAT AGAIN', resizable=True, fullscreen=False)
    window.set_exclusive_mouse(True)
    pyglet.app.run()
