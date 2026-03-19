import pygame

class Button:
    def __init__(self, x, y, w, h, text, color=(70,70,70), hover_color=(100,100,100), text_color=(255,255,255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, screen, font):
        self.is_hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=6)
        # Optional gradient effect
        if self.is_hovered:
            pygame.draw.rect(screen, (255,255,255,30), self.rect, 2, border_radius=6)
        label = font.render(self.text, True, self.text_color)
        text_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, text_rect)

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val, label=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.min = min_val
        self.max = max_val
        self.val = start_val
        self.label = label
        self.grabbed = False
        self.handle_rect = pygame.Rect(x + (start_val-min_val)/(max_val-min_val)*w - 5, y-5, 10, h+10)

    def draw(self, screen, font):
        # Draw track
        pygame.draw.rect(screen, (80,80,80), self.rect, border_radius=3)
        # Draw filled portion
        fill_width = (self.val - self.min) / (self.max - self.min) * self.rect.width
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        pygame.draw.rect(screen, (100,200,255), fill_rect, border_radius=3)
        # Draw handle
        self.handle_rect.centerx = self.rect.x + fill_width
        pygame.draw.rect(screen, (220,220,220), self.handle_rect, border_radius=5)
        # Label
        if self.label:
            label_surf = font.render(f"{self.label}: {int(self.val)}", True, (200,200,200))
            screen.blit(label_surf, (self.rect.x, self.rect.y - 20))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.handle_rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION and self.grabbed:
            # Move handle
            new_x = min(max(event.pos[0], self.rect.x), self.rect.x + self.rect.width)
            self.val = self.min + (new_x - self.rect.x) / self.rect.width * (self.max - self.min)
            self.handle_rect.centerx = new_x