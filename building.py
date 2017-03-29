from pyglet.gl import *
import pointer
import terrain


class Building(object):
    def __init__(self, shape, x, y, scale):
        self.x = x
        self.y = y
        self.scale = scale
        self.shape = shape
        self.x_loc, self.y_loc, self.z_loc = shape.get_xyz(self.x, self.y)
        self.hp = 100

    def get_center(self):
        return self.x_loc, self.y_loc, self.z_loc

    def attack(self, damage):
        self.hp -= damage

    def heal(self, healing):
        if self.hp > 0:
            self.hp += healing

    def get_hp(self):
        return self.hp

    def clean(self):
        return self.hp <= 0  # if the building has got no hp, git rid of it

    def update(self, delta_time):
        pass

    def draw(self):
        self._draw_xyz(self.x_loc, self.z_loc, self.y_loc)

    def _draw_xyz(self, x, y, z):
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

        # bottom
        # Red
        # glBegin(GL_POLYGON)

        # glVertex3f(self.scale, -self.scale, -self.scale)
        # glVertex3f(self.scale, -self.scale, self.scale)
        # glVertex3f(-self.scale, -self.scale, self.scale)
        # glVertex3f(-self.scale, -self.scale, -self.scale)

        # glEnd()

        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, self.scale, -self.scale)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        glPopMatrix()


class Turret(Building):
    def __init__(self, shape, x, y, scale, color=(0.3, 0.3, 0.3), pointer_pointer=None):
        # type: (terrain.Terrain, int, int, float, tuple, list) -> None
        self.color = color
        Building.__init__(self, shape=shape, x=x, y=y, scale=scale)
        # need to swap some values
        temp = self.y_loc
        self.y_loc = self.z_loc
        self.z_loc = temp

        self.pointer_pointer = pointer_pointer

        self.arrow = pointer.Laser(location=(self.x_loc, self.y_loc + self.scale, self.z_loc),
                                   scale=self.scale / 2)

    def point_at(self, direction):
        self.arrow.point_at(direction)

    def cancel_pointing(self):
        self.arrow.cancel_pointing()

    def update(self, delta_time):
        if self.pointer_pointer:
            min_index = 0
            center = self.pointer_pointer[min_index].get_center()
            min_distance = (((self.x_loc - center[0]) ** 2) +
                            ((self.y_loc - center[2]) ** 2) +
                            ((self.z_loc - center[1]) ** 2)) ** 0.5

            for i in range(len(self.pointer_pointer)):
                center = self.pointer_pointer[i].get_center()
                distance = (((self.x_loc - center[0]) ** 2) +
                            ((self.y_loc - center[2]) ** 2) +
                            ((self.z_loc - center[1]) ** 2)) ** 0.5
                if distance < min_distance:
                    min_index = i
                    min_distance = distance
            self.arrow.point_at(self.pointer_pointer[min_index])
            self.arrow.update(delta_time)
            damage = self.arrow.get_damage()
            self.pointer_pointer[min_index].attack(damage)
        else:
            self.arrow.cancel_pointing()
            self.arrow.update(delta_time)

    def draw(self):
        self.arrow.draw()

        glPushMatrix()

        glTranslatef(self.x_loc, self.y_loc, self.z_loc)
        # print self.x_loc, self.y_loc, self.z_loc

        glColor3f(*self.color)

        glBegin(GL_POLYGON)

        h = 2.0

        glVertex3f(self.scale, -self.scale, self.scale)
        glVertex3f(self.scale / 2, self.scale / h, self.scale / 2)
        glVertex3f(-self.scale / 2, self.scale / h, self.scale / 2)
        glVertex3f(-self.scale, -self.scale, self.scale)

        glEnd()

        # Purple
        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(self.scale / 2, self.scale / h, self.scale / 2)
        glVertex3f(self.scale, -self.scale, self.scale)

        glEnd()

        # Green
        glBegin(GL_POLYGON)

        glVertex3f(-self.scale, -self.scale, self.scale)
        glVertex3f(-self.scale / 2, self.scale / h, self.scale / 2)
        glVertex3f(-self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        # Blue
        glBegin(GL_POLYGON)

        glVertex3f(self.scale / 2, self.scale / h, self.scale / 2)
        glVertex3f(self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(-self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(-self.scale / 2, self.scale / h, self.scale / 2)

        glEnd()

        glBegin(GL_POLYGON)

        glVertex3f(self.scale, -self.scale, -self.scale)
        glVertex3f(self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(-self.scale / 2, self.scale / h, -self.scale / 2)
        glVertex3f(-self.scale, -self.scale, -self.scale)

        glEnd()

        glPopMatrix()
