import pygame
import os

# Initialize Pygame
pygame.init()

# Font file paths
japanese_font_path = os.path.join(os.path.dirname(__file__), "fonts", "Noto Sans Mono CJK JP Regular.otf")

# Load fonts
try:
    japanese_font = pygame.font.Font(japanese_font_path, 24)
    japanese_font_small = pygame.font.Font(japanese_font_path, 16)
    
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

KEYBOARD_LAYOUT = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM"
]

ROMAJI_MAP = {
    # Vowels
    "a": "あ", "i": "い", "u": "う", "e": "え", "o": "お",

    # K-group
    "ka": "か", "ki": "き", "ku": "く", "ke": "け", "ko": "こ",
    "kya": "きゃ", "kyu": "きゅ", "kyo": "きょ",

    # S-group
    "sa": "さ", "shi": "し", "su": "す", "se": "せ", "so": "そ",
    "sha": "しゃ", "shu": "しゅ", "sho": "しょ",

    # T-group
    "ta": "た", "chi": "ち", "tsu": "つ", "te": "て", "to": "と",
    "cha": "ちゃ", "chu": "ちゅ", "cho": "ちょ",

    # N-group
    "na": "な", "ni": "に", "nu": "ぬ", "ne": "ね", "no": "の",
    "nya": "にゃ", "nyu": "にゅ", "nyo": "にょ",

    # H-group
    "ha": "は", "hi": "ひ", "fu": "ふ", "he": "へ", "ho": "ほ",
    "hya": "ひゃ", "hyu": "ひゅ", "hyo": "ひょ",

    # M-group
    "ma": "ま", "mi": "み", "mu": "む", "me": "め", "mo": "も",
    "mya": "みゃ", "myu": "みゅ", "myo": "みょ",

    # Y-group
    "ya": "や", "yu": "ゆ", "yo": "よ",

    # R-group
    "ra": "ら", "ri": "り", "ru": "る", "re": "れ", "ro": "ろ",
    "rya": "りゃ", "ryu": "りゅ", "ryo": "りょ",

    # W-group
    "wa": "わ", "wo": "を",

    # N-group
    "nn": "ん",

    # G-group
    "ga": "が", "gi": "ぎ", "gu": "ぐ", "ge": "げ", "go": "ご",
    "gya": "ぎゃ", "gyu": "ぎゅ", "gyo": "ぎょ",

    # Z-group
    "za": "ざ", "ji": "じ", "zu": "ず", "ze": "ぜ", "zo": "ぞ",
    "ja": "じゃ", "ju": "じゅ", "jo": "じょ",

    # D-group
    "da": "だ", "dji": "ぢ", "dzu": "づ", "de": "で", "do": "ど",
    "dya": "ぢゃ", "dyu": "ぢゅ", "dyo": "ぢょ",

    # B-group
    "ba": "ば", "bi": "び", "bu": "ぶ", "be": "べ", "bo": "ぼ",
    "bya": "びゃ", "byu": "びゅ", "byo": "びょ",

    # P-group
    "pa": "ぱ", "pi": "ぴ", "pu": "ぷ", "pe": "ぺ", "po": "ぽ",
    "pya": "ぴゃ", "pyu": "ぴゅ", "pyo": "ぴょ",

    # Small Kana
    "la": "ぁ", "li": "ぃ", "lu": "ぅ", "le": "ぇ", "lo": "ぉ",
    "lya": "ゃ", "lyu": "ゅ", "lyo": "ょ",
    "ltsu": "っ",

    # Special compound sounds
    "v": "ゔ", "va": "ゔぁ", "vi": "ゔぃ", "vu": "ゔ", "ve": "ゔぇ", "vo": "ゔぉ",

    # Double consonants (small つ for pause sounds)
    "kka": "っか", "kki": "っき", "kku": "っく", "kke": "っけ", "kko": "っこ",
    "ssa": "っさ", "shi": "っし", "ssu": "っす", "sse": "っせ", "sso": "っそ",
    "tta": "った", "chi": "っち", "ttsu": "っつ", "tte": "って", "tto": "っと",
    "ppa": "っぱ", "ppi": "っぴ", "ppu": "っぷ", "ppe": "っぺ", "ppo": "っぽ",
    # Extend further if necessary
}