# main.py
import pygame
from app_manager import AppManager
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
import os, sys

def is_raspberry_pi():
    # Detect if running on Raspberry Pi
    return os.name.startswith("arm")

def main():
    pygame.init()
    
    # Check if running on Raspberry Pi for full-screen mode
    if is_raspberry_pi():
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pygame.display.set_caption("KANJI TRAINER")

    app_manager = AppManager(screen)
    app_manager.run()

    pygame.quit()

    sys.exit()

if __name__ == "__main__":
    main()
