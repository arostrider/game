from pathlib import Path


class GameWindow:
    CAPTION = "Testing out Pygame!"
    WIDTH = 640
    HEIGHT = 480
    FPS = 30
    BACKGROUND_COLOR = (50, 200, 255)


class ContentDir:
    ROOT = Path("../content")
    GRAPHICS = ROOT / "graphics"
