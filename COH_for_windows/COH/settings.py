class Settings():
    """Классдля хранения всех настроек игры Alien Invasion."""
    
    def __init__(self):
        """Инициаллизирует статические настройки игры."""   
        self.screen_width = 1920
        self.screen_hiegth = 1080
        self.bg_color = (230, 230, 230)

        # Настройка коробля.
        self.ship_limit = 3

        # Параметры снаряда
        self.bullet_speed = 3
        self.bullet_width = 100
        self.bullet_height = 100
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # Настройки пришельцев.
        self.fleet_drop_speed = 10

        # Темп ускорения игры
        self.speedup_scale = 1.2

        # Темп роста стоймости пришельца
        self.score_scale = 1.5

        self.initialize_dynamic_sttings()


    def initialize_dynamic_sttings(self):
        """Инициализирует настройки, изменяющие в ходе игры.""" 
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 1.0

        # Если 1 то движение в вправо, если -1 то движение в лево.
        self.fleet_direction = 1 

        # Подсчёт очков.
        self.alien_points = 50 


    def increase_speed(self):
        """Увеличивает настройки скорости и стоймости пришельцев."""
        self.ship_speed *= self.speedup_scale 
        self.bullet_speed *= self.speedup_scale 
        self.alien_speed *= self.speedup_scale 

        self.alien_points = int(self.alien_points * self.score_scale)  

