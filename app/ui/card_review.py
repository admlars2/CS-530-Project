from ..ui import Page
from ..ui.elements import FlipScreenButton, Button
from ..config import tint_hex, FEEDBACK_BAD_COLOR, FEEDBACK_GREAT_COLOR, FONT_SMALL

class CardReview(Page):
    def __init__(self, screen, manager, study_menu):
        super().__init__(screen, manager)
        self.study_manager = study_menu

        flip_button = FlipScreenButton(self.manager, (0.9, 0.1, 0.1, 0.05))
        flip_button.on_click = self.flip_on_click

        hover_tint = "#101010"

        undo_button = Button(self.manager, (0.3, 0.1, 0.1, 0.1), "Undo")
        undo_button.on_click = self.study_manager.canvas.undo

        back_button = Button(self.manager, (0.1, 0.1, 0.1, 0.05), "←")
        back_button.on_click = self.study_manager.back_to_menu

        wrong_button = Button(self.manager, (0.35, 0.8, 0.11, 0.09), "Wrong", FEEDBACK_BAD_COLOR, tint_hex(FEEDBACK_BAD_COLOR, hover_tint), font=FONT_SMALL)
        wrong_button.on_click = lambda: self.study_manager.update_card(False)
        right_button = Button(self.manager, (0.65, 0.8, 0.11, 0.09), "Right", FEEDBACK_GREAT_COLOR, tint_hex(FEEDBACK_GREAT_COLOR, hover_tint), font=FONT_SMALL)
        right_button.on_click = lambda: self.study_manager.update_card(True)

        self.components = [
            flip_button,
            self.study_manager.canvas,
            undo_button,
            back_button,
            wrong_button,
            right_button
        ]

    def render(self):
        """Render the page content. To be overridden by subclasses."""
        self.study_manager.canvas.set_y_prop_disp(-0.25)

        self.draw_text(f"Word: {self.study_manager.current_card['word']}", 0.5, 0.15)
        self.draw_text(f"Reading: {self.study_manager.current_card['reading']} | Translation: {self.study_manager.current_card['translations']}", 0.5, 0.225)

        for component in self.components:
            component.render(self.screen)

    def handle_event(self, event):
        """Handle user input. To be overridden by subclasses."""
        for component in self.components:
            component.handle_event(event)

    def flip_on_click(self):
        self.study_manager.canvas.clear()
        self.manager.toggle_orientation()