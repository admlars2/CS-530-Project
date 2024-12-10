import pygame
from .ui import MainMenu, Database, StudyMenu, Word
from .config import BACKGROUND_COLOR, FONT_COLOR, FONT_MED
from .ui.elements import Button, FlipScreenButton
from .database import DBManager

class AppManager:
    # Page keys
    MAIN = 'main'
    DATABASE = 'database'
    STUDYMENU = 'study_menu'
    WORD = 'word'

    PAGE_KEYS = {MAIN, DATABASE, STUDYMENU, WORD}

    def __init__(self, screen: pygame.Surface):
        self.db_manager = DBManager()

        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.screen = screen
        self.background_color = BACKGROUND_COLOR
        self.font_color = FONT_COLOR
        self.is_portrait = True
        self.font = FONT_MED
        self.clock = pygame.time.Clock()
        self.running = True

        self.default_header = [
            FlipScreenButton(self, (0.9, 0.1, 0.1, 0.05)),
            Button(self, (0.1, 0.1, 0.1, 0.05), "←")
        ]

        self.default_header[1].on_click = lambda: self.change_page(self.MAIN)

        # Create pages after that might use previously defined variables
        self.pages = {
            self.MAIN: MainMenu(screen, self),
            self.DATABASE: Database(screen, self),
            self.STUDYMENU: StudyMenu(screen, self),
            self.WORD: Word(screen, self)
        }

        self.current_page = self.pages[self.MAIN]  # Pass self as manager

    def close_dbs(self):
        self.db_manager.close()

    def set_background_color(self, color):
        """Change the background color."""
        self.background_color = color

    def set_font_color(self, color):
        """Change the font color."""
        self.font_color = color

    def toggle_orientation(self):
        """Toggle between portrait and landscape modes."""
        self.is_portrait = not self.is_portrait

    def change_page(self, page_key: str):
        if page_key in self.PAGE_KEYS:
            self.current_page = self.pages[page_key]

    def handle_event(self, event: pygame.event.Event):
        """Forward events to the current page."""
        self.current_page.handle_event(event)

    def render(self):
        """Render the current page."""
        self.screen.fill(self.background_color)
        self.current_page.render()

    def update(self):
        """Update the current page."""
        self.current_page.update()

    def run(self):
        """Main loop."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.handle_event(event)
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)

    def map_rect(self, x_prop, y_prop, width_prop, height_prop, corrected=False):
        """Map proportional coordinates to pixel coordinates based on orientation."""
        if self.is_portrait:
            # Swap width and height proportions for rotation
            width = height_prop * self.screen_width
            height = width_prop * self.screen_height

            # Map coordinates and adjust for the center of rotation
            x_pixel = y_prop * self.screen_width
            x_pixel_prop = (1-x_prop) if x_prop != 0 else x_prop
            x_pixel_prop = x_pixel_prop if not corrected else (1-x_prop-width_prop)
            y_pixel = x_pixel_prop * self.screen_height
        else:
            # Standard calculation for landscape orientation
            width = width_prop * self.screen_width
            height = height_prop * self.screen_height

            x_pixel = x_prop * self.screen_width
            y_pixel = y_prop * self.screen_height

        # Convert to integers and return all values
        return int(x_pixel), int(y_pixel), int(width), int(height)
    
    def render_svg(self, svg_path, x, y, width, height):
        png_image = pygame.image.load(svg_path)

        scaled_image = pygame.transform.smoothscale(png_image, (width, height))
        if self.is_portrait:
            scaled_image = pygame.transform.rotate(scaled_image, 90)
        self.screen.blit(scaled_image, (x, y))