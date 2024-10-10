import pygame
import sys

pygame.init()
screen_width, screen_height = 800, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PFAD')

ball_radius = 8

start_color = (0, 0, 255)
end_color = (240, 248, 255)

ball_pos = [screen_width // 2, screen_height // 2]
ball_velocity = [0, 0]

trail_points = []

def interpolate_color(color1, color2, factor):
    return (
        int(color1[0] + (color2[0] - color1[0]) * factor),
        int(color1[1] + (color2[1] - color1[1]) * factor),
        int(color1[2] + (color2[2] - color1[2]) * factor)
    )

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse_pos = pygame.mouse.get_pos()

    ball_velocity[0] = (mouse_pos[0] - ball_pos[0]) * 0.1
    ball_velocity[1] = (mouse_pos[1] - ball_pos[1]) * 0.1

    ball_pos[0] += int(ball_velocity[0])
    ball_pos[1] += int(ball_velocity[1])

    trail_points.append(ball_pos.copy())

    trail_points = trail_points[-100:]

    screen.fill((240, 248, 255))

    for i, point in enumerate(trail_points):
        factor = i / len(trail_points)
        color = interpolate_color(start_color, end_color, factor)
        pygame.draw.circle(screen, color, point, ball_radius)

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
