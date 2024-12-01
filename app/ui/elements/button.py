import pygame

class Button:
    def __init__(self, manager, rect_prop, text, color, hover_color):
        self.manager = manager  # Reference to AppManager for coordinate mapping
        self.rect_prop = rect_prop  # Proportional rectangle (x_prop, y_prop, width_prop, height_prop)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.rect_obj = None

    def render(self, screen):
        # Map logical rectangle to screen coordinates based on orientation
        x, y, width, height = self.manager.map_rect(*self.rect_prop)
        self.rect_obj = pygame.Rect((x, y), (width, height))

        # Draw the button rectangle
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect_obj)

        # Render the text
        text_surface = self.manager.font.render(self.text, True, self.manager.font_color)
        if self.manager.is_portrait:
            text_surface = pygame.transform.rotate(text_surface, 90)
        text_rect = text_surface.get_rect(center=self.rect_obj.center)
        screen.blit(text_surface, text_rect)    # Display to the screen

    def handle_event(self, event):
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            try:
                rect_collision = self.rect_obj.collidepoint(mouse_x, mouse_y)
            except:
                return
            
            if rect_collision:
                if event.type == pygame.MOUSEMOTION:
                    self.is_hovered = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click()
            else:
                if event.type == pygame.MOUSEMOTION:
                    self.is_hovered = False

    def on_click(self):
        """Override this method in subclasses or instances to define button click behavior."""
        pass
