import pygame
from sys import exit

TITLE = 'Runner'

def display_score():
    new_score = current_score
    score_surf = score_font.render(f'{new_score}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 400))

pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
score_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
game_active = True
current_score = 0

sky_surf =  pygame.image.load('assets/graphics/Sky.png').convert()
ground_surf = pygame.image.load('assets/graphics/ground.png').convert()

snail_surf = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(midbottom = (900, 300))


player_surf = pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.collidepoint(event.pos):
                if player_rect.bottom == 300:
                    player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                        player_gravity = -20
            
            
        else:
             if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                snail_rect.x=900
                player_rect.bottom = 300
                current_score = 0
                game_active = True
       


    if game_active:
        screen.blit(ground_surf,(0,300))
        screen.blit(sky_surf,(0,0))
        
        
        # Snail
        snail_rect.x -= 4
        if snail_rect.right <= 0: snail_rect.left = 800
        screen.blit(snail_surf, snail_rect)
        
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        
        if player_rect.bottom > 300: 
            player_rect.bottom = 300
        

        screen.blit(player_surf, player_rect)

        # collision
        if snail_rect.colliderect(player_rect):
            game_active = False

        # score
        display_score()

    else:
        screen.fill('Red')

    pygame.display.update()
    clock.tick(60)