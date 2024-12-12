from ..ui import Page
from ..ui.elements import Button
from ..config import FEEDBACK_BAD_COLOR, FONT_SMALL, tint_hex

class MainMenu(Page):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)

        tint = "#101010"

        self.buttons = [
            Button(manager, (0.5, 0.3, 0.5, 0.07), "Database Search"),
            Button(manager, (0.5, 0.4, 0.5, 0.07), "Start Studying"),
            Button(manager, (0.5, 0.5, 0.5, 0.07), "Toggle Orientation"),
            Button(manager, (0.9, 0.1, 0.1, 0.05), "X", FEEDBACK_BAD_COLOR, tint_hex(FEEDBACK_BAD_COLOR, tint), font=FONT_SMALL)
        ]

        def quit_app():
            self.manager.running = False

        # Assign on_click methods
        self.buttons[0].on_click = lambda: self.manager.change_page(self.manager.DATABASE)
        self.buttons[1].on_click = lambda: self.manager.change_page(self.manager.STUDYMENU)
        self.buttons[2].on_click = self.manager.toggle_orientation
        self.buttons[3].on_click = quit_app

    def render(self):
        """Render the page content."""
        for button in self.buttons:
            button.render(self.screen)

    def handle_event(self, event):
        """Handle user input."""
        for button in self.buttons:
            button.handle_event(event)