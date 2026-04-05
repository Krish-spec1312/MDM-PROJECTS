import pygame
import random

pygame.init()

WIDTH = 900
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Mario Platformer")

clock = pygame.time.Clock()

# Colors
SKY = (135,206,235)
GROUND = (120,70,15)
BRICK = (178,34,34)
YELLOW = (255,223,0)
RED = (200,50,50)
BLACK = (0,0,0)

font = pygame.font.SysFont("Arial",30)
big_font = pygame.font.SysFont("Arial",50)

# Player
player = pygame.Rect(200,350,40,50)
velocity_y = 0
gravity = 0.6
jump_power = -12
speed = 6

# Platforms (Mario blocks)
platforms = [
    pygame.Rect(0,420,1200,80),
    pygame.Rect(300,330,120,20),
    pygame.Rect(550,260,120,20),
    pygame.Rect(750,200,120,20)
]

# Coins
coins = []
for i in range(8):
    coins.append(pygame.Rect(random.randint(200,1200),
                             random.randint(100,350),20,20))

# Enemies
enemies = []
for i in range(4):
    enemies.append(pygame.Rect(random.randint(400,1200),390,30,30))

score = 0
game_over = False
game_won = False

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over and not game_won:

        if keys[pygame.K_LEFT]:
            player.x -= speed

        if keys[pygame.K_RIGHT]:
            player.x += speed

        if keys[pygame.K_UP] and velocity_y == 0:
            velocity_y = jump_power

    # Gravity
    velocity_y += gravity
    player.y += velocity_y

    # Platform collision
    for platform in platforms:
        if player.colliderect(platform) and velocity_y > 0:
            player.bottom = platform.top
            velocity_y = 0

    # Move enemies
    for enemy in enemies:
        enemy.x -= 2
        if enemy.x < -50:
            enemy.x = random.randint(900,1200)

    # Enemy collision
    for enemy in enemies:
        if player.colliderect(enemy):
            game_over = True

    # Coin collection
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 1
            coins.append(pygame.Rect(random.randint(900,1200),
                                     random.randint(100,350),20,20))

    if score >= 50:
        game_won = True

    # Scroll world
    if player.x > 400:
        shift = player.x - 400
        player.x = 400

        for platform in platforms:
            platform.x -= shift

        for coin in coins:
            coin.x -= shift

        for enemy in enemies:
            enemy.x -= shift

    # Draw background
    screen.fill(SKY)

    # Platforms
    for platform in platforms:
        pygame.draw.rect(screen,BRICK,platform)

    # Coins
    for coin in coins:
        pygame.draw.circle(screen,YELLOW,(coin.x+10,coin.y+10),10)

    # Enemies
    for enemy in enemies:
        pygame.draw.rect(screen,(139,69,19),enemy)

    # Player
    pygame.draw.rect(screen,RED,player)

    # Score
    score_text = font.render("Coins: "+str(score),True,BLACK)
    screen.blit(score_text,(10,10))

    # Win message
    if game_won:
        win = big_font.render("YOU WIN!",True,(0,150,0))
        screen.blit(win,(350,200))

    # Game over
    if game_over:
        over = big_font.render("GAME OVER",True,(200,0,0))
        screen.blit(over,(320,200))

    pygame.display.update()

pygame.quit()