import pygame as pg
pg.init()

window_w, window_h = 1280, 720
display = pg.display.set_mode((window_w, window_h))
pg.display.set_caption('Falschung')
my_font = pg.font.SysFont('Helvetica', 20)

window_c = (window_w//2, window_h//2)


bg_k = 6
mp_k = 0.4
true_bg = pg.image.load('./Media/images/background/bg.png')

spn = (155, 630)


global_pos = pg.Vector2(2400,1440)

class Map(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(image, (image.get_width()*bg_k, image.get_height()*bg_k))
        self.rect = self.image.get_rect()
        self.w, self.h = image.get_width(), image.get_height()
        self.blit_pos = pg.Vector2(global_pos)
    
    def update(self):
        #pass
        self.blit_pos.x, self.blit_pos.y = window_c[0]-global_pos.x, window_c[1]-global_pos.y
    
    def blit(self):
        display.blit(self.image, self.blit_pos)

map = Map(image=true_bg)

class Player(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image.convert_alpha()
        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_width(), self.image.get_height()
        PLAYER_BLIT_CENTER = pg.Vector2(window_c[0] - self.w//2, window_c[1] - self.h//2)
        self.blit_pos = pg.Vector2(PLAYER_BLIT_CENTER.x, PLAYER_BLIT_CENTER.y)
        self.speed = 10
        self.leg_cycle = ['_wrf', '_wrf', '_wrf', '', '', '', '_wlf', '_wlf', '_wlf', '', '', '']
        self.cycle_len = len(self.leg_cycle)
        self.sprite_direction, self.this_leg = 'f', 0
        self.walking = False
        
    def update(self, keys):
        if keys[pg.K_3]:
            self.speed+=2
        elif keys[pg.K_1]:
            self.speed-=2
            
        if keys[pg.K_w] or keys[pg.K_UP]:
            global_pos.y -= self.speed
            self.walking = True
            self.sprite_direction = 'b'
        elif keys[pg.K_s] or keys[pg.K_DOWN]:
            global_pos.y += self.speed
            self.walking = True
            self.sprite_direction = 'f'
        elif keys[pg.K_a] or keys[pg.K_LEFT]:
            global_pos.x -= self.speed
            self.walking = True
            self.sprite_direction = 'l'
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:
            global_pos.x += self.speed
            self.walking = True
            self.sprite_direction = 'r'
        self.this_leg = (self.this_leg + 1) % self.cycle_len
    
        self.image = pg.image.load(f'./Media/images/player/{self.sprite_direction}player{self.leg_cycle[self.this_leg] if self.walking else ""}.png')
        self.walking = False
        
    def blit(self):
        display.blit(self.image, self.blit_pos)
        
player = Player(image=pg.image.load('./Media/images/player/fplayer.png'))

class Minimap(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(image, (image.get_width()*mp_k, image.get_height()*mp_k))
        self.player_image = pg.transform.scale(player.image, (player.w*mp_k/bg_k, player.h*mp_k/bg_k))
        self.rect = self.image.get_rect()
        self.blit_pos = pg.Vector2(10,10)
        self.player_blit_pos = pg.Vector2(global_pos.x*mp_k, global_pos.y*mp_k)
        self.w, self.h = self.image.get_width(), self.image.get_height()
        self.player_w, self.player_h = self.player_image.get_width(), self.player_image.get_height()
        self.border_color = (164, 116, 73)
    
    def update(self):
        self.player_blit_pos = pg.Vector2(global_pos.x*mp_k/bg_k - self.player_w//2 + 10, global_pos.y*mp_k/bg_k - self.player_h//2 + 10)
    
    def blit(self):
        pg.draw.rect(display, self.border_color, [5, 5, self.w+10, self.h+10])
        display.blit(self.image, self.blit_pos)
        display.blit(self.player_image, self.player_blit_pos)
    
minimap = Minimap(image=true_bg)


game_run = True
clock = pg.time.Clock()
while game_run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_run = False

    keys = pg.key.get_pressed()
   
    player.update(keys)
    map.update()
    minimap.update()
    """
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
        this_pos_y.y -= this_way_y
        mp_player_pos.y -= speed * true_mp_k
        walking = True
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
    this_leg = (this_leg + 1) % cycle_len

    flag_debug = my_font.render(f"player_blit_pos Flag:{player_blit_pos.x <= PLAYER_BLIT_CENTER.x}            map_pos Flag:{map_pos.x >= 0}", False, (200, 255, 200), (70,100,80))
    display.blit(flag_debug, (0, 0))
    """
    display.fill((0, 0, 0))
    map.blit()
    minimap.blit()
    text_surface = my_font.render(f"Global: {global_pos}, Speed: {player.speed}, Mouse: {pg.mouse.get_pos()}", False, (200, 255, 200), (70,100,80))
    display.blit(text_surface, (0, window_h-24))
    player.blit()
    pg.display.flip()
    clock.tick(15)

pg.quit()