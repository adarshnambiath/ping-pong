import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        # 🎵 Load sound effects
        self.hit_sound = pygame.mixer.Sound("/Users/adarsh/Documents/College/Sem-5/SE/ping-pong/game/paddle_hit.wav")
        self.wall_sound = pygame.mixer.Sound("/Users/adarsh/Documents/College/Sem-5/SE/ping-pong/game/wall_bounce.wav")
        self.score_sound = pygame.mixer.Sound("/Users/adarsh/Documents/College/Sem-5/SE/ping-pong/game/coin.mp3")

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom walls
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            self.wall_sound.play()  # 🎵 play wall bounce sound

    def check_collision(self, player, ai):
        if self.rect().colliderect(player.rect()):
            self.x = player.x + player.width
            self.velocity_x *= -1
            self.hit_sound.play()  # 🎵 paddle hit sound

        elif self.rect().colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x *= -1
            self.hit_sound.play()  # 🎵 paddle hit sound

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.score_sound.play()  # 🎵 play score sound

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
