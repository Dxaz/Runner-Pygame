import pygame
from sys import exit
from random import randint

TITLE = 'Runner'

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = game_font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def obstacle_movement(obstacle_list):

    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5

            if obstacle_rect.bottom == 300:screen.blit(snail_surf, obstacle_rect)
            else:screen.blit(fly_surf, obstacle_rect )

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    
    return []


# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 400))

pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()
game_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = None

sky_surf =  pygame.image.load('assets/graphics/Sky.png').convert()
ground_surf = pygame.image.load('assets/graphics/ground.png').convert()

# Obstacles
snail_surf = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
fly_surf = pygame.image.load('assets/graphics/Fly/Fly1.png').convert_alpha()

obstacle_rect_list = []

player_surf = pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

# Intro screen
player_stand = pygame.image.load('assets/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

title_surf = game_font.render('Pixel Runner!',False, (111,196,169))
title_surf_rect = title_surf.get_rect(midtop = (400,50))

start_ins_surf = game_font.render('PRESS  [SPACE]  TO  START',False, (111,196,169))
start_ins_rect = start_ins_surf.get_rect(midtop = (400,350))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


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
            
            if event.type == obstacle_timer:
                if randint(0,2):
                    obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100), 300)))
                else:
                    obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100), 210)))

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player_rect.bottom = 300
                game_active = True

    if game_active:
        screen.blit(ground_surf,(0,300))
        screen.blit(sky_surf,(0,0))
         # score
        score = display_score()
        
        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        # snail_rect.x -= 4
        # if snail_rect.right <= 0: snail_rect.left = 800
        # screen.blit(snail_surf, snail_rect)
        
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 300: player_rect.bottom = 300
        screen.blit(player_surf, player_rect)
        

        # collision
    
    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        screen.blit(title_surf,title_surf_rect )

        title_score_surf = game_font.render(f"Your score: {score}",False, (111,196,169))
        title_score_rect = title_score_surf.get_rect(midtop = (400,300))
        if score == None:
            screen.blit(start_ins_surf, start_ins_rect)
        else:
            screen.blit(title_score_surf, title_score_rect)

    pygame.display.update()
    clock.tick(60)