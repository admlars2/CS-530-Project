import pygame
from ..config import FONT_MED

class Page:
    def __init__(self, screen: pygame.Surface, manager):
        self.screen = screen
        self.manager = manager  # Reference to AppManager

    def render(self):
        """Render the page content. To be overridden by subclasses."""
        pass

    def handle_event(self, event):
        """Handle user input. To be overridden by subclasses."""
        pass

    def update(self):
        """Update the page state if necessary. To be overridden by subclasses."""
        pass

    def draw_text(self, text, x_prop, y_prop, font=FONT_MED, x_centered = True):
        """Helper function to draw text on the screen at the given proportions."""
        x, y, _, _ = self.manager.map_rect(x_prop, y_prop, 0, 0)
        text_surface = font.render(text, True, self.manager.font_color)
        text_width, text_height = text_surface.get_size()

        if self.manager.is_portrait:
            text_surface = pygame.transform.rotate(text_surface, 90)
            
            x -= text_height // 2
            if x_centered:
                y -= text_width // 2
            else:
                y -= text_width

        else:
            if x_centered:
                x -= text_width // 2
            y -= text_height // 2
        self.screen.blit(text_surface, (x, y))