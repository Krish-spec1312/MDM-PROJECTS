import pygame
import random
import time

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sky Shooter")

clock = pygame.time.Clock()

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (160,160,160)
DARK = (80,80,80)
RED = (255,50,50)
ORANGE = (255,150,0)
BLUE = (100,200,255)

# Player
player_x = 380
player_y = 520
player_speed = 7

# Bullets
bullets = []
laser_bullets = []
bullet_speed = 10
laser_speed = 15

# Enemies
enemies = []

# Explosions
explosions = []

# Space stars
stars = [[random.randint(0,WIDTH),random.randint(0,HEIGHT)] for _ in range(100)]

# Score
score = 0
font = pygame.font.SysFont("Arial",28)
big_font = pygame.font.SysFont("Arial",60)

# TIMER
TIME_LIMIT = 180
start_time = time.time()

game_over = False
game_won = False

running = True

while running:

    clock.tick(60)

    elapsed = int(time.time() - start_time)
    remaining = max(0, TIME_LIMIT - elapsed)

    if remaining == 0:
        game_over = True

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and not game_over:

            if event.key == pygame.K_SPACE:
                bullets.append([player_x+25, player_y])

            if event.key == pygame.K_l:  # LASER
                laser_bullets.append([player_x+25, player_y])

    keys = pygame.key.get_pressed()

    if not game_over:

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] and player_x < WIDTH-60:
            player_x += player_speed

    # Spawn enemies (different types)
    if random.randint(1,60) == 1 and not game_over:

        enemy_type = random.choice(["normal","fast","big"])

        if enemy_type == "normal":
            enemies.append({"x":random.randint(50,750),"y":0,"speed":3,"hp":1,"type":"normal"})

        elif enemy_type == "fast":
            enemies.append({"x":random.randint(50,750),"y":0,"speed":6,"hp":1,"type":"fast"})

        elif enemy_type == "big":
            enemies.append({"x":random.randint(50,750),"y":0,"speed":2,"hp":3,"type":"big"})

    # Move bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed

    bullets = [b for b in bullets if b[1] > 0]

    # Move laser bullets
    for laser in laser_bullets:
        laser[1] -= laser_speed

    laser_bullets = [l for l in laser_bullets if l[1] > 0]

    # Move enemies
    for enemy in enemies:

        enemy["y"] += enemy["speed"]
        enemy["x"] += random.randint(-2,2)

        if abs(enemy["x"] - player_x) < 40 and abs(enemy["y"] - player_y) < 40:
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

                    if enemy["type"] == "normal":
                        score += 1
                    elif enemy["type"] == "fast":
                        score += 2
                    elif enemy["type"] == "big":
                        score += 5

                break

    # Laser collision
    for enemy in enemies[:]:
        for laser in laser_bullets[:]:

            if abs(enemy["x"]-laser[0]) < 40 and abs(enemy["y"]-laser[1]) < 40:

                enemies.remove(enemy)
                laser_bullets.remove(laser)
                explosions.append([enemy["x"],enemy["y"],20])
                score += 3
                break

    # Update explosions
    for exp in explosions[:]:
        exp[2] += 3
        if exp[2] > 40:
            explosions.remove(exp)

    # Move stars (space effect)
    for star in stars:
        star[1] += 1
        if star[1] > HEIGHT:
            star[0] = random.randint(0,WIDTH)
            star[1] = 0

    # Background
    screen.fill((10,10,30))

    # Stars
    for star in stars:
        pygame.draw.circle(screen,WHITE,(star[0],star[1]),2)

    # Spaceship
    pygame.draw.rect(screen,DARK,(player_x+20,player_y+10,20,40))
    pygame.draw.polygon(screen,GRAY,[
        (player_x+30,player_y-10),
        (player_x+15,player_y+10),
        (player_x+45,player_y+10)
    ])
    pygame.draw.polygon(screen,RED,[
        (player_x+20,player_y+50),
        (player_x+30,player_y+65),
        (player_x+40,player_y+50)
    ])

    # Bullets
    for bullet in bullets:
        pygame.draw.rect(screen,WHITE,(bullet[0],bullet[1],5,15))

    # Laser bullets
    for laser in laser_bullets:
        pygame.draw.rect(screen,BLUE,(laser[0],laser[1],6,20))

    # Draw enemies
    for enemy in enemies:

        x = enemy["x"]
        y = enemy["y"]

        if enemy["type"] == "normal":
            pygame.draw.ellipse(screen,GRAY,(x-20,y+10,60,20))

        elif enemy["type"] == "fast":
            pygame.draw.ellipse(screen,RED,(x-15,y+10,50,18))

        elif enemy["type"] == "big":
            pygame.draw.ellipse(screen,(200,200,50),(x-30,y+10,80,30))

    # Explosion animation
    for exp in explosions:
        pygame.draw.circle(screen,ORANGE,(exp[0],exp[1]),exp[2])
        pygame.draw.circle(screen,RED,(exp[0],exp[1]),exp[2]//2)

    # Score
    text = font.render("Score: "+str(score),True,WHITE)
    screen.blit(text,(10,10))

    # Timer
    minutes = remaining // 60
    seconds = remaining % 60
    timer = font.render(f"Time {minutes:02}:{seconds:02}",True,WHITE)
    screen.blit(timer,(650,10))

    if game_over:
        over_text = big_font.render("GAME OVER",True,(200,0,0))
        screen.blit(over_text,(250,250))

    pygame.display.update()

pygame.quit()