import random

import pygame


class Plane:
    def __init__(self, plane_type, pax, fuel, state, game, callsign="N/A"):
        self.callsign = callsign[0]
        self.from_airport = callsign[1]
        self.plane_type = plane_type
        if self.plane_type in [5, 7, 8, 9, 10, 11]:
            self.texture = pygame.image.load("assets/large_plane.png")
            self.transform_x = 48
            self.transform_y = 58
        else:
            self.texture = pygame.image.load("assets/medium_plane.png")
            self.transform_x = 35
            self.transform_y = 42
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

        self.speed_fluctuation = 0
        self.altitude_fluctuation = 0
        self.heading = 0

        self.pilot_stress_level = 0

    def change_state(self, new_state):
        self.state = new_state
        self.progress = 0.0

    def calculate_height_loss_s_1(self):
        final_height = 2000  # height in ft at 100% progress
        self.altitude = self.cleared_altitude - (self.cleared_altitude - final_height) * ((self.progress - 50) / 50)

    def calculate_height_loss_s_2(self):
        final_height = 100  # height in ft at 100% progress
        self.altitude = 2000 - (2000 - final_height) * (self.progress / 100)

    def get_waypoints(self):
        # TODO ADD WAYPOINTS FOR DIFFERENT GATES
        gate = 1
        if gate == 1:
            waypoints = [
                (450, 445, 0),
                (402, 418, 90),
                (402, 380, 90),
                (448, 345, 180),
                (569, 345, 180),
                (691, 345, 180),
                (780, 272, 90)
            ]

        return waypoints

    def update_progress(self):
        self.speed_fluctuation = random.randint(-2, 2)
        self.altitude_fluctuation = random.randint(-8, 8)
        # print("\n")
        # print("Plane type:", self.plane_type, "state:", self.state, "progress:", self.progress)
        # print("Cleared_to_land:", self.cleared_to_land, "Cleared_to_gate:", self.cleared_to_gate, "Wind_given:", self.wind_given)
        print("Plane speed:", self.speed, "Cleared speed:", self.cleared_speed)
        print("\n")
        if self.speed > self.cleared_speed - 1 or self.speed < self.cleared_speed - 6:
            if self.speed < self.cleared_speed:
                self.speed += (self.speed / self.cleared_speed)
            else:
                self.speed -= (self.speed / self.cleared_speed)

        # if self.altitude != self.cleared_altitude:
        #     if self.altitude < self.cleared_altitude:
        #         self.altitude += self.rate
        #     else:
        #         self.altitude -= self.rate

        if self.state == 0:  # About to enter airspace (Automatically switch to Approach)
            self.progress += 2

            if self.progress > 100:
                self.change_state(1)
                self.game.airport.airspace.planes_in_airspace.append(self)
                self.game.airport.airspace.planes_about_to_enter_airspace.remove(self)

        elif self.state == 1:  # Approach (manual switch to Landing)
            self.progress += self.speed / 220.0
            if self.progress > 50:
                self.calculate_height_loss_s_1()

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
            self.calculate_height_loss_s_2()
            if self.progress > 60 and not self.wind_given:
                self.change_state(10)
            if self.progress > 100:
                self.change_state(3)
                self.game.airport.planes_at_airport.append(self)
                self.game.airport.airspace.planes_in_airspace.remove(self)
                self.wind_given = False

        elif self.state == 3:  # Touchdown+Runway (manual switch to Taxiing to Gate)
            self.progress += self.speed / 50.0
            self.cleared_speed = 20.0
            if self.cleared_to_gate and self.progress > 51:
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
                self.altitude = 500
                self.game.airport.airspace.planes_in_airspace.append(self)
                self.game.airport.planes_at_airport.remove(self)

        elif self.state == 8:  # In Air
            self.progress += 4
            self.altitude += 42
            if self.progress > 100:

                self.score -= self.pilot_stress_level
                if self.score < 0:
                    self.score = 0
                self.game.score += self.score

                self.game.airport.airspace.planes_in_airspace.remove(self)

    def interpolate(self, p1, p2, t):
        x1, y1, angle1 = p1
        x2, y2, angle2 = p2
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        angle = angle1 + (angle2 - angle1) * t
        return (x, y, angle)

    def rotate_image(self, image, angle):
        return pygame.transform.rotate(image, -angle)

    def draw(self, screen):
        x = 1800
        y = 400
        screen_texture = self.texture
        angle = 0

        if self.state == 0:
            pass

        elif self.state == 1:
            x = 1920 - self.progress * 5
            y = 410

        elif self.state == 2:

            x = 1420 - self.progress * 3.6
            y = 410
        elif self.state == 3:
            y = 445
            if self.progress <= 50:
                x = 1100 - self.progress * 13
            else:
                x = 1100 - 650

        elif self.state == 4:
            waypoints = self.get_waypoints()
            # Determine the current and next waypoints based on progress
            num_segments = len(waypoints) - 1
            total_progress = (self.progress / 100) * num_segments  # Scale progress to number of segments
            segment_index = int(total_progress)  # Get the current segment index
            segment_t = total_progress - segment_index  # Get the progress within the current segment

            if segment_index >= num_segments:
                segment_index = num_segments - 1
                segment_t = 1.0

            start_point = waypoints[segment_index]
            end_point = waypoints[segment_index + 1]

            x, y, angle = self.interpolate(start_point, end_point, segment_t)

        elif self.state == 7:
            y = 405
            if self.progress >= 10:
                x = 750 - self.progress * 9
            else:
                x = 750
        elif self.state == 8:
            y = 400
            x = 90 - self.progress * 4
        print(self.progress)

        if self.state in [1, 2]:
            display_speed = round(self.speed + self.speed_fluctuation)
            display_altitude = round(self.altitude + self.altitude_fluctuation)
            screen_texture = pygame.transform.scale(self.texture, (self.transform_x, self.transform_y))
            plane_callsign_text = self.game.UI.font_small.render(f"{self.callsign}", True, (255, 255, 255))
            plane_height_text = self.game.UI.font_small.render(f"{display_altitude} ft @ {round(display_speed)} kts",
                                                               True,
                                                               (255, 255, 255))
            screen.blit(plane_callsign_text,
                        (x - plane_callsign_text.get_width() / 2 + self.transform_x / 2, y + self.transform_y + 5))
            screen.blit(plane_height_text,
                        (x - plane_height_text.get_width() / 2 + self.transform_x / 2, y + self.transform_y + 20))
            screen.blit(screen_texture, (x, y))
        elif self.state == 4:
            # Rotate the image
            screen_texture = self.rotate_image(screen_texture, angle)

            # Calculate the top-left corner of the image to center it on (x, y)
            image_x = x - screen_texture.get_width() / 2
            image_y = y - screen_texture.get_height() / 2

            # Blit (draw) the image on the screen at the calculated position
            screen.blit(screen_texture, (image_x, image_y))
        elif self.state == 8:
            clip_rect = pygame.Rect(0, 0, 77, 580)
            # Get the current texture and calculate its destination rectangle
            screen_texture = pygame.transform.scale(self.texture, (self.transform_x, self.transform_y))
            image_rect = screen_texture.get_rect(topleft=(x, y))

            # Calculate the visible part of the image within the clipping rectangle
            visible_rect = clip_rect.clip(image_rect)
            if visible_rect.width > 0 and visible_rect.height > 0:
                source_rect = pygame.Rect(
                    visible_rect.x - x,
                    visible_rect.y - y,
                    visible_rect.width,
                    visible_rect.height
                )

                # Blit the part of the image that is within the clipping rectangle
                screen.blit(screen_texture, visible_rect.topleft, source_rect)
        else:
            clip_rect = pygame.Rect(88, 193, 1001, 382)

            # Get the current texture and calculate its destination rectangle with the center at (x, y)
            screen_texture = self.texture
            image_rect = screen_texture.get_rect(center=(x, y))

            # Calculate the visible part of the image within the clipping rectangle
            visible_rect = clip_rect.clip(image_rect)
            if visible_rect.width > 0 and visible_rect.height > 0:
                source_rect = pygame.Rect(
                    visible_rect.x - image_rect.x,
                    visible_rect.y - image_rect.y,
                    visible_rect.width,
                    visible_rect.height
                )

                # Blit the part of the image that is within the clipping rectangle
                screen.blit(screen_texture, visible_rect.topleft, source_rect)

    # TODO display callsign in other states
