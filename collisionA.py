import pygame as pg
pg.init()

window_w, window_h = 1280, 720
display = pg.display.set_mode((window_w, window_h))
pg.display.set_caption('Falschung')
my_font = pg.font.SysFont('Helvetica', 20)

window_c = (window_w//2, window_h//2)


bg_k = 6
mp_k = 0.4
true_bg_img = pg.image.load('./Media/images/background/bg.png')
player_img = pg.image.load('./Media/images/player/fplayer.png')
def draw_rect_alpha(surface, color, rect):
    shape_surf = pg.Surface(pg.Rect(rect).size, pg.SRCALPHA)
    pg.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

spn = (2450, 2040)
global_pos = pg.Vector2(spn[0],spn[1])

class Map(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        image = pg.transform.scale(image, (image.get_width()*bg_k, image.get_height()*bg_k))
        self.image = image
        self.rect = self.image.get_rect()
        self.w, self.h = image.get_width(), image.get_height()
        self.blit_pos = pg.Vector2(global_pos)
            
    def update(self):
        self.boundary_update()
    
    def boundary_update(self):
        if global_pos.x<=window_c[0]:
            self.blit_pos.x = window_c[0]
        elif global_pos.x>=self.w-window_c[0]:
            self.blit_pos.x = self.w-window_c[0]
        else:
            self.blit_pos.x = global_pos.x
        if global_pos.y<=window_c[1]:
            self.blit_pos.y = window_c[1]
        elif global_pos.y>=self.h-window_c[1]:
            self.blit_pos.y = self.h-window_c[1]
        else:
            self.blit_pos.y = global_pos.y
        
        self.blit_pos.x, self.blit_pos.y = window_c[0]-self.blit_pos.x, window_c[1]-self.blit_pos.y
    
    def blit(self):
        display.blit(self.image, self.blit_pos)


class Player(pg.sprite.Sprite):
    def __init__(self,top_left ,image ):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.top_left =top_left
        self.left = top_left[0] * bg_k
        self.top = top_left[1] * bg_k
        self.w, self.h = self.image.get_width(), self.image.get_height()
        self.PLAYER_BLIT_CENTER = pg.Vector2(window_c[0] - self.w//2, window_c[1] - self.h//2)
        self.blit_pos = pg.Vector2(self.PLAYER_BLIT_CENTER.x, self.PLAYER_BLIT_CENTER.y)
        self.speed = 50
        self.leg_cycle = ['_wrf', '_wrf', '_wrf', '', '', '', '_wlf', '_wlf', '_wlf', '', '', '']
        self.cycle_len = len(self.leg_cycle)
        self.sprite_direction, self.this_leg = 'f', 0
        self.walking = False
        self.prev_pos = pg.Vector2(global_pos)
        self.collide = False
    
    def movement_update(self, keys):
        self.prev_pos = pg.Vector2(global_pos)
        self.rect.x, self.rect.y = self.blit_pos.x, self.blit_pos.y
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
        
    def boundary_update(self, map):    
        # pass
        if global_pos.x<=window_c[0]:
            self.blit_pos.x = global_pos.x
        elif global_pos.x>=map.w-window_c[0]:
            self.blit_pos.x = self.PLAYER_BLIT_CENTER.x + (global_pos.x-(map.w-window_c[0]))
        else:
            self.blit_pos.x = self.PLAYER_BLIT_CENTER.x
            
        if global_pos.y<=window_c[1]:
            self.blit_pos.y = global_pos.y
        elif global_pos.y>=map.h-window_c[1]:
            self.blit_pos.y = self.PLAYER_BLIT_CENTER.y + (global_pos.y-(map.h-window_c[1]))
        else:
            self.blit_pos.y = self.PLAYER_BLIT_CENTER.y

    def collide_update(self, object):
        self.collide = False
        
        if self.rect.colliderect(object.rect):
            self.collide = True
            global_pos = self.prev_pos
            
    
    def update(self, keys, map, object):
        self.movement_update(keys)
        self.boundary_update(map)
        self.collide_update(object)
        
    def blit(self):
        display.blit(self.image, self.blit_pos)

    def givetopleft(self):
        return self.top_left

class Minimap(pg.sprite.Sprite):
    def __init__(self, image, player_image):
        pg.sprite.Sprite.__init__(self)
        image = pg.transform.scale(image, (image.get_width()*mp_k, image.get_height()*mp_k))
        self.image = image
        player_image = pg.transform.scale(player_image, (player.w*mp_k/bg_k, player.h*mp_k/bg_k))
        self.player_image = player_image
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

class Object(pg.sprite.Sprite):
    def __init__(self, top_left, bottom_right):
        self.left = top_left[0]* bg_k
        self.top = top_left[1] * bg_k
        self.w = (bottom_right[0] - top_left[0])*bg_k
        self.h = (bottom_right[1] - top_left[1])*bg_k
        self.rect = pg.Rect(self.top, self.left, self.w, self.h)
        self.color = (0,255,0,100)
    
    def update(self):
        self.rect.x, self.rect.y = window_c[0]+(self.left-global_pos[0]), window_c[1]+(self.top-global_pos[1])
        draw_rect_alpha(display, self.color, self.rect)

player = Player((0, 0),image=player_img)
map = Map(image=true_bg_img)
minimap = Minimap(image=true_bg_img, player_image = player_img)
game_run = True
clock = pg.time.Clock()

red_house = Object((472, 314), (533, 380))

while game_run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_run = False

    keys = pg.key.get_pressed()
   
    player.update(keys, map,red_house)
    map.update()
    minimap.update()
    prev_rect1_pos = player.givetopleft()
   
    
    display.fill((255, 0, 0))
    map.blit()
    minimap.blit()
    red_house.update()
    text_surface = my_font.render(f"Global: {global_pos}, Speed: {player.speed}, Mouse: {pg.mouse.get_pos()} Map:{map.w} {player.rect} {red_house.rect}", False, (200, 255, 200), (70,100,80))
    display.blit(text_surface, (0, window_h-24))
    player.blit()
    
    pg.display.flip()
    clock.tick(15)

pg.quit()
