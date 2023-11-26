import pygame
from sys import exit
from random import randint

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

# Forground and background
sky_surf =  pygame.image.load('assets/graphics/Sky.png').convert()
ground_surf = pygame.image.load('assets/graphics/ground.png').convert()

# Snail
snail_frame_1 = pygame.image.load('assets/graphics/snail/snail1.png').convert_alpha()
snail_frame_2 = pygame.image.load('assets/graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# Fly
fly_frame_1 = pygame.image.load('assets/graphics/Fly/Fly1.png').convert_alpha()
fly_frame_2 = pygame.image.load('assets/graphics/Fly/Fly2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

# Obstacle list of rectangles
obstacle_rect_list = []

# Player
player_walk_1 = pygame.image.load('assets/graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('assets/graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('assets/graphics/Player/jump.png').convert_alpha()

player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))
player_gravity = 0

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

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(fly_animation_timer, 200)


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

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def player_animation():
    global player_surf, player_index
    
    if player_rect.bottom < 300: player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]


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
                if randint(0,2): obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900,1100), 300)))
                else: obstacle_rect_list.append(fly_surf.get_rect(midbottom = (randint(900,1100), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0 : snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0 : fly_frame_index = 1
                else: fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]            

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
        
        # Player
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom > 300: player_rect.bottom = 300
        player_animation()
        screen.blit(player_surf, player_rect)

        # collision
        game_active = collisions(player_rect, obstacle_rect_list)

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand, player_stand_rect)
        
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        score_message = game_font.render(f"Your score: {score}",False, (111,196,169))
        score_message_rect = score_message.get_rect(midtop = (400,300))
        screen.blit(game_name,game_name_rect )
        
        if score == None: screen.blit(start_ins_surf, start_ins_rect)
        else: screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)