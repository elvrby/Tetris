import pygame
import random

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
WIDTH, HEIGHT = 300, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Warna
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan
    (255, 165, 0),  # Orange
    (0, 0, 255),    # Blue
    (255, 0, 0),    # Red
    (0, 255, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 255, 0),  # Yellow
]

SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]],  # Z
    [[1, 0, 0], [1, 1, 1]],  # L
    [[0, 0, 1], [1, 1, 1]],  # J
]

class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = WIDTH // 30 // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Grid
grid = [[0 for _ in range(WIDTH // 30)] for _ in range(HEIGHT // 30)]

def draw_grid():
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x]:
                pygame.draw.rect(screen, grid[y][x], (x * 30, y * 30, 30, 30))

def check_collision(piece, offset_x=0, offset_y=0):
    for y, row in enumerate(piece.shape):
        for x, value in enumerate(row):
            if value:
                new_x = piece.x + x + offset_x
                new_y = piece.y + y + offset_y
                if new_x < 0 or new_x >= len(grid[0]) or new_y >= len(grid):
                    return True
                if new_y >= 0 and grid[new_y][new_x]:
                    return True
    return False

def merge(piece):
    for y, row in enumerate(piece.shape):
        for x, value in enumerate(row):
            if value:
                grid[piece.y + y][piece.x + x] = piece.color

def clear_lines():
    global grid
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = HEIGHT // 30 - len(new_grid)
    new_grid = [[0 for _ in range(WIDTH // 30)] for _ in range(lines_cleared)] + new_grid
    grid = new_grid

def game_over():
    return any(grid[0])

# Loop utama
def main():
    clock = pygame.time.Clock()
    piece = Piece()
    fall_time = 0
    fall_speed = 1000

    running = True
    while running:
        screen.fill(BLACK)
        fall_time += clock.get_rawtime()
        clock.tick()

        if fall_time >= fall_speed:
            fall_time = 0
            if not check_collision(piece, 0, 1):
                piece.y += 1
            else:
                merge(piece)
                clear_lines()
                piece = Piece()
                if game_over():
                    running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not check_collision(piece, -1):
                    piece.x -= 1
                if event.key == pygame.K_RIGHT and not check_collision(piece, 1):
                    piece.x += 1
                if event.key == pygame.K_DOWN and not check_collision(piece, 0, 1):
                    piece.y += 1
                if event.key == pygame.K_UP:
                    piece.rotate()
                    if check_collision(piece):
                        piece.rotate()  # Undo rotation if collision

        draw_grid()
        for y, row in enumerate(piece.shape):
            for x, value in enumerate(row):
                if value:
                    pygame.draw.rect(screen, piece.color, ((piece.x + x) * 30, (piece.y + y) * 30, 30, 30))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
