from ..ui import Page
from ..ui.elements import FlipScreenButton, Button
from ..config import tint_hex, FEEDBACK_BAD_COLOR, FEEDBACK_GOOD_COLOR, FEEDBACK_GREAT_COLOR, FEEDBACK_OKAY_COLOR, FONT_SMALL

class CardFront(Page):
    def __init__(self, screen, manager, study_menu):
        super().__init__(screen, manager)
        self.study_manager = study_menu

        flip_button = FlipScreenButton(self.manager, (0.9, 0.1, 0.1, 0.05))
        flip_button.on_click = self.flip_on_click

        hover_tint = "#101010"

        bad_button = Button(self.manager, (0.2, 0.8, 0.09, 0.09), "Bad", FEEDBACK_BAD_COLOR, tint_hex(FEEDBACK_BAD_COLOR, hover_tint), font=FONT_SMALL)
        bad_button.on_click = lambda: self.study_manager.review_card(0)
        okay_button = Button(self.manager, (0.4, 0.8, 0.09, 0.09), "Okay", FEEDBACK_OKAY_COLOR, tint_hex(FEEDBACK_OKAY_COLOR, hover_tint), font=FONT_SMALL)
        okay_button.on_click = lambda: self.study_manager.review_card(1)
        good_button = Button(self.manager, (0.6, 0.8, 0.09, 0.09), "Good", FEEDBACK_GOOD_COLOR, tint_hex(FEEDBACK_GOOD_COLOR, hover_tint), font=FONT_SMALL)
        good_button.on_click = lambda: self.study_manager.review_card(2)
        great_button = Button(self.manager, (0.8, 0.8, 0.09, 0.09), "Great", FEEDBACK_GREAT_COLOR, tint_hex(FEEDBACK_GREAT_COLOR, hover_tint), font=FONT_SMALL)
        great_button.on_click = lambda: self.study_manager.review_card(3)

        undo_button = Button(self.manager, (0.3, 0.1, 0.1, 0.1), "Undo")
        undo_button.on_click = self.study_manager.canvas.undo

        self.components = [
            flip_button,
            self.study_manager.canvas,
            undo_button,
            bad_button,
            okay_button,
            good_button,
            great_button
        ]

    def render(self):
        """Render the page content. To be overridden by subclasses."""
        self.study_manager.canvas.set_y_prop_disp(0)
        
        if self.study_manager.current_study_card["reversed"]:
            word = self.study_manager.current_card["word"]
            reading = self.study_manager.current_card['reading']
            self.study_manager.canvas.set_length(len(word))
            self.draw_text("Word: ?", 0.5, 0.15)
            show_reading = "?" if word == reading else reading 
            self.draw_text(f"Reading: {show_reading} | Translation: {self.study_manager.current_card['translations']}", 0.5, 0.225)
        else:
            self.study_manager.canvas.set_length(len(self.study_manager.current_card["reading"]))
            self.draw_text(f"Word: {self.study_manager.current_card['word']}", 0.5, 0.15)
            self.draw_text("Reading: ? | Translation: ?", 0.5, 0.225)

        for component in self.components:
            component.render(self.screen)

    def handle_event(self, event):
        """Handle user input. To be overridden by subclasses."""
        for component in self.components:
            component.handle_event(event)

    def flip_on_click(self):
        self.study_manager.canvas.clear()
        self.manager.toggle_orientation()