import pygame
import sys

# Inicialize o Pygame
pygame.init()

# Defina as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Configurações da tela
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Fonte para o menu
font = pygame.font.Font(None, 36)

# Musica menu

pygame.mixer.init()
game_music = pygame.mixer.Sound("sons/game_music.wav")
game_music.set_volume(0.1)
pygame.mixer.Channel(0).play(game_music, -1)

# Função para desenhar o texto
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

# Função principal
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_1:
                    print("Iniciar jogo!")
                    from game import Game
                    game_instance = Game()
                    game_instance.start_game()
                elif event.key == pygame.K_2:
                    print("Abrir configurações!")
                    # altura, largura = 1920, 1080
                    # screen = pygame.display.set_mode((altura, largura))
                    # screen.fill(BLACK)
                elif event.key == pygame.K_3:
                    print("Ver créditos!")
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()

        # Limpa a tela
        screen.fill(BLACK)

        # Desenha o menu
        draw_text("Jogar (Pressione 1)", font, WHITE, WIDTH // 2, HEIGHT // 2 - 50)
        draw_text("Configurações (Pressione 2)", font, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Créditos (Pressione 3)", font, WHITE, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text("Sair (Pressione 4)", font, WHITE, WIDTH // 2, HEIGHT // 2 + 100)

        # Atualiza a tela
        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
