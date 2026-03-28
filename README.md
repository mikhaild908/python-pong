# Python Pong

A classic two-player Pong game built with Python and [pygame](https://www.pygame.org/).

## Overview

Two paddles, one ball, escalating speed. Each time the ball hits a paddle, it speeds up by 5% — keeping rallies tense. A point is scored when the ball exits the left or right edge of the screen. The serve alternates direction after each point.

![Python](https://img.shields.io/badge/python-3.8%2B-blue) ![pygame](https://img.shields.io/badge/pygame-2.x-green)

---

## Installation

**Requirements:** Python 3.8+ and pip.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/python-pong.git
cd python-pong

# 2. Install the only dependency
pip install pygame
```

---

## Usage

```bash
python pong.py
```

### Controls

| Action        | Left Player | Right Player |
|---------------|-------------|--------------|
| Move Up       | `W`         | `↑`          |
| Move Down     | `S`         | `↓`          |
| Quit          | `Esc`       | `Esc`        |

---

## File Structure

```
python-pong/
├── pong.py        # All game code: constants, Paddle/Ball classes, main loop
└── test_pong.py   # pytest test suite for Paddle and Ball logic
```

### `pong.py`

The entire game lives here, organized into three sections:

- **Constants block** — all tunable values (window size, speeds, colors, paddle dimensions, etc.) are defined at the top as module-level constants. Tweak here to adjust feel.
- **`Paddle` class** — wraps a `pygame.Rect`; handles clamped vertical movement and drawing.
- **`Ball` class** — wraps a `pygame.Rect`; handles movement, wall/paddle bouncing (with 1.05× speed escalation per hit), and center-respawn with alternating serve direction.
- **`main()` function** — the game loop: event handling → input → physics update → collision → scoring → draw.

### `test_pong.py`

Headless pytest suite (no window required). Covers:

- `Paddle` initialization, movement clamping, and type validation
- `Ball` initialization, reset/serve alternation, wall bouncing, paddle bouncing, and the zero-speed guard

---

## Running Tests

```bash
pip install pytest
pytest test_pong.py -v
```

No display or GPU required — the tests run in headless mode.

---

## Customization

All physics and visual values are constants at the top of `pong.py`:

| Constant              | Default | Effect                          |
|-----------------------|---------|---------------------------------|
| `WINDOW_WIDTH/HEIGHT` | 800×600 | Window size                     |
| `FPS`                 | 60      | Frame rate                      |
| `PADDLE_SPEED`        | 6       | How fast paddles move           |
| `BALL_INITIAL_SPEED_X`| 5       | Initial horizontal ball speed   |
| `BALL_INITIAL_SPEED_Y`| 4       | Initial vertical ball speed     |
| `PADDLE_HEIGHT`       | 90      | Paddle height in pixels         |

---

## Contributing

1. Fork the repository and create a feature branch.
2. Make your changes — keep all tunable values in the constants block.
3. Run the test suite and ensure it passes: `pytest test_pong.py -v`
4. Open a pull request with a clear description of your change.
