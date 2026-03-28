import pytest
import pygame

import pong
from pong import (
    Ball,
    Paddle,
    BALL_INITIAL_SPEED_X,
    BALL_INITIAL_SPEED_Y,
    BALL_SIZE,
    PADDLE_HEIGHT,
    PADDLE_WIDTH,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)


# ---------------------------------------------------------------------------
# Session-scoped pygame initialisation (headless — no window required)
# ---------------------------------------------------------------------------

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Initialise pygame once for the entire test session."""
    pygame.display.init()
    pygame.font.init()
    yield
    pygame.quit()


# ---------------------------------------------------------------------------
# Shared fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def centered_paddle():
    """A paddle placed at the vertical centre of the screen."""
    x = 30
    y = WINDOW_HEIGHT // 2 - PADDLE_HEIGHT // 2
    return Paddle(x, y)


@pytest.fixture
def ball():
    """A freshly created ball (first serve → moving right)."""
    return Ball()


@pytest.fixture
def mock_surface():
    """A minimal off-screen surface usable for draw calls."""
    return pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))


# ===========================================================================
# Paddle
# ===========================================================================

class TestPaddleInit:
    def test_rect_position_matches_constructor_args(self):
        paddle = Paddle(50, 100)
        assert paddle.rect.x == 50
        assert paddle.rect.y == 100

    def test_rect_size_matches_constants(self):
        paddle = Paddle(0, 0)
        assert paddle.rect.width == PADDLE_WIDTH
        assert paddle.rect.height == PADDLE_HEIGHT


class TestPaddleMove:
    def test_move_down_increases_y(self, centered_paddle):
        original_y = centered_paddle.rect.y
        centered_paddle.move(10)
        assert centered_paddle.rect.y == original_y + 10

    def test_move_up_decreases_y(self, centered_paddle):
        original_y = centered_paddle.rect.y
        centered_paddle.move(-10)
        assert centered_paddle.rect.y == original_y - 10

    def test_move_zero_does_not_change_position(self, centered_paddle):
        original_y = centered_paddle.rect.y
        centered_paddle.move(0)
        assert centered_paddle.rect.y == original_y

    def test_clamp_at_top_edge(self):
        paddle = Paddle(30, 0)
        paddle.move(-50)  # attempt to go above the screen
        assert paddle.rect.y == 0

    def test_clamp_at_bottom_edge(self):
        paddle = Paddle(30, WINDOW_HEIGHT - PADDLE_HEIGHT)
        paddle.move(50)  # attempt to go below the screen
        assert paddle.rect.y == WINDOW_HEIGHT - PADDLE_HEIGHT

    def test_clamp_prevents_partial_overlap_at_bottom(self):
        paddle = Paddle(30, WINDOW_HEIGHT - PADDLE_HEIGHT - 5)
        paddle.move(100)
        assert paddle.rect.bottom <= WINDOW_HEIGHT

    # Note: bool is a subclass of int in Python, so True/False are accepted by
    # isinstance(dy, int) and are intentionally excluded from this parametrize list.
    @pytest.mark.parametrize("bad_value", [1.5, "up", None])
    def test_non_int_dy_raises_type_error(self, centered_paddle, bad_value):
        with pytest.raises(TypeError):
            centered_paddle.move(bad_value)

    def test_type_error_message_includes_actual_type(self, centered_paddle):
        with pytest.raises(TypeError, match="float"):
            centered_paddle.move(3.0)


class TestPaddleDraw:
    def test_draw_does_not_raise(self, centered_paddle, mock_surface):
        centered_paddle.draw(mock_surface)  # should complete without error


# ===========================================================================
# Ball
# ===========================================================================

class TestBallInit:
    def test_ball_starts_at_centre(self, ball):
        expected_x = WINDOW_WIDTH // 2 - BALL_SIZE // 2
        expected_y = WINDOW_HEIGHT // 2 - BALL_SIZE // 2
        assert ball.rect.x == expected_x
        assert ball.rect.y == expected_y

    def test_ball_has_correct_size(self, ball):
        assert ball.rect.width == BALL_SIZE
        assert ball.rect.height == BALL_SIZE

    def test_first_serve_moves_right(self, ball):
        assert ball.speed_x > 0

    def test_initial_speed_x_matches_constant(self, ball):
        assert ball.speed_x == BALL_INITIAL_SPEED_X

    def test_initial_speed_y_matches_constant(self, ball):
        assert ball.speed_y == BALL_INITIAL_SPEED_Y


class TestBallReset:
    def test_reset_centres_ball(self, ball):
        ball.rect.x = 0
        ball.rect.y = 0
        ball.reset()
        assert ball.rect.x == WINDOW_WIDTH // 2 - BALL_SIZE // 2
        assert ball.rect.y == WINDOW_HEIGHT // 2 - BALL_SIZE // 2

    def test_reset_restores_speed_y(self, ball):
        ball.speed_y = 99
        ball.reset()
        assert ball.speed_y == BALL_INITIAL_SPEED_Y

    def test_reset_alternates_serve_direction(self, ball):
        first_direction = ball.speed_x
        ball.reset()
        assert ball.speed_x == -first_direction

    def test_reset_alternates_twice_returns_original_direction(self, ball):
        original = ball.speed_x
        ball.reset()
        ball.reset()
        assert ball.speed_x == original

    def test_reset_multiple_times_always_alternates(self, ball):
        directions = [ball.speed_x]
        for _ in range(5):
            ball.reset()
            directions.append(ball.speed_x)
        # Each consecutive pair must be opposite in sign
        for a, b in zip(directions, directions[1:]):
            assert (a > 0) != (b > 0)


class TestBallUpdate:
    def test_update_moves_ball_in_x(self, ball):
        original_x = ball.rect.x
        ball.update()
        assert ball.rect.x == original_x + ball.speed_x

    def test_update_moves_ball_in_y(self, ball):
        original_y = ball.rect.y
        original_speed_y = ball.speed_y
        ball.update()
        assert ball.rect.y == original_y + original_speed_y

    def test_bounce_off_top_wall_reflects_speed_y(self, ball):
        ball.rect.top = 0
        ball.speed_y = -3
        ball.update()
        assert ball.speed_y > 0

    def test_bounce_off_top_wall_clamps_position(self, ball):
        ball.rect.top = 0
        ball.speed_y = -3
        ball.update()
        assert ball.rect.top >= 0

    def test_bounce_off_bottom_wall_reflects_speed_y(self, ball):
        ball.rect.bottom = WINDOW_HEIGHT
        ball.speed_y = 3
        ball.update()
        assert ball.speed_y < 0

    def test_bounce_off_bottom_wall_clamps_position(self, ball):
        ball.rect.bottom = WINDOW_HEIGHT
        ball.speed_y = 3
        ball.update()
        assert ball.rect.bottom <= WINDOW_HEIGHT

    def test_no_wall_bounce_when_mid_screen(self, ball):
        ball.rect.y = WINDOW_HEIGHT // 2
        ball.speed_y = 3
        ball.update()
        assert ball.speed_y == 3  # unchanged


class TestBallBounceOffPaddle:
    def test_reverses_speed_x(self, ball):
        ball.speed_x = 5
        ball.bounce_off_paddle()
        assert ball.speed_x < 0

    def test_speed_increases_on_each_bounce(self, ball):
        # Use a value large enough that int(x * 1.05) > x after truncation
        ball.speed_x = 20
        ball.bounce_off_paddle()
        assert abs(ball.speed_x) > 20

    def test_speed_multiplier_is_roughly_1_05(self, ball):
        ball.speed_x = 100  # large enough that int() rounding is negligible
        ball.bounce_off_paddle()
        assert abs(ball.speed_x) == int(100 * 1.05)

    def test_speed_never_rounds_to_zero(self, ball):
        # With small speeds the 1.05× factor can round to 0; the guard must prevent that
        ball.speed_x = 1
        for _ in range(20):
            ball.bounce_off_paddle()
            assert ball.speed_x != 0

    def test_direction_flips_on_consecutive_bounces(self, ball):
        ball.speed_x = 5
        ball.bounce_off_paddle()
        assert ball.speed_x < 0
        ball.bounce_off_paddle()
        assert ball.speed_x > 0


class TestBallDraw:
    def test_draw_does_not_raise(self, ball, mock_surface):
        ball.draw(mock_surface)  # should complete without error
