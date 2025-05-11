import pygame
import random
import sys

# Initialize pygame
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH = SCREEN_WIDTH // BLOCK_SIZE
FPS = 60
GAME_DURATION = 60


# Colors & Assets
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
backgroundImage = pygame.image.load("BackgroundImage.jpg")

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Stacking Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30, bold=True)


# Block shape definitions
SHAPES = {
    1: {"offsets": [(0, 0), (1, 0), (2, 0), (-1, 0)], "width": 4, "height": 1},  # I
    2: {"offsets": [(0, 0), (0, 1), (1, 0), (1, 1)], "width": 2, "height": 2},    # O
    3: {"offsets": [(0, 0), (-1, 0), (1, 0), (0, 1)], "width": 3, "height": 2},   # T
    4: {"offsets": [(0, 0), (-1, 0), (0, 1), (1, 1)], "width": 3, "height": 2},   # S
    5: {"offsets": [(0, 0), (1, 0), (0, 1), (-1, 1)], "width": 3, "height": 2},   # Z
    6: {"offsets": [(0, 0), (-1, 0), (1, 0), (1, 1)], "width": 3, "height": 2},   # L
    7: {"offsets": [(0, 0), (1, 0), (-1, 0), (-1, 1)], "width": 3, "height": 2},  # J
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

    def draw(self, surface, offset_y):
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

            # Lock the block
            grid.append(current_block)
            current_block = Block(GRID_WIDTH // 2, camera_offset)
        fall_time = 0

    # Camera follows the tallest tile
    max_y = max((y for block in grid for _, y in block.get_tile_positions()), default=0)
    camera_offset = max(0, max_y - (SCREEN_HEIGHT // BLOCK_SIZE) + 5)

    # Draw blocks
    for block in grid:
        block.draw(screen, camera_offset)
    current_block.draw(screen, camera_offset)

    # Score is height of tower
    score = max(0, camera_offset * 10)
    score_text = font.render(f"Score: {score}", True, black)
    screen.blit(score_text, (SCREEN_WIDTH - 120, 10))

    pygame.display.update()

pygame.quit()
  
