import random


class Plane:
    def __init__(self, plane_type, pax, fuel, state, game, callsign="N/A"):
        self.callsign = callsign[0]
        self.from_airport = callsign[1]
        self.plane_type = plane_type
        self.pax = pax
        self.fuel = fuel
        self.state = state
        self.game = game
        self.cleared_approach = False
        self.cleared_to_land = False
        self.cleared_to_gate = False
        self.wind_given = False
        self.cleared_to_land = False
        self.cleared_to_lineup = False
        self.cleared_to_start = False
        self.cleared_to_runway = False
        self.pushback_and_start_approved = False
        self.departure_frequency = False
        self.controller = 0  # 0 = Approach, 1 = Tower, 2 = Ground
        self.score = 10
        # 0 = About to enter airspace, 1 = Approach, 2 = Landing, 3 = Touchdown+Runway, 4 = Taxiing to Gate
        # 5 = At Gate, 6 = Taxiing to Runway, 6.5 = Line up and wait, 7 = Taking off, 8 = In Air, 9 = Crashed,
        # 10 = Holding, 11 = Go Around, 12 = Emergency

        self.atc_history = []
        self.progress = 0.0

        random_speed = random.randint(200, 250)
        self.speed = random_speed if self.state == 0.0 else 0.0
        self.cleared_speed = random_speed if self.state == 0.0 else 0.0

        random_height = random.randint(5000, 8000)
        self.altitude = random_height if self.state == 0 else 0
        self.cleared_altitude = random_height if self.state == 0 else 0
        self.rate = 52.3  # Standard descent/ascend rate, can be expedited

        self.heading = 0

        self.pilot_stress_level = 0

    def change_state(self, new_state):
        self.state = new_state
        self.progress = 0.0

    def update_progress(self):
        print("\n")
        print("Plane type:", self.plane_type, "state:", self.state, "progress:", self.progress)
        print("Cleared_to_land:", self.cleared_to_land, "Cleared_to_gate:", self.cleared_to_gate, "Wind_given:", self.wind_given)
        print("\n")
        if self.speed > self.cleared_speed + 5 or self.speed < self.cleared_speed - 5:
            if self.speed < self.cleared_speed:
                self.speed += (self.cleared_speed / self.speed) * 2
            else:
                self.speed -= (self.cleared_speed / self.speed) * 2

        if self.altitude != self.cleared_altitude:
            if self.altitude < self.cleared_altitude:
                self.altitude += self.rate
            else:
                self.altitude -= self.rate

        if self.state == 0:  # About to enter airspace (Automatically switch to Approach)
            self.progress += 2

            if self.progress > 100:
                self.change_state(1)
                self.game.airport.airspace.planes_in_airspace.append(self)
                self.game.airport.airspace.planes_about_to_enter_airspace.remove(self)

        elif self.state == 1:  # Approach (manual switch to Landing)
            self.progress += self.speed / 220.0
            if self.controller == 0 and self.progress > 50:
                self.change_state(10)

            if self.progress > 100:
                if self.cleared_to_land:
                    if not self.wind_given:
                        self.pilot_stress_level += 1
                    self.change_state(2)
                else:
                    self.change_state(10)

        elif self.state == 2:  # Landing (Automatically switch to Touhdown+Runway)
            self.cleared_speed = 135.0
            self.progress += self.speed / 125.0
            if self.progress > 60 and not self.wind_given:
                self.change_state(10)
            if self.progress > 100:
                self.change_state(3)
                self.game.airport.planes_at_airport.append(self)
                self.game.airport.airspace.planes_in_airspace.remove(self)
                self.wind_given = False

        elif self.state == 3:  # Touchdown+Runway (manual switch to Taxiing to Gate)
            self.progress += self.speed / 20.0
            self.cleared_speed = 20.0
            if self.cleared_to_gate and self.progress > 100:
                self.change_state(4)

        elif self.state == 4:  # Taxiing to Gate (automatically switch to At Gate)
            self.progress += self.speed / 20.0
            if self.progress > 100:
                self.change_state(5)

        elif self.state == 5:  # At Gate (manual switch to Taxiing to Runway)
            if self.progress == 70 and not self.pushback_and_start_approved:
                self.pilot_stress_level += 1
            elif self.progress == 72 and not self.pushback_and_start_approved:
                self.progress -= 1.0
            self.progress += 1.0
            if self.progress > 100 and self.cleared_to_runway:
                self.change_state(6)

        elif self.state == 6:  # Taxiing to Runway (manual switch to Taking off)
            self.progress += self.speed / 20.0

            if self.progress > 100 and self.cleared_to_start:
                self.change_state(7)
            elif self.progress > 100 and self.cleared_to_lineup:
                self.change_state(6.5)

        elif self.state == 6.5:  # Line up and wait (manual switch to Taking off)
            self.progress += 1.0
            if self.cleared_to_start:
                self.change_state(7)

        elif self.state == 7:  # Taking off (automatically switch to In Air)
            self.cleared_speed = 250.0
            self.progress += self.speed / 100.0
            # TODO: Add more conditions for taking off, like wind
            if self.progress > 100 and self.departure_frequency:
                self.change_state(8)
                self.game.airport.airspace.planes_in_airspace.append(self)
                self.game.airport.planes_at_airport.remove(self)

        elif self.state == 8:  # In Air
            self.progress += 4

            if self.progress > 100:
                if self.pilot_stress_level > 5:
                    self.score -= self.pilot_stress_level
                if self.score < 0:
                    self.score = 0
                self.game.score += self.score

                self.game.airport.airspace.planes_in_airspace.remove(self)
