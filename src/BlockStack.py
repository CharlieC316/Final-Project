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
        self.shape = SHAPES[self.shape_id]["offsets"]
        self.blockWidth = SHAPES[self.shape_id]["width"]
        self.blockHeight = SHAPES[self.shape_id]["height"]
        self.rotated = False

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        if self.shape_id == 2:  # O-shape doesn't rotate
            return
        
        new_shape = [(-py, px) for px, py in self.shape]  # 90Â° clockwise
        original_shape = self.shape
        self.shape = new_shape
        self.blockWidth, self.blockHeight = self.blockHeight, self.blockWidth
        self.rotated = not self.rotated
        
        if check_collision(self):
            self.shape = original_shape
            self.blockWidth, self.blockHeight = self.blockHeight, self.blockWidth
            self.rotated = not self.rotated

    def get_tile_positions(self, dx=0, dy=0):
        return [(self.x + px + dx, self.y + py + dy) for px, py in self.shape]

    def draw(self, surface):
        for px, py in self.shape:
            pygame.draw.rect(surface, self.color, ((self.x + px) * BLOCK_SIZE, (self.y + py) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Collision detection
def check_collision(block, dx=0, dy=0):
    for x, y in block.get_tile_positions(dx, dy):
        if x < 0 or x >= GRID_WIDTH or y >= SCREEN_HEIGHT // BLOCK_SIZE:
            return True
        for b in grid:
            if (x, y) in b.get_tile_positions():
                return True
    return False

# --- GAME STATE ---
fall_time = 0
fall_speed = 500
fast_fall_speed = 150
current_block = Block(GRID_WIDTH // 2, 0)
grid = []
score = 0
tower_height = 0
crumble_particles = []
crumbling = False
game_start_time = pygame.time.get_ticks()
game_over = False
rotate_cooldown = 200
move_cooldown = 100
rotate_timer = 0
move_timer = 0

# --- MAIN GAME LOOP ---
running = True
while running:
    time_passed = clock.tick(FPS)

# Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            game_over = False
            grid = []
            score = 0
            tower_height = 0
            crumble_particles = []
            crumbling = False
            current_block = Block(GRID_WIDTH // 2, 0)
            game_start_time = pygame.time.get_ticks()

    # Game timer
    remaining_time = max(0, GAME_DURATION - (pygame.time.get_ticks() - game_start_time)/1000)
    if remaining_time <= 0 and not game_over:
        game_over = True

     # Active game logic
    if not game_over:
        rotate_timer += time_passed
        move_timer += time_passed
        fall_time += time_passed

    keys = pygame.key.get_pressed()
    speed = fast_fall_speed if keys[pygame.K_DOWN] else fall_speed

    if keys[pygame.K_LEFT] and move_timer >= move_cooldown:
            if not check_collision(current_block, dx=-1):
                current_block.move(-1, 0)
            move_timer = 0

    if keys[pygame.K_RIGHT] and move_timer >= move_cooldown:
            if not check_collision(current_block, dx=1):
                current_block.move(1, 0)
            move_timer = 0

    if keys[pygame.K_UP] and rotate_timer >= rotate_cooldown:
            current_block.rotate()
            rotate_timer = 0

    
    # Block falling
    if fall_time >= speed:
            if not check_collision(current_block, dy=1):
                current_block.move(0, 1)
            else:
                grid.append(current_block)
                current_max_y = min(y for block in grid for _, y in block.get_tile_positions())
                new_height = (SCREEN_HEIGHT // BLOCK_SIZE) - current_max_y
                
                if new_height > tower_height:
                    score += (new_height - tower_height) * 5
                    tower_height = new_height
                
                current_block = Block(GRID_WIDTH // 2, 0)

             # Tower crumble effect
                if tower_height >= 16 and not crumbling and len(crumble_particles) == 0:
                    crumbling = True
                    for block in grid:
                        for px, py in block.get_tile_positions():
                            screen_x = (block.x + px) * BLOCK_SIZE / 2
                            screen_y = (block.y + py) * BLOCK_SIZE
                            for _ in range(6):
                                crumble_particles.append([
                                    screen_x + random.randint(0, BLOCK_SIZE),
                                    screen_y + random.randint(0, BLOCK_SIZE),
                                    block.color,
                                    0,
                                    random.uniform(-1.5, 1.5),
                                    random.uniform(0, 2)
                                ])
                    grid.clear()
                    score += 100
                
            fall_time = 0

     # --- RENDERING ---
    screen.blit(backgroundImage, (0, 0))

    # Draw blocks
    for block in grid:
        block.draw(screen)
    if not game_over:
        current_block.draw(screen)
    
    # Particle effects
    for particle in crumble_particles[:]:
        age_ratio = particle[3] / 180
        size = max(3, 8 - (age_ratio * 6))
        
        particle_surf = pygame.Surface((size*5, size*5), pygame.SRCALPHA)
        pygame.draw.circle(
            particle_surf,
            (*particle[2], int(150 * (1 - age_ratio))),
            (size*2, size*2),
            size*1.5
        )
    pygame.draw.circle(
            particle_surf,
            (*particle[2], int(255 * (1 - age_ratio/2))),
            (size*2, size*2),
            size
        )

    

    pygame.display.update()

pygame.quit()
  
