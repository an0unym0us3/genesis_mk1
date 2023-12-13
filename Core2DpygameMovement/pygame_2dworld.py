import pygame, time
pygame.init()

screen = pygame.display.set_mode((1280, 720))

screen_coefficient = 5
truebg = pygame.image.load('bg.png')
bg = pygame.transform.scale(truebg, (truebg.get_width()*screen_coefficient, truebg.get_height()*screen_coefficient))
bgw, bgh = bg.get_width(), bg.get_height()

spawn_x, spawn_y = 100*screen_coefficient, 0
player_pos = pygame.Vector2((screen.get_width() - bgw)//2 - spawn_x, (screen.get_height() - bgh)//2 - spawn_y)
player_img = pygame.image.load('fplayer_wf.png')
pgw, pgh = player_img.get_width(), player_img.get_height()
display_center = pygame.Vector2((screen.get_width() - pgw)//2, (screen.get_height() - pgh)//2)
speed = 8

leg_cycle = ['r', '', 'l', '',]
x, this_leg = 'f', 0
game_run = True
walking = False

while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

    screen.fill((0, 0, 0))
    screen.blit(bg, (player_pos.x, player_pos.y))

    player_img = pygame.image.load(f'{x}player_w{leg_cycle[int(this_leg)] if walking else ""}f.png')
    screen.blit(player_img, (display_center.x, display_center.y))
    walking = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_pos.y -= -speed
        walking = True
        x = 'b'
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_pos.y += -speed
        walking = True
        x = 'f'
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_pos.x -= -speed
        walking = True
        x = 'l'
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_pos.x += -speed
        walking = True
        x = 'r'

    this_leg = (this_leg + 1) % 3
    pygame.display.flip()
    time.sleep(0.01)

pygame.quit()
