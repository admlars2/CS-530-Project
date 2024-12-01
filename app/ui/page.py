import pygame

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