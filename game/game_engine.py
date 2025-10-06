import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.win_font = pygame.font.SysFont("Arial", 60)

        # Default target score (Best of 5)
        self.winning_score = 5

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self, screen):
        self.ball.move()

        # Collision with paddles
        if self.ball.rect().colliderect(self.player.rect()):
            self.ball.x = self.player.x + self.player.width
            self.ball.velocity_x *= -1
            self.ball.hit_sound.play() 
        elif self.ball.rect().colliderect(self.ai.rect()):
            self.ball.x = self.ai.x - self.ball.width
            self.ball.velocity_x *= -1
            self.ball.hit_sound.play() 

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.score_sound.play()
            self.ball.reset()
        elif self.ball.x + self.ball.width >= self.width:
            self.player_score += 1
            self.ball.score_sound.play()
            self.ball.reset()

        # AI follows ball
        self.ai.auto_track(self.ball, self.height)

        # Check game over
        self.check_game_over(screen)

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

    def check_game_over(self, screen):
        if self.player_score >= self.winning_score or self.ai_score >= self.winning_score:
            winner_text = "Player Wins!" if self.player_score > self.ai_score else "AI Wins!"
            text_surface = self.win_font.render(winner_text, True, WHITE)
            screen.fill(BLACK)
            screen.blit(text_surface, (self.width // 2 - text_surface.get_width() // 2, self.height // 2 - 100))
            pygame.display.flip()
            pygame.time.delay(1500)
            self.show_replay_menu(screen)

    def show_replay_menu(self, screen):
        screen.fill(BLACK)

        menu_font = pygame.font.SysFont("Arial", 40)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]

        for i, option in enumerate(options):
            text = menu_font.render(option, True, WHITE)
            screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - 80 + i * 50))

        pygame.display.flip()

        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        self.winning_score = 2  # Best of 3 → first to 2
                        waiting = False
                    elif event.key == pygame.K_5:
                        self.winning_score = 3  # Best of 5 → first to 3
                        waiting = False
                    elif event.key == pygame.K_7:
                        self.winning_score = 4  # Best of 7 → first to 4
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

        # Reset scores and ball
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.player.height // 2
        self.ai.y = self.height // 2 - self.ai.height // 2
        screen.fill(BLACK)
        pygame.display.flip()
        pygame.time.delay(500)
