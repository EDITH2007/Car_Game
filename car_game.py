# car_racing_game.py
# A simple car racing game using Pygame
# Install pygame first: pip install pygame

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (255, 255, 0)
ROAD_COLOR = (50, 50, 50)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Car Racing Game")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 72)

class PlayerCar:
    def __init__(self):
        self.width = 40
        self.height = 70
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.speed = 5
        self.color = BLUE
    
    def move(self, direction):
        self.x += direction * self.speed
        # Keep car on screen
        if self.x < 60:  # Left road boundary
            self.x = 60
        if self.x > SCREEN_WIDTH - 60 - self.width:  # Right road boundary
            self.x = SCREEN_WIDTH - 60 - self.width
    
    def draw(self):
        # Car body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Windows
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 10, self.width - 10, 20))
        # Wheels
        pygame.draw.circle(screen, BLACK, (self.x + 5, self.y + 10), 5)
        pygame.draw.circle(screen, BLACK, (self.x + self.width - 5, self.y + 10), 5)
        pygame.draw.circle(screen, BLACK, (self.x + 5, self.y + self.height - 10), 5)
        pygame.draw.circle(screen, BLACK, (self.x + self.width - 5, self.y + self.height - 10), 5)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class EnemyCar:
    def __init__(self):
        self.width = 40
        self.height = 70
        self.x = random.choice([80, 140, 200, 260])
        self.y = -self.height
        self.speed = random.randint(3, 6)
        self.color = RED
    
    def move(self):
        self.y += self.speed
    
    def draw(self):
        # Car body
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Windows
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 30, self.width - 10, 20))
        # Headlights
        pygame.draw.circle(screen, YELLOW, (self.x + 8, self.y + self.height - 5), 4)
        pygame.draw.circle(screen, YELLOW, (self.x + self.width - 8, self.y + self.height - 5), 4)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def off_screen(self):
        return self.y > SCREEN_HEIGHT

class RoadLine:
    def __init__(self, y):
        self.x = SCREEN_WIDTH // 2 - 5
        self.y = y
        self.width = 10
        self.height = 40
        self.speed = 5
    
    def move(self):
        self.y += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))
    
    def off_screen(self):
        return self.y > SCREEN_HEIGHT

def draw_road():
    # Road background
    pygame.draw.rect(screen, ROAD_COLOR, (50, 0, 300, SCREEN_HEIGHT))
    # Side lines
    pygame.draw.rect(screen, WHITE, (50, 0, 5, SCREEN_HEIGHT))
    pygame.draw.rect(screen, WHITE, (345, 0, 5, SCREEN_HEIGHT))

def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def draw_game_over(score):
    # Dark overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(200)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    game_over_text = game_over_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, GREEN)
    quit_text = font.render("Press Q to Quit", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 200))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 300))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, 380))
    screen.blit(quit_text, (SCREEN_WIDTH//2 - quit_text.get_width()//2, 430))

def main():
    running = True
    game_over = False
    score = 0
    
    player = PlayerCar()
    enemies = []
    road_lines = []
    
    # Create initial road lines
    for i in range(0, SCREEN_HEIGHT, 80):
        road_lines.append(RoadLine(i))
    
    enemy_spawn_timer = 0
    enemy_spawn_delay = 60  # Frames between enemy spawns
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        # Restart game
                        main()
                        return
                    elif event.key == pygame.K_q:
                        running = False
        
        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.move(-1)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.move(1)
            
            # Spawn enemies
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= enemy_spawn_delay:
                enemies.append(EnemyCar())
                enemy_spawn_timer = 0
                # Decrease spawn delay as score increases (max difficulty)
                if enemy_spawn_delay > 20:
                    enemy_spawn_delay -= 1
            
            # Update road lines
            for line in road_lines:
                line.move()
                if line.off_screen():
                    line.y = -line.height
            
            # Update enemies
            for enemy in enemies[:]:
                enemy.move()
                
                # Check collision
                if player.get_rect().colliderect(enemy.get_rect()):
                    game_over = True
                
                # Remove off-screen enemies and increase score
                if enemy.off_screen():
                    enemies.remove(enemy)
                    score += 10
            
            # Increase enemy speed based on score
            for enemy in enemies:
                enemy.speed = 3 + (score // 100)
        
        # Drawing
        screen.fill(GREEN)  # Grass background
        draw_road()
        
        # Draw road lines
        for line in road_lines:
            line.draw()
        
        # Draw enemies
        for enemy in enemies:
            enemy.draw()
        
        # Draw player
        player.draw()
        
        # Draw score
        draw_score(score)
        
        # Draw game over screen
        if game_over:
            draw_game_over(score)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()