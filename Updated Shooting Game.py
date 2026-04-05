import pygame
import random

pygame.init()

# Screen
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
SKY = (135,206,235)

# Player
player = pygame.Rect(375,520,50,50)
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
    x = random.randint(0, WIDTH)
    y = random.randint(0, 200)
    clouds.append([x,y])

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
                bullet = pygame.Rect(player.x+20, player.y, 10, 20)
                bullets.append(bullet)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player.x > 0:
        player.x -= player_speed

    if keys[pygame.K_RIGHT] and player.x < WIDTH-50:
        player.x += player_speed

    # Spawn enemies
    if random.randint(1,30) == 1:
        enemy = pygame.Rect(random.randint(0,750),0,50,50)
        enemies.append(enemy)

    # Move bullets
    for bullet in bullets:
        bullet.y -= bullet_speed

    # Move enemies
    for enemy in enemies:
        enemy.y += enemy_speed

    # Move clouds
    for cloud in clouds:
        cloud[0] -= 1
        if cloud[0] < -100:
            cloud[0] = WIDTH
            cloud[1] = random.randint(0,200)

    # Collision detection
    for enemy in enemies[:]:
        for bullet in bullets[:]:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                break

    # Remove off-screen bullets
    bullets = [b for b in bullets if b.y > 0]

    # Background
    screen.fill(SKY)

    # Draw clouds
    for cloud in clouds:
        pygame.draw.circle(screen, WHITE, (cloud[0],cloud[1]),25)
        pygame.draw.circle(screen, WHITE, (cloud[0]+25,cloud[1]),30)
        pygame.draw.circle(screen, WHITE, (cloud[0]+50,cloud[1]),25)

    # Draw player
    pygame.draw.rect(screen,GREEN,player)

    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen,BLACK,bullet)

    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen,RED,enemy)

    # Score
    text = font.render("Score: "+str(score),True,BLACK)
    screen.blit(text,(10,10))

    pygame.display.update()

pygame.quit()