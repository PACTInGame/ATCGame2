class Runway:
    def __init__(self, name, opposite_name, x, y, x_end, y_end):
        self.name = name
        self.opposite_name = opposite_name
        self.planes_on_runway = []
        self.x = x
        self.y = y
        self.x_end = x_end
        self.y_end = y_end