import pygame

class SearchBar:
    def __init__(self, manager, rect_prop, placeholder_text='', color=(255, 255, 255), active_color=(200, 200, 200)):
        self.manager = manager  # Reference to AppManager
        self.rect_prop = rect_prop  # Proportional rectangle (x_prop, y_prop, width_prop, height_prop)
        self.placeholder_text = placeholder_text
        self.text = ''
        self.color = color
        self.active_color = active_color
        self.is_active = False
        self.rect_obj = None
        self.cursor_visible = True
        self.cursor_counter = 0
        self.max_length = 30  # Optional: limit the length of input text

    def render(self, screen):
        # Map logical rectangle to screen coordinates
        x, y, width, height = self.manager.map_rect(*self.rect_prop)
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
        text_rect = text_surface.get_rect(midleft=(x + 10, y + height // 2))
        screen.blit(text_surface, text_rect)

        # Handle cursor blinking
        if self.is_active and (self.cursor_counter // 30) % 2 == 0:
            cursor_x = text_rect.right + 2
            cursor_y = text_rect.y
            cursor_height = text_rect.height
            pygame.draw.line(screen, self.manager.font_color, (cursor_x, cursor_y), (cursor_x, cursor_y + cursor_height), 2)

        # Update cursor counter
        self.cursor_counter += 1

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
            else:
                # Only add character if max length not exceeded
                if len(self.text) < self.max_length:
                    self.text += event.unicode

    def on_search(self, query):
        """Override this method to define search behavior."""
        print(f"Search query: {query}")
