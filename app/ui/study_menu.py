from ..ui import Page, CardFront
from ..ui.elements import Button, Canvas

class StudyMenu(Page):
    MENU = 'menu'
    CARD_FRONT = 'front'
    CARD_REVIEW = 'review'

    def __init__(self, screen, manager):
        super().__init__(screen, manager)

        self.daily_streak, self.max_daily_streak = self.manager.db_manager.study_card_db.update_login_and_streak()
        self.manager.db_manager.aggregate_cards()
        self.current_card = self.manager.db_manager.study_card_db.get_next_due_card()

        self.studying = False
        self.current_page_key = self.MENU
        self.last_review = 0

        self.canvas = Canvas(manager, 0.5, 3)

        self.start_button = Button(self.manager, (0.5, 0.4, 0.5, 0.07), "Start")
        self.start_button.on_click = self.start_studying

        self.components = [*self.manager.default_header,
                           self.start_button]
        
        self.total_cards = self.manager.db_manager.num_study_cards + self.manager.db_manager.num_new

        self.pages = {
            self.CARD_FRONT: CardFront(screen, manager, self),
            self.CARD_REVIEW: Page(screen, manager)
        }
        
    def render(self):
        """Render the page content. To be overridden by subclasses."""
        if self.current_page_key == self.MENU:
            self.draw_text(f"Streak: {self.daily_streak}", 0.1, 0.2, x_centered=False)
            self.draw_text(f"Best: {self.max_daily_streak}", 0.1, 0.25, x_centered=False)
            self.draw_text(f"DUE: {self.manager.db_manager.num_study_cards}", 0.775, 0.2, x_centered=False)
            self.draw_text(f"NEW: {self.manager.db_manager.num_new}", 0.775, 0.25, x_centered=False)                

            for component in self.components:
                component.render(self.screen)

        else:
            self.pages[self.current_page_key].render()

    def handle_event(self, event):
        """Handle user input. To be overridden by subclasses."""
        if self.current_page_key == self.MENU:
            for component in self.components:
                component.handle_event(event)

        else:
            self.pages[self.current_page_key].handle_event(event)

    def start_studying(self):
        if self.total_cards > 0:
            self.studying = True
            
            self.current_page_key = self.CARD_FRONT
            self.start_button.text = "Continue"

    def review_card(self, quality):
        self.last_review = quality
        self.current_page_key = self.CARD_REVIEW
    
    def update_card(self, was_correct):
        self.current_card = self.manager.db_manager.review_card_get_next(self.current_card["id"], self.last_review if was_correct else 0)
        if self.current_card == None:
            self.current_page_key = self.MENU
        else:
            self.current_page_key = self.CARD_REVIEW