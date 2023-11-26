import pygame

from _player import Player
from _obstacle import Obstacle
from pygame.sprite import (Group, 
                           GroupSingle, 
                           spritecollide)
from random import choice
from sys import exit

TITLE = 'Runner'

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Global variables
game_font = pygame.font.Font('assets/font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = None

# Foreground & Background
sky_surf =  pygame.image.load('assets/graphics/Sky.png').convert()
ground_surf = pygame.image.load('assets/graphics/ground.png').convert()


# Obstacles
obstacles_list = ['fly', 'snail', 'snail', 'snail']
obstacles = Group()

# Player
player = GroupSingle()
player.add(Player())

# Intro screen
player_stand = pygame.image.load('assets/graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand,0,2)
player_stand_rect = player_stand.get_rect(center = (400,200))

game_name = game_font.render('Pixel Runner!',False, (111,196,169))
game_name_rect = game_name.get_rect(midtop = (400,50))

start_ins_surf = game_font.render('PRESS  [SPACE]  TO  START',False, (111,196,169))
start_ins_rect = start_ins_surf.get_rect(midtop = (400,350))

# Timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = game_font.render(f'{current_time}', False, (64,64,64))
    score_rect = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf, score_rect)
    return current_time

def collision_sprite():
    if spritecollide(player.sprite, obstacles, True): return False
    return True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if game_active:
            if event.type == obstacle_timer:
                obstacles.add(Obstacle(choice(obstacles_list)))
               
        else:
            # In start or game over menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)     
                

    if game_active:
        # Foreground & Background
        screen.blit(ground_surf,(0,300))
        screen.blit(sky_surf,(0,0))
        
        # Score
        score = display_score()
        
        # Obstacles
        obstacles.draw(screen)
        obstacles.update()
        
        # Player
        player.draw(screen)
        player.update()
        
        # Collision
        game_active = collision_sprite()

    else:
        # Background and character
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)

        # Text
        score_message = game_font.render(f"Your score: {score}",False, (111,196,169))
        score_message_rect = score_message.get_rect(midtop = (400,300))
        screen.blit(game_name,game_name_rect)
        
        if score == None: screen.blit(start_ins_surf, start_ins_rect)
        else: screen.blit(score_message, score_message_rect)
        
        # Clear obstacles group
        obstacles.empty()

    pygame.display.update()
    clock.tick(60)