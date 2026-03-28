# Copilot Instructions

## Running the Game

```bash
python pong.py
```

Requires `pygame` (`pip install pygame`).

## Architecture

All game logic lives in a single file, `pong.py`, structured as:

- **Constants block** at the top — all tunable values (window size, speeds, colors, etc.) are defined here as module-level constants.
- **`Paddle` class** — wraps a `pygame.Rect`, handles clamped movement and drawing.
- **`Ball` class** — wraps a `pygame.Rect`, handles physics (movement, wall bouncing, paddle bouncing with speed escalation), and resets with alternating serve direction.
- **`main()` function** — owns the game loop: event handling → input → update → collision → scoring → draw.

## Key Conventions

- All visual/physics tuning goes in the constants block, not inline.
- `Ball.bounce_off_paddle()` applies a 1.05× speed multiplier each hit; the `or self.speed_x` guard prevents the speed from rounding to zero.
- Paddle collision checks guard on `ball.speed_x` direction to prevent the ball from sticking inside a paddle.
- Controls: **W/S** — left paddle, **↑/↓** — right paddle, **Esc** — quit.
