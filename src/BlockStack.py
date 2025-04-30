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

    def rotate(self):
        if self.shape_id == 2:  # O-shape doesn't rotate
            return
        new_shape = [(-py, px) for px, py in self.shape]  # 90Â° clockwise
        original_shape = self.shape
        self.shape = new_shape
        if check_collision(self):
            self.shape = original_shape

    def get_tile_positions(self, dx=0, dy=0):
        return [(self.x + px + dx, self.y + py + dy) for px, py in self.shape]
    
    def draw(self, surface):
        for px, py in self.shape:
            pygame.draw.rect(surface, self.color,
                             ((self.x + px) * BLOCK_SIZE, (self.y + py - offset_y) * BLOCK_SIZE,
                              BLOCK_SIZE, BLOCK_SIZE))
    # Collision detection
    def check_collision(block, dx=0, dy=0):
        for x, y in block.get_tile_positions(dx, dy):
            if x < 0 or x >= GRID_WIDTH or y >= 100:  # 100 is soft max to allow scrolling
                return True
        for b in grid:
            if (x, y) in b.get_tile_positions():
                return True
        return False

    def drop_to_bottom(block):
    while not check_collision(block, dy=1):
        block.move(0, 1)

# Game variables
fall_time = 0
fall_speed = 500  # milliseconds
current_block = Block(GRID_WIDTH // 2, 0)
grid = []
score = 0
camera_offset = 0

# Game loop
running = True
while running:
    time_passed = clock.tick(FPS)
    fall_time += time_passed
    rotateBreak -= 1

    screen.blit(backgroundImage, (0, 0))

  # Input handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if not check_collision(current_block, dx=-1):
            current_block.move(-1, 0)
    if keys[pygame.K_RIGHT]:
        if not check_collision(current_block, dx=1):
            current_block.move(1, 0)
    if keys[pygame.K_UP] and rotateBreak == 0:
        current_block.rotate()
        rotateBreak = 60
    if keys[pygame.K_SPACE]:
        drop_to_bottom(current_block)
        fall_time = fall_speed  # force placement

     # Block falls
    if fall_time > fall_speed:
        if not check_collision(current_block, dy=1):
            current_block.move(0, 1)
        else:
            # Game over check
            if any(y <= camera_offset + 1 for _, y in current_block.get_tile_positions()):
                print("Game Over!")
                pygame.quit()
                sys.exit()


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