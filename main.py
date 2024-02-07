import sys
import pygame
import random
import os
from object import Player, Bullet, CurvedBullet, Button

pygame.init()

WIDTH, HEIGHT = 600, 600
FPS = 240


#pygame stuff
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge")
clock = pygame.time.Clock()
BOLD_FONT = pygame.font.Font(os.path.abspath('fonts/bold_font.ttf'), 21)
NORM_FONT = pygame.font.Font(os.path.abspath('fonts/norm_font.ttf'), 16)

#game stuff
score = 1
score_board = BOLD_FONT.render(
    f"Round: {score}", True, (240, 240, 240), (115, 117, 117))

player = Player()
player_group = pygame.sprite.Group(player)
bullet_group = pygame.sprite.Group()
countdown_group = pygame.sprite.Group()
wait_time = 0
wait_delay = 2 * FPS

bullet_spawn_time = 0
bullet_spawn_delay = FPS
current_bullet_count = 1
max_bullet_count = current_bullet_count

prepare_time = 0
prepare_delay = 5 * FPS

state = "PREPARE"

def reset():
    global state, score, player, current_bullet_count, max_bullet_count, bullet_spawn_delay, bullet_spawn_time, prepare_time, prepare_delay
    score = 1
    current_bullet_count = 1
    max_bullet_count = current_bullet_count
    bullet_spawn_time = 0
    bullet_spawn_delay = FPS
    prepare_time = 0
    prepare_delay = 5 * FPS
    state = "PREPARE"
    
def endGame():
    global running
    running = False
    sys.exit(0)
    
reset_button = Button(WIDTH / 2 - 50, HEIGHT / 2 + 100, 75, 50, 'PLAY', NORM_FONT, (0, 128, 0), (0, 255, 0), reset)
quit_button = Button(WIDTH / 2 + 50, HEIGHT / 2 + 100, 75, 50, 'QUIT', NORM_FONT, (128, 0, 0), (255, 0, 0), endGame)
button_group = pygame.sprite.Group()
button_group.add(reset_button)
button_group.add(quit_button)

last_time = pygame.time.get_ticks()
run = True
while run:
    current_time = pygame.time.get_ticks()
    delta = (current_time - last_time) / 1000.0  # Convert milliseconds to seconds
    last_time = current_time
    
    event_list = pygame.event.get()
    for event in event_list:
        if event.type == pygame.QUIT:
            endGame()

    if state == "PREPARE":
        pygame.mouse.set_visible(False)
        prepare_time += 1
        prepare_text = BOLD_FONT.render(
            str(int((prepare_delay-prepare_time) / FPS)), True, (240, 240, 240), (115, 117, 117))
        text_rect = prepare_text.get_rect()
        text_rect.center = (WIDTH / 2, HEIGHT / 2)
        screen.blit(prepare_text, text_rect)
        if prepare_time > prepare_delay:
            state = "PLAY"
            player.move = True
    if state == "WAIT":
        wait_time += 1
        # print(wait_time)
        if wait_time > wait_delay:
            wait_time = 0
            state = "PLAY"
    elif state == "PLAY":
        if current_bullet_count <= 0 and len(bullet_group):
            state = "WAIT"
            score += 1
            bullet_spawn_delay = int(bullet_spawn_delay * 0.95)
            # max_bullet_count = int(max_bullet_count * 1.5)
            max_bullet_count += 1
            current_bullet_count = max_bullet_count
        bullet_spawn_time += 1
        if bullet_spawn_time > bullet_spawn_delay:
            bullet_spawn_time = 0
            current_bullet_count -= 1
            side = random.choice([0, 1])
            pos_out = random.choice([-50, WIDTH + 50])
            pos_in = random.randint(0, WIDTH)
            if side == 0:
                x = pos_out
                y = pos_in
            else:
                y = pos_out
                x = pos_in
            l = [Bullet(FPS, x, y), CurvedBullet(FPS, x, y)]
            if (score > 5):
                bullet_group.add(random.choice(l))
            else:
                bullet_group.add(l[0])
    elif state == "STOP":
        death_text = BOLD_FONT.render(f"YOU DIED at round {score}!", True, (240, 240, 240), (115, 117, 117))
        text_rect = death_text.get_rect()
        text_rect.center = (WIDTH / 2, HEIGHT / 2)
        screen.blit(death_text, text_rect)
        button_group.draw(screen)
        button_group.update(event_list)
    pygame.display.flip()
    screen.fill((0, 0, 0))
    score_board = BOLD_FONT.render(
                f"Round: {score}", True, (240, 240, 240), (115, 117, 117))
    screen.blit(score_board, (0, 0))
    if player.move:
        player_group.draw(screen)
        player_group.update(WIDTH, HEIGHT)
    bullet_group.draw(screen)
    bullet_group.update(delta, WIDTH, HEIGHT)
    hit = pygame.sprite.groupcollide(
        player_group, bullet_group, False, False)
    if hit:
        player.move = False
        bullet_group.empty()
        pygame.mouse.set_visible(True)
        state = "STOP"
    clock.tick(FPS)
