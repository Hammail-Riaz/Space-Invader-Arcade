#Importing required Module
import pygame as pg
import os
SCREEN_WIDTH, SCREEN_HEIGHT = 700, 800
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 120, 100
SPACESTATION_WIDTH, SPACESTATION_HEIGHT = SCREEN_WIDTH, 100
ENEMY_WIDTH, ENEMY_HEIGHT = 80, 120
ROCKET_WIDTH, ROCKET_HEIGHT = 10, 20
WHITE = (255, 255, 255)
MAX_ROCKETS = 3
FPS = 60

def load_assets():

    assets = {}

    # Load game sound effects
    assets["fire_sfx"] =   pg.mixer.Sound(os.path.join("assets", "Sound effects", "game_sound", "rocket fire.wav"))
    assets["hit_sfx"] =  pg.mixer.Sound(os.path.join("assets", "Sound effects","game_sound", "enemy_explode.wav"))
    assets["attack_sfx"] = pg.mixer.Sound(os.path.join("assets", "Sound effects","game_sound", "attack.wav"))
    assets["bg_sfx"] = pg.mixer.Sound(os.path.join("assets", "Sound effects","game_sound", "bg.mp3"))
    assets["win_sfx"] = pg.mixer.Sound(os.path.join("assets", "Sound effects","game_sound", "winning_effect.mp3"))

    # Load static game images
    assets["spaceship"] = pg.transform.scale(pg.image.load(os.path.join("assets", "game_items", "spaceship.png")), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
    assets["rocket"] = pg.transform.scale(pg.image.load(os.path.join("assets", "game_items", "rocket.png")), (ROCKET_WIDTH, ROCKET_HEIGHT))
    assets["enemy"] = pg.transform.scale(pg.image.load(os.path.join("assets", "game_items", "enemy.png")), (ENEMY_WIDTH, ENEMY_HEIGHT))
    assets["bg"] = pg.transform.scale(pg.image.load(os.path.join("assets", "game_items", "bg.jpg")), (SCREEN_WIDTH, SCREEN_HEIGHT))
    assets["spacestation"] = pg.transform.scale(pg.image.load(os.path.join("assets", "game_items", "spacestation.png")), (SPACESTATION_WIDTH, SPACESTATION_HEIGHT))
    assets["icon"] = pg.image.load("icon.ico")

    # Load story scenes (1.png to 10.png and 1.mp3 to 10.mp3)
    story_scenes = []
    for i in range(1, 11):
        image_path = os.path.join("assets", "story", f"{i}.png")
        audio_path = os.path.join("assets","Sound effects", "story_audios", f"{i}.mp3")
        
        story_scenes.append((image_path, audio_path))

    assets["story_scenes"] = story_scenes

    return assets
