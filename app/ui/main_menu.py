from ..ui import Page
from ..ui.elements import Button

class MainMenu(Page):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)

        self.buttons = [
            Button(manager, (0.5, 0.3, 0.5, 0.07), "Database Search"),
            Button(manager, (0.5, 0.4, 0.5, 0.07), "Start Studying"),
            Button(manager, (0.5, 0.5, 0.5, 0.07), "Toggle Orientation")
        ]

        # Assign on_click methods
        self.buttons[0].on_click = lambda: self.manager.change_page(self.manager.DATABASE)
        self.buttons[1].on_click = lambda: self.manager.change_page(self.manager.STUDYMENU)
        self.buttons[2].on_click = self.manager.toggle_orientation

    def render(self):
        """Render the page content."""
        for button in self.buttons:
            button.render(self.screen)

    def handle_event(self, event):
        """Handle user input."""
        for button in self.buttons:
            button.handle_event(event)