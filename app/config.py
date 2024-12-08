import pygame, os, yaml, json

project_root = os.path.dirname(os.path.dirname(__file__))

def load_config(file_name):
    file_path = os.path.join(project_root, file_name)
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

def load_json(file_name):
    file_path = os.path.join(project_root, "app", "config", file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Utility function to convert HEX to RGB
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

static_config = load_config(os.path.join("app", "config", "static_config.yaml"))
dynamic_config = load_config("config.yaml")

# General App Settings
APP_TITLE = static_config["general"]["app_title"]
APP_FPS = static_config["general"]["fps"]

# Rasberry Pi Screen dimensions
SCREEN_WIDTH = static_config["general"]["screen_width"]
SCREEN_HEIGHT = static_config["general"]["screen_height"]

# Fonts
font_name = static_config["fonts"]["font"]
font_path = os.path.join(project_root, "fonts", font_name)
font_size_large = dynamic_config["appearance"]["font_size_large"]
font_size_med = dynamic_config["appearance"]["font_size_med"]
font_size_small = dynamic_config["appearance"]["font_size_small"]

# Initialize Pygame for Loading Fonts
pygame.init()

try:
    FONT_LARGE = pygame.font.Font(font_path, font_size_large)
    FONT_MED = pygame.font.Font(font_path, font_size_med)
    FONT_SMALL = pygame.font.Font(font_path, font_size_small)

except FileNotFoundError:
    print(f"Error: Font files not found in {font_path}")
    pygame.quit()
    exit()

# Keyboard Settings
KEYBOARD_LAYOUT = static_config["keyboard"]["layout"]

romaji_json_name = static_config["keyboard"]["romaji_json_name"]
ROMAJI_MAP = load_json(romaji_json_name)

BACKGROUND_COLOR = dynamic_config["appearance"]["background_color"]
FONT_COLOR = dynamic_config["appearance"]["font_color"]
BUTTON_COLOR = dynamic_config["appearance"]["button_color"]
BUTTON_HOVER_COLOR = dynamic_config["appearance"]["button_hover_color"]
SEARCH_BAR_COLOR = dynamic_config["appearance"]["search_bar_color"]
SEARCH_ACTIVE_COLOR = dynamic_config["appearance"]["search_active_color"]
KEYBOARD_ACTIVE_COLOR = dynamic_config["appearance"]["keyboard_active_color"]