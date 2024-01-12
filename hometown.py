import pygame as pg
pg.init()

# Setting up basic information like how the pop-up window should be, what font, etc. Variables for convenience
window_w, window_h = 1280, 720
display = pg.display.set_mode((window_w, window_h))
pg.display.set_caption('Falschung')
window_c = (window_w//2, window_h//2)
my_font = pg.font.SysFont('Helvetica', 20)

# Loading all core images to be transformed later for different use cases
true_bg = pg.image.load('./images/background/bg.png')
player = pg.image.load('./images/player/fplayer.png')

# Setting up world map with desired core image multiplier, variables for convenience
bg_k = 6
bg = pg.transform.scale(true_bg, (true_bg.get_width()*bg_k, true_bg.get_height()*bg_k))
bg_w, bg_h = bg.get_width(), bg.get_height()

# Giving spawn coordinates (with respect to world map, not core image, therefore no multiplier)
spn = (55, 630)

# From the center of the window, go back halfway the size of yourself to center, then deviated by the given spawn data
map_pos = pg.Vector2(window_c[0] - bg_w//2 - spn[0], window_c[1] - bg_h//2 - spn[1])

# Variables for convenience, From the center of the window, go back halfway your size to center
player_w, player_h = player.get_width(), player.get_height()
PLAYER_BLIT_CENTER = pg.Vector2(window_c[0] - player_w//2, window_c[1] - player_h//2)
player_blit_pos = pg.Vector2(PLAYER_BLIT_CENTER.x, PLAYER_BLIT_CENTER.y)

mp_k = 0.4             # When translating core image to minimap
true_mp_k = mp_k/bg_k  # When translating world map to minimap
# Shrink using core image multiplier to get minimap size, variables for convenience
mp = pg.transform.scale(true_bg, (true_bg.get_width()*mp_k, true_bg.get_height()*mp_k))
mp_w, mp_h = mp.get_width(), mp.get_height()
# Giving some margin for the minimap, only for aesthetics
mp_pos = pg.Vector2(10, 10)
# Transform player size using world map multiplier, as the image is not upscaled and is used as is in the world map
mplayer = pg.transform.scale(player, (player_w*true_mp_k, player_h*true_mp_k))
mplayer_w, mplayer_h = mplayer.get_width(), mplayer.get_height()
# similarly, spawn is with respect to world map, therefore world map multiplier is used
mp_spn = (spn[0]*true_mp_k, spn[1]*true_mp_k)
# Account for margins, go halfway across the map, then center the minimap player icon, and finally go to spawn point
mp_player_pos = pg.Vector2(mp_pos.x + mp_w//2 - mplayer.get_width()//2 + mp_spn[0], mp_pos.y + mp_h//2 - mplayer.get_height()//2 + mp_spn[1])

speed = 10
leg_cycle = ['_wrf', '_wrf', '_wrf', '', '', '', '_wlf', '_wlf', '_wlf', '', '', '']
cycle_len = len(leg_cycle) -1
sprite_direction, this_leg = 'f', 0
# It's some nice woody color... I think, for the border of the minimap... hence the margins
mp_border = (164, 116, 73)

walking = False
game_run = True
clock = pg.time.Clock()
while game_run:
    # Very important for closing the actual window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_run = False

    # Here's where the key detection and movement are done
    keys = pg.key.get_pressed()
    
    # For debugging 
    if keys[pg.K_3]:
        speed+=2
    elif keys[pg.K_1]:
        speed-=2

    # this_pos, this_way = map_pos, -speed
    
    # Made the boundary conditions
    if map_pos.x >= 0:
        map_pos.x = 0
        if player_blit_pos.x <= PLAYER_BLIT_CENTER.x:
            this_pos_x, this_way_x = player_blit_pos, speed
        else:
            this_pos_x, this_way_x = map_pos, -speed
    elif map_pos.x <= -bg_w + window_w:
        map_pos.x = -bg_w + window_w
        if player_blit_pos.x >= PLAYER_BLIT_CENTER.x:
            this_pos_x, this_way_x = player_blit_pos, speed
        else:
            this_pos_x, this_way_x = map_pos, -speed
    else:
        player_blit_pos.x = PLAYER_BLIT_CENTER.x
        this_pos_x, this_way_x = map_pos, -speed
        
    if map_pos.y >= 0:
        map_pos.y = 0
        if player_blit_pos.y <= PLAYER_BLIT_CENTER.y:
            this_pos_y, this_way_y = player_blit_pos, speed
        else:
            this_pos_y, this_way_y = map_pos, -speed
    elif map_pos.y <= -bg_h + window_h:
        map_pos.y = -bg_h + window_h
        if player_blit_pos.y >= PLAYER_BLIT_CENTER.y:
            this_pos_y, this_way_y = player_blit_pos, speed
        else:
            this_pos_y, this_way_y = map_pos, -speed
    else:
        player_blit_pos.y = PLAYER_BLIT_CENTER.y
        this_pos_y, this_way_y = map_pos, -speed
    
    if keys[pg.K_w] or keys[pg.K_UP]:
        # The whole world revolves around the player, so the movement has to be mirrored
        this_pos_y.y -= this_way_y
        # The minimap stays static, so the player has to move... with the world map multiplier
        mp_player_pos.y -= speed * true_mp_k
        # Looks like the user pressed a key... again... *sigh*... Time to get walking
        walking = True
        # As you know which key was pressed, you can figure out where the user is going
        sprite_direction = 'b'
    elif keys[pg.K_s] or keys[pg.K_DOWN]:
        this_pos_y.y += this_way_y
        mp_player_pos.y += speed * true_mp_k
        walking = True
        sprite_direction = 'f'
    elif keys[pg.K_a] or keys[pg.K_LEFT]:
        this_pos_x.x -= this_way_x
        mp_player_pos.x -= speed * true_mp_k
        walking = True
        sprite_direction = 'l'
    elif keys[pg.K_d] or keys[pg.K_RIGHT]:
        this_pos_x.x += this_way_x
        mp_player_pos.x += speed * true_mp_k
        walking = True
        sprite_direction = 'r'
    # Keep traversing through the legs
    this_leg = (this_leg + 1) % cycle_len
    
    # Fill the screen with some color to clear all previous images
    display.fill((0, 0, 0))
    # Drawn the world
    display.blit(bg, (map_pos.x, map_pos.y))

    # Determine the state of the player; is he walking? then what direction is he walking?
    player = pg.image.load(f'./images/player/{sprite_direction}player{leg_cycle[this_leg] if walking else ""}.png')
    # Draw the actual player ont he screen
    display.blit(player, (player_blit_pos.x, player_blit_pos.y))
    # Assume user has stopped inputting, as we will check it in the if statements again
    walking = False

    # Draw a solid rectangle before the minimap to LOOK like it has a border... IDK how to actually do it though
    pg.draw.rect(display, mp_border, [5, 5, mp_w+10, mp_h+10])
    # Draw the minimap on top of that solid rectangle
    display.blit(mp, (mp_pos.x, mp_pos.y))
    
    # Draw the player on top of the minimap. Needs a bit more readjusting, but now the minimap player works based on calculation and doesn't need it's own speed
    mp_player_pos.x=-(map_pos.x-window_w//2)*true_mp_k + mplayer_w//2
    mp_player_pos.y=-(map_pos.y-window_h//2)*true_mp_k + mplayer_h//2
    display.blit(mplayer, (mp_player_pos.x, mp_player_pos.y))
    
    # Debugging coordinate awesomeness
    text_surface = my_font.render(f"Mouse_Pos: {pg.mouse.get_pos()} Player_Pos:{map_pos} Blit Pos:{player_blit_pos} Speed:{speed} Bg:{bg_w,bg_h} Map:{mp_player_pos,(map_pos.y-window_h)//(bg_k/mp_k)}", False, (200, 255, 200), (70,100,80))
    display.blit(text_surface, (0, window_h-24))
    flag_debug = my_font.render(f"player_blit_pos Flag:{player_blit_pos.x <= PLAYER_BLIT_CENTER.x}            map_pos Flag:{map_pos.x >= 0}", False, (200, 255, 200), (70,100,80))
    display.blit(flag_debug, (0, 0))

    

    # Update the display to show the next frame and our hard work
    pg.display.flip()
    # This guy just takes care of frame rates, he's very good at it too. For now the game runs at 15 fps
    clock.tick(15)

# This will terminate the game and close the window!
pg.quit()
