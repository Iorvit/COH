import sys
from time import sleep

import pygame

from settings import Settings
from game_statsr import GameStats
from b4 import Ship
from bulletr import Bullet
from tigr import Alien
from buttonr import Button
from scoreboardr import Scoreboard

class AlienInvasion():
    """Класс для управления ресурсами и поведением игры."""

    def __init__(self):
        """Инициализирует игру и создаёт игровые ресырсы."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, 
                                                self.settings.screen_hiegth))
        pygame.display.set_caption('Alien Invasion')

        # Создание экземпляра для хранения игровой статистики
        # и панели реультатов.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        # Создание экземпляра коробля.
        self.ship = Ship(self)

        # Список с расширенной функциональностью.
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Создание кнопки Play.
        self.play_button = Button(self, "Play")
   
   
    def run_game(self):
        """Запуск основного цикла."""
        while True:  
            self._chek_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets() 
                self._update_aliens()

            self._update_screen()


    def _create_fleet(self):
        """Создыние флота вторжения."""
        # Создание пришельца и вычисление количества пришельцев в ряду.
        # Интервал между соседними пришельцами равен ширине пришельца.    
        alien = Alien(self)
        alien_widht, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (alien_widht * 2)
        number_aliens_x = available_space_x // (2 * alien_widht)

        # Определим количтеств рядов пемещающихся на экран.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_hiegth - 
                                (alien_height * 3) - ship_height)
        number_rows = available_space_y // (2 * alien_height)
        
        # Создание флота вторжения.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number) 

    
    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду."""   
        alien = Alien(self)
        alien_widht, alien_height = alien.rect.size
        alien.x = alien_widht + 2 * alien_widht * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien_height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        """Реагирует на достижение пришельцем края экрана."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Опускает весь флот и меняет направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1    


    def _update_screen(self):
        """При каждом смене цикла перерисовывает экран."""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Выводит информацию о счёте.
        self.sb.show_score()

        # Кнопка Play отображается в том случае, если игра неактивна.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Отображает последние прорисованные экраны.
        pygame.display.flip()

        
    def _ship_hit(self):
        """Обрабатывает столкновение коробля с пришельцем."""
        if self.stats.ships_left > 0:
            # Уменьшает ships_left и обновляет панели счета.
            self.stats.ships_left -= 1
            self.sb.prep_lives()

            # Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            # Создание нового флота и размещение коробля в центре.
            self._create_fleet()
            self.ship.center_ship()

            # Пауза.
            sleep(0.5)
        else:
            self.stats.game_active = False 
            pygame.mouse.set_visible(True)   


    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана."""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Происходит то же, что при столкновении с короблём.
                self._ship_hit()
                break   


    def _update_bullets(self):
        """Обновляет позицию снаряда, и уничтожает старые сноряды."""
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet) 

        self._check_bullets_alien_collisions()
        self._update_screen() 

    
    def _check_bullets_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами."""
        # Удаление снарядов и прищельцев, участвующих в коллизиях.    
        collisions = pygame.sprite.groupcollide(self.bullets, 
            self.aliens, False, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens) 
            self.sb.prep_score()
            self.sb.check_high_score() 

        # Проверяет пустая ли группа.
        if not self.aliens: 
            # Уничтожает существующие снаряды и создаёт новыйе. 
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed() 

            # Увелечение уровня.
            self.stats.level += 1
            self.sb.prep_level()


    def _update_aliens(self):
        """Обновяет позиции всех пришельцев во флоте."""   
        self._check_fleet_edges()
        self.aliens.update()

        # Проверка коаллизий 'пришелец - корабль'.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Проверить, дорались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()    


    def _chek_events(self):
        """Отслеживает соытия клавиатуры и мыши."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Сохраняет рекорд в текстовом файле.
                record = 'high_record.txt'
                with open(record, 'w') as file_object:
                    file_object.write(f"{self.stats.high_score}")
                sys.exit() 
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._chek_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    
    def _check_play_button(self, mouse_pos):
        """Запускает новую игру при нажатии кнопки Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Сброс игровых настроек.
            self.settings.initialize_dynamic_sttings()            
            self._start_game()
                    
    
    def _start_game(self):
        # Сброс игровой статистики.
        self.stats.reset_stats()
        self.stats.game_active = True
        self.sb.prep_score()
        self.sb.prep_level()
        self.sb.prep_lives()

        # Отчистка списков пришельцев и снарядов.
        self.aliens.empty()
        self.bullets.empty()

        # Создание нового влота и размещение кораблтя в центре.
        self._create_fleet()
        self.ship.center_ship()

        # Указатель мыши скрывает.
        pygame.mouse.set_visible(False)
             

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True    
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_ESCAPE:
            # Сохраняет рекорд в текстовом файле.
            record = 'high_record.txt'
            with open(record, 'w') as file_object:
                file_object.write(f"{self.stats.high_score}")
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()   
        elif event.key == pygame.K_RETURN:
            self.settings.initialize_dynamic_sttings()
            self._start_game()
                                   

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)            


    def _chek_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


ai = AlienInvasion()
# Запуск игры.
ai.run_game()                        
