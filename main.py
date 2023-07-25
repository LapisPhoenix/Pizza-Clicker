import os
import random
import time
import json
import pygame

# Setup


class Game:
    def __init__(self):
        # Pygame setup
        pygame.init()

        # Window setup
        self.width, self.height = 1000, 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.clock = pygame.time.Clock()
        self.target_fps = 60
        pygame.display.set_caption("Pizza Clicker")
        icon = pygame.image.load("./assets/sprites/icon.png")
        pygame.display.set_icon(icon)

        # Logic
        self.stats = {}
        self.last_played_song = None
        self.is_playing_song = False

        # Pizza animation
        self.pizza_scale = 400  # original size is 800x800
        self.pizza_x = self.width / 2 - self.pizza_scale / 2
        self.pizza_y = self.height / 2 - self.pizza_scale / 2
        self.max_pizza_y_offset = 7
        self.at_origin = True
        self.pizza_y_offset = 0

        self.create_stats_file()

    def create_stats_file(self):
        files = os.listdir()
        if "stats.json" not in files:
            with open("stats.json", "w") as f:
                basic_data = {
                    "pizzas": 0,
                    "clickers": 0,
                    "pizzarias": 0,
                    "pizza_portals": 0
                }

                json.dump(basic_data, f)
                self.stats = basic_data
        else:
            with open("stats.json", "r") as f:
                try:
                    self.stats = json.load(f)
                except json.decoder.JSONDecodeError:
                    # Its broken, lets see if we can grab any data
                    f.seek(0)
                    data = f.read()
                    if data == "":
                        # File is empty
                        os.remove("stats.json")
                        self.create_stats_file()
                    else:
                        # File is not empty, but is broken
                        # Lets grab whatever data we can
                        self.stats = {}
                        for line in data.split("\n"):
                            if line != "":
                                key, value = line.split(":")
                                self.stats[key] = int(value)

                        # Now lets save it
                        os.remove("stats.json")
                        self.create_stats_file()
                        with open("stats.json", "w") as f:
                            json.dump(self.stats, f)

    def play_background_music(self):
        if self.is_playing_song:
            return

        if self.last_played_song is None:
            # Random song
            songs = os.listdir("./assets/sounds/")
            song = random.choice(songs)
            pygame.mixer.music.load(f"./assets/sounds/{song}")
            pygame.mixer.music.play()
            self.last_played_song = song
            self.is_playing_song = True
        else:
            # Play a random song, but make sure it's not the same as the last one
            songs = os.listdir("./assets/sounds/")
            song = random.choice(songs)

            while song == self.last_played_song:
                song = random.choice(songs)

            pygame.mixer.music.load(f"./assets/sounds/{song}")
            # Add a little pause
            time.sleep(random.randint(1, 3))
            pygame.mixer.music.play()
            self.last_played_song = song
            self.is_playing_song = True

    def animate_pizza(self):
        # Just a simple animation, float up and down
        pizza = pygame.image.load("./assets/sprites/pizza.png")
        pizza = pygame.transform.scale(pizza, (self.pizza_scale, self.pizza_scale))

        if self.at_origin:
            self.pizza_y_offset += 1
            if self.pizza_y_offset >= self.max_pizza_y_offset:
                self.at_origin = False
            else:
                self.pizza_y += 1
        else:
            self.pizza_y_offset -= 1
            if self.pizza_y_offset <= -self.max_pizza_y_offset:
                self.at_origin = True
            else:
                self.pizza_y -= 1

        # interpolate
        self.pizza_y += self.pizza_y_offset

        self.screen.blit(pizza, (self.pizza_x, self.pizza_y))


    def run(self):
        while self.running:
            # Play Background Music
            # Check if we are playing a song
            if pygame.mixer.music.get_busy():
                self.is_playing_song = True
            else:
                self.is_playing_song = False

            if not self.is_playing_song:
                self.play_background_music()

            self.screen.fill((0, 0, 0))

            # Draw background
            background = pygame.image.load("./assets/sprites/background.png")
            self.screen.blit(background, (0, 0))

            # Draw pizza
            self.animate_pizza()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.flip()
            self.clock.tick(self.target_fps)


if __name__ == "__main__":
    print("Thanks for playing my game!")
    game = Game()
    game.run()