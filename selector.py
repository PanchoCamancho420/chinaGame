import pointer
import math
import inputHandler
import pyglet
import terrain


class Selector(object):
    def __init__(self, window, shape):
        # type: (pyglet.window, terrain.Terrain)->None
        self.shape = shape
        self.handler = inputHandler.InputHandler()
        window.push_handlers(self.handler)
        self.arrow = pointer.Arrow()
        self.arrow.color = (1.0, 0.0, 1.0)
        self.arrow._angle = -90.0
        self.height = .5
        self.z_bob = 0.0
        self.z_bob_distance = .1
        self.z_bob_speed = 2.0
        self.total_time = 0.0

        self.up_bump = self.handler.add_bumped(pyglet.window.key.DOWN)
        self.down_bump = self.handler.add_bumped(pyglet.window.key.UP)
        self.right_bump = self.handler.add_bumped(pyglet.window.key.RIGHT)
        self.left_bump = self.handler.add_bumped(pyglet.window.key.LEFT)

        self.mat_x = 1
        self.mat_y = 1

        self.update(0.0)

    def get_mat_selection(self):
        return self.mat_x, self.mat_y

    def get_center(self):
        x_loc, z_loc, y_loc = self.shape.get_xyz(self.mat_x, self.mat_y)
        y_loc += self.height + (self.z_bob * self.z_bob_distance)
        return x_loc, y_loc, z_loc

    def update(self, delta_time):
        self.total_time += delta_time
        self.z_bob = math.cos(self.total_time * self.z_bob_speed)
        if self.up_bump.get_bumped():
            self.mat_x -= 1
        if self.down_bump.get_bumped():
            self.mat_x += 1
        if self.left_bump.get_bumped():
            self.mat_y -= 1
        if self.right_bump.get_bumped():
            self.mat_y += 1

    def draw(self):
        x_loc, z_loc, y_loc = self.shape.get_xyz(self.mat_x, self.mat_y)
        y_loc += self.height + (self.z_bob * self.z_bob_distance)
        self.arrow.set_xyz(x_loc, y_loc, z_loc)
        self.arrow.draw()
