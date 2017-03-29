import water
import building as building_class


class Map(object):
    def __init__(self, water_texture, land, buildings=None):
        self.land = land
        self.water_texture = water_texture
        self.water = water.Water(self.land, self.water_texture, 1.0)
        self.buildings = []
        if buildings is not None:
            for building in buildings:
                self.buildings.append(building)

    def add_building(self, building):
        # type: (building_class.Building) -> None
        self.buildings.append(building)

    def try_delete(self, x, y):
        for i in range(len(self.buildings)):
            building = self.buildings[i]
            if building.x == x and building.y == y:
                del self.buildings[i]
                return True
        return False

    @staticmethod
    def clean():
        return False

    def update(self, delta_time):
        """change the way the water and towers look"""
        self.water.update(delta_time)
        self.land.update(delta_time)

        i = 0  # looks through each element and deletes or updates
        while i < len(self.buildings):
            if self.buildings[i].clean():
                del self.buildings[i]
            else:
                self.buildings[i].update(delta_time=delta_time)
                i += 1

    def get_buildings(self):
        return self.buildings

    def draw(self):
        """draw buildings, land and water"""
        self.water.draw()
        self.land.draw()
        for building in self.buildings:
            building.draw()
