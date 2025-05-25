"""Template classes for spaceships and obstacles
Credits : Hammail...
"""

#importing requried module
import pygame as pg
import os
from random import randint

class Spaceship:
    """Protagnist's spaceship template..."""
    def __init__(self,loaded_assets , spaceship_width, spaceship_height, rocket_width, rocket_height,spacestation_vel):
        self.loaded_assets = loaded_assets        
        self.img_rect = pg.Rect(700 // 2, 800 - spaceship_height , spaceship_width, spaceship_height)
        self.vel = spacestation_vel
        self.spaceship_width = spaceship_width
        self.space_height = spaceship_height
        
        self.rocket_width = rocket_width
        self.rocket_height = rocket_height
        self.rocket_vel = 18
        self.img = pg.transform.scale(self.loaded_assets["spaceship"], (self.spaceship_width, self.space_height)).convert_alpha()
        self.rocket_img = pg.transform.scale(self.loaded_assets['rocket'], (self.rocket_width, self.rocket_height)).convert_alpha()
        self.loaded_assets["hit_sfx"].set_volume(0.5)
        

    def generate_rockets(self):
        """Generate the firing rocket for the spaceship and return it."""
        self.rocket_rect = pg.Rect(self.img_rect.x + (int(self.img_rect.width) // 2) - 4 , self.img_rect.y, self.rocket_width, self.rocket_height)
        return (self.rocket_rect)
       
    def draw_rockets(self, surface, rockets):
        """Draw the rockets of spaceship on window.""" 
        for rocket in rockets:            
            surface.blit(self.rocket_img, (rocket.x, rocket.y))
            
    def move_rockets(self, rockets):
        """Move the rockets of spaceship in upward direction."""
        for rocket in rockets:
            rocket.y -= self.rocket_vel
            
    def remove_rockets(self, rockets):
        """Remove spaceship rockets if they are outside the screen."""
        for rocket in rockets[:]:
            if rocket.y <= 0:
                rockets.remove(rocket)
                
    def check_rocket_collision(self,rockets, obstacles, kills):
        """Check collision for the rocket of spaceship with enemys. return kills of spaceship."""        
        for rocket in rockets[:]:
            for obstacle in obstacles[:]:
                if rocket.colliderect(obstacle) and rocket in rockets and obstacle in obstacles:
                    rockets.remove(rocket)
                    obstacles.remove(obstacle)
                    kills += 1
                    self.loaded_assets["hit_sfx"].play()
        return kills
        
    def draw_spaceship(self, surface):
        """Draw the spaceship on window."""
        surface.blit(self.img, (self.img_rect.x,self.img_rect.y))
        
    def spaceship_movement_control(self, key_press):
        """Check for the Movement of spaceship.
            *Controls:
                ->Up arrow key : Up movement
                ->Down arrow key : Down movement
                ->Left arrow key : Left movement
                ->Right arrow key : Right movement
            *Additional :
                ->Spaceship can only move in sight of user mean it do not cross windows border.
        """
        #Right movement
        if key_press[pg.K_RIGHT] and self.img_rect.x < 700  - self.spaceship_width:
            self.img_rect.x += self.vel
            
        #Left movement            
        if key_press[pg.K_LEFT] and self.img_rect.x > 0:
            self.img_rect.x -= self.vel
            
        #Up movement
        if key_press[pg.K_UP] and self.img_rect.y > 0:
            self.img_rect.y -= self.vel
        
        #Down movement
        if key_press[pg.K_DOWN] and self.img_rect.y < 800 - self.space_height:
            self.img_rect.y += self.vel
            
class Enemy:
    """Enemy (Ailens) templates."""
    def __init__(self,loaded_assets, ene_width , ene_height, enemy_vel):
        self.loaded_assets = loaded_assets
        self.ene_width = ene_width
        self.ene_height = ene_height

        self.img = pg.transform.scale(self.loaded_assets["enemy"], (self.ene_width, self.ene_height)).convert_alpha()
        self.enemy_vel = enemy_vel
        self.loaded_assets["attack_sfx"].set_volume(0.5)
        
    def generate_enemys(self):
        """Generate enemy and return it"""
        self.pos_y = randint(-150, - self.ene_height)
        self.pos_x = randint(8, 700 - self.ene_width - 8)
        self.img_rect = pg.Rect(self.pos_x, self.pos_y , self.ene_width, self.ene_height)
        return (self.img_rect)
    
    def move_enemys(self, enemys):
        """Move enemys from top to the bottom of the game window."""
        for enemy in enemys:
            enemy.y += self.enemy_vel
    
    def draw_enemys(self,surface, enemys):
        """Drawing the enemys on the game window."""
        for enemy in enemys:
            surface.blit(self.img, (enemy.x, enemy.y))
            
    def attacking_enemys(self, enemys, screen_height, spacestation_height, es_health):
        """creating the affect enemys are attacking on spaceship."""
        for enemy in enemys[:]:
            if enemy.y >= screen_height - spacestation_height:
                enemys.remove(enemy)
                self.loaded_assets['attack_sfx'].play()
                es_health -= 1 if es_health > 0 else 0 #here is no need but when game end (at last moment) it show earth spacestation health in negative. 
        return es_health


         
