import pygame
from ui import MainMenu, Database, StudyMenu
from constants import WHITE, GRAY, japanese_font, button_color, hover_color
from ui.elements import Button

class AppManager:
    # Page keys
    MAIN = 'main'
    DATABASE = 'database'
    STUDYMENU = 'study_menu'

    PAGE_KEYS = {MAIN, DATABASE, STUDYMENU}

    def __init__(self, screen: pygame.Surface):
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.screen = screen
        self.background_color = GRAY
        self.font_color = WHITE
        self.is_portrait = True
        self.font = japanese_font
        self.clock = pygame.time.Clock()
        self.running = True

        # Create pages after that might use previously defined variables
        self.pages = {
            self.MAIN: MainMenu(screen, self),
            self.DATABASE: Database(screen, self),
            self.STUDYMENU: StudyMenu(screen, self)
        }

        self.default_header = [
            Button(self, (0.9, 0.1, 0.1, 0.05), "↜",
                   button_color, hover_color),
            Button(self, (0.1, 0.1, 0.1, 0.05), "←",
                   button_color, hover_color)
        ]

        self.current_page = self.pages[self.MAIN]  # Pass self as manager

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

    def map_rect(self, x_prop, y_prop, width_prop, height_prop):
        """Map proportional coordinates to pixel coordinates based on orientation."""
        if self.is_portrait:
            # Swap width and height proportions for rotation
            width = height_prop * self.screen_height
            height = width_prop * self.screen_width

            # Map coordinates and adjust for the center of rotation
            x_pixel = y_prop * self.screen_width - width // 2
            y_pixel = x_prop * self.screen_height - height // 2
        else:
            # Standard calculation for landscape orientation
            width = width_prop * self.screen_width
            height = height_prop * self.screen_height

            x_pixel = x_prop * self.screen_width - width // 2
            y_pixel = y_prop * self.screen_height - height // 2

        # Convert to integers and return all values
        return int(x_pixel), int(y_pixel), int(width), int(height)