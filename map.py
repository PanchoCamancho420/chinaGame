import water


class Map(object):
    def __init__(self, water_texture, land, buildings=None, waves=0.01):
        self.land = land
        self.waves = waves
        self.water_texture = water_texture
        self.water = water.Water(self.land, self.water_texture, 1.0)
        self.buildings = []
        if buildings is not None:
            for building in buildings:
                self.buildings.append(building)

    def add_building(self, building):
        self.buildings.append(building)

    def update(self, delta_time):
        """change the way the water and towers look"""
        self.water.update()
        self.land.update()
        for building in self.buildings:
            building.update(delta_time=delta_time)

    def draw(self):
        """draw buildings, land and water"""
        self.water.draw()
        self.land.draw()
        for building in self.buildings:
            x_loc, y_loc, z_loc = self.land.get_xyz(building.x, building.y)
            building.draw_xyz(x_loc, z_loc, y_loc)