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
SKY = (135,206,235)
YELLOW = (255,223,0)
GRAY = (160,160,160)
DARK = (80,80,80)
RED = (255,50,50)
ORANGE = (255,150,0)

# Player
player_x = 380
player_y = 520
player_speed = 7

# Bullets
bullets = []
bullet_speed = 10

# UFO enemies
enemies = []
enemy_speed = 3

# Explosion effects
explosions = []

# Clouds
clouds = [[random.randint(0,WIDTH),random.randint(0,200)] for _ in range(5)]

# Birds
birds = [[random.randint(0,WIDTH),random.randint(40,150)] for _ in range(3)]

# Score
score = 0
font = pygame.font.SysFont("Arial",28)
big_font = pygame.font.SysFont("Arial",60)

# TIMER
TIME_LIMIT = 180
start_time = time.time()
remaining = TIME_LIMIT

game_over = False
game_won = False

running = True

while running:

    clock.tick(60)

    # TIMER LOGIC
    if not game_over and not game_won:
        elapsed = int(time.time() - start_time)
        remaining = max(0, TIME_LIMIT - elapsed)

        if remaining == 0:
            game_over = True

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over and not game_won:
                bullets.append([player_x+25, player_y])

    keys = pygame.key.get_pressed()

    if not game_over and not game_won:

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] and player_x < WIDTH-60:
            player_x += player_speed

    # Spawn UFO enemies
    if random.randint(1,30) == 1 and not game_over and not game_won:
        enemies.append([random.randint(50,750),0])

    # Move bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed

    bullets = [b for b in bullets if b[1] > 0]

    # Move enemies
    for enemy in enemies:
        enemy[1] += enemy_speed

    # Move clouds
    for cloud in clouds:
        cloud[0] -= 1
        if cloud[0] < -100:
            cloud[0] = WIDTH
            cloud[1] = random.randint(0,200)

    # Move birds
    for bird in birds:
        bird[0] += 2
        if bird[0] > WIDTH:
            bird[0] = -50
            bird[1] = random.randint(50,150)

    # Collision detection
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if abs(enemy[0]-bullet[0]) < 35 and abs(enemy[1]-bullet[1]) < 35:
                enemies.remove(enemy)
                bullets.remove(bullet)
                explosions.append([enemy[0],enemy[1],20])
                score += 1
                break

    # Win condition
    if score >= 100:
        game_won = True

    # Update explosions
    for exp in explosions[:]:
        exp[2] += 3
        if exp[2] > 40:
            explosions.remove(exp)

    # Background
    screen.fill(SKY)

    # Sun
    pygame.draw.circle(screen,YELLOW,(700,80),40)

    # Clouds
    for c in clouds:
        pygame.draw.circle(screen,WHITE,(c[0],c[1]),25)
        pygame.draw.circle(screen,WHITE,(c[0]+25,c[1]),30)
        pygame.draw.circle(screen,WHITE,(c[0]+50,c[1]),25)

    # Birds
    for b in birds:
        pygame.draw.line(screen,BLACK,(b[0],b[1]),(b[0]+10,b[1]-5),2)
        pygame.draw.line(screen,BLACK,(b[0]+10,b[1]-5),(b[0]+20,b[1]),2)

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
        pygame.draw.rect(screen,BLACK,(bullet[0],bullet[1],5,15))

    # UFO enemies
    for enemy in enemies:
        x,y = enemy
        pygame.draw.ellipse(screen,GRAY,(x-20,y+10,60,20))
        pygame.draw.circle(screen,DARK,(x+10,y+10),10)

    # Explosion animation
    for exp in explosions:
        pygame.draw.circle(screen,ORANGE,(exp[0],exp[1]),exp[2])
        pygame.draw.circle(screen,RED,(exp[0],exp[1]),exp[2]//2)

    # Score
    text = font.render("Score: "+str(score),True,BLACK)
    screen.blit(text,(10,10))

    # TIMER DISPLAY
    minutes = remaining // 60
    seconds = remaining % 60
    timer = font.render(f"Time {minutes:02}:{seconds:02}",True,BLACK)
    screen.blit(timer,(650,10))

    # WIN MESSAGE
    if game_won:
        win_text = big_font.render("YOU WIN!",True,(0,150,0))
        screen.blit(win_text,(250,250))

    # GAME OVER MESSAGE
    if game_over and not game_won:
        over_text = big_font.render("GAME OVER",True,(200,0,0))
        screen.blit(over_text,(250,250))

    pygame.display.update()

pygame.quit()