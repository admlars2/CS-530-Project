import pygame, sys, platform
from .app_manager import AppManager
from .config import SCREEN_WIDTH, SCREEN_HEIGHT

def is_raspberry_pi():
    # Check for Raspberry Pi using environment variables
    return platform.system() == 'Linux'

def run_app():
    pygame.init()
    
    # Check if running on Raspberry Pi for full-screen mode
    if is_raspberry_pi():
        pygame.event.set_blocked(pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEWHEEL)
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF)
        print("Entering PI Mode...")
    else:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    pygame.display.set_caption("KANJI TRAINER")

    app_manager = AppManager(screen)
    app_manager.run()

    app_manager.close_dbs()

    pygame.quit()
    sys.exit()