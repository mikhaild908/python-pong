import sys
import pygame

# --- Constants ---
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
FOREGROUND_COLOR = (255, 255, 255)

PADDLE_WIDTH = 12
PADDLE_HEIGHT = 90
PADDLE_SPEED = 6
PADDLE_MARGIN = 30  # distance from edge of screen

BALL_SIZE = 12
BALL_INITIAL_SPEED_X = 5
BALL_INITIAL_SPEED_Y = 4

SCORE_FONT_SIZE = 48


# --- Helper classes ---

class Paddle:
    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, dy: int) -> None:
        if not isinstance(dy, int):
            raise TypeError(f"dy must be an int, got {type(dy).__name__}")
        self.rect.y += dy
        # Clamp paddle inside the window
        self.rect.y = max(0, min(WINDOW_HEIGHT - PADDLE_HEIGHT, self.rect.y))

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, FOREGROUND_COLOR, self.rect)


class Ball:
    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        self.rect = pygame.Rect(
            WINDOW_WIDTH // 2 - BALL_SIZE // 2,
            WINDOW_HEIGHT // 2 - BALL_SIZE // 2,
            BALL_SIZE,
            BALL_SIZE,
        )
        # Alternate serve direction each reset
        if not hasattr(self, "speed_x"):
            self.speed_x = BALL_INITIAL_SPEED_X
        else:
            self.speed_x = -self.speed_x
        self.speed_y = BALL_INITIAL_SPEED_Y

    def update(self) -> None:
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Bounce off top and bottom edges
        if self.rect.top <= 0:
            self.rect.top = 0
            self.speed_y = abs(self.speed_y)
        elif self.rect.bottom >= WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.speed_y = -abs(self.speed_y)

    def bounce_off_paddle(self) -> None:
        self.speed_x = -self.speed_x
        # Slightly increase speed on each hit for escalating difficulty
        self.speed_x = int(self.speed_x * 1.05) or self.speed_x

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, FOREGROUND_COLOR, self.rect)


# --- Main game logic ---

def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pong")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, SCORE_FONT_SIZE)

    # Place paddles vertically centered
    left_paddle = Paddle(PADDLE_MARGIN, WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    right_paddle = Paddle(
        WINDOW_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH,
        WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2,
    )
    ball = Ball()

    left_score = 0
    right_score = 0

    running = True
    while running:
        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # --- Paddle input ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_s]:
            left_paddle.move(PADDLE_SPEED)
        if keys[pygame.K_UP]:
            right_paddle.move(-PADDLE_SPEED)
        if keys[pygame.K_DOWN]:
            right_paddle.move(PADDLE_SPEED)

        # --- Ball update ---
        ball.update()

        # Ball collision with paddles
        if ball.rect.colliderect(left_paddle.rect) and ball.speed_x < 0:
            ball.rect.left = left_paddle.rect.right
            ball.bounce_off_paddle()
        elif ball.rect.colliderect(right_paddle.rect) and ball.speed_x > 0:
            ball.rect.right = right_paddle.rect.left
            ball.bounce_off_paddle()

        # --- Scoring: ball exits left or right side ---
        if ball.rect.right < 0:
            right_score += 1
            ball.reset()
        elif ball.rect.left > WINDOW_WIDTH:
            left_score += 1
            ball.reset()

        # --- Drawing ---
        screen.fill(BACKGROUND_COLOR)

        # Center dividing line
        pygame.draw.aaline(
            screen, FOREGROUND_COLOR,
            (WINDOW_WIDTH // 2, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT)
        )

        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)

        # Score display
        score_text = font.render(f"{left_score}   {right_score}", True, FOREGROUND_COLOR)
        screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
