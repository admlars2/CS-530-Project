import pygame

class Canvas:
    def __init__(self, manager, y_prop, word_len=1):
        self.manager = manager
        self.y_prop = y_prop
        self.y_prop_disp = 0
        self.word_len = max(word_len, 1)

        # Get screen dimensions from manager
        self.screen_width = self.manager.screen_width
        self.screen_height = self.manager.screen_height

        self.side_length = 0
        x, y, width, height = self.calc_pos()

        self.draw_rect = pygame.Rect(x, y, width, height)

        # Create a drawing surface sized to the canvas area
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((255, 255, 255, 0))

        # Drawing state
        self.drawing = False
        self.last_pos = None
        self.last_smoothed_pos = None
        self.pressure = 1.0  # default

        # Brush attributes
        self.brush_color = (0, 0, 0)
        self.base_brush_size = 5

        # Keep track of strokes
        self.strokes = []
        self.current_stroke = []

        # Smoothing parameter
        self.smoothing_alpha = 0.5

    def calc_pos(self):
        side_prop = min((1 - 0.05) / self.word_len, 0.4)
        x_prop = 0.5 - side_prop * (self.word_len - 1) * 0.5
        x, y, _, _ = self.manager.map_rect(x_prop, self.y_prop + self.y_prop_disp, 0, 0)
        self.side_length = self.screen_height * side_prop

        width = int(self.side_length * self.word_len)
        height = int(self.side_length)

        # If portrait, swap width and height
        if self.manager.is_portrait:
            width, height = height, width

        # Center the canvas at (x, y)
        x -= self.side_length // 2
        y -= self.side_length // 2

        return x, y, width, height

    def set_length(self, word_len):
        self.word_len = max(word_len, 1)

    def set_y_prop_disp(self, disp_prop):
        self.y_prop_disp = disp_prop

    def render(self, screen):
        # Recalculate position in case orientation or layout changed
        x, y, width, height = self.calc_pos()
        if (width, height) != (self.draw_rect.width, self.draw_rect.height) or (x, y) != (self.draw_rect.x, self.draw_rect.y):
            # Recreate surface and redraw if size/position changed
            self.draw_rect = pygame.Rect(x, y, width, height)
            self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
            self.surface.fill((255, 255, 255, 0))
            self._redraw_strokes()

        screen.blit(self.surface, self.draw_rect)
        pygame.draw.rect(screen, (0, 0, 0), self.draw_rect, width=2)

    def handle_event(self, event):
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            x, y = pygame.mouse.get_pos()
        elif event.type in (pygame.FINGERMOTION, pygame.FINGERDOWN, pygame.FINGERUP):
            x = int(event.x * self.screen_width)
            y = int(event.y * self.screen_height)
        else:
            return

        local_x = x - self.draw_rect.x
        local_y = y - self.draw_rect.y

        if event.type == pygame.FINGERMOTION:
            if self.drawing and self.last_smoothed_pos:
                pos = self._smooth_point((local_x, local_y))
                self.draw_line(self.last_smoothed_pos, pos, pressure=event.pressure)
                self.current_stroke.append((pos[0], pos[1], event.pressure))
                self.last_pos = pos
                self.last_smoothed_pos = pos

        elif event.type == pygame.FINGERDOWN:
            pos = self._smooth_point((local_x, local_y), reset=True)
            if self.draw_rect.collidepoint(x, y):
                self.start_drawing(x, y, pressure=event.pressure)

        elif event.type == pygame.FINGERUP:
            self.stop_drawing()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = self._smooth_point((local_x, local_y), reset=True)
                if self.draw_rect.collidepoint(x, y):
                    self.start_drawing(x, y)

        elif event.type == pygame.MOUSEMOTION:
            if self.drawing and self.last_smoothed_pos:
                pos = self._smooth_point((local_x, local_y))
                self.draw_line(self.last_smoothed_pos, pos, pressure=1.0)
                self.current_stroke.append((pos[0], pos[1], 1.0))
                self.last_pos = pos
                self.last_smoothed_pos = pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.stop_drawing()

    def start_drawing(self, x, y, pressure=1.0):
        if not self.draw_rect.collidepoint(x, y):
            return
        local_x = x - self.draw_rect.x
        local_y = y - self.draw_rect.y
        self.drawing = True
        self.last_pos = (local_x, local_y)
        self.last_smoothed_pos = (local_x, local_y)
        self.pressure = pressure
        self.current_stroke = [(local_x, local_y, pressure)]

    def stop_drawing(self):
        if self.drawing and self.current_stroke:
            self.strokes.append(self.current_stroke)
        self.drawing = False
        self.last_pos = None
        self.last_smoothed_pos = None
        self.current_stroke = []

    def draw_line(self, start_pos, end_pos, pressure=1.0):
        brush_size = int(self.base_brush_size * pressure)
        pygame.draw.line(self.surface, self.brush_color, start_pos, end_pos, brush_size)

    def undo(self):
        if self.strokes:
            self.strokes.pop()
            self._redraw_strokes()

    def clear(self):
        self.strokes = []
        self.surface.fill((255, 255, 255, 0))
        self._redraw_strokes()

    def _redraw_strokes(self):
        self.surface.fill((255, 255, 255, 0))
        for stroke in self.strokes:
            if not stroke:
                continue
            for i in range(len(stroke) - 1):
                start = stroke[i]
                end = stroke[i+1]
                start_pos = (start[0], start[1])
                end_pos = (end[0], end[1])
                pressure = (start[2] + end[2]) / 2.0
                self.draw_line(start_pos, end_pos, pressure=pressure)

        # Redraw main dividers after clearing
        for i in range(1, self.word_len):
            if self.manager.is_portrait:
                x_1 = self.draw_rect.x
                y_1 = y_2 = self.draw_rect.y - self.side_length*i
                x_2 = self.draw_rect.x + self.draw_rect.width
            else:
                x_1 = x_2 = self.draw_rect.x + self.side_length*i
                y_1 = self.draw_rect.y
                y_2 = self.draw_rect.y + self.draw_rect.height
            pygame.draw.line(self.surface, (0, 0, 0), (x_1, y_1), (x_2, y_2), 2)

    def _smooth_point(self, pos, reset=False):
        if reset or self.last_smoothed_pos is None:
            self.last_smoothed_pos = pos
            return pos
        old_x, old_y = self.last_smoothed_pos
        new_x, new_y = pos
        alpha = self.smoothing_alpha
        smoothed_x = alpha * new_x + (1 - alpha) * old_x
        smoothed_y = alpha * new_y + (1 - alpha) * old_y
        smoothed_pos = (smoothed_x, smoothed_y)
        return smoothed_pos
