import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
FPS = 60
rotateBreak = 0


# Colors & Textures
white = (255, 255, 255)
red = (255, 0, 0)
backgroundImage = pygame.image.load("BackgroundImage.jpg")

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Stacking Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Block shapes (offsets from the center)
SHAPES = {
    1: [(0, 0), (1, 0), (2, 0), (-1, 0)],      # I-shape
    2: [(0, 0), (0, 1), (1, 0), (1, 1)],       # O-shape
    3: [(0, 0), (-1, 0), (1, 0), (0, 1)],      # T-shape
    4: [(0, 0), (-1, 0), (0, 1), (1, 1)],      # S-shape
    5: [(0, 0), (1, 0), (0, 1), (-1, 1)],      # Z-shape
    6: [(0, 0), (-1, 0), (1, 0), (1, 1)],      # L-shape
    7: [(0, 0), (1, 0), (-1, 0), (-1, 1)],     # J-shape
}
# Block class
class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        self.shape_id = random.randint(1, 7)
        self.shape = SHAPES[self.shape_id]

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, 
                         (self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    
# Game variables
fall_time = 0
fall_speed = 0.5  # blocks fall every 0.5 seconds
current_block = Block(5, 0)
grid = []


# Main game loop
running = True
while running:
    screen.blit(backgroundImage, (0,0))
    fall_time += clock.get_rawtime()
    clock.tick(FPS)

    # Quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

 # Block falls
    # if fall_time / 1000 > fall_speed:
    if 0 == 0:
        current_block.move(0, 1)
        fall_time = 0

        # Check if it hit the bottom or other blocks
        if current_block.y * BLOCK_SIZE >= SCREEN_HEIGHT - BLOCK_SIZE:
            grid.append(current_block)
            current_block = Block(5, 0)

    # Draw current and stacked blocks
    for block in grid:
        block.draw(screen)
    current_block.draw(screen)

    pygame.display.update()

pygame.quit()