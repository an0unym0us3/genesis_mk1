import pygame as pg
pg.init()

window_w, window_h = 720, 720
display = pg.display.set_mode((window_w, window_h))

PLAYER_BLIT_CENTER = pg.Vector2(window_c[0] - player_w//2, window_c[1] - player_h//2)

'''
this = player(20, 40)

player = player(10, 30)
'''

class player:
    def __init__(self, height, width):
        self.pos = pg.Vector2(PLAYER_BLIT_CENTER.x, PLAYER_BLIT_CENTER.y)
        self.h = height
        self.w = width

    def is_colliding(self, this):
        delta_x = self.x - this.x
        delta_y = self.y - this.y

        if delta_x + this.w >= 0:
            print('Left collision detected')
        elif delta_x + self.w <= 0:
            print('Right collision detected')

        if delta_y + this.h >= 0:
            print('Top collision detected')
        elif delta_x + self.h <= 0:
            print('Bottom collision detected')

walking = False
game_run = True
clock = pg.time.Clock()11
while game_run:
    # Very important for closing the actual window
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_run = False
    

    # Update the display to show the next frame and our hard work
    pg.display.flip()
    # This guy just takes care of frame rates, he's very good at it too. For now the game runs at 15 fps
    clock.tick(15)

# This will terminate the game and close the window!
pg.quit()
