import pygame
from ui.elements import Button
from constants import KEYBOARD_LAYOUT, ROMAJI_MAP

class SearchBar:
    def __init__(self, manager, rect_prop, centered=True, placeholder_text='', color=(120, 120, 120), active_color=(100, 100, 100)):
        self.manager = manager  # Reference to AppManager
        self.rect_prop = rect_prop  # Proportional rectangle (x_prop, y_prop, width_prop, height_prop)
        self.placeholder_text = placeholder_text
        self.text: str = ''
        self.color = color
        self.active_color = active_color
        self.is_active = False
        self.rect_obj = None
        self.cursor_visible = True
        self.cursor_counter = 0
        self.max_length = 30
        self.centered=centered
        
        self.keyboard_props = (0, 0.5, 1, 0.5)
        self.keyboard_buttons = []
        self.mode = "EN"
        self.romaji_buffer = ""

        self.generate_keyboard()

    def render(self, screen):
        # Map logical rectangle to screen coordinates
        x, y, width, height = self.manager.map_rect(*self.rect_prop)
        if self.centered:
            x -= width // 2
            y -= height // 2
        self.rect_obj = pygame.Rect((x, y), (width, height))

        # Draw the search bar rectangle
        current_color = self.active_color if self.is_active else self.color
        pygame.draw.rect(screen, current_color, self.rect_obj, border_radius=5)

        # Render the text
        font = self.manager.font
        if self.text:
            display_text = self.text
        else:
            display_text = self.placeholder_text

        text_surface = font.render(display_text, True, self.manager.font_color)
        if self.manager.is_portrait:
            text_surface = pygame.transform.rotate(text_surface, 90)
            text_rect = text_surface.get_rect(midbottom=(x + width // 2, self.manager.screen_height - y - 10))
        else:
            text_rect = text_surface.get_rect(midleft=(x + 10, y + height // 2))
        screen.blit(text_surface, text_rect)

        # Handle cursor blinking
        if self.is_active:
            self.render_keyboard(screen)

            if (self.cursor_counter // 30) % 2 == 0:
                if self.manager.is_portrait:
                    cursor_height = width - 2

                    # Calculate cursor position for portrait mode
                    if self.text:
                        cursor_x = text_rect.x + text_rect.width // 2
                        cursor_y = text_rect.y - 3
                    else:
                        # Default cursor position for empty input
                        cursor_x = x + width // 2
                        cursor_y = self.manager.screen_height - y - 10

                    # Draw a horizontal line for the cursor
                    pygame.draw.line(screen, self.manager.font_color,
                                    (cursor_x - cursor_height // 3, cursor_y),
                                    (cursor_x + cursor_height // 3, cursor_y), 2)
                else:
                    cursor_height = height - 2

                    # Landscape mode (original logic)
                    cursor_x = text_rect.right + 2
                    cursor_y = text_rect.y + cursor_height // 2
                    # Draw vertical line cursor
                    pygame.draw.line(screen, self.manager.font_color,
                                    (cursor_x, cursor_y),
                                    (cursor_x, cursor_y + cursor_height // 1.5), 2)

        # Update cursor counter
        self.cursor_counter += 1

    def generate_keyboard(self):
        x_prop, y_prop, w_prop, h_prop = self.keyboard_props

        key_padding = 0.01

        rows = KEYBOARD_LAYOUT
        
        rows.append("    ")

        max_keys = max([len(r) for r in rows])

        key_width = w_prop / max_keys
        double_key_width = key_width * 2
        key_height = h_prop / 4

        key_width_padded = key_width - 2 * key_padding
        double_key_width_padded = double_key_width - 2 * key_padding
        key_height_padded = key_height - 2 * key_padding

        # For each row, we create button objects
        for row_index, row_keys in enumerate(rows):
            # Trim extra spaces if we artificially added for placeholders
            keys = list(row_keys)
            if row_index == 3:  # last row
                keys[0] = "MODE"
                keys[1] = " "
                keys[2] = "ENTER"
                keys[3] = "←"

            for key_index, key_char in enumerate(keys):
                x_disp = (max_keys - len(keys)) * key_width / 2
                if row_index != 3:
                    button_x_prop = x_prop + key_index * key_width + key_width // 2 + key_padding + x_disp
                    button_y_prop = y_prop + row_index * key_height + key_height // 2 + key_padding
                    key_width_prop = key_width_padded
                    key_height_prop = key_height_padded
                else:
                    button_x_prop = x_prop + key_index * double_key_width + double_key_width // 2 + key_padding + x_disp / 2
                    button_y_prop = y_prop + row_index * key_height + key_height // 2 + key_padding
                    key_width_prop = double_key_width_padded
                    key_height_padded = key_height_padded

                # Determine button behavior on click
                def on_click_factory(c):
                    def on_click():
                        if c == "MODE":
                            # Toggle mode
                            self.mode = "JP" if self.mode == "EN" else "EN"
                        elif c == "ENTER":
                            # Execute search
                            self.on_search(self.text)
                            self.text = ""
                        elif c == "←":
                            self.text = self.text[:-1]
                            if self.mode == "JP":
                                self.romaji_buffer = self.romaji_buffer[:-1]
                        else:
                            # Append character
                            if len(self.text) < self.max_length:
                                self.text += c.lower()
                                # Handle romaji conversion if JP mode
                                if self.mode == "JP":
                                    self.romaji_buffer += c.lower()
                                    # Check if romaji buffer forms a valid kana
                                    if self.romaji_buffer in ROMAJI_MAP:
                                        # Replace the end of the text with the kana
                                        # For example, if text = 'ka', and romaji_buffer='ka', and it maps to か
                                        # We remove the last len(romaji_buffer) chars from text and append the kana
                                        self.text = self.text[:-len(self.romaji_buffer)] + ROMAJI_MAP[self.romaji_buffer]
                                        self.romaji_buffer = ""
                                    if c == " ":
                                        self.romaji_buffer = ""
                    return on_click

                # Create the button
                button_color = (200, 200, 200)
                hover_color = (170, 170, 170)
                btn = Button(
                    manager=self.manager, 
                    rect_prop=(button_x_prop, button_y_prop, key_width_prop, key_height_prop), 
                    text=key_char, 
                    color=button_color, 
                    hover_color=hover_color,
                    centered=False,
                    corrected=True
                )
                btn.on_click = on_click_factory(key_char)
                self.keyboard_buttons.append(btn)

    def render_keyboard(self, screen):
        x, y, width, height = self.manager.map_rect(0, 0.5, 1, 0.5)
        self.rect_obj = pygame.Rect((x, y), (width, height))

        current_color = self.active_color if self.is_active else self.color
        pygame.draw.rect(screen, current_color, self.rect_obj, border_radius=5)

        for button in self.keyboard_buttons:
            button.render(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked on the search bar
            if self.rect_obj.collidepoint(event.pos):
                self.is_active = True
            else:
                self.is_active = False
        elif event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_RETURN:
                self.on_search(self.text)
                self.text = ''
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                if self.mode == "JP":
                    self.romaji_buffer = self.romaji_buffer[:-1]
            else:
                # Only add character if max length not exceeded
                if len(self.text) < self.max_length and (event.unicode.isalpha() or event.unicode.isspace()):
                    self.text += event.unicode

                    if self.mode == "JP":
                        self.romaji_buffer += event.unicode
                        if self.romaji_buffer in ROMAJI_MAP:
                            self.text = self.text.replace(self.romaji_buffer, ROMAJI_MAP[self.romaji_buffer])
                            self.romaji_buffer = ""

                        if event.unicode == " ":
                            self.romaji_buffer = ""

        if self.is_active:
            for button in self.keyboard_buttons:
                button.handle_event(event)

    def on_search(self, query):
        """Override this method to define search behavior."""
        print(f"Search query: {query}")
