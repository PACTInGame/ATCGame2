import random


class Plane:
    def __init__(self, plane_type, pax, fuel, state, game):
        self.plane_type = plane_type
        self.pax = pax
        self.fuel = fuel
        self.state = state
        self.game = game
        # 0 = About to enter airspace, 1 = Approach, 2 = Landing, 3 = Touchdown+Runway, 4 = Taxiing to Gate
        # 5 = At Gate, 6 = Taxiing to Runway, 7 = Taking off, 8 = In Air, 9 = Crashed, 10 = Holding, 11 = Emergency

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

        elif self.state == 1:  # Approach (manual switch to Landing)
            self.progress += self.speed / 220.0

        elif self.state == 2:  # Landing (Automatically switch to Touhdown+Runway)
            self.cleared_speed = 135.0
            self.progress += self.speed / 125.0

            if self.progress > 100:
                self.change_state(3)

        elif self.state == 3:  # Touchdown+Runway (manual switch to Taxiing to Gate)
            self.progress += self.speed / 20.0
            if self.speed > 20.0:
                self.speed -= self.speed / 20.0
            else:
                self.speed = 20.0

        elif self.state == 4:  # Taxiing to Gate (automatically switch to At Gate)
            self.progress += self.speed / 20.0

            if self.progress > 100:
                self.change_state(5)

        elif self.state == 5:  # At Gate (manual switch to Taxiing to Runway)
            self.progress += 1.0

        elif self.state == 6:  # Taxiing to Runway (manual switch to Taking off)
            self.progress += self.speed / 20.0

        elif self.state == 7:  # Taking off (automatically switch to In Air)
            self.cleared_speed = 250.0
            self.progress += self.speed / 100.0

        elif self.state == 8:  # In Air
            self.progress += self.speed / 220.0

            if self.progress > 100:
                self.game.score += 1
                # TODO remove plane
