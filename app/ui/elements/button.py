import pygame
from ...config import BUTTON_COLOR, BUTTON_HOVER_COLOR

class Button:
    def __init__(self, manager, rect_prop, text, color = BUTTON_COLOR, hover_color = BUTTON_HOVER_COLOR, centered = True, font = None, corrected = False):
        self.manager = manager  # Reference to AppManager for coordinate mapping
        self.rect_prop = rect_prop  # Proportional rectangle (x_prop, y_prop, width_prop, height_prop)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.rect_obj = None
        self.centered = centered
        self.corrected = corrected

        if not font:
            self.font = self.manager.font
        else:
            self.font = font

    def render(self, screen):
        # Map logical rectangle to screen coordinates based on orientation
        x, y, width, height = self.manager.map_rect(*self.rect_prop, corrected = self.corrected)
        if self.centered:
            x -= width // 2
            y -= height // 2
        self.rect_obj = pygame.Rect((x, y), (width, height))

        # Draw the button rectangle
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect_obj)

        # Render the text
        text_surface = self.font.render(self.text, True, self.manager.font_color)
        if self.manager.is_portrait:
            text_surface = pygame.transform.rotate(text_surface, 90)
        text_rect = text_surface.get_rect(center=self.rect_obj.center)
        screen.blit(text_surface, text_rect)    # Display to the screen

    def handle_event(self, event):
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.FINGERMOTION, pygame.FINGERDOWN):
            # Get the input coordinates based on event type
            if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                input_x, input_y = pygame.mouse.get_pos()
            elif event.type in (pygame.FINGERMOTION, pygame.FINGERDOWN):
                input_x = int(event.x * self.manager.screen_width)  # Normalize finger position to screen size
                input_y = int(event.y * self.manager.screen_height)

            try:
                rect_collision = self.rect_obj.collidepoint(input_x, input_y)
            except:
                return

            if rect_collision:
                if event.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION):
                    self.is_hovered = True
                elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                    self.on_click()
            else:
                if event.type in (pygame.MOUSEMOTION, pygame.FINGERMOTION):
                    self.is_hovered = False

    def on_click(self):
        """Override this method in subclasses or instances to define button click behavior."""
        pass
