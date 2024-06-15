import time

import Airport
import PlaneType
import Runway
from Gate import Gate
from Plane import Plane


class GameController:
    def __init__(self):
        self.airport = Airport.Airport("Airport", [], Runway.Runway("32", "14", 0, 0, 0, 0))  # TODO Edit x,y
        self.spawn_rate_planes = 60
        self.time_plane_spawned = time.perf_counter()

        self.game_start_time = time.time()
        self.playing_start_time = -1
        self.state = 0  # 0 = Menu, 1 = Game, 2 = End, 3 = Pause
        self.score = 0
        self.atc_history = []

    def start_game(self):
        self.state = 1
        self.playing_start_time = time.time()

    def create_level_debug(self):
        self.airport.add_gate(Gate("A1", 0, 1, 0))  # TODO Edit x,y
        self.airport.add_gate(Gate("A2", 1, 1, 0))
        self.airport.add_gate(Gate("A3", 2, 1, 0))

    def create_airplane(self, state):
        ptype = PlaneType.get_random_plane_type()
        pax = PlaneType.get_number_of_seats_for_plane_type(ptype)
        fuel = PlaneType.get_max_fuel_for_plane_type(ptype)

        plane = Plane(ptype, pax, fuel, state, self)
        return plane

