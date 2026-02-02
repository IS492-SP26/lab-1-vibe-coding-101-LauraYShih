import math
import random

import pygame

WIDTH = 800
HEIGHT = 500

BG_COLOR = (20, 20, 20)
WHITE = (240, 240, 240)
PADDLE_COLOR = (200, 200, 200)
BALL_COLOR = (240, 80, 80)

PADDLE_WIDTH = 12
PADDLE_HEIGHT = 90
BALL_RADIUS = 8

PADDLE_SPEED = 6
BALL_SPEED = 5
MAX_BALL_SPEED = 12
MAX_BOUNCE_ANGLE = math.radians(60)


def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))


def reset_ball(direction):
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    angle = random.uniform(-MAX_BOUNCE_ANGLE / 2, MAX_BOUNCE_ANGLE / 2)
    vx = BALL_SPEED * math.cos(angle) * direction
    vy = BALL_SPEED * math.sin(angle)
    return ball_x, ball_y, vx, vy


def handle_paddle_collision(ball_x, ball_y, ball_vx, ball_vy, paddle, direction):
    relative = (ball_y - paddle.centery) / (PADDLE_HEIGHT / 2)
    relative = clamp(relative, -1, 1)
    bounce_angle = relative * MAX_BOUNCE_ANGLE
    new_speed = min(MAX_BALL_SPEED, math.hypot(ball_vx, ball_vy) + 0.3)
    new_vx = new_speed * math.cos(bounce_angle) * direction
    new_vy = new_speed * math.sin(bounce_angle)
    return new_vx, new_vy


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Ping Pong")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 48)
    hint_font = pygame.font.Font(None, 24)

    left_paddle = pygame.Rect(
        30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT
    )
    right_paddle = pygame.Rect(
        WIDTH - 30 - PADDLE_WIDTH,
        HEIGHT // 2 - PADDLE_HEIGHT // 2,
        PADDLE_WIDTH,
        PADDLE_HEIGHT,
    )

    left_score = 0
    right_score = 0

    ball_x, ball_y, ball_vx, ball_vy = reset_ball(random.choice((-1, 1)))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            left_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_s]:
            left_paddle.y += PADDLE_SPEED
        if keys[pygame.K_UP]:
            right_paddle.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN]:
            right_paddle.y += PADDLE_SPEED

        left_paddle.y = clamp(left_paddle.y, 0, HEIGHT - PADDLE_HEIGHT)
        right_paddle.y = clamp(right_paddle.y, 0, HEIGHT - PADDLE_HEIGHT)

        ball_x += ball_vx
        ball_y += ball_vy

        if ball_y - BALL_RADIUS <= 0:
            ball_y = BALL_RADIUS
            ball_vy *= -1
        elif ball_y + BALL_RADIUS >= HEIGHT:
            ball_y = HEIGHT - BALL_RADIUS
            ball_vy *= -1

        ball_rect = pygame.Rect(
            int(ball_x - BALL_RADIUS),
            int(ball_y - BALL_RADIUS),
            BALL_RADIUS * 2,
            BALL_RADIUS * 2,
        )

        if ball_rect.colliderect(left_paddle) and ball_vx < 0:
            ball_x = left_paddle.right + BALL_RADIUS
            ball_vx, ball_vy = handle_paddle_collision(
                ball_x, ball_y, ball_vx, ball_vy, left_paddle, 1
            )

        if ball_rect.colliderect(right_paddle) and ball_vx > 0:
            ball_x = right_paddle.left - BALL_RADIUS
            ball_vx, ball_vy = handle_paddle_collision(
                ball_x, ball_y, ball_vx, ball_vy, right_paddle, -1
            )

        if ball_x < 0:
            right_score += 1
            ball_x, ball_y, ball_vx, ball_vy = reset_ball(-1)
        elif ball_x > WIDTH:
            left_score += 1
            ball_x, ball_y, ball_vx, ball_vy = reset_ball(1)

        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, PADDLE_COLOR, left_paddle)
        pygame.draw.rect(screen, PADDLE_COLOR, right_paddle)
        pygame.draw.circle(screen, BALL_COLOR, (int(ball_x), int(ball_y)), BALL_RADIUS)

        pygame.draw.aaline(
            screen, (80, 80, 80), (WIDTH // 2, 10), (WIDTH // 2, HEIGHT - 10)
        )

        score_text = font.render(f"{left_score}   {right_score}", True, WHITE)
        screen.blit(
            score_text,
            (WIDTH // 2 - score_text.get_width() // 2, 20),
        )

        hint_text = hint_font.render(
            "Left: W/S   Right: Up/Down   Esc: Quit", True, (160, 160, 160)
        )
        screen.blit(
            hint_text,
            (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 30),
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
