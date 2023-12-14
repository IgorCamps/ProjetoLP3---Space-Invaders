import pygame
import random
import sys
from pygame.locals import *
from scripts.player import Player, Shot
from scripts.enemy import Enemy
from MainMenu import main_menu

class Game():
    def __init__(self):
        #inicializa os atributos e configurações do jogo
        self.__is_running = True
        self.__game_over = False
        self.__window_width = 1200
        self.__window_height = 600
        self.__window = pygame.display.set_mode((self.__window_width, self.__window_height))
        self.__clock = pygame.time.Clock()
        
        # Carregamento e escala do fundo
        self.__background = pygame.image.load("img/background/fundo.png")
        self.__background = pygame.transform.scale(self.__background, (self.__window_width, self.__window_height))

         # Grupos de sprites para jogador, tiros e inimigos
        self.__player_group = pygame.sprite.Group()
        self.__player = Player()
        self.__player_group.add(self.__player)
        self.__player_right = False
        self.__player_left = False

        self.__shoot_group = pygame.sprite.Group()
        self.__create_enemy = True
        self.__enemy_group = pygame.sprite.Group()

        # Atributos relacionados à pontuação, nível e outros elementos do jogo
        self.__player_points = self.__player.points
        self.__font = pygame.font.Font("font/8bit.ttf", 30)
        self.__points_text = self.__font.render("SCORE: " + str(self.__player_points), 1, (255, 255, 255))
        self.__level = 0
        self.__enemy_in_window = 5
        self.__level_text = self.__font.render("LEVEL: " + str(self.__level), 1, (255, 255, 255))
        self.__meteors_missed = 0
        self.__max_meteors_missed = 3
        self.__player_lives = 3

        # Inicialização do som do jogo
        pygame.mixer.init()
        self.__game_music = pygame.mixer.Sound("sons/game_music.wav")
        self.__game_music.set_volume(0.01)
        pygame.mixer.Channel(0).play(self.__game_music, -1)

    def __handle_events(self):
         # Trata os eventos do jogo
        for event in pygame.event.get():
            if event.type == QUIT:
                self.__is_running = False
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_d:
                    self.__player_right = True
                elif event.key == K_LEFT or event.key == K_a:
                    self.__player_left = True
                elif event.key == K_SPACE:
                    self.__player_shot = Shot()
                    self.__player_shot.rect[0] = self.__player.rect[0] + 23
                    self.__player_shot.rect[1] = self.__player.rect[1]
                    self.__shoot_group.add(self.__player_shot)
                    self.__game_shot = pygame.mixer.Sound("sons/shot.wav")
                    self.__game_shot.set_volume(0.3)
                    pygame.mixer.Channel(1).play(self.__game_shot)

            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    self.__player_right = False
                elif event.key == K_LEFT or event.key == K_a:
                    self.__player_left = False

    def __update(self):
        # Atualiza a posição do jogador
        if self.__player_right:
            self.__player.rect[0] += self.__player.speed
        if self.__player_left:
            self.__player.rect[0] -= self.__player.speed

        # Atualiza os grupos
        self.__shoot_group.update()
        self.__player_group.update()
        self.__enemy_group.update()

        # Adiciona meteoros se necessário
        if len(self.__enemy_group) < 5:
            for i in range(5 - len(self.__enemy_group)):
                self.__enemy = Enemy()
                self.__enemy_group.add(self.__enemy)

        # Remove meteoros que passaram da tela
        for enemy in self.__enemy_group.sprites():
            if enemy.rect[1] > self.__window_height:
                self.__enemy_group.remove(enemy)
                self.__meteors_missed += 1

                if self.__meteors_missed >= self.__max_meteors_missed:
                    self.__game_over()

        # Atualiza a velocidade dos meteoros com base nos pontos
        if self.__player_points <= 100:
            self.__enemy.speed = 2
            self.__level = 1
            self.__level_text = self.__font.render("LEVEL: " + str(self.__level), 1, (255, 255, 255))
        elif self.__player_points > 200:
            self.__enemy.speed = 3
            self.__level = 2
            self.__level_text = self.__font.render("LEVEL: " + str(self.__level), 1, (255, 255, 255))
        elif self.__player_points > 300:
            self.__enemy.speed = 4
            self.__level = 3
            self.__level_text = self.__font.render("LEVEL: " + str(self.__level), 1, (255, 255, 255))
        elif self.__player_points > 400:
            self.__enemy.speed = 5
            self.__level = 4
            self.__level_text = self.__font.render("LEVEL: " + str(self.__level), 1, (255, 255, 255))
        elif self.__player_points > 500:
            self.__enemy.speed = 6
            self.__level = 5
            self.__level_text = self.__font.render("LEVEL: " + str(self.__level), 1, (255, 255, 255))

        # Remove tiros que saíram da tela
        for bullet in self.__shoot_group:
            if bullet.rect[1] < -20:
                self.__shoot_group.remove(bullet)

        # Colisão entre tiros e meteoros
        if pygame.sprite.groupcollide(self.__shoot_group, self.__enemy_group, True, True):
            self.__player_points += random.randint(1, 10)
            self.__points_text = self.__font.render("SCORE: " + str(self.__player_points), 1, (255, 255, 255))
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("sons/enemy_death.wav"))

        # Colisão entre jogador e meteoros
        for enemy in self.__enemy_group.sprites():
            if pygame.sprite.collide_rect(self.__player, enemy):
                # O jogador foi atingido por um meteoro
                self.game_over()

    def __render(self):
        # Renderiza os elementos do jogo na tela
        self.__window.blit(self.__background, (0, 0))
        self.__window.blit(self.__points_text, (850, 10))
        self.__window.blit(self.__level_text, (650, 10))
        self.__player_group.draw(self.__window)
        self.__shoot_group.draw(self.__window)
        self.__enemy_group.draw(self.__window)

    def game_over(self):
        # Exibe a tela de Game Over e volta para o menu principal
        self.__is_running = False
        while not self.__game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.__game_over = True

            self.__window.blit(self.__background, (0, 0))
            self.__window.blit(self.__points_text, (850, 10))
            self.__window.blit(self.__level_text, (650, 10))
            self.__player_group.draw(self.__window)
            self.__shoot_group.draw(self.__window)
            self.__enemy_group.draw(self.__window)

            # Adiciona uma mensagem de "Game Over" na tela
            game_over_font = pygame.font.Font("font/8bit.ttf", 72)
            game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(self.__window_width // 2, self.__window_height // 2))
            self.__window.blit(game_over_text, game_over_rect)

            pygame.display.flip()
            self.__clock.tick(30)

        # Quando o loop terminar, chama a função do menu principal
        main_menu()

    def restart_game(self):
        # Reinicializa o jogo
        self.__init__()

    def start_game(self):
        # Inicia o loop principal do jogo
        while self.__is_running:
            self.__handle_events()
            self.__update()
            self.__render()
            pygame.display.flip()
            self.__clock.tick(30)

# Inicializa o jogo
game_instance = Game()
game_instance.start_game()
