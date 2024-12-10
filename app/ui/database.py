from ..ui import Page
from ..ui.elements import InputBar
from ..ui.elements import Button
from ..config import ENGLISH, JAPANESE

class Database(Page):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        self.button_color = (70, 130, 180)  # SteelBlue
        self.hover_color = (100, 149, 237)  # CornflowerBlue
        self.text_color = (255, 255, 255)   # White

        search_bar = InputBar(manager, (0.5, 0.2, 0.6, 0.05))
        search_bar.on_search = self.on_search

        self.components = [
            *self.manager.default_header,
            search_bar
        ]

        self.search_results = []

        # Assign on_click methods
        self.components[0].on_click = self.manager.toggle_orientation

    def render(self):
        """Render the page content."""
        for component in self.components:
            component.render(self.screen)

        for result in self.search_results:
            result.render(self.screen)

    def handle_event(self, event):
        """Handle user input."""
        for component in self.components:
            component.handle_event(event)

        for result in self.search_results:
            result.handle_event(event)

    def on_search(self, query, mode):
        results = self.manager.db_manager.word_db.search(query, mode)

        self.search_results = []

        for i, result in enumerate(results):
            button_result = Button(self.manager,
                   (0.25+i*0.25, 0.35, 0.24, 0.24),
                   result["word"])
            
            button_result.on_click = self.on_click_generator(result)
            
            self.search_results.append(button_result)

    def on_click_generator(self, result):
        def on_click():
            self.manager.pages[self.manager.WORD].data = result
            self.manager.change_page(self.manager.WORD)
        return on_click