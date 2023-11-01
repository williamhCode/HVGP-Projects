import pygame

pygame.init()

screen = pygame.display.set_mode((640, 480))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    screen.fill((0, 0, 0))
    
    pygame.draw.circle(screen, (255, 0, 0), (320, 240), 100, width=1)
    
    pygame.display.flip()