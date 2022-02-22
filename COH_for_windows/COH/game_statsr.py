class GameStats():
    """Отслеживание статистики для игры Alien INvasion."""

    def __init__(self, ai_game):
        """Инициализирует статистику."""
        self.settings = ai_game.settings 
        
        # Игра Alien Invasion запускается в неактивном состоянии.
        self.game_active = False

        self.reset_stats() 

        # Берёт из текста лучший результат прошлой игры и сохраняет его!
        with open('high_record.txt') as rr:
            rec = rr.read()   
        self.high_score = int(rec)


    def reset_stats(self):
        """Инициализирует статистику, изменяющуюся в ходе игры."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1