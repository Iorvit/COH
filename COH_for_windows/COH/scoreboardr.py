import pygame.font
from pygame.sprite import Group

from livesr import Lives
class Scoreboard():
    """Класс для вывода игровой информации."""

    def __init__(self, ai_game):
        """Инициализирует атрибуты посчета очков."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Настройки шрифта для высоты счёта.
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Подготвка изображений счетов.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_lives()


    def prep_score(self):
        """Преобразует текущий счёт в графическое изображение.""" 
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, 
            self.text_color, self.settings.bg_color)
        
        # Вывод счёта в правой верхней части экрана.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20 

    
    def prep_high_score(self):
        """Преобразует рекордный счёт в графическое преображение."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
            self.text_color, self.settings.bg_color)

        # Рекорд выравнивается по центру верхней стороны.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top


    def check_high_score(self):
        """Проверяет, поевился ли новый рекорд.""" 
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score   
            self.prep_high_score()


    def prep_level(self):
        """Преобразует уровень в графическое изображение."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, 
            self.text_color, self.settings.bg_color)

        # Уровень выводится под текущем счётом.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    
    def prep_lives(self):
        """Сообщает количество оставшихся жизней."""
        self.lives = Group()   
        for live_number in range(self.stats.ships_left):
            live = Lives(self.ai_game)
            live.rect.x = 10 + live_number * live.rect.width
            live.rect.y = 10
            self.lives.add(live) 


    def show_score(self):
        """Выводит текущий счёт, рекорд и число оставшихся жизней."""
        self.screen.blit(self.score_image, self.score_rect) 
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.lives.draw(self.screen)
