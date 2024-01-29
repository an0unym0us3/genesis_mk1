import pygame
pygame.init()

screen_w, screen_h = 1280, 720
screen = pygame.display.set_mode((screen_w, screen_h))
# width, height
default_button_size = (280, 100)

class Button:
    def __init__(self, position=(0, 0), button_size=default_button_size, button_color=(255, 0 , 0), font_name='courier', font_size=36, font_text='-default-', font_color=(0, 0, 255)):
        # positon[0], positon[1], button_size[1], button_size[1]
        # x, y, width, height
        self.w = button_size[0]
        self.h = button_size[1]
        self.color = button_color
        new_pos = position[0] - button_size[0]//2, position[1] -  button_size[1]//2
        self.Rect = pygame.Rect(new_pos[0], new_pos[1], button_size[0], button_size[1])

        self.font_name = font_name
        self.font_size = font_size
        self.font = pygame.font.Font(pygame.font.match_font(font_name), font_size)
        
        self.text = self.font.render(font_text, True, font_color)
        self.text_rect = self.text.get_rect(center=self.Rect.center)

    def check_button(self, mouse):
        '''
        if self.Rect.collidepoint(mouse):
            print('E')
        else
        '''

        
        self.font_size += 10*self.Rect.collidepoint(mouse)
        #= pygame.font.Font(pygame.font.match_font(self.font_name), self.font_size + 10*(self.Rect.collidepoint(mouse)))
  

start_button = Button( position=(screen_w//2,  screen_h//2))



clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")

    start_button.check_button(pygame.mouse.get_pos())
    pygame.draw.rect(screen, start_button.color, start_button.Rect)
    screen.blit(start_button.text, start_button.text_rect)
    
    pygame.display.flip()
    clock.tick(60)  

pygame.quit()

