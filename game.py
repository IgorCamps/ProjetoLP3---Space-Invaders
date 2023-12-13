import pygame
import random
from pygame.locals import *
from scripts.player import Player, Shot
from scripts.enemy import Enemy

class Game():
    def __init__(self):
        self.is_running = True
        self.window_width = 1200
        self.window_height = 600
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        self.clock = pygame.time.Clock()

        self.background = pygame.image.load("img/background/fundo.png")
        self.background = pygame.transform.scale(self.background, (self.window_width, self.window_height))

        self.player_group = pygame.sprite.Group()
        self.player = Player()
        self.player_group.add(self.player)
        self.player_right = False
        self.player_left = False


        # self.game_shot = pygame.sprite.Group()



        self.shoot_group = pygame.sprite.Group()
        self.create_enemy = True
        self.enemy_group = pygame.sprite.Group()

        self.player_points = self.player.points
        self.font = pygame.font.Font("font/8bit.ttf", 30)
        self.points_text = self.font.render("SCORE: " + str(self.player_points), 1, (255, 255, 255))
        self.level = 0
        self.enemy_in_window = 5
        self.level_text = self.font.render("LEVEL: " + str(self.level), 1, (255, 255, 255))

        pygame.mixer.init()
        self.game_music = pygame.mixer.Sound("sons/game_music.wav")
        self.game_music.set_volume(0.1)
        pygame.mixer.Channel(0).play(self.game_music, -1)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.is_running = False
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_d:
                    self.player_right = True
                elif event.key == K_LEFT or event.key == K_a:
                    self.player_left = True
                elif event.key == K_SPACE:
                    self.player_shot = Shot()
                    self.player_shot.rect[0] = self.player.rect[0] + 23
                    self.player_shot.rect[1] = self.player.rect[1]
                    self.shoot_group.add(self.player_shot)
                    self.game_shot = pygame.mixer.Sound("sons/shot.wav")
                    self.game_shot.set_volume(0.3)
                    pygame.mixer.Channel(1).play(self.game_shot)

            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    self.player_right = False
                elif event.key == K_LEFT or event.key == K_a:
                    self.player_left = False
    def update(self):
        if self.player_right:
            self.player.rect[0] += self.player.speed
        if self.player_left:
            self.player.rect[0] -= self.player.speed

        self.shoot_group.update()
        self.player_group.update()
        self.enemy_group.update()

        if len(self.enemy_group) < 5:
            for i in range(5):
                self.enemy = Enemy()
                self.enemy_group.add(self.enemy)

        if self.enemy.rect[1] > 600:
            self.enemy_group.remove(self.enemy)

        if self.player_points <= 100:
            self.enemy.speed = 2
            self.level = 1
            self.level_text = self.font.render("LEVEL: " + str(self.level), 1, (255, 255, 255))
        
        elif self.player_points > 100:
            self.enemy.speed = 3
            self.level = 2
            self.level_text = self.font.render("LEVEL: " + str(self.level), 1, (255, 255, 255))
        
        # elif self.enemy

        for bullet in self.shoot_group:
            if self.player_shot.rect[1] < -20:
                self.shoot_group.remove(self.player_shot)

        if pygame.sprite.groupcollide(self.shoot_group, self.enemy_group, True, True):
            self.player_points += random.randint(1, 10)
            self.points_text = self.font.render("SCORE: " + str(self.player_points), 1, (255, 255, 255))
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("sons/enemy_death.wav"))

        if pygame.sprite.groupcollide(self.player_group, self.enemy_group, True, False):
            self.restart_game()

    def render(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.points_text, (850, 10))
        self.window.blit(self.level_text, (650, 10))
        self.player_group.draw(self.window)
        self.shoot_group.draw(self.window)
        self.enemy_group.draw(self.window)

    def restart_game(self):
        self.__init__()

    def start_game(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            
            pygame.display.flip()
            self.clock.tick(30)
Game()
