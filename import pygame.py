import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Plataforma")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
GOLD = (255, 215, 0)

# Relógio para controlar FPS
clock = pygame.time.Clock()
FPS = 60

# Classes do jogo
class Player:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = 100
        self.y = HEIGHT - self.height - 20
        self.vel_y = 0
        self.jump_power = -15
        self.gravity = 0.8
        self.is_jumping = False
        self.color = BLUE
        self.score = 0
    
    def jump(self):
        if not self.is_jumping:
            self.vel_y = self.jump_power
            self.is_jumping = True
    
    def update(self):
        # Aplicar gravidade
        self.vel_y += self.gravity
        self.y += self.vel_y
        
        # Verificar colisão com o chão
        if self.y > HEIGHT - self.height - 20:
            self.y = HEIGHT - self.height - 20
            self.vel_y = 0
            self.is_jumping = False
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Desenhar olhos
        pygame.draw.circle(screen, WHITE, (self.x + 30, self.y + 20), 8)
        pygame.draw.circle(screen, BLACK, (self.x + 30, self.y + 20), 4)

class Obstacle:
    def __init__(self, x):
        self.width = 30
        self.height = random.randint(30, 70)
        self.x = x
        self.y = HEIGHT - self.height - 20
        self.speed = 5
        self.color = RED
    
    def update(self):
        self.x -= self.speed
    
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

class Coin:
    def __init__(self, x):
        self.radius = 15
        self.x = x
        self.y = random.randint(100, HEIGHT - 100)
        self.speed = 5
        self.color = GOLD
    
    def update(self):
        self.x -= self.speed
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, BLACK, (self.x, self.y), self.radius, 2)

# Função para desenhar o chão
def draw_ground():
    pygame.draw.rect(screen, GREEN, (0, HEIGHT - 20, WIDTH, 20))

# Função para mostrar a pontuação
def show_score(score):
    font = pygame.font.SysFont(None, 36)
    text = font.render(f"Pontuação: {score}", True, BLACK)
    screen.blit(text, (10, 10))

# Função principal do jogo
def game():
    player = Player()
    obstacles = []
    coins = []
    obstacle_timer = 0
    coin_timer = 0
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_r and game_over:
                    # Reiniciar o jogo
                    return game()
        
        if not game_over:
            # Atualizar jogador
            player.update()
            
            # Gerar obstáculos
            obstacle_timer += 1
            if obstacle_timer > 60:  # A cada 60 frames (1 segundo)
                obstacles.append(Obstacle(WIDTH))
                obstacle_timer = 0
            
            # Gerar moedas
            coin_timer += 1
            if coin_timer > 90:  # A cada 90 frames (1.5 segundos)
                coins.append(Coin(WIDTH))
                coin_timer = 0
            
            # Atualizar obstáculos
            for obstacle in obstacles[:]:
                obstacle.update()
                
                # Verificar colisão com jogador
                if (player.x < obstacle.x + obstacle.width and
                    player.x + player.width > obstacle.x and
                    player.y < obstacle.y + obstacle.height and
                    player.y + player.height > obstacle.y):
                    game_over = True
                
                # Remover obstáculos que saíram da tela
                if obstacle.x + obstacle.width < 0:
                    obstacles.remove(obstacle)
            
            # Atualizar moedas
            for coin in coins[:]:
                coin.update()
                
                # Verificar colisão com jogador
                if (player.x < coin.x + coin.radius and
                    player.x + player.width > coin.x - coin.radius and
                    player.y < coin.y + coin.radius and
                    player.y + player.height > coin.y - coin.radius):
                    player.score += 10
                    coins.remove(coin)
                
                # Remover moedas que saíram da tela
                if coin.x + coin.radius < 0:
                    coins.remove(coin)
        
        # Desenhar tudo
        screen.fill(WHITE)
        draw_ground()
        
        for obstacle in obstacles:
            obstacle.draw()
        
        for coin in coins:
            coin.draw()
        
        player.draw()
        show_score(player.score)
        
        if game_over:
            font = pygame.font.SysFont(None, 72)
            text = font.render("Game Over", True, RED)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 36))
            
            font = pygame.font.SysFont(None, 36)
            text = font.render("Pressione R para reiniciar", True, BLACK)
            screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 + 36))
        
        pygame.display.update()
        clock.tick(FPS)

# Iniciar o jogo
if __name__ == "__main__":
    game()