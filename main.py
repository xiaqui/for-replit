import pygame
import sys
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ブロック崩し - Block Breaker")
clock = pygame.time.Clock()

class Paddle:
    def __init__(self):
        self.width = 100
        self.height = 15
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 40
        self.speed = 8
        self.color = BLUE
        
    def move(self, dx):
        self.x += dx * self.speed
        if self.x < 0:
            self.x = 0
        if self.x > WIDTH - self.width:
            self.x = WIDTH - self.width
            
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), 2)

class Ball:
    def __init__(self):
        self.radius = 8
        self.reset()
        
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        angle = random.uniform(-60, 60)
        self.dx = 5 * (1 if random.random() > 0.5 else -1)
        self.dy = -5
        self.color = YELLOW
        self.speed_multiplier = 1.0
        
    def move(self):
        self.x += self.dx * self.speed_multiplier
        self.y += self.dy * self.speed_multiplier
        
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.dx = -self.dx
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
            
        if self.y - self.radius <= 0:
            self.dy = -self.dy
            self.y = self.radius
            
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius, 1)
        
    def is_out(self):
        return self.y - self.radius > HEIGHT

class Block:
    def __init__(self, x, y, width, height, color, points):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.points = points
        self.active = True
        
    def draw(self, surface):
        if self.active:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(surface, WHITE, (self.x, self.y, self.width, self.height), 2)

def create_blocks():
    blocks = []
    block_width = 75
    block_height = 25
    gap = 5
    start_x = 50
    start_y = 60
    
    colors = [RED, ORANGE, YELLOW, GREEN, CYAN, BLUE, PURPLE, MAGENTA]
    
    rows = 6
    cols = 9
    
    for row in range(rows):
        color = colors[row % len(colors)]
        points = (rows - row) * 10
        for col in range(cols):
            x = start_x + col * (block_width + gap)
            y = start_y + row * (block_height + gap)
            blocks.append(Block(x, y, block_width, block_height, color, points))
            
    return blocks

def check_collision_paddle(ball, paddle):
    if (ball.y + ball.radius >= paddle.y and 
        ball.y - ball.radius <= paddle.y + paddle.height and
        ball.x >= paddle.x and 
        ball.x <= paddle.x + paddle.width):
        
        ball.dy = -abs(ball.dy)
        ball.y = paddle.y - ball.radius
        
        hit_pos = (ball.x - paddle.x) / paddle.width
        ball.dx = (hit_pos - 0.5) * 10
        
        return True
    return False

def check_collision_blocks(ball, blocks):
    score = 0
    for block in blocks:
        if not block.active:
            continue
            
        if (ball.x + ball.radius >= block.x and 
            ball.x - ball.radius <= block.x + block.width and
            ball.y + ball.radius >= block.y and 
            ball.y - ball.radius <= block.y + block.height):
            
            block.active = False
            score += block.points
            
            center_x = block.x + block.width / 2
            center_y = block.y + block.height / 2
            
            if abs(ball.x - center_x) > abs(ball.y - center_y):
                ball.dx = -ball.dx
            else:
                ball.dy = -ball.dy
                
            break
            
    return score

def draw_text(surface, text, size, x, y, color=WHITE):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_surface, text_rect)

def main():
    paddle = Paddle()
    ball = Ball()
    blocks = create_blocks()
    
    score = 0
    game_over = False
    game_clear = False
    running = True
    
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and (game_over or game_clear):
                    paddle = Paddle()
                    ball = Ball()
                    blocks = create_blocks()
                    score = 0
                    game_over = False
                    game_clear = False
                    
        if not game_over and not game_clear:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move(-1)
            if keys[pygame.K_RIGHT]:
                paddle.move(1)
                
            ball.move()
            
            check_collision_paddle(ball, paddle)
            score += check_collision_blocks(ball, blocks)
            
            if ball.is_out():
                game_over = True
                
            active_blocks = sum(1 for block in blocks if block.active)
            if active_blocks == 0:
                game_clear = True
        
        screen.fill(BLACK)
        
        paddle.draw(screen)
        ball.draw(screen)
        
        for block in blocks:
            block.draw(screen)
            
        draw_text(screen, f"スコア: {score}", 36, WIDTH // 2, 25)
        
        if game_over:
            draw_text(screen, "ゲームオーバー!", 72, WIDTH // 2, HEIGHT // 2 - 40, RED)
            draw_text(screen, f"最終スコア: {score}", 48, WIDTH // 2, HEIGHT // 2 + 20)
            draw_text(screen, "Rキーでリスタート", 36, WIDTH // 2, HEIGHT // 2 + 70, YELLOW)
            
        if game_clear:
            draw_text(screen, "ゲームクリア！", 72, WIDTH // 2, HEIGHT // 2 - 40, GREEN)
            draw_text(screen, f"最終スコア: {score}", 48, WIDTH // 2, HEIGHT // 2 + 20)
            draw_text(screen, "Rキーでリスタート", 36, WIDTH // 2, HEIGHT // 2 + 70, YELLOW)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
