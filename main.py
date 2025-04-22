import pygame
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sokoban')

# Colors
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load and scale images
def load_image(name, size):
    image = pygame.image.load(os.path.join('assets', name))
    return pygame.transform.scale(image, size)

player_img = load_image('player.png', (64, 64))
box_img = load_image('box.png', (64, 64))
target_img = load_image('target.png', (64, 64))
wall_img = load_image('wall.png', (64, 64))
ground_img = load_image('ground.png', (64, 64))
title_img = load_image('title.png', (400, 200))  # Ensure you have title.png in assets

# Level layouts
levels = [
    [
        "#####",
        "#@ $.#",
        "# $  #",
        "#  . #",
        "#####"
    ],
    [
        "#####",
        "#@  #",
        "# $$ #",
        "# .. #",
        "#####"
    ]
]

# Define classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def move(self, dx, dy):
        if not self.collide_with_walls(dx, dy):
            if self.collide_with_boxes(dx, dy):
                if self.push_box(dx, dy):
                    self.rect.x += dx
                    self.rect.y += dy
            else:
                self.rect.x += dx
                self.rect.y += dy

    def collide_with_walls(self, dx, dy):
        for wall in walls:
            if self.rect.move(dx, dy).colliderect(wall.rect):
                return True
        return False

    def collide_with_boxes(self, dx, dy):
        for box in boxes:
            if self.rect.move(dx, dy).colliderect(box.rect):
                return box
        return None

    def push_box(self, dx, dy):
        box = self.collide_with_boxes(dx, dy)
        if box:
            if not box.collide_with_walls(dx, dy) and not box.collide_with_boxes(dx, dy):
                box.rect.x += dx
                box.rect.y += dy
                return True
        return False

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = wall_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = box_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def collide_with_walls(self, dx, dy):
        for wall in walls:
            if self.rect.move(dx, dy).colliderect(wall.rect):
                return True
        return False

    def collide_with_boxes(self, dx, dy):
        for box in boxes:
            if self != box and self.rect.move(dx, dy).colliderect(box.rect):
                return True
        return False

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = target_img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

# Create sprite groups
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
boxes = pygame.sprite.Group()
targets = pygame.sprite.Group()

# Function to load level
def load_level(level):
    global all_sprites, walls, boxes, targets
    all_sprites = pygame.sprite.Group()
    walls = pygame.sprite.Group()
    boxes = pygame.sprite.Group()
    targets = pygame.sprite.Group()
    
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == '#':
                wall = Wall(x * 64, y * 64)
                walls.add(wall)
                all_sprites.add(wall)
            elif char == '$':
                box = Box(x * 64, y * 64)
                boxes.add(box)
                all_sprites.add(box)
            elif char == '.':
                target = Target(x * 64, y * 64)
                targets.add(target)
                all_sprites.add(target)
            elif char == '@':
                global player
                player = Player(x * 64, y * 64)
                all_sprites.add(player)

# Check for win condition
def check_win():
    for box in boxes:
        if not any(box.rect.colliderect(target.rect) for target in targets):
            return False
    return True

# Draw reset button
def draw_reset_button():
    font = pygame.font.Font(None, 36)
    text = font.render('Reset', True, WHITE)
    rect = text.get_rect()
    rect.topleft = (SCREEN_WIDTH - 100, 10)
    pygame.draw.rect(screen, BLACK, rect)
    screen.blit(text, rect)
    return rect

# Draw win message
def draw_win_message():
    font = pygame.font.Font(None, 72)
    text = font.render('You Win!', True, WHITE)
    rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, rect)

# Draw start button
def draw_start_button():
    font = pygame.font.Font(None, 48)
    text = font.render('Start', True, WHITE)
    rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    pygame.draw.rect(screen, BLACK, rect.inflate(20, 20))
    screen.blit(text, rect)
    return rect

# Title screen
def title_screen():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if start_button_rect.collidepoint(event.pos):
                        running = False  # Exit title screen
        
        screen.fill(BLUE)
        screen.blit(title_img, (SCREEN_WIDTH // 2 - title_img.get_width() // 2, SCREEN_HEIGHT // 2 - title_img.get_height() - 50))
        start_button_rect = draw_start_button()
        
        pygame.display.flip()

# Game loop
def game_loop():
    current_level = 0
    load_level(levels[current_level])
    
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move(-64, 0)
                elif event.key == pygame.K_RIGHT:
                    player.move(64, 0)
                elif event.key == pygame.K_UP:
                    player.move(0, -64)
                elif event.key == pygame.K_DOWN:
                    player.move(0, 64)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if reset_button_rect.collidepoint(event.pos):
                        load_level(levels[current_level])  # Reset the current level
        
        screen.fill(BLUE)  # Fill screen with blue background
        
        # Draw targets first, so they are visible
        targets.draw(screen)
        
        # Draw other sprites
        all_sprites.draw(screen)
        
        reset_button_rect = draw_reset_button()  # Draw the reset button

        # Check for win
        if check_win():
            draw_win_message()
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds
            current_level = (current_level + 1) % len(levels)  # Next level or loop back to first
            load_level(levels[current_level])
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()

# Start the game with title screen
title_screen()
game_loop()
