import pygame
import os

# Initialize Pygame
pygame.init()

# Font file paths
japanese_font_path = os.path.join(os.path.dirname(__file__), "fonts", "Noto Sans Mono CJK JP Regular.otf")

# Load fonts
try:
    japanese_font = pygame.font.Font(japanese_font_path, 24)
except FileNotFoundError:
    print(f"Error: Font files not found in {japanese_font_path}")
    pygame.quit()
    exit()

# Rasberry Pi Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

# Utility function to convert HEX to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Colors
WHITE = hex_to_rgb("#FFFFFF")
BLACK = hex_to_rgb("#000000")
GRAY = hex_to_rgb("#C8C8C8")
RED = hex_to_rgb("#FF0000")
BLUE = hex_to_rgb("#0000FF")

button_color = (70, 130, 180)  # SteelBlue
hover_color = (100, 149, 237)  # CornflowerBlue
text_color = (255, 255, 255)   # White