from ..ui import Page
from ..ui.elements import Button
from ..config import KANJIVG_FOLDER, ROMAJI_MAP, FONT_MED
import os, pygame


class Word(Page):
    def __init__(self, screen, manager):
        super().__init__(screen, manager)
        self.data = {}  # Holds the word data (e.g., passed by the manager)
        self.components = [*self.manager.default_header]

        # Duplicate and modify the second button
        original_button: Button = self.components[1]
        alternate_button = Button(original_button.manager, original_button.rect_prop, original_button.text)
        alternate_button.on_click = lambda: self.manager.change_page(self.manager.DATABASE)

        self.components[1] = alternate_button

    def render(self):
        """Render the page content."""
        for component in self.components:
            component.render(self.screen)

        if self.data:  # Check if data exists
            
            y_prop = 0.3 # Set starting vertical position

            svg_filenames = self.data.get("svgs", "")
            svg_filenames = svg_filenames.split(",")

            if svg_filenames:
                # Calculate individual SVG width (proportional to screen width)
                side_prop = min((1 - 0.05) / len(svg_filenames), 0.4)

                x_prop = 0.5 - side_prop*(len(svg_filenames) - 1) * 0.5 # Calculate SVG placement centered

                # Render each SVG
                for i, filename in enumerate(svg_filenames):
                    svg_path = os.path.join(KANJIVG_FOLDER, filename.strip())
                    if os.path.exists(svg_path):
                        self.render_svg(svg_path, x_prop+side_prop*i, y_prop, side_prop)
                
                y_prop += side_prop * 0.5 + 0.05

            # Display the word
            word_text = f"Word: {self.data.get('word', '')}"
            self.draw_text(word_text, x_prop=0.5, y_prop=y_prop)

            y_prop += 0.1

            # Display the reading
            reading_text = f"Reading: {self.data.get('reading', '')}"
            self.draw_text(reading_text, x_prop=0.5, y_prop=y_prop)

            y_prop += 0.1

            # Display the translations
            translations_text = f"Translations: {self.data.get('translations', '')}"
            self.draw_text(translations_text, x_prop=0.5, y_prop=y_prop)

    def handle_event(self, event):
        """Handle user input."""
        for component in self.components:
            component.handle_event(event)

    def draw_text(self, text, x_prop, y_prop, font=FONT_MED):
        """Helper function to draw text on the screen at the given proportions."""
        x, y, _, _ = self.manager.map_rect(x_prop, y_prop, 0, 0)
        text_surface = font.render(text, True, self.manager.font_color)
        text_width, text_height = text_surface.get_size()
        
        if self.manager.is_portrait:
            text_surface = pygame.transform.rotate(text_surface, 90)
            x -= text_height // 2
            y -= text_width // 2

        else:
            x -= text_width // 2
            y -= text_height // 2
        self.screen.blit(text_surface, (x, y))

    def render_svg(self, svg_path, x_prop, y_prop, side_prop):
        """Render an SVG at the given proportions."""
        # Assuming your framework provides SVG rendering or you have implemented it
        x, y, _, _ = self.manager.map_rect(x_prop, y_prop, 0, 0)
        side_length = self.manager.screen_height * side_prop
        x -= side_length // 2
        y -= side_length // 2
        # Render SVG to the screen at the given coordinates and size
        self.manager.render_svg(svg_path, x, y, side_length, side_length)
