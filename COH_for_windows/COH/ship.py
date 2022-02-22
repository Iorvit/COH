import pygame


class Ship():
    """Класс для управления кораблём."""

    def __init__(self, ai_game):
        """Инициализирует корабль и задаёт его начальную позицию."""
        super().__init__()
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings

        # Загружает изображение и получает прямоугольник коробля.
        self.image = pygame.image.load("images/b4.bmp")
        self.rect = self.image.get_rect()

        # Каждый новый корабль появляется у нижнего экрана.
        self.rect.midbottom = self.screen_rect.midbottom

        # Соохранине вещественной координаты в центре коробля.
        self.x = float(self.rect.x)

        # Флаг перемещения.
        self.moving_right = False
        self.moving_left = False


    def update(self):
        """Обновляет позицию коробля с учётом флага."""
        # Обновляем x, не rect. 
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.x -= self.settings.ship_speed  

        # Обновлие атрибута rect на основании self.x.
        self.rect.x = self.x     
         
                   
    def blitme(self):
        """Рисует корабль в текущей позиции."""
        self.screen.blit(self.image, self.rect)  


    def center_ship(self):
        """Размещает корабль в центре нижней стороны."""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)     