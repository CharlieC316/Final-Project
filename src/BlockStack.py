import pygame
import random

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 300, 600
BLOCK_SIZE = 30
FPS = 60

# Colors & Textures
white = (255, 255, 255)
red = (255, 0, 0)
backgroundImage = pygame.image.load("BackgroundImage.jpg")

# Set up screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Block Stacking Game")
clock = pygame.time.Clock()

# Block class
class Block:
    def __init__(self, x, y):
        self.x = x  # grid position
        self.y = y
        self.color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
   
    


pygame.quit()