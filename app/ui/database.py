from ..ui import Page
from ..ui.elements import SearchBar

class Database(Page):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        self.button_color = (70, 130, 180)  # SteelBlue
        self.hover_color = (100, 149, 237)  # CornflowerBlue
        self.text_color = (255, 255, 255)   # White

        self.components = [
            *self.manager.default_header,
            SearchBar(manager, (0.5, 0.2, 0.6, 0.05))
        ]

        # Assign on_click methods
        self.components[0].on_click = self.manager.toggle_orientation

    def render(self):
        """Render the page content."""
        for component in self.components:
            component.render(self.screen)

    def handle_event(self, event):
        """Handle user input."""
        for component in self.components:
            component.handle_event(event)