"""Игра «Змейка»."""

from random import choice, randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self):
        """Инициализация игрового объекта."""
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        self.body_color = None

    def draw(self, surface):
        """Отрисовка игрового объекта."""
        raise NotImplementedError


class Apple(GameObject):
    """Класс яблока."""

    def __init__(
        self,
        occupied_positions=(),
        body_color=APPLE_COLOR
    ):
        """Создание яблока."""
        super().__init__()
        self.body_color = body_color
        self.randomize_position(occupied_positions)

    def randomize_position(self, occupied_positions):
        """Перемещает яблоко в свободную клетку."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

            if position not in occupied_positions:
                self.position = position
                break

    def draw(self, surface):
        """Отрисовка яблока."""
        rect = pygame.Rect(
            self.position,
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(
            surface,
            self.body_color,
            rect
        )


class Snake(GameObject):
    """Класс змейки."""

    def __init__(self):
        """Создание змейки."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения."""
        if self.next_direction is not None:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction

        new_head = (
            (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
        )

        self.positions.insert(0, new_head)
        self.last = self.positions.pop()

        if self.length > len(self.positions):
            self.positions.append(self.last)

    def draw(self, surface):
        """Отрисовывает змейку."""
        for position in self.positions:
            rect = pygame.Rect(
                position,
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(
                surface,
                self.body_color,
                rect
            )

    def reset(self):
        """Сбрасывает змейку."""
        self.length = 1
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        self.positions = [self.position]
        self.direction = choice(
            (UP, DOWN, LEFT, RIGHT)
        )
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш."""
    directions = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT
    }

    opposite_directions = {
        UP: DOWN,
        DOWN: UP,
        LEFT: RIGHT,
        RIGHT: LEFT
    }

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            direction = directions.get(event.key)

            if direction is not None:
                if direction != opposite_directions[
                    game_object.direction
                ]:
                    game_object.next_direction = direction


def main():
    """Запускает игру."""
    pygame.display.set_caption('Змейка')

    snake = Snake()
    apple = Apple(set(snake.positions))

    while True:
        clock.tick(10)

        handle_keys(snake)

        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(set(snake.positions))

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(set(snake.positions))
            continue

        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw(screen)
        apple.draw(screen)

        pygame.display.update()


if __name__ == '__main__':
    main()
