import sprite


class Boat(sprite.Sprite):
    def __init__(self, *args):
        sprite.Sprite.__init__(self, *args)

    def get_center(self):
        x, y, z = self.shape.get_xyz(self.xy[0], self.xy[1])
        if z <= 0.4:
            z = 0.4
        return x, y, z
