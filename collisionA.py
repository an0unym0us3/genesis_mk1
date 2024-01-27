import pygame as pg
import subprocess
import random
import os, json
import math

pg.init()

window_w, window_h = 1280, 720
display = pg.display.set_mode((window_w, window_h))
pg.display.set_caption('Falschung')
my_font = pg.font.SysFont('Helvetica', 20)

window_c = (window_w//2, window_h//2)


bg_k = 6
mp_k = 0.4

true_bg_img = pg.image.load('./Media/images/background/bg.png')
transp_bg_img = pg.image.load('./Media/images/background/bg_trans.png')
player_img = pg.image.load('./Media/images/player/normal/fplayer.png')
coin_img = pg.image.load('./Media/images/coin.png')
gun_img = pg.image.load('./Media/images/weapons/gun_green.png')

transp_layer_opacity=127
coin_spawns = (((0,200), (160,480)), ((250,270), (400,480)), ((430,390),(800,480)), ((690,230),(800,380)))

spn = (2450, 2040)
global_pos = pg.Vector2(spn[0],spn[1])

class Map(pg.sprite.Sprite):
    def __init__(self, image, transp_image):
        pg.sprite.Sprite.__init__(self)
        image = pg.transform.scale(image, (image.get_width()*bg_k, image.get_height()*bg_k))
        transp_image = pg.transform.scale(transp_image, (transp_image.get_width()*bg_k, transp_image.get_height()*bg_k))
        transp_image.set_alpha(transp_layer_opacity)
        self.image = image
        self.transp_image = transp_image
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
    def transp_blit(self):
        display.blit(self.transp_image, self.blit_pos)
        

class Player(pg.sprite.Sprite):
    def __init__(self, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.w, self.h = self.image.get_width(), self.image.get_height()
        self.PLAYER_BLIT_CENTER = pg.Vector2(window_c[0] - self.w//2, window_c[1] - self.h//2)
        self.blit_pos = pg.Vector2(self.PLAYER_BLIT_CENTER.x, self.PLAYER_BLIT_CENTER.y)
        self.speed = 10
        self.leg_cycle = ['_wrf', '_wrf', '_wrf', '', '', '', '_wlf', '_wlf', '_wlf', '', '', '']
        self.cycle_len = len(self.leg_cycle)
        self.sprite_direction, self.this_leg = 'f', 0
        self.walking = False
        self.prev_pos = pg.Vector2(global_pos)
        self.collide = False
        self.changed = 0,0
        self.color = (255,0,0)
        self.camouflage=False
        self.shooting = True
        self.bullet_shot = False
        self.left, self.right, self.top, self.bottom = False, False, False, False

        
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
        self.changed = global_pos.x - self.prev_pos.x, global_pos.y- self.prev_pos.y
        self.this_leg = (self.this_leg + 1) % self.cycle_len
        self.image = pg.image.load(f'./Media/images/player/{"camouflage" if self.camouflage else "normal"}/{self.sprite_direction}player{self.leg_cycle[self.this_leg] if self.walking else ""}.png')
        self.walking = False
        
    def boundary_update(self, map):    
        # pass
        if global_pos.x<=0:
            global_pos.x=0
        elif global_pos.x>=map.w-self.w/2:
            global_pos.x=map.w-self.w/2
        if global_pos.y<=0:
            global_pos.y=0
        elif global_pos.y>=map.h-self.h/2:
            global_pos.y=map.h-self.h/2
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
        global global_pos
        self.collide = False
        self.left, self.right, self.top, self.bottom = False, False, False, False
        
        if self.rect.colliderect(object.rect):
            self.left, self.right, self.top, self.bottom =(abs(object.rect.x - (self.blit_pos[0]+self.w))<=self.speed,
                                                       abs((object.rect.x + object.w) - self.blit_pos[0])<=self.speed,
                                                       abs(object.rect.y - (self.blit_pos[1]+self.h))<=self.speed,
                                                       abs((object.rect.y + object.h) - self.blit_pos[1])<=self.speed)  
            self.collide = True
            self.offset = [0,0]
                                                            
            if self.changed[0]>0:
                if abs(object.rect.x - (self.blit_pos[0]+self.w))<=self.speed:
                    self.offset[0] = -1
                else:
                    self.offset[0] = 1
            elif self.changed[0]<0:
                if abs((object.rect.x + object.w) - self.blit_pos[0])<=self.speed:
                    self.offset[0] = 1
                else:
                    self.offset[0] = -1
            if self.changed[1]>0:
                if abs(object.rect.y - (self.blit_pos[1]+self.h))<=self.speed:
                    self.offset[1] = -1
                else:
                    self.offset[1] = 1
            elif self.changed[1]<0:
                if abs((object.rect.y + object.h) - self.blit_pos[1])<=self.speed:
                    self.offset[1] = 1
                else:
                    self.offset[1] = -1

           
            global_pos = pg.Vector2(self.prev_pos.x+self.speed*self.offset[0], self.prev_pos.y+self.speed*self.offset[1])
            
    def draw(self):
        pg.draw.rect(display, self.color, self.rect)
    
    def gun_update(self, keys, gun):
        if keys[pg.K_CAPSLOCK]:
            self.shooting = not self.shooting
        if self.shooting:
            if keys[pg.K_SPACE]:
                self.bullet_shot= True
                gun.shoot()
        gun.update(self.shooting)
    
    def update(self, keys, map, gun, *objects):
        self.movement_update(keys)
        self.gun_update(keys, gun)
        self.boundary_update(map)
        self.camouflage=False
        for object in objects:
            if object.collide:
                self.collide_update(object)
            elif self.rect.colliderect(object.rect):
                if object.func:
                    object.func()
                else:
                    self.camouflage=True
        
        self.boundary_update(map)
        
    def blit(self):
        display.blit(self.image, self.blit_pos)
        
        for bullet in gun.bullets:
            bullet.draw()
        if self.shooting:
            gun.blit()
        

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
    def __init__(self, top_left, bottom_right, collide=True, func=None):   
        pg.sprite.Sprite.__init__(self)
        self.left = top_left[0]* bg_k
        self.top = top_left[1] * bg_k
        self.collide=collide
        self.func = func
        self.w = (bottom_right[0] - top_left[0])*bg_k
        self.h = (bottom_right[1] - top_left[1])*bg_k
        self.rect = pg.Rect(self.top, self.left, self.w, self.h)
        self.color = (0,0,255)         
    
    def update(self):
        global player
        self.rect.x, self.rect.y = player.blit_pos.x+(self.left-global_pos[0]) + player.w/2, player.blit_pos.y+(self.top-global_pos[1])+player.h/2
        pg.draw.rect(display, self.color, self.rect)

class Coin(Object):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        top_left=[0,0]
        spawn_choice = coin_spawns[random.randint(0, len(coin_spawns)-1)]
        top_left[0] = random.randrange(spawn_choice[0][0], spawn_choice[1][0])
        top_left[1] = random.randrange(spawn_choice[0][1], spawn_choice[1][1])
        super().__init__(top_left, (top_left[0]+50, top_left[1]+50))
        self.collected = False
        self.image = pg.transform.scale(coin_img, (50, 50))
        self.rect = self.image.get_rect()
    
    def update_coin(self):
        global player, score
        if player.rect.colliderect(self.rect):
            self.collected = True
        if not self.collected:
            super().update()
            self.blit()
        else:
            data["coins"]+=1
            self.__init__()
        
    def blit(self):
        self.blit_pos = pg.Vector2(self.rect.x,self.rect.y)
        display.blit(self.image, self.blit_pos)

class Bullet(pg.sprite.Sprite):
    def __init__(self, pos, angle, dimension=(10,10), color=(0,0,0), velocity=10):
        pg.sprite.Sprite.__init__(self)
        self.pos = pos
        self.velocity = velocity
        self.w, self.h = dimension[0], dimension[1]
        self.color = color
        self.angle = angle
        self.rect = pg.rect.Rect(self.pos[0], self.pos[1], self.w, self.h)
    
    def draw(self):
        self.rect.x, self.rect.y = self.pos
        pg.draw.rect(display, self.color, self.rect)
    
        

class Gun(pg.sprite.Sprite):
    def __init__(self, image, player, gun_space=25, gun_scale=1.25):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.gun_space = gun_space
        self.gun_scale = gun_scale
        self.angle = pg.Vector2(pg.mouse.get_pos())-player.blit_pos
        self.w, self.h = self.image.get_width(), self.image.get_height()
        self.image=pg.transform.scale(self.image, (self.w*self.gun_scale, self.h*self.gun_scale))
        self.blit_pos = pg.Vector2(player.blit_pos.x, player.blit_pos.y+self.gun_space)
        self.images = []        
        for i in range(8):
            self.images.append(pg.transform.flip(pg.transform.rotate(self.image, (45*i +((3<=i<=5)*(4-2*i)*45))), (3<=i<=5), False))
        self.bullets = []
        
    def gun_tilt_update(self):
        global player
        mouse_pos = pg.mouse.get_pos()
        player_pos = player.blit_pos.x + player.w/2-self.w/2, player.blit_pos.y + player.h/2-self.h/2
        angle_pos = mouse_pos[0]-player_pos[0], player_pos[1]-mouse_pos[1]
        self.angle = math.atan((angle_pos[1]+0.001)/(angle_pos[0]+0.001))
        if angle_pos[0] <0:
            self.angle = self.angle + math.pi
        self.image = self.images[int((self.angle//(math.pi/8)+1)//2)]
        self.blit_pos.x, self.blit_pos.y = (player_pos[0] + math.cos(self.angle)*self.gun_space), (player_pos[1] - math.sin(self.angle)*self.gun_space/2 + player.h/10)
    
    def bullet_update(self):
        for bullet in self.bullets:
            if 0<=bullet.pos[0]<=window_w and 0<=bullet.pos[1]<=window_h:
                bullet.pos[0] += math.cos(bullet.angle)*bullet.velocity
                bullet.pos[1] -= math.sin(bullet.angle)*bullet.velocity
            else:
                self.bullets.pop(self.bullets.index(bullet))
    def update(self, shooting):
        if shooting:
            self.gun_tilt_update()
        self.bullet_update()           
              
    def shoot(self):
        if len(self.bullets)<10:
            angle_mult = float(self.images.index(self.image))
            pos = list(self.blit_pos)
            if angle_mult==1 or angle_mult==5:
                pos[0] += self.h
            
            self.bullets.append(Bullet(pos=pos, angle=angle_mult*math.pi/4))
    
    def blit(self):
        display.blit(self.image, self.blit_pos)
        
        
def snake_game():
    subprocess.run(snake_game)

data = {}
with open('./data/saved.json', 'r') as file:
    data = json.load(file)

          
player = Player(image=player_img)
map = Map(image=true_bg_img, transp_image=transp_bg_img)
minimap = Minimap(image=true_bg_img, player_image = player_img)
gun = Gun(image = gun_img, player=player)
game_run = True

clock = pg.time.Clock()

objects = dict()
coins = list()

house_bottom = Object([472, 314], [533, 360])
house_top = Object([167, 170], [228, 217])
health = Object([242, 177], [315, 234])
mart = Object([322, 191], [404, 249])
big_house = Object([566, 170],[654, 230])
block_1 = Object([400,0], [458,194])
block_2 = Object([460,86], [587,100])
block_3 = Object([590,0], [800,187])    
block_4 = Object([0,134], [165, 165])
trees_1 = Object([192,313], [235, 349])
trees_2 = Object([621, 281], [672, 314])
board = Object([400,320],[412, 327])
forest_1 = Object([0,200], [120,480], False)

door_1 = Object([478, 361], [496, 365], False, snake_game)

objects["house_top"]=house_top
objects["house_bottom"]=house_bottom
objects["health"]=health
objects["block_1"] = block_1
objects["block_2"] = block_2
objects["block_3"] = block_3
objects["block_4"] = block_4
objects["trees_1"] = trees_1
objects["trees_2"] = trees_2
objects["board"] = board
objects["forest_1"] = forest_1
objects["mart"]=mart

objects["big_house"]=big_house
objects["door_1"] = door_1


a_coin = Coin()
b_coin = Coin()
c_coin = Coin()
d_coin = Coin()
e_coin = Coin()
coins = [a_coin,b_coin,c_coin,d_coin,e_coin]

while game_run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_run = False


    keys = pg.key.get_pressed()
   
    player.update(keys, map, gun, *objects.values())
    map.update()
    minimap.update()
    
    display.fill((255, 0, 0))
    map.blit()
    for object in objects.values():
        object.update()
    
    for coin in coins:
        coin.update_coin()
    
    if gun.bullets:
        bul = gun.bullets[0].pos
    else:
        bul=0
    text_surface = my_font.render(f"Score: {data}, Global: {global_pos}, Speed: {player.speed}, Mouse: {pg.mouse.get_pos()} Map:{map.w} {bul}{gun.angle}{player.changed}", False, (200, 255, 200), (70,100,80))
    display.blit(text_surface, (0, window_h-24))
    player.blit()
    map.transp_blit()
    #player.draw()
    minimap.blit()
    pg.display.flip()
    clock.tick(15)

with open("./data/saved.json", "w") as outfile:
    json.dump(data, outfile)
    
pg.quit()
