from pyglet.gl import *
import math


class Arrow(object):
    def __init__(self, location=(0.0, 0.0, 0.0), color=(0.0, 0.0, 0.0), scale=.25):
        self._scale = scale
        self._x_loc = location[0]
        self._y_loc = location[1]
        self._z_loc = location[2]

        self.color = color

        self._direction = 0.0
        self._angle = 0.0

        self._direction_getter = None
        self._is_pointing = False

    def calc_direction(self):
        center = self._direction_getter.get_center()
        x_diff = center[0] - self._x_loc
        z_diff = center[1] - self._z_loc

        if z_diff == 0:
            z_diff = .0001
        direction = math.degrees(math.atan(x_diff / z_diff))
        if z_diff > 0:
            direction += 180.0

        xz_diff = (((center[0] - self._x_loc) ** 2) + ((center[1] - self._z_loc) ** 2)) ** .5  # euler distance easy
        y_diff = center[2] - self._y_loc

        if y_diff == 0:
            y_diff = .0001
        if xz_diff == 0:
            xz_diff = .0001
        angle = math.degrees(math.atan(y_diff / xz_diff))
        return direction, angle

    def __point_void(self):
        direction, angle = self.calc_direction()
        self._direction = direction
        self._angle = angle

    def update(self, delta_time):
        del delta_time
        # self.direction += 1.0 * delta_time
        # self.angle += 1.0 * delta_time
        if self._is_pointing:
            self.__point_void()
        # self.z_loc += 0.1 * delta_time
        # self.x_loc += .5 * delta_time

    def point_at(self, direction):
        self._direction_getter = direction
        self._is_pointing = True

    def cancel_pointing(self):
        self._direction_getter = None
        self._is_pointing = False

    def set_xyz(self, x, y, z):
        self._x_loc = x
        self._y_loc = y
        self._z_loc = z

    def draw(self):
        glPushMatrix()

        glTranslatef(self._x_loc, self._y_loc, self._z_loc)

        glRotatef(self._direction, 0.0, 1.0, 0.0)
        glRotatef(self._angle, 1.0, 0.0, 0.0)

        # draws cube don't really want that
        if False:
            glColor3f(0.7, 0.3, 0.3)
            # wierd color z
            glBegin(GL_POLYGON)

            glVertex3f(self._scale, -self._scale, self._scale)
            glVertex3f(self._scale, self._scale, self._scale)
            glVertex3f(-self._scale, self._scale, self._scale)
            glVertex3f(-self._scale, -self._scale, self._scale)

            glEnd()

            # Purple
            # x
            glColor3f(1.0, .3, 1.0)
            glBegin(GL_POLYGON)

            glVertex3f(self._scale, -self._scale, -self._scale)
            glVertex3f(self._scale, self._scale, -self._scale)
            glVertex3f(self._scale, self._scale, self._scale)
            glVertex3f(self._scale, -self._scale, self._scale)

            glEnd()

            # Blue
            # anti x
            glColor3f(0.3, 0.3, 1.0)
            glBegin(GL_POLYGON)

            glVertex3f(-self._scale, -self._scale, self._scale)
            glVertex3f(-self._scale, self._scale, self._scale)
            glVertex3f(-self._scale, self._scale, -self._scale)
            glVertex3f(-self._scale, -self._scale, -self._scale)

            glEnd()

            # white
            # top
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_POLYGON)

            glVertex3f(self._scale, self._scale, self._scale)
            glVertex3f(self._scale, self._scale, -self._scale)
            glVertex3f(-self._scale, self._scale, -self._scale)
            glVertex3f(-self._scale, self._scale, self._scale)

            glEnd()

            # bottom
            # black
            glColor3f(0.0, 0.0, 0.0)
            glBegin(GL_POLYGON)

            glVertex3f(self._scale, -self._scale, -self._scale)
            glVertex3f(self._scale, -self._scale, self._scale)
            glVertex3f(-self._scale, -self._scale, self._scale)
            glVertex3f(-self._scale, -self._scale, -self._scale)

            glEnd()

            # green anti y
            glColor3f(0.3, 1.0, 0.3)
            glBegin(GL_POLYGON)

            glVertex3f(self._scale, -self._scale, -self._scale)
            glVertex3f(self._scale, self._scale, -self._scale)
            glVertex3f(-self._scale, self._scale, -self._scale)
            glVertex3f(-self._scale, -self._scale, -self._scale)

            glEnd()

        pointed_ness = 2.5

        glColor3f(*self.color)
        glBegin(GL_TRIANGLES)

        glVertex3f(0.0, self._scale / pointed_ness, self._scale)
        glVertex3f(0.0, 0.0, -self._scale)  # point
        glVertex3f(0.0, -self._scale / pointed_ness, self._scale)

        glVertex3f(self._scale / pointed_ness, 0.0, self._scale)
        glVertex3f(0.0, 0.0, -self._scale)  # point
        glVertex3f(-self._scale / pointed_ness, 0.0, self._scale)

        glEnd()

        glPopMatrix()


class Laser(Arrow):
    def __init__(self, location=(0.0, 0.0, 0.0), normal_color=(0.0, 1.0, 0.0), aiming_color=(1.0, 0.0, 0.0),
                 firing_color=(1.0, .3, 1.0), scale=.25):
        Arrow.__init__(self, location=location, scale=scale)
        self.reload_time = 1.0
        self.reload = 0.0
        self.fire_time = 0.2
        self.rotate_speed = 1.0
        self.aim_speed = 20.0
        self.detection_distance = 4.0
        self.firing_distance = 1.0
        self.color = normal_color
        self.normal_color = normal_color
        self.aiming_color = aiming_color
        self.firing_color = firing_color

    def aim(self, delta_time):
        self.color = self.aiming_color
        target_direction, target_angle = self.calc_direction()

        normal_distance = math.fabs(target_direction - self._direction)
        should_loop = normal_distance >= 180

        print 'amin', should_loop, target_direction, self._direction

        if math.fabs(self._direction - target_direction) <= delta_time * self.aim_speed:
            self._direction = target_direction
        else:
            if target_direction < self._direction:
                if not should_loop:
                    self._direction -= self.aim_speed * delta_time
                else:
                    self._direction += self.aim_speed * delta_time
            else:
                if not should_loop:
                    self._direction += self.aim_speed * delta_time
                else:
                    self._direction -= self.aim_speed * delta_time

    def in_range(self, max_range):
        center = self._direction_getter.get_center()
        distance = (((self._x_loc - center[0]) ** 2) +
                    ((self._y_loc - center[2]) ** 2) +
                    ((self._z_loc - center[1]) ** 2)) ** 0.5
        return distance <= max_range

    def update(self, delta_time):
        if self._is_pointing:
            if self.in_range(self.detection_distance):
                self.aim(delta_time)
            else:
                self.color = self.normal_color
        self._direction %= 360.0
