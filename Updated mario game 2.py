import pygame
import random

pygame.init()

WIDTH = 900
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Endless Mario World")

clock = pygame.time.Clock()

# Colors
SKY = (135,206,235)
BROWN = (120,70,15)
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

# World offset (for scrolling)
world_shift = 0

# Platforms
platforms = [pygame.Rect(0,420,1200,80)]

# Coins
coins = []

score = 0
game_won = False

def spawn_platform():
    x = random.randint(900,1200)
    y = random.randint(200,380)
    return pygame.Rect(x,y,150,20)

def spawn_coin():
    x = random.randint(900,1200)
    y = random.randint(120,350)
    return pygame.Rect(x,y,20,20)

for i in range(5):
    platforms.append(spawn_platform())

for i in range(6):
    coins.append(spawn_coin())

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_won:

        if keys[pygame.K_LEFT]:
            player.x -= speed

        if keys[pygame.K_RIGHT]:
            player.x += speed

        if keys[pygame.K_UP] and velocity_y == 0:
            velocity_y = jump_power

        if keys[pygame.K_DOWN]:
            player.height = 30
        else:
            player.height = 50

    # Gravity
    velocity_y += gravity
    player.y += velocity_y

    # Platform collision
    for platform in platforms:
        if player.colliderect(platform) and velocity_y > 0:
            player.bottom = platform.top
            velocity_y = 0

    # World scrolling
    if player.x > 400:
        shift = player.x - 400
        player.x = 400

        for platform in platforms:
            platform.x -= shift

        for coin in coins:
            coin.x -= shift

    # Remove old platforms
    platforms = [p for p in platforms if p.x > -200]

    # Generate new platforms
    if len(platforms) < 6:
        platforms.append(spawn_platform())

    # Remove old coins
    coins = [c for c in coins if c.x > -50]

    # Spawn new coins
    if len(coins) < 6:
        coins.append(spawn_coin())

    # Coin collection
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 1

    # Win condition
    if score >= 50:
        game_won = True

    # Draw background
    screen.fill(SKY)

    # Platforms
    for platform in platforms:
        pygame.draw.rect(screen,BROWN,platform)

    # Coins
    for coin in coins:
        pygame.draw.circle(screen,YELLOW,(coin.x+10,coin.y+10),10)

    # Player
    pygame.draw.rect(screen,RED,player)

    # Score
    score_text = font.render("Score: "+str(score),True,BLACK)
    screen.blit(score_text,(10,10))

    # Win message
    if game_won:
        win_text = big_font.render("YOU WIN!",True,(0,150,0))
        screen.blit(win_text,(350,200))

    pygame.display.update()

pygame.quit()