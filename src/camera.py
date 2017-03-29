import math

import pyglet

import inputHandler


class Camera(object):

    DEFAULT_MOVEMENT_SPEED = 1.0

    DEFAULT_MOUSE_SENSITIVITY = 0.5

    DEFAULT_KEY_MAP = {
        'forward': pyglet.window.key.W,
        'backward': pyglet.window.key.S,
        'left': pyglet.window.key.A,
        'right': pyglet.window.key.D,
        'up': pyglet.window.key.SPACE,
        'down': pyglet.window.key.LSHIFT
    }

    def __init__(self, window, shape, position=(0, -3.0, 0), key_map=DEFAULT_KEY_MAP, movement_speed=DEFAULT_MOVEMENT_SPEED,
                 mouse_sensitivity=DEFAULT_MOUSE_SENSITIVITY, y_inv=True):
        """Create camera object
        Arguments:
            window -- pyglet window which camera attach
            position -- position of camera
            key_map -- dict like FirstPersonCamera.DEFAULT_KEY_MAP
            movement_speed -- speed of camera move (scalar)
            mouse_sensitivity -- sensitivity of mouse (scalar)
            y_inv -- inversion turn above y-axis
        """
        self.sand = shape

        self.__position = list(position)

        self.__direction = 0.0
        self.__angle = 0.0

        self.__input_handler = inputHandler.InputHandler()

        window.push_handlers(self.__input_handler)

        self.y_inv = y_inv
        self.key_map = key_map
        self.movement_speed = movement_speed
        self.mouse_sensitivity = mouse_sensitivity

        self.keyboard_control = False
        self.mouse_control = False

        self.direction_getter = None
        self.is_pointing = False

        self.max_distance = 5.0
        self.max_height = 5.0

    def yaw(self, yaw):
        """Turn above x-axis"""
        self.__direction += yaw * self.mouse_sensitivity
        # print str(self.__yaw) + ' <yaw'

    def pitch(self, pitch):
        """Turn above y-axis"""
        self.__angle += pitch * self.mouse_sensitivity * ((-1) if self.y_inv else 1)
        if self.__angle < -90.0:
            self.__angle = -90
        if self.__angle > 90:
            self.__angle = 90
        # print str(self.__pitch) + ' <pitch'

    def move_forward(self, distance):
        """Move forward on distance"""
        self.__position[0] -= distance * math.sin(math.radians(self.__direction))
        self.__position[2] += distance * math.cos(math.radians(self.__direction))

    def move_backward(self, distance):
        """Move backward on distance"""
        self.__position[0] += distance * math.sin(math.radians(self.__direction))
        self.__position[2] -= distance * math.cos(math.radians(self.__direction))

        # watch this
        # print str(self.__position) + ' <cam'

    def move_left(self, distance):
        """Move left on distance"""
        self.__position[0] -= distance * math.sin(math.radians(self.__direction - 90))
        self.__position[2] += distance * math.cos(math.radians(self.__direction - 90))

    def move_right(self, distance):
        """Move right on distance"""
        self.__position[0] -= distance * math.sin(math.radians(self.__direction + 90))
        self.__position[2] += distance * math.cos(math.radians(self.__direction + 90))

    def move_up(self, distance):
        """Move up on distance"""
        self.__position[1] -= distance

    def move_down(self, distance):
        """Move down on distance"""
        self.__position[1] += distance

    def update(self, delta_time):
        """Update camera state"""
        if self.mouse_control is True:
            self.yaw(self.__input_handler.get_dx())
            self.__input_handler.__dx = 0

            self.pitch(self.__input_handler.get_dy())
            self.__input_handler.__dy = 0
        # self.__input_handler.reset_mouse()

        if self.keyboard_control is True:
            if self.__input_handler.get_pressed()[self.key_map['forward']]:
                self.move_forward(delta_time * self.movement_speed)

            if self.__input_handler.get_pressed()[self.key_map['backward']]:
                self.move_backward(delta_time * self.movement_speed)

            if self.__input_handler.get_pressed()[self.key_map['left']]:
                self.move_left(delta_time * self.movement_speed)

            if self.__input_handler.get_pressed()[self.key_map['right']]:
                self.move_right(delta_time * self.movement_speed)

            if self.__input_handler.get_pressed()[self.key_map['up']]:
                self.move_up(delta_time * self.movement_speed)

            if self.__input_handler.get_pressed()[self.key_map['down']]:
                self.move_down(delta_time * self.movement_speed)
        if self.is_pointing:
            self.calc_direction()

        if math.fabs(self.__position[0]) >= self.max_distance:
            if self.__position[0] >= 0:
                self.__position[0] = self.max_distance
            else:
                self.__position[0] = -self.max_distance

        if math.fabs(self.__position[2]) >= self.max_distance:
            if self.__position[2] >= 0:
                self.__position[2] = self.max_distance
            else:
                self.__position[2] = -self.max_distance

        if -self.__position[1] >= self.max_height:
            self.__position[1] = -self.max_height

        min_height = self.sand.get_z(self.__position[0], self.__position[2]) + .5
        if self.__position[1] >= -min_height:
            self.__position[1] = -min_height

    def set_control(self, mouse, key_board):
        self.mouse_control = mouse
        self.keyboard_control = key_board
        # do this because wants both
        return not mouse, not key_board

    def point_at(self, direction):
        self.direction_getter = direction
        self.is_pointing = True

    def cancel_pointing(self):
        self.direction_getter = None
        self.is_pointing = False

    def calc_direction(self):
        center = self.direction_getter.get_center()
        x_diff = -(-self.__position[0] - center[0])  # x
        z_diff = -(-self.__position[2] - center[1])  # z

        if z_diff == 0:
            z_diff = .0001
        direction = math.degrees(math.atan(z_diff / x_diff))
        direction += 90.0
        if x_diff < 0:
            direction += 180.0
        self.__direction = direction

        # euler distance
        xz_diff = (((-center[0] - self.__position[0]) ** 2) + ((-center[1] - self.__position[2]) ** 2)) ** .5
        y_diff = -(-center[2] - self.__position[1])

        if y_diff == 0:
            y_diff = .0001
        if xz_diff == 0:
            xz_diff = .0001
        angle = math.degrees(math.atan(y_diff / xz_diff))
        # if y_diff > 0:
        #     angle += 180.0

        self.__angle = -angle

    def draw(self):
        """Apply transform"""
        pyglet.gl.glRotatef(self.__angle, 1.0, 0.0, 0.0)
        pyglet.gl.glRotatef(self.__direction, 0.0, 1.0, 0.0)
        pyglet.gl.glTranslatef(*self.__position)
