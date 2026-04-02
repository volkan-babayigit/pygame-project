# --- Constants ---
WIDTH, HEIGHT = 800, 600
NUM_SQUARES = 50
MIN_SIZE = 10
MAX_SIZE = 50
FPS = 60
TURN_ANGLE = 0.1


class Square:
    def __init__(self, x=None, y=None):
        self.size = random.randint(MIN_SIZE, MAX_SIZE)

        # Position
        if x is None:
            self.x = random.randint(0, WIDTH - self.size)
        else:
            self.x = x

        if y is None:
            self.y = random.randint(0, HEIGHT - self.size)
        else:
            self.y = y

        # Speed depends on size
        self.speed = max(1, 60 / self.size)

        # Direction
        angle = random.uniform(0, 2 * math.pi)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed

        # Colors
        self.color = (
            random.randint(50, 255),
            random.randint(50, 255),
            random.randint(50, 255)
        )

        self.border_color = (
            max(0, self.color[0] - 80),
            max(0, self.color[1] - 80),
            max(0, self.color[2] - 80)
        )

    def rotate_velocity(self):
        theta = random.uniform(-TURN_ANGLE, TURN_ANGLE)

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

        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, self.border_color, rect, 2)

        # Inner square
        inner_size = self.size // 3
        inner_rect = pygame.Rect(
            rect.centerx - inner_size // 2,
            rect.centery - inner_size // 2,
            inner_size,
            inner_size
        )
        pygame.draw.rect(screen, self.border_color, inner_rect)


def create_squares():
    return [Square() for _ in range(NUM_SQUARES)]


def handle_events(squares):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        # Mouse click → add square
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            squares.append(Square(x, y))

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
    pygame.display.set_caption("Random Squares")

    clock = pygame.time.Clock()
    squares = create_squares()

    font = pygame.font.SysFont(None, 28)

    running = True
    while running:
        running = handle_events(squares)

        update_squares(squares)

        screen.fill((0, 0, 0))
        draw_squares(screen, squares)

        # Info text
        text = f"Squares: {len(squares)} | Click to add | Close window to exit"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (20, 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
