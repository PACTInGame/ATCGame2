import sys

import pygame

from Button import Button
from Colors import colors
from GameController import GameController
from threading import Thread


class GameUI:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 1920, 1080
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game Window")
        self.clock = pygame.time.Clock()
        self.game_instance = GameController(self)
        self.plane_buttons = []
        self.state = 'menu'
        self.font = pygame.font.SysFont('Roboto', 25)  # font for notifications
        self.font_small = pygame.font.SysFont('Roboto', 15)  # font for notifications
        self.background = pygame.image.load('assets/Background.png')
        self.airport = pygame.image.load('assets/Airport.png')

        self.approach_communications = []
        self.tower_communications = []
        self.ground_communications = []
        # Define buttons
        self.buttons = {
            'menu': [
                Button((0, 0, 50), 860, 400, 200, 80, 'Start'),
                Button((0, 0, 50), 860, 500, 200, 80, 'Options'),
                Button((0, 0, 50), 860, 600, 200, 80, 'Quit')
            ],
            'play': [],
            'plane': [],
            'pause': [
                Button((0, 0, 50), 860, 500, 200, 80, 'Resume')
            ],
            'radio': [
                Button((0, 40, 40), 20, 20, 190, 50, '1: Radar Contact', 20),
                Button((0, 40, 40), 20, 90, 190, 50, '2: Contact Tower', 20),
                Button((0, 50, 0), 20, 180, 190, 50, '3: Clear to Land', 20),
                Button((0, 50, 0), 20, 250, 190, 50, '4: Wind Information', 20),
                Button((0, 50, 0), 20, 320, 190, 50, '5: Contact Ground', 20),
                Button((40, 40, 0), 20, 410, 190, 50, '6: Taxi to Gate', 20),
                Button((40, 40, 0), 20, 480, 190, 50, '7: Pushback and Startup', 20),
                Button((40, 40, 0), 20, 550, 190, 50, '8: Taxi to Runway', 20),
                Button((40, 40, 0), 20, 620, 190, 50, '9: Contact Tower', 20),
                Button((0, 50, 0), 20, 710, 190, 50, '10: Line up and Wait', 20),
                Button((0, 50, 0), 20, 780, 190, 50, '11: Clear for Takeoff', 20),
                Button((0, 50, 0), 20, 850, 190, 50, '12: Contact Departure', 20),
                Button((40, 40, 40), 20, 920, 190, 50, '13: Go Around', 20)
            ]
        }

        # Red close button common to all states
        self.close_button = Button((70, 0, 0), 1720, 20, 180, 60, 'Close')

    def start_game(self):
        print("Starting game...")
        self.state = 'play'
        thread = Thread(target=self.game_instance.start_game)
        thread.start()

    def show_options(self):
        print("Showing options...")
        # Add your options handling here

    def quit_game(self):
        self.game_instance.running = False
        pygame.quit()
        sys.exit()

    def resume_game(self):
        print("Resuming game...")
        self.state = 'play'

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if self.close_button.is_over(mouse_pos):
                    self.quit_game()

                if self.state == 'menu':
                    for button in self.buttons[self.state]:
                        if button.is_over(mouse_pos):

                            if button.text == 'Start':
                                self.start_game()
                            elif button.text == 'Options':
                                self.show_options()
                            elif button.text == 'Quit':
                                self.quit_game()
                elif self.state == 'play':
                    pass
                elif self.state == 'pause':
                    for button in self.buttons[self.state]:
                        if button.is_over(mouse_pos):

                            if button.text == 'Resume':
                                self.resume_game()
                elif self.state == 'radio':
                    for button in self.buttons[self.state]:
                        if button.is_over(mouse_pos):
                            self.game_instance.handle_radio_selection(button.text)

                elif self.state == 'plane':
                    for button in self.plane_buttons:
                        if button.is_over(mouse_pos):
                            self.game_instance.handle_plane_selection(button.text)

    def draw_texts(self):

        score_text = self.font.render(f"Score: {self.game_instance.score}", True, colors['PINK'])
        self.screen.blit(score_text, (self.WIDTH / 2 - score_text.get_width() / 2, 45 - score_text.get_height()))

        approach_text = self.font.render("Approach 120.5", True, colors['BLUE'])
        self.screen.blit(approach_text, (self.WIDTH - 550, self.HEIGHT - 220 - score_text.get_height()))

        tower_text = self.font.render("Tower 118.1", True, colors['GREEN'])
        self.screen.blit(tower_text, (self.WIDTH - 1100, self.HEIGHT - 220 - score_text.get_height()))

        ground_text = self.font.render("Ground 121.9", True, colors['ORANGE'])
        self.screen.blit(ground_text, (self.WIDTH - 1650, self.HEIGHT - 220 - score_text.get_height()))
        if len(self.approach_communications) > 7:
            self.approach_communications.pop(0)
        if len(self.tower_communications) > 7:
            self.tower_communications.pop(0)
        if len(self.ground_communications) > 7:
            self.ground_communications.pop(0)
        for i, text in enumerate(self.approach_communications):
            color = colors['BLUE'] if text[2] == 1 else colors['WHITE']
            text_surface = self.font.render(text[1], True, color)
            self.screen.blit(text_surface, (self.WIDTH - 550, self.HEIGHT - 20 - i * 30))

        for i, text in enumerate(self.tower_communications):
            color = colors['GREEN'] if text[2] == 1 else colors['WHITE']
            text_surface = self.font.render(text[1], True, color)
            self.screen.blit(text_surface, (self.WIDTH - 1100, self.HEIGHT - 20 - i * 30))

        for i, text in enumerate(self.ground_communications):
            color = colors['ORANGE'] if text[2] == 1 else colors['WHITE']
            text_surface = self.font.render(text[1], True, color)
            self.screen.blit(text_surface, (self.WIDTH - 1650, self.HEIGHT - 20 - i * 30))

    def draw_buttons(self):
        for button in self.buttons[self.state]:
            button.draw(self.screen)
        if self.state == 'plane':
            for button in self.plane_buttons:
                button.draw(self.screen)
        self.close_button.draw(self.screen)

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def draw_planes_airspace(self):
        planes = self.game_instance.airport.airspace.planes_about_to_enter_airspace + self.game_instance.airport.airspace.planes_in_airspace + self.game_instance.airport.planes_at_airport
        for plane in planes:
            if plane.state in [1, 2, 8]:
                plane.draw(self.screen)

    def draw_airport(self):
        self.screen.blit(self.airport, (78, 180))

    def draw_planes_airport(self):
        planes = self.game_instance.airport.airspace.planes_about_to_enter_airspace + self.game_instance.airport.airspace.planes_in_airspace + self.game_instance.airport.planes_at_airport
        for plane in planes:
            if 3 <= plane.state <= 7:
                plane.draw(self.screen)

    def run(self):
        while True:
            self.handle_events()
            if self.state != 'menu':
                self.draw_background()
                self.draw_planes_airspace()
                self.draw_airport()
                self.draw_planes_airport()
            else:
                self.screen.fill((0, 0, 0))

            self.draw_buttons()

            if self.state == 'play' or self.state == 'plane' or self.state == 'radio':
                self.draw_texts()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    game = GameUI()
    game.run()
