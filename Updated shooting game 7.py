import pygame
import random
import time
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sky Shooter")

clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (160,160,160)
RED = (255,60,60)
GREEN = (50,255,50)
BLUE = (100,200,255)
ORANGE = (255,150,0)

font = pygame.font.SysFont("Arial",28)
big_font = pygame.font.SysFont("Arial",60)

def reset_game():

    global player_x, player_y, bullets, lasers, enemies, explosions
    global score, start_time, game_over

    player_x = 380
    player_y = 520

    bullets = []
    lasers = []
    enemies = []
    explosions = []

    score = 0
    start_time = time.time()
    game_over = False

reset_game()

player_speed = 7
bullet_speed = 10
laser_speed = 15

# Space stars
stars = [[random.randint(0,WIDTH),random.randint(0,HEIGHT)] for _ in range(100)]

TIME_LIMIT = 180

menu = True
running = True

while running:

    clock.tick(60)

    # START MENU
    while menu:

        screen.fill((10,10,30))

        title = big_font.render("SKY SHOOTER",True,WHITE)
        start = font.render("Press S to Start Game",True,WHITE)
        exit_game = font.render("Press E to Exit",True,WHITE)

        screen.blit(title,(230,200))
        screen.blit(start,(300,300))
        screen.blit(exit_game,(320,340))

        pygame.display.update()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_s:
                    menu = False
                    reset_game()

                if event.key == pygame.K_e:
                    pygame.quit()
                    sys.exit()

    # TIMER
    if not game_over:
        elapsed = int(time.time() - start_time)
        remaining = max(0, TIME_LIMIT - elapsed)
    else:
        remaining = remaining

    if remaining == 0:
        game_over = True

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and not game_over:
                bullets.append([player_x+25, player_y])

            if event.key == pygame.K_l and not game_over:
                lasers.append([player_x+25, player_y])

            if event.key == pygame.K_r:
                reset_game()

    keys = pygame.key.get_pressed()

    if not game_over:

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] and player_x < WIDTH-60:
            player_x += player_speed

    # Spawn enemies (slower)
    if random.randint(1,80) == 1 and not game_over:

        enemy_type = random.choice(["ufo","alien"])

        if enemy_type == "ufo":
            enemies.append({"x":random.randint(50,750),"y":0,"speed":2,"type":"ufo","hp":1})

        if enemy_type == "alien":
            enemies.append({"x":random.randint(50,750),"y":0,"speed":1.5,"type":"alien","hp":2})

    # Move bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed

    bullets = [b for b in bullets if b[1] > 0]

    # Move lasers
    for laser in lasers:
        laser[1] -= laser_speed

    lasers = [l for l in lasers if l[1] > 0]

    # Move enemies
    for enemy in enemies:

        enemy["y"] += enemy["speed"]
        enemy["x"] += random.randint(-1,1)

        if abs(enemy["x"]-player_x) < 40 and abs(enemy["y"]-player_y) < 40:
            game_over = True

    # Bullet collision
    for enemy in enemies[:]:
        for bullet in bullets[:]:

            if abs(enemy["x"]-bullet[0]) < 35 and abs(enemy["y"]-bullet[1]) < 35:

                enemy["hp"] -= 1
                bullets.remove(bullet)

                if enemy["hp"] <= 0:
                    enemies.remove(enemy)
                    explosions.append([enemy["x"],enemy["y"],20])
                    score += 1

                break

    # Laser collision
    for enemy in enemies[:]:
        for laser in lasers[:]:

            if abs(enemy["x"]-laser[0]) < 40 and abs(enemy["y"]-laser[1]) < 40:

                enemies.remove(enemy)
                lasers.remove(laser)
                explosions.append([enemy["x"],enemy["y"],20])
                score += 2
                break

    # Update explosions
    for exp in explosions[:]:
        exp[2] += 3
        if exp[2] > 40:
            explosions.remove(exp)

    # Move stars
    for star in stars:
        star[1] += 1
        if star[1] > HEIGHT:
            star[0] = random.randint(0,WIDTH)
            star[1] = 0

    # Background
    screen.fill((10,10,30))

    for star in stars:
        pygame.draw.circle(screen,WHITE,(star[0],star[1]),2)

    # Spaceship
    pygame.draw.rect(screen,GRAY,(player_x+20,player_y+10,20,40))
    pygame.draw.polygon(screen,WHITE,[
        (player_x+30,player_y-10),
        (player_x+15,player_y+10),
        (player_x+45,player_y+10)
    ])

    # Bullets
    for bullet in bullets:
        pygame.draw.rect(screen,WHITE,(bullet[0],bullet[1],5,15))

    # Lasers
    for laser in lasers:
        pygame.draw.rect(screen,BLUE,(laser[0],laser[1],6,20))

    # Enemies
    for enemy in enemies:

        x = enemy["x"]
        y = enemy["y"]

        if enemy["type"] == "ufo":
            pygame.draw.ellipse(screen,GRAY,(x-20,y+10,60,20))
            pygame.draw.circle(screen,BLUE,(x+10,y+10),10)

        if enemy["type"] == "alien":
            pygame.draw.circle(screen,GREEN,(x,y+20),18)
            pygame.draw.circle(screen,BLACK,(x-5,y+15),3)
            pygame.draw.circle(screen,BLACK,(x+5,y+15),3)

    # Explosion
    for exp in explosions:
        pygame.draw.circle(screen,ORANGE,(exp[0],exp[1]),exp[2])

    # Score
    score_text = font.render("Score: "+str(score),True,WHITE)
    screen.blit(score_text,(10,10))

    # Timer
    minutes = remaining // 60
    seconds = remaining % 60
    timer = font.render(f"Time {minutes:02}:{seconds:02}",True,WHITE)
    screen.blit(timer,(650,10))

    if game_over:

        over = big_font.render("GAME OVER",True,RED)
        restart = font.render("Press R to Restart",True,WHITE)

        screen.blit(over,(250,250))
        screen.blit(restart,(300,330))

    pygame.display.update()

pygame.quit()