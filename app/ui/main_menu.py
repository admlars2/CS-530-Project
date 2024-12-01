# ui/main_menu.py
import pygame
from ui import Page
from ui.elements import Button

class MainMenu(Page):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        self.button_color = (70, 130, 180)  # SteelBlue
        self.hover_color = (100, 149, 237)  # CornflowerBlue
        self.text_color = (255, 255, 255)   # White

        self.buttons = [
            Button(manager, (0.5, 0.3, 0.5, 0.07), "Database Search",
                   self.button_color, self.hover_color),
            Button(manager, (0.5, 0.4, 0.5, 0.07), "Start Studying",
                   self.button_color, self.hover_color),
            Button(manager, (0.5, 0.5, 0.5, 0.07), "Toggle Orientation",
                   self.button_color, self.hover_color)
        ]

        # Assign on_click methods
        self.buttons[0].on_click = self.database_search
        self.buttons[1].on_click = self.start_studying
        self.buttons[2].on_click = self.manager.toggle_orientation

    def render(self):
        """Render the page content."""
        for button in self.buttons:
            button.render(self.screen)

    def handle_event(self, event):
        """Handle user input."""
        for button in self.buttons:
            button.handle_event(event)

    def database_search(self):
        """Handle Database Search button click."""
        self.manager.change_page(self.manager.DATABASE)

    def start_studying(self):
        """Handle Start Studying button click."""
        self.manager.change_page(self.manager.STUDYMENU)
