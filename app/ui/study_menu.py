from ..ui import Page

class StudyMenu(Page):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)

        self.components = [*self.manager.default_header]

    def render(self):
        """Render the page content. To be overridden by subclasses."""
        for component in self.components:
            component.render(self.screen)

    def handle_event(self, event):
        """Handle user input. To be overridden by subclasses."""
        for component in self.components:
            component.handle_event(event)