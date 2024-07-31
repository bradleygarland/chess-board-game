import pygame


def handle_button_clicks(buttons, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        for button in buttons:
            if button.rect.collidepoint(event.pos):
                button.action()


class Button:
    def __init__(self, rect, text, action):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont(None, 36)
        self.text_surface = self.font.render(text, True, (0, 0, 0))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        screen.blit(self.text_surface, (self.rect.left, self.rect.top))
