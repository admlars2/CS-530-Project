import pygame

def draw_slider(screen: pygame.Surface, rect: pygame.Rect, value: float, min_value: float, max_value: float, bar_color: tuple, knob_color: tuple):
    """
    Draws a slider with a bar and a movable knob based on the current value.

    Parameters:
    - screen: The pygame surface where the slider will be drawn.
    - rect: The rectangle defining the position and size of the slider bar.
    - value: The current value of the slider.
    - min_value: The minimum value of the slider.
    - max_value: The maximum value of the slider.
    - bar_color: RGB color of the slider bar.
    - knob_color: RGB color of the slider knob.
    """
    # Draw the slider bar
    pygame.draw.rect(screen, bar_color, rect)

    # Calculate knob position based on the current value
    knob_x = rect.x + (value - min_value) / (max_value - min_value) * rect.width
    knob_y = rect.centery
    knob_radius = rect.height // 2  # Knob size proportional to slider height

    # Draw the knob
    pygame.draw.circle(screen, knob_color, (int(knob_x), int(knob_y)), knob_radius)

def slider_get_value(mouse_pos: tuple, rect: pygame.Rect, min_value: float, max_value: float) -> float:
    """
    Calculates the slider value based on the mouse position.

    Parameters:
    - mouse_pos: The (x, y) position of the mouse.
    - rect: The rectangle defining the slider bar's position and size.
    - min_value: The minimum value of the slider.
    - max_value: The maximum value of the slider.

    Returns:
    - The value corresponding to the mouse's x position on the slider bar.
    """
    # Map mouse position to value range, clamping it within slider bounds
    relative_x = max(min(mouse_pos[0], rect.right), rect.left)
    normalized_x = (relative_x - rect.x) / rect.width
    return min_value + normalized_x * (max_value - min_value)
