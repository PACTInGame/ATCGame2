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
        self.font = pygame.font.SysFont('Roboto', 30)  # font for notifications

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
                Button((0, 40, 40), 20, 20, 200, 60, '1: Radar Contact', 20),
                Button((0, 40, 40), 20, 100, 200, 60, '2: Contact Tower', 20),
                Button((0, 50, 0), 20, 200, 200, 60, '3: Clear to Land', 20),
                Button((0, 50, 0), 20, 280, 200, 60, '4: Wind Information', 20),
                Button((0, 50, 0), 20, 360, 200, 60, '5: Contact Ground', 20),
                Button((40, 40, 0), 20, 460, 200, 60, '6: Taxi to Gate', 20),
                Button((40, 40, 0), 20, 540, 200, 60, '7: Pushback and Startup', 20),
                Button((40, 40, 0), 20, 620, 200, 60, '8: Taxi to Runway', 20),
                Button((40, 40, 0), 20, 700, 200, 60, '9: Line up and Wait', 20),
                Button((40, 40, 0), 20, 780, 200, 60, '10: Clear for Takeoff', 20),
                Button((40, 40, 0), 20, 860, 200, 60, '11: Contact Departure', 20),
                Button((40, 40, 40), 20, 940, 200, 60, '12: Go Around', 20)
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
                    self.close_button.color = (200, 0, 0)
                    self.close_button.draw(self.screen)
                    self.close_button.color = (255, 0, 0)
                    self.quit_game()

                if self.state == 'menu':
                    for button in self.buttons[self.state]:
                        if button.is_over(mouse_pos):
                            button.color = (0, 0, 200)
                            button.draw(self.screen)
                            button.color = (0, 0, 255)
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
                            button.color = (0, 0, 200)
                            button.draw(self.screen)
                            button.color = (0, 0, 255)
                            if button.text == 'Resume':
                                self.resume_game()
                elif self.state == 'radio':
                    for button in self.buttons[self.state]:
                        if button.is_over(mouse_pos):
                            button.color = (0, 0, 200)
                            button.draw(self.screen)
                            button.color = (0, 0, 255)
                            self.game_instance.handle_radio_selection(button.text)

                elif self.state == 'plane':
                    for button in self.plane_buttons:
                        if button.is_over(mouse_pos):
                            button.color = (0, 0, 200)
                            button.draw(self.screen)
                            button.color = (0, 0, 255)
                            self.game_instance.handle_plane_selection(button.text)

    def draw_texts(self):

        score_text = self.font.render(f"Score: {self.game_instance.score}", True, colors['PINK'])
        self.screen.blit(score_text, (self.WIDTH / 2 - score_text.get_width() / 2, 45 - score_text.get_height()))
        if len(self.approach_communications) > 6:
            self.approach_communications.pop(0)
        if len(self.tower_communications) > 6:
            self.tower_communications.pop(0)
        if len(self.ground_communications) > 6:
            self.ground_communications.pop(0)
        for i, text in enumerate(self.approach_communications):
            color = colors['BLUE'] if text[2] == 1 else colors['WHITE']
            text_surface = self.font.render(text[1], True, color)
            self.screen.blit(text_surface, (self.WIDTH - 520 - score_text.get_width(), self.HEIGHT - 20 - i * 30))

        for i, text in enumerate(self.tower_communications):
            color = colors['GREEN'] if text[2] == 1 else colors['WHITE']
            text_surface = self.font.render(text[1], True, color)
            self.screen.blit(text_surface, (self.WIDTH - 1040 - score_text.get_width(), self.HEIGHT - 20 - i * 30))

        for i, text in enumerate(self.ground_communications):
            color = colors['ORANGE'] if text[2] == 1 else colors['WHITE']
            text_surface = self.font.render(text[1], True, color)
            self.screen.blit(text_surface, (self.WIDTH - 1580 - score_text.get_width(), self.HEIGHT - 20 - i * 30))


    def draw_buttons(self):
        for button in self.buttons[self.state]:
            button.draw(self.screen)
        if self.state == 'plane':
            for button in self.plane_buttons:
                button.draw(self.screen)
        self.close_button.draw(self.screen)

    def run(self):
        while True:
            self.handle_events()
            self.screen.fill((0, 0, 0))
            self.draw_buttons()
            if self.state == 'play' or self.state == 'plane' or self.state == 'radio':
                self.draw_texts()
            pygame.display.flip()
            self.clock.tick(60)


if __name__ == '__main__':
    game = GameUI()
    game.run()
