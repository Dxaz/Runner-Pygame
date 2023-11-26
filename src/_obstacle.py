from pygame import (K_SPACE,
                    MOUSEBUTTONDOWN)
from pygame.image import load
from pygame.sprite import Sprite
from random import randint

class Obstacle(Sprite):
    def __init__(self, type) -> None:
        super().__init__()
        if type == 'fly':
            fly_frame_1 = load('assets/graphics/Fly/Fly1.png').convert_alpha()
            fly_frame_2 = load('assets/graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            self.y_pos = 210
        else:
            snail_frame_1 = load('assets/graphics/snail/snail1.png').convert_alpha()
            snail_frame_2 = load('assets/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            self.y_pos = 300

        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(midbottom = ((randint(900,1100), self.y_pos)))

    def obstacle_animation(self):
        self.frame_index += 0.1
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def self_destruct(self):
        if self.rect.x <= -100:
            self.kill()
    
    def update(self):
        self.obstacle_animation()
        self.rect.x -= 6
        self.self_destruct()