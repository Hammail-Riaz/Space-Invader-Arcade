# --- TOP MODULE IMPORTS & INIT ---
import pygame as pg
import os, time
from core import Spaceship, Enemy
from assets import load_assets, SCREEN_WIDTH, SCREEN_HEIGHT, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, SPACESTATION_WIDTH, SPACESTATION_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT, ROCKET_WIDTH, ROCKET_HEIGHT,WHITE , MAX_ROCKETS, FPS

pg.init()
pg.mixer.init()

# --- GAME CONSTANTS ---


# --- ASSETS AND FONTS ---
ASSETS = load_assets()
FONT = pg.font.SysFont(None, 45)
END_FONT = pg.font.SysFont(None, 40)

# --- HIGHSCORE HANDLING ---
HIGHSCORE = ["0", "0.0"]
if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as file:
        file.write("0 0.0")
else:
    with open("highscore.txt") as file:
        HIGHSCORE = file.read().strip().split()

# --- WINDOW SETUP ---
window = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Space Invader - Hammail")
pg.display.set_icon(ASSETS["icon"])
CLOCK = pg.time.Clock()

# --- DRAWING FUNCTIONS ---
def draw_ui(es_health, time_passed, kills):
    health = FONT.render(f"Nexus-6 Health : {es_health}", 1 , "green")
    window.blit(health, (SCREEN_WIDTH - int(health.get_width()) - 10, 10))
    
    Time = FONT.render(f"Time : {time_passed}s", 1 , "white")
    window.blit(Time, (10,10))

    kill_text = FONT.render(f"Kills : {kills}", 1 , "red")
    window.blit(kill_text, (10,50))

    best_text = FONT.render(f"Best : {HIGHSCORE[0]} ({HIGHSCORE[1]}s)", 1 , "green")
    window.blit(best_text, (SCREEN_WIDTH - int(best_text.get_width()) - 10, 50))


def draw_background(bg_img, station_img):
    window.blit(bg_img, (0, 0))
    window.blit(station_img, (0, SCREEN_HEIGHT - SPACESHIP_HEIGHT))

def draw_defeat_msg(kills, elapsed, win):
    window.fill((0, 0, 0))
    lines = [
        ("You fought like a supernova", "green"),
        ("In the dark — brilliant, fierce, unforgettable.", "green"),
        ("Nexus-6 may be gone,", "green"),
        ("But the Xeridians bled for every inch they took.", "green"),
        ("You're not just a survivor...", "green"),
        ("you're a legend written in plasma and fire.", "green")
    ] if win else [
        ("You were too late...", "red"),
        ("Nexus-6 screams in silence as it burns,", "red"),
        ("and Earth is next.", "red"),
        ("The Xeridians aren’t coming — they’re here.", "red"),
        ("You didn’t lose the war...", "red"),
        ("you handed them the keys to humanity’s last door.", "red")
    ]
    for i, (line, color) in enumerate(lines):
        msg = END_FONT.render(line, True, color)
        window.blit(msg, ((SCREEN_WIDTH - msg.get_width()) // 2, 80 + i * 40))
    summary = END_FONT.render(f"Kills: {kills}   Time: {elapsed}s", 1, "white")
    window.blit(summary, ((SCREEN_WIDTH - summary.get_width()) // 2, 400))
    restart_msg = END_FONT.render("Press R to Restart or Q to Quit", 1, "gray")
    window.blit(restart_msg, ((SCREEN_WIDTH - restart_msg.get_width()) // 2, 460))


# --- STORY SCENES ---
def show_story_intro():
    for img_path, audio_path in ASSETS["story_scenes"]:
        image = pg.transform.scale(pg.image.load(img_path), (SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        sound = pg.mixer.Sound(audio_path)
        sound.set_volume(0.5)
        window.blit(image, (0, 0))
        pg.display.update()
        sound.play()

        while pg.mixer.get_busy():
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit(); exit()
                if event.type == pg.KEYDOWN:
                    sound.stop()
                    break

# --- MAIN GAME FUNCTION ---
def main(spacestation_health, spaceship_vel, enemy_vel):
    global HIGHSCORE

    spaceship = Spaceship(ASSETS, SPACESHIP_WIDTH, SPACESHIP_HEIGHT, ROCKET_WIDTH, ROCKET_HEIGHT, spaceship_vel)
    enemy = Enemy(ASSETS, ENEMY_WIDTH, ENEMY_HEIGHT, enemy_vel)

    rockets, enemies = [], []
    enemy_timer, enemy_spawn_interval = 0, 2000
    start_time = time.time()
    kills = 0

    bg_music = ASSETS["bg_sfx"]
    bg_music.set_volume(0.4)
    bg_music.play(-1)

    bg_img = ASSETS['bg'].convert_alpha()
    station_img = ASSETS["spacestation"].convert_alpha()

    run = True
    while run:
        dt = CLOCK.tick(FPS)
        elapsed = round(time.time() - start_time, 1)
        enemy_timer += dt

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE and len(rockets) < MAX_ROCKETS:
                rockets.append(spaceship.generate_rockets())
                ASSETS["fire_sfx"].play()

        if spacestation_health <= 0:
            best_kills, best_time = int(HIGHSCORE[0]), float(HIGHSCORE[1])
            win = kills > best_kills or (kills == best_kills and elapsed < best_time)
            draw_defeat_msg(kills, elapsed, win)
            pg.display.update()

            if win:
                with open("highscore.txt", "w") as file:
                    file.write(f"{kills} {elapsed}")
                HIGHSCORE = [str(kills), str(elapsed)]
                ASSETS['win_sfx'].play()

            waiting = True
            while waiting:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        waiting = False
                        run = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_r:
                            # Restart game
                            main(10, 10, 4)  # Restart with default values
                            return  # Exit current game loop after restart
                        elif event.key == pg.K_q:
                            waiting = False
                            run = False

        # Spawn enemies
        if enemy_timer >= enemy_spawn_interval:
            enemies.extend(enemy.generate_enemys() for _ in range(3))
            enemy_timer = 0
            enemy_spawn_interval = max(100, enemy_spawn_interval - 20)

        # UPDATE DRAW LOGIC
        draw_background(bg_img, station_img)
        spaceship.spaceship_movement_control(pg.key.get_pressed())
        kills = spaceship.check_rocket_collision(rockets, enemies, kills)
        spaceship.move_rockets(rockets)
        spaceship.draw_rockets(window, rockets)
        spaceship.draw_spaceship(window)
        spaceship.remove_rockets(rockets)

        enemy.move_enemys(enemies)
        spacestation_health = enemy.attacking_enemys(enemies, SCREEN_HEIGHT, SPACESTATION_HEIGHT, spacestation_health)
        enemy.draw_enemys(window, enemies)

        draw_ui(spacestation_health, elapsed, kills)
        pg.display.update()

    pg.quit()

# --- MAIN ---
if __name__ == "__main__":
    show_story_intro()
    main(10, 10, 4)

