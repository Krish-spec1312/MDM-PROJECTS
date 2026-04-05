import pygame
import random

pygame.init()

# Screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Creative Space Shooter")

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
SKY = (135,206,235)
YELLOW = (255,223,0)
GRAY = (150,150,150)

# Player position
player_x = 375
player_y = 520
player_speed = 7

# Bullets
bullets = []
bullet_speed = 10

# Enemies
enemies = []
enemy_speed = 3

# Clouds
clouds = []
for i in range(5):
    clouds.append([random.randint(0, WIDTH), random.randint(0,200)])

# Birds
birds = []
for i in range(3):
    birds.append([random.randint(0, WIDTH), random.randint(50,150)])

# Score
score = 0
font = pygame.font.SysFont("Arial",30)

clock = pygame.time.Clock()
running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullets.append([player_x+20, player_y])

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed

    if keys[pygame.K_RIGHT] and player_x < WIDTH-50:
        player_x += player_speed

    # Spawn enemies
    if random.randint(1,30) == 1:
        enemies.append([random.randint(0,750),0])

    # Move bullets
    for bullet in bullets:
        bullet[1] -= bullet_speed

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
            if abs(enemy[0]-bullet[0]) < 40 and abs(enemy[1]-bullet[1]) < 40:
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                break

    bullets = [b for b in bullets if b[1] > 0]

    # SKY
    screen.fill(SKY)

    # SUN
    pygame.draw.circle(screen,YELLOW,(700,80),40)

    # CLOUDS
    for cloud in clouds:
        pygame.draw.circle(screen, WHITE, (cloud[0],cloud[1]),25)
        pygame.draw.circle(screen, WHITE, (cloud[0]+25,cloud[1]),30)
        pygame.draw.circle(screen, WHITE, (cloud[0]+50,cloud[1]),25)

    # BIRDS
    for bird in birds:
        pygame.draw.line(screen,BLACK,(bird[0],bird[1]),(bird[0]+10,bird[1]-5),2)
        pygame.draw.line(screen,BLACK,(bird[0]+10,bird[1]-5),(bird[0]+20,bird[1]),2)

    # ROCKET (player)
    pygame.draw.polygon(screen,GRAY,[
        (player_x+25, player_y),
        (player_x, player_y+50),
        (player_x+50, player_y+50)
    ])

    # Bullets
    for bullet in bullets:
        pygame.draw.rect(screen,BLACK,(bullet[0],bullet[1],5,15))

    # Enemies
    for enemy in enemies:
        pygame.draw.rect(screen,RED,(enemy[0],enemy[1],40,40))

    # Score
    text = font.render("Score: "+str(score),True,BLACK)
    screen.blit(text,(10,10))

    pygame.display.update()

pygame.quit()