import pygame
import sys
from random import randint, uniform


def laser_update(laser_lst, speed=200):
    for rect in laser_lst:
        rect.y -= (speed * dt)
        if rect.bottom < 0:
            laser_lst.remove(rect)


def display_score(value):
    score_txt = f'Score: {value}'
    text_surf = font.render(score_txt, True, (255, 255, 255))
    text_rect = text_surf.get_rect(midbottom=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 80))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, (255, 255, 255), text_rect.inflate(30, 30), width=8, border_radius=5)


def laser_timer(can_shoot, duration=500):
    if not can_shoot:
        cur_time = pygame.time.get_ticks()
        if (cur_time - shoot_time) > duration:
            can_shoot = True
    return can_shoot


def meteor_update(meteor_lst, speed=40):
    for meteor_tuple in meteor_lst:
        direction = meteor_tuple[1]
        rect = meteor_tuple[0]
        rect.center += (direction * speed * dt)
        if rect.top > WINDOW_HEIGHT:
            meteor_lst.remove(meteor_tuple)

        # game init


pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Asteroid shooter')
clock = pygame.time.Clock()

# ship import
ship_surf = pygame.image.load('./images/ship.png').convert_alpha()
ship_rect = ship_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

# background
bg_surf = pygame.image.load('./images/background.png').convert()

# laser import
laser_surf = pygame.image.load('./images/laser.png').convert_alpha()
# laser_rect = laser_surf.get_rect(midbottom=ship_rect.midtop)
laser_lst = []

# laser timer
can_shoot = True
shoot_time = None

# import text
font = pygame.font.Font('./font/subatomic.ttf', 50)

# meteor timer
meteor_timer = pygame.event.custom_type()
pygame.time.set_timer(meteor_timer, 600)

# meteor import
meteor_surf = pygame.image.load("./images/meteor.png").convert_alpha()
meteor_lst = []

score_value = 0

# import sound
laser_sound = pygame.mixer.Sound("./sounds/laser.ogg")
explosion_sound = pygame.mixer.Sound("./sounds/explosion.wav")
music = pygame.mixer.Sound("./sounds/music.wav")
music.play(loops=-1)

while True:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and can_shoot:
            # laser
            laser_rect = laser_surf.get_rect(midbottom=ship_rect.midtop)
            laser_lst.append(laser_rect)

            # timer
            can_shoot = False
            shoot_time = pygame.time.get_ticks()

            # laser sound
            laser_sound.play()

        if event.type == meteor_timer:
            # random pos
            xpos = randint(-100, WINDOW_WIDTH + 100)
            ypos = randint(-100, -50)
            meteor_rect = meteor_surf.get_rect(center=(xpos, ypos))

            # random direction
            direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)

            meteor_lst.append((meteor_rect, direction))

    # framerate limit
    dt = clock.tick(120) / 100

    # mouse input
    ship_rect.center = pygame.mouse.get_pos()

    # update
    # laser_rect.y -= 10 *dt
    laser_update(laser_lst)
    meteor_update(meteor_lst)
    can_shoot = laser_timer(can_shoot)

    # meteor ship collisions
    for meteor_tuple in meteor_lst:
        if ship_rect.colliderect(meteor_tuple[0]):
            pygame.quit()
            sys.exit()
    for laser in laser_lst:
        for meteor_tuple in meteor_lst:
            if meteor_tuple[0].colliderect(laser):
                explosion_sound.play()
                meteor_lst.remove(meteor_tuple)
                score_value += 1
    # drawing
    display_surface.fill((0, 0, 0))
    display_surface.blit(bg_surf, (0, 0))

    display_score(score_value)

    for x in laser_lst:
        display_surface.blit(laser_surf, x)
    display_surface.blit(ship_surf, ship_rect)
    for x in meteor_lst:
        display_surface.blit(meteor_surf, x[0])

    # draw the final frame
    pygame.display.update()
