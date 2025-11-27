import pygame
import sys
import math

# busniss.py
# Simple Pygame demo: an "office" scene where a pen slides off a table and falls.
# Run: python busniss.py

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
WALL = (230, 230, 240)
FLOOR = (200, 180, 160)
TABLE = (120, 80, 40)
PEN_BODY = (15, 90, 160)
PEN_CLIP = (200, 200, 200)
PICT = (180, 210, 255)

# Scene geometry
table_w = 520
table_h = 20
table_x = (WIDTH - table_w) // 2
table_top = 300
table_rect = pygame.Rect(table_x, table_top, table_w, table_h)
floor_y = 520

# Pen physical model (rectangle rotated)
pen_len = 90
pen_w = 10
# Start near left of table top and slowly slide to the right
pen_x = table_x + 40 + pen_len / 2
pen_y = table_top - pen_w / 2
pen_angle = -8  # degrees, slight tilt
slide_speed = 40.0  # px/sec while on table toward edge

# Physics after falling
falling = False
vx = 30.0  # horizontal speed once it leaves table (px/sec)
vy = 0.0
ang_vel = 0.0  # degrees/sec when falling
g = 900.0  # px/sec^2
restitution = 0.25

def draw_office():
    screen.fill(WALL)
    # window/picture on wall
    pygame.draw.rect(screen, PICT, (60, 60, 160, 110), border_radius=6)
    # floor area
    pygame.draw.rect(screen, FLOOR, (0, floor_y, WIDTH, HEIGHT - floor_y))
    # table
    pygame.draw.rect(screen, TABLE, table_rect, border_radius=4)
    # table legs
    leg_w, leg_h = 20, 120
    pygame.draw.rect(screen, TABLE, (table_x + 40, table_top + table_h, leg_w, leg_h))
    pygame.draw.rect(screen, TABLE, (table_x + table_w - 40 - leg_w, table_top + table_h, leg_w, leg_h))

def draw_pen(cx, cy, angle_deg):
    # Draw a rotated pen centered at (cx, cy) with length pen_len and width pen_w
    angle = math.radians(angle_deg)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    # Pen rectangle corners relative to center
    hx = pen_len / 2
    hy = pen_w / 2
    corners = [(-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy)]
    rot = []
    for x, y in corners:
        rx = x * cos_a - y * sin_a + cx
        ry = x * sin_a + y * cos_a + cy
        rot.append((rx, ry))
    pygame.draw.polygon(screen, PEN_BODY, rot)
    # pen clip near one end (small rectangle)
    clip_center_x = cx + (pen_len * 0.3) * cos_a
    clip_center_y = cy + (pen_len * 0.3) * sin_a
    clip_w = 16
    clip_h = 4
    # draw clip as small rotated rectangle
    chx = clip_w / 2
    chy = clip_h / 2
    clip_corners = [(-chx, -chy), (chx, -chy), (chx, chy), (-chx, chy)]
    clip_rot = []
    for x, y in clip_corners:
        rx = x * cos_a - y * sin_a + clip_center_x
        ry = x * sin_a + y * cos_a + clip_center_y
        clip_rot.append((rx, ry))
    pygame.draw.polygon(screen, PEN_CLIP, clip_rot)

def main():
    global pen_x, pen_y, pen_angle, falling, vx, vy, ang_vel
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # press SPACE to restart
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset()

        # If not falling, slide pen toward table edge
        if not falling:
            pen_x += slide_speed * dt
            # check if pen center passes table edge - then it becomes unsupported and falls
            right_support = table_x + table_w  # table right edge x
            # simple criterion: pen center beyond right edge minus a small margin
            if pen_x + pen_len/2 * math.cos(math.radians(pen_angle)) > right_support:
                falling = True
                # initial velocities at moment of leaving
                vx = 160.0  # give it a push horizontally
                vy = 40.0
                ang_vel = 600.0 * (1 if pen_angle >= 0 else -1)
        else:
            # physics integration
            vy += g * dt
            pen_x += vx * dt
            pen_y += vy * dt
            pen_angle += ang_vel * dt
            # collision with floor (use half-diagonal of pen to approximate)
            half_diag = math.hypot(pen_len / 2, pen_w / 2)
            if pen_y + half_diag >= floor_y:
                # place pen on floor
                pen_y = floor_y - half_diag
                # simple bounce
                vy = -vy * restitution
                vx *= 0.7
                ang_vel *= 0.3
                # if nearly stopped, zero velocities
                if abs(vy) < 40 and abs(ang_vel) < 40:
                    vy = 0
                    vx = 0
                    ang_vel = 0

        # draw scene
        draw_office()
        draw_pen(pen_x, pen_y, pen_angle)
        # small instructions
        font = pygame.font.SysFont(None, 20)
        txt = font.render("Press SPACE to restart. Close window to quit.", True, (30,30,30))
        screen.blit(txt, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

def reset():
    global pen_x, pen_y, pen_angle, falling, vx, vy, ang_vel
    pen_x = table_x + 40 + pen_len / 2
    pen_y = table_top - pen_w / 2
    pen_angle = -8
    falling = False
    vx = 30.0
    vy = 0.0
    ang_vel = 0.0

if __name__ == "__main__":
    main()