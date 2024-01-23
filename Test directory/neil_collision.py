import pygame
import sys

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1200, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Collision Detector")
IMAGE = pygame.image.load('/Users/admin/PycharmProjects/backtobasics/genesis_mk1/Media/images/pokemon house.png').convert()
# Image.small makes the image smaller. rect2 and rect3 MUST be equal
IMAGE_SMALL = pygame.transform.scale(IMAGE, (100, 100))


# Set up colors
white = (255, 255, 255)
red = (255, 0, 0)
btn_color = (0, 255, 0)
trans_color = [0, 0, 255, 100]

# Set up rectangles
#IMAGE.get_rect()
rect1 = pygame.Rect(100, 100, 50, 50)
rect2 = pygame.Rect(200, 200, 100, 100)
rect3 = pygame.Rect(200, 200, 100, 100)
font = pygame.font.Font(None, 36)

# Set up toggle button
toggle_button = pygame.Rect(20, 20, 80, 50)
toggle_text = font.render("see", True, white)
# Set up clock
clock = pygame.time.Clock()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Toggle the red RGB value on button click
            if toggle_button.collidepoint(event.pos):
                if trans_color[3] > 0:
                    trans_color[3] = 0
                else:
                    trans_color[3] = 200



    # Save the previous position of rect1
    prev_rect1_pos = rect1.topleft

    # Move rectangles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rect1.x -= 20
    if keys[pygame.K_RIGHT]:
        rect1.x += 20
    if keys[pygame.K_UP]:
        rect1.y -= 20
    if keys[pygame.K_DOWN]:
        rect1.y += 20

    # Check for collisions
    if rect1.colliderect(rect2):
        # Handle collision by setting the position back to the previous position
        rect1.topleft = prev_rect1_pos

    # Clear the screen
    screen.fill(white)

    # Draw rectangles using the draw_rect_alpha function
    draw_rect_alpha(screen, red, rect1)
    draw_rect_alpha(screen, btn_color, rect3)
    draw_rect_alpha(screen, trans_color, rect2)
    pygame.draw.rect(screen, btn_color, toggle_button)
    screen.blit(toggle_text, (30, 30))
    screen.blit(IMAGE_SMALL, rect3)

    # Update the display
    pygame.display.flip()
    # Cap the frame rate
    clock.tick(60)
