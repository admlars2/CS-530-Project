import pygame
import math
from ui.elements import Button
from constants import WHITE

class FlipScreenButton(Button):
    def __init__(self, manager, rect_prop, color, hover_color):
        super().__init__(manager, rect_prop, "", color, hover_color)
        self.arrow_color = WHITE  # Default arrow color (black)
        self.on_click = self.manager.toggle_orientation

    def render(self, screen):
        # Call the parent render method to draw the button
        super().render(screen)

        # Draw a circular arrow icon on top of the button
        x, y, width, height = self.rect_obj
        center = (x + width // 2, y + height // 2)
        radius = min(width, height) // 3  # Arrow size based on button size

        # Draw the arrow circle
        start_angle = math.radians(30)
        end_angle = math.radians(300)
        pygame.draw.arc(screen, self.arrow_color, 
                        (center[0] - radius, center[1] - radius, radius * 2, radius * 2),
                        start_angle, end_angle, 1)

        # Draw the arrowhead
        arrow_length = 5  # Length of the arrowhead lines
        arrow_angle = math.radians(45)  # Angle of the arrowhead lines

        # Arrowhead end point (on the arc)
        arrow_x = center[0] + math.cos(end_angle) * radius
        arrow_y = center[1] - math.sin(end_angle) * radius

        # Arrowhead line coordinates
        line1_x = arrow_x + math.cos(end_angle - arrow_angle) * arrow_length
        line1_y = arrow_y - math.sin(end_angle - arrow_angle) * arrow_length
        line2_x = arrow_x - math.cos(end_angle + arrow_angle) * arrow_length
        line2_y = arrow_y + math.sin(end_angle + arrow_angle) * arrow_length

        # Draw the arrowhead lines
        pygame.draw.line(screen, self.arrow_color, (arrow_x, arrow_y), (line1_x, line1_y), 1)
        pygame.draw.line(screen, self.arrow_color, (arrow_x, arrow_y), (line2_x, line2_y), 1)

    def on_click(self):
        """Handle the flip screen logic."""
        ...
