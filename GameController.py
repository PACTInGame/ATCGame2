import time

import keyboard

import Airport
import Airspace
import Flights
import GameLogic
import PlaneType
import Runway
from Button import Button
from Gate import Gate
from Plane import Plane


class GameController:
    def __init__(self, UI):
        self.airport = Airport.Airport("Airport", [], Runway.Runway("32", "14", 0, 0, 0, 0),
                                       Airspace.Airspace(20))  # TODO Edit x,y

        self.spawn_rate_planes = 350
        self.time_plane_spawned = time.perf_counter()

        self.game_start_time = time.time()
        self.playing_start_time = -1
        self.state = 0  # 0 = Menu, 1 = Game, 2 = End, 3 = Pause
        self.score = 0
        self.atc_history = []
        self.fps_counter = time.perf_counter()
        self.UI = UI
        self.running = True
        self.selected_plane = None

    def start_game(self):
        self.state = 1
        self.playing_start_time = time.time()
        self.create_level_debug()
        self.game_loop()

    def create_level_debug(self):
        print("Creating level...")
        self.airport.add_gate(Gate("A1", 0, 1, 0))  # TODO Edit x,y
        self.airport.add_gate(Gate("A2", 1, 1, 0))
        self.airport.add_gate(Gate("A3", 2, 1, 0))
        self.airport.add_gate(Gate("A4", 2, 1, 0))
        self.airport.add_gate(Gate("A5", 2, 1, 0))

        plane = self.create_airplane(0)
        self.airport.airspace.planes_about_to_enter_airspace.append(plane)

    def create_airplane(self, state):
        callsign = Flights.get_random_flight(self)
        ptype = PlaneType.get_random_plane_type()
        pax = PlaneType.get_number_of_seats_for_plane_type(ptype)
        fuel = PlaneType.get_max_fuel_for_plane_type(ptype)

        plane = Plane(ptype, pax, fuel, state, self, callsign)
        return plane

    def handle_keyboard_events(self, event):
        key = event.name
        if key == 'q' and self.state == 1:
            self.state = 3
            self.UI.state = 'pause'
        elif key == 'q' and self.state == 3:
            self.state = 1
            self.UI.state = 'play'

        if key == 'r' and self.state == 1:
            print("Select a Plane:")
            planes = self.airport.airspace.planes_about_to_enter_airspace + self.airport.airspace.planes_in_airspace + self.airport.planes_at_airport
            buttons = []
            x = 20
            y = 20
            for plane in planes:
                button = Button((60, 60, 100), x, y, 100, 50, plane.callsign, 20)
                y = y + 70
                buttons.append(button)
            self.UI.plane_buttons = buttons
            print(buttons)
            self.UI.state = 'plane'

    def handle_plane_selection(self, plane_name):
        planes = self.airport.airspace.planes_about_to_enter_airspace + self.airport.airspace.planes_in_airspace + self.airport.planes_at_airport
        for plane in planes:
            if plane.callsign == plane_name:
                self.selected_plane = plane
                print("Selected Plane: ", plane.callsign)
                print("Select a Radio Transmission:")
                self.UI.state = 'radio'
                break

    def handle_radio_selection(self, radio_name):
        radio_selection = radio_name.split(":")[0]
        print("Selected Radio Transmission: ", radio_selection)
        GameLogic.atc_calls(int(radio_selection) - 1, self.selected_plane, self)
        self.UI.state = 'play'
        # TODO handle radios with Info parameters

    def quit_game(self):
        self.running = False
        self.state = -1

    def game_loop(self):
        keyboard.hook(self.handle_keyboard_events)
        while self.running:
            while self.state == 1:
                if self.spawn_rate_planes + self.time_plane_spawned < time.perf_counter():
                    self.time_plane_spawned = time.perf_counter()
                    plane = self.create_airplane(0)
                    self.airport.airspace.planes_about_to_enter_airspace.append(plane)
                if self.fps_counter + 1 < time.perf_counter():
                    self.fps_counter = time.perf_counter()

                    # Update all planes
                    [plane.update_progress() for plane in self.airport.planes_at_airport]
                    [plane.update_progress() for plane in self.airport.airspace.planes_in_airspace]
                    [plane.update_progress() for plane in self.airport.airspace.planes_about_to_enter_airspace]

                    # Radio simulation
                    GameLogic.simulate_aircraft_radio_transmissions(self.airport.planes_at_airport,
                                                                    self.airport.airspace.planes_in_airspace,
                                                                    self.airport.airspace.planes_about_to_enter_airspace)
        keyboard.unhook(self.handle_keyboard_events)
