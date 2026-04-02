import pygame
import random
import math

# --- Constants ---
WIDTH, HEIGHT = 800, 600
NUM_SQUARES = 100
MIN_SIZE = 10
MAX_SIZE = 50
FPS = 60
TURN_ANGLE = 0.1   # maximum random turn in radians per frame


class Square:
    def __init__(self):
        self.size = random.randint(MIN_SIZE, MAX_SIZE)

        self.x = random.randint(0, WIDTH - self.size)
        self.y = random.randint(0, HEIGHT - self.size)

        # Speed (size-based)
        self.speed = max(1, 60 / self.size)

        # Random direction
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

        # 🎨 Random main color
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )

        # Border color (slightly darker)
        self.border_color = (
            max(0, self.color[0] - 80),
            max(0, self.color[1] - 80),
            max(0, self.color[2] - 80)
        )

    def rotate_velocity(self):
        theta = random.uniform(-0.1, 0.1)

        new_dx = self.dx * math.cos(theta) - self.dy * math.sin(theta)
        new_dy = self.dx * math.sin(theta) + self.dy * math.cos(theta)

        self.dx = new_dx
        self.dy = new_dy

    def update(self):
        self.rotate_velocity()

        self.x += self.dx
        self.y += self.dy

        # Bounce
        if self.x <= 0 or self.x + self.size >= WIDTH:
            self.dx *= -1

        if self.y <= 0 or self.y + self.size >= HEIGHT:
            self.dy *= -1

    def draw(self, screen):
        rect = pygame.Rect(int(self.x), int(self.y), self.size, self.size)

        # 🎨 Fill
        pygame.draw.rect(screen, self.color, rect)

        # 🔲 Border
        pygame.draw.rect(screen, self.border_color, rect, 2)

        # ✨ Inner decoration (small center square)
        inner_size = self.size // 3
        inner_rect = pygame.Rect(
            rect.centerx - inner_size // 2,
            rect.centery - inner_size // 2,
            inner_size,
            inner_size
        )

        pygame.draw.rect(screen, self.border_color, inner_rect)

def create_squares():
    squares = []
    for _ in range(NUM_SQUARES):
        squares.append(Square())
    return squares


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True


def update_squares(squares):
    for square in squares:
        square.update()


def draw_squares(screen, squares):
    for square in squares:
        square.draw(screen)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Randomly Turning Squares")

    clock = pygame.time.Clock()
    squares = create_squares()

    running = True
    while running:
        running = handle_events()

        update_squares(squares)

        screen.fill((0, 0, 0))
        draw_squares(screen, squares)
        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()