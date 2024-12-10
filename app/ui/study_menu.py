from ..ui import Page
from ..ui.elements import Button

class StudyMenu(Page):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)

        self.daily_streak, self.max_daily_streak = self.manager.db_manager.study_card_db.update_login_and_streak()
        self.manager.db_manager.aggregate_cards()

        self.components = [*self.manager.default_header,
                           Button(self.manager, (0.5, 0.4, 0.5, 0.07), "Start")]
        
        print(self.manager.db_manager.study_card_db.get_next_due_card())

    def render(self):
        """Render the page content. To be overridden by subclasses."""

        self.draw_text(f"Streak: {self.daily_streak}", 0.1, 0.2, x_centered=False)
        self.draw_text(f"Best: {self.max_daily_streak}", 0.1, 0.25, x_centered=False)
        self.draw_text(f"DUE: {self.manager.db_manager.num_study_cards}", 0.775, 0.2, x_centered=False)
        self.draw_text(f"NEW: {self.manager.db_manager.num_new}", 0.775, 0.25, x_centered=False)

        for component in self.components:
            component.render(self.screen)

    def handle_event(self, event):
        """Handle user input. To be overridden by subclasses."""
        for component in self.components:
            component.handle_event(event)