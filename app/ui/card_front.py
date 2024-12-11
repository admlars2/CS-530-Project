import pygame
from ..ui import Page
from ..ui.elements import FlipScreenButton

class CardFront(Page):
    def __init__(self, screen, manager, study_menu):
        super().__init__(screen, manager)
        self.study_manager = study_menu

        flip_button = FlipScreenButton(self.manager, (0.9, 0.1, 0.1, 0.05))
        flip_button.on_click = self.flip_on_click

        self.components = [
            flip_button,
            self.study_manager.canvas
        ]

        self.components[1].on_click = lambda: self.change_page(self.MAIN)

    def render(self):
        """Render the page content. To be overridden by subclasses."""
        for component in self.components:
            component.render(self.screen)

    def handle_event(self, event):
        """Handle user input. To be overridden by subclasses."""
        for component in self.components:
            component.handle_event(event)

    def flip_on_click(self):
        self.study_manager.canvas.clear()
        self.manager.toggle_orientation()