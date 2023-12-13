import pygame, time
pygame.init()

window_w, window_h = 1280, 720
screen = pygame.display.set_mode((window_w, window_h), pygame.RESIZABLE)

true_bg = pygame.image.load('bg.png')

screen_coefficient = 6
bg = pygame.transform.scale(true_bg, (true_bg.get_width()*screen_coefficient, true_bg.get_height()*screen_coefficient))
bgw, bgh = bg.get_width(), bg.get_height()

spawn_x, spawn_y = 100*screen_coefficient, 0*screen_coefficient
player_pos = pygame.Vector2((screen.get_width() - bgw)//2 - spawn_x, (screen.get_height() - bgh)//2 - spawn_y)
player_img = pygame.image.load('fplayer_wf.png')
pgw, pgh = player_img.get_width(), player_img.get_height()
display_center = pygame.Vector2((screen.get_width() - pgw)//2, (screen.get_height() - pgh)//2)
speed = 10

minimap_coefficient = 0.4
mp_player_coefficient = 0.1
mp = pygame.transform.scale(true_bg, (true_bg.get_width()*minimap_coefficient, true_bg.get_height()*minimap_coefficient))
mp_w, mp_h = mp.get_width(), mp.get_height()
mp_player = pygame.transform.scale(player_img, (player_img.get_width()*mp_player_coefficient, player_img.get_height()*mp_player_coefficient))
mp_player_pos = pygame.Vector2(200, 100)
mp_speed_coefficient = 0.07

# coordinates
# y=400->-2000 x=-3600->400

leg_cycle = ['r', '', 'l', '',]
sprite_direction, this_leg = 'f', 0

walking = False

game_run = True
clock = pygame.time.Clock()
while game_run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_run = False

    screen.fill((0, 0, 0))
    screen.blit(bg, (player_pos.x, player_pos.y))

    player_img = pygame.image.load(f'{sprite_direction}player_w{leg_cycle[this_leg] if walking else ""}f.png')
    screen.blit(player_img, (display_center.x, display_center.y))
    walking = False

    pygame.draw.rect(screen, (164,116,73), [5, 5, mp_w+10, mp_h+10])
    screen.blit(mp, (10, 10))
    screen.blit(mp_player, (mp_player_pos.x, mp_player_pos.y))


    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        player_pos.y -= -speed
        mp_player_pos.y -= speed * mp_speed_coefficient
        walking = True
        sprite_direction = 'b'
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        player_pos.y += -speed
        mp_player_pos.y += speed * mp_speed_coefficient
        walking = True
        sprite_direction = 'f'
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player_pos.x -= -speed
        mp_player_pos.x -= speed * mp_speed_coefficient
        walking = True
        sprite_direction = 'l'
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_pos.x += -speed
        mp_player_pos.x += speed * mp_speed_coefficient
        walking = True
        sprite_direction = 'r'

    this_leg = (this_leg + 1) % 3
    pygame.display.flip()
    clock.tick(15)

pygame.quit()
