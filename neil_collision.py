import pygame
import random

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Collision")

#create main rectangle & obstacle rectangle
rect_1 = pygame.Rect(0, 0, 25, 25)
obstacle_rect = pygame.Rect(random.randint(0, 500), random.randint(0, 300), 25, 25)

#define colours
BG = (50, 50, 50)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#hide mouse cursor
pygame.mouse.set_visible(False)

run = True
while run:
  #update background
  screen.fill(BG)

  #check collision and change colour


  #get mouse coordinates and use them to position the rectangle
  pos = pygame.mouse.get_pos()
  #print(pos)
  rect_1.center = pos

  col = GREEN
  if rect_1.colliderect(obstacle_rect):
    overlap_x = max(0, min(rect_1.right, obstacle_rect.right) - max(rect_1.left, obstacle_rect.left))
    overlap_y = max(0, min(rect_1.bottom, obstacle_rect.bottom) - max(rect_1.top, obstacle_rect.top))

    # Adjust the position based on the smaller overlap
    if overlap_x < overlap_y:
      if rect_1.centerx < obstacle_rect.centerx:
        rect_1.right = obstacle_rect.left
      else:
        rect_1.left = obstacle_rect.right
    else:
      if rect_1.centery < obstacle_rect.centery:
        rect_1.bottom = obstacle_rect.top
      else:
        rect_1.top = obstacle_rect.bottom



  #draw both rectangles
  pygame.draw.rect(screen, col, rect_1)
  pygame.draw.rect(screen, BLUE, obstacle_rect)

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  #update display
  pygame.display.flip()

pygame.quit()
