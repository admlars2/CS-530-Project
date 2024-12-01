import pygame
from ui import Page

class StudyMenu(Page):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)

    def render(self):
        """Render the page content. To be overridden by subclasses."""
        pass

    def handle_event(self, event):
        """Handle user input. To be overridden by subclasses."""
        pass

    def update(self):
        """Update the page state if necessary. To be overridden by subclasses."""
        pass