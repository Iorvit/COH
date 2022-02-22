import pygame
from pygame.sprite import Sprite

class Lives(Sprite):
    """Класс для управления кораблём."""

    def __init__(self, ai_game):
        """Инициализирует корабль и задаёт его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Загружает изображение и получает прямоугольник коробля.
        self.image = pygame.image.load("images/livest.bmp")
        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется у нижнего экрана.
        self.rect.midbottom = self.screen_rect.midbottom

        # Соохранине вещественной координаты в центре коробля.
        self.x = float(self.rect.x)