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

        self.shoot_group = pygame.sprite.Group()
        self.create_enemy = True
        self.enemy_group = pygame.sprite.Group()

        self.player_points = self.player.points
        self.font = pygame.font.Font("font/8bit.ttf", 30)
        self.points_text = self.font.render("SCORE: " + str(self.player_points), 1, (255, 255, 255))
        self.level = 0
        self.enemy_in_window = 5
        self.level_text = self.font.render("LEVEL: " + str(self.level), 1, (255, 255, 255))
        self.meteors_missed = 0
        self.max_meteors_missed = 3
        self.player_lives = 3

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
        # Atualiza a posição do jogador
        if self.player_right:
            self.player.rect[0] += self.player.speed
        if self.player_left:
            self.player.rect[0] -= self.player.speed

        # Atualiza os grupos
        self.shoot_group.update()
        self.player_group.update()
        self.enemy_group.update()

        # Adiciona meteoros se necessário
        if len(self.enemy_group) < 5:
            for i in range(5 - len(self.enemy_group)):
                self.enemy = Enemy()
                self.enemy_group.add(self.enemy)

        # Remove meteoros que passaram da tela
        for enemy in self.enemy_group.sprites():
            if enemy.rect[1] > self.window_height:
                self.enemy_group.remove(enemy)
                self.meteors_missed += 1

                if self.meteors_missed >= self.max_meteors_missed:
                    self.game_over()

        # Atualiza a velocidade dos meteoros com base nos pontos
        if self.player_points <= 100:
            self.enemy.speed = 2
            self.level = 1
            self.level_text = self.font.render("LEVEL: " + str(self.level), 1, (255, 255, 255))
        elif self.player_points > 100:
            self.enemy.speed = 3
            self.level = 2
            self.level_text = self.font.render("LEVEL: " + str(self.level), 1, (255, 255, 255))

        # Remove tiros que saíram da tela
        for bullet in self.shoot_group:
            if bullet.rect[1] < -20:
                self.shoot_group.remove(bullet)

        # Colisão entre tiros e meteoros
        if pygame.sprite.groupcollide(self.shoot_group, self.enemy_group, True, True):
            self.player_points += random.randint(1, 10)
            self.points_text = self.font.render("SCORE: " + str(self.player_points), 1, (255, 255, 255))
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("sons/enemy_death.wav"))

        # Colisão entre jogador e meteoros
        for enemy in self.enemy_group.sprites():
            if pygame.sprite.collide_rect(self.player, enemy):
                # O jogador foi atingido por um meteoro
                self.player_lives -= 1
                if self.player_lives <= 0:
                    self.game_over()

    def render(self):
        self.window.blit(self.background, (0, 0))
        self.window.blit(self.points_text, (850, 10))
        self.window.blit(self.level_text, (650, 10))
        lives_text = self.font.render("LIVES: " + str(self.player_lives), 1, (255, 255, 255))
        self.window.blit(lives_text, (10, 10))
        self.player_group.draw(self.window)
        self.shoot_group.draw(self.window)
        self.enemy_group.draw(self.window)

    def game_over(self):
        self.is_running = False
        # Adicione aqui a lógica para exibir "Game Over" e encerrar o jogo.

    def restart_game(self):
        self.__init__()

    def start_game(self):
        while self.is_running:
            self.handle_events()
            self.update()
            self.render()
            
            pygame.display.flip()
            self.clock.tick(30)

# Inicializa o jogo
game_instance = Game()
game_instance.start_game()
