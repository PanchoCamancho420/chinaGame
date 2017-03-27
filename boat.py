import sprite


class Amphibian(sprite.Sprite):
    def __init__(self, *args):
        sprite.Sprite.__init__(self, *args)
        self.xy = [0.0, 0.0]

    def get_center(self):
        x, y, z = self.shape.get_xyz(self.xy[0], self.xy[1])
        if z <= 0.4:
            z = 0.4
        return x, y, z


class BeachAble(sprite.Sprite):
    def __init__(self, *args):
        sprite.Sprite.__init__(self, *args)
        self.xy = [6.0, 6.0]
        self.is_beached = False
        self.beach_x = 0
        self.beach_z = 0

    def get_center(self):
        x, y, z = self.shape.get_xyz(self.xy[0], self.xy[1])
        if z <= 0.4:
            z = 0.4
        return x, y, z

    def update(self, delta_time):
        sprite.Sprite.update(self, delta_time)
        if not self.is_beached:
            center = self.get_center()
            if center[2] > 0.4:
                self.is_beached = True
                self.beach_x = center[0]
                self.beach_z = center[1]
        else:
            self.xy[0] = self.beach_x
            self.xy[1] = self.beach_z
