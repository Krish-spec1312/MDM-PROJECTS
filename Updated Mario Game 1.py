import pygame
import random

pygame.init()

WIDTH = 900
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Mario Adventure")

clock = pygame.time.Clock()

# Colors
SKY = (135,206,235)
BROWN = (120,70,15)
YELLOW = (255,223,0)
RED = (200,50,50)
GREEN = (34,177,76)
BLACK = (0,0,0)

font = pygame.font.SysFont("Arial",30)
big_font = pygame.font.SysFont("Arial",50)

# Player
player = pygame.Rect(100,350,40,50)
velocity_y = 0
gravity = 0.6
jump_power = -12
speed = 6

crouching = False

# Platforms
platforms = [
    pygame.Rect(0,420,900,80),
    pygame.Rect(200,330,150,20),
    pygame.Rect(450,280,150,20),
    pygame.Rect(700,230,150,20)
]

# Coins
coins = []

def spawn_coin():
    return pygame.Rect(random.randint(50,850),random.randint(80,350),20,20)

for i in range(6):
    coins.append(spawn_coin())

score = 0
game_won = False

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_won:

        # Movement
        if keys[pygame.K_LEFT]:
            player.x -= speed

        if keys[pygame.K_RIGHT]:
            player.x += speed

        # Jump
        if keys[pygame.K_UP] and velocity_y == 0:
            velocity_y = jump_power

        # Crouch
        if keys[pygame.K_DOWN]:
            crouching = True
            player.height = 30
        else:
            crouching = False
            player.height = 50

    # Gravity
    velocity_y += gravity
    player.y += velocity_y

    # Platform collision
    for platform in platforms:
        if player.colliderect(platform) and velocity_y > 0:
            player.bottom = platform.top
            velocity_y = 0

    # Coin collection
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            coins.append(spawn_coin())   # endless spawning
            score += 1

    # Win condition
    if score >= 50:
        game_won = True

    # Background
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
    text = font.render("Score: "+str(score),True,BLACK)
    screen.blit(text,(10,10))

    # Win screen
    if game_won:
        win_text = big_font.render("YOU WIN!",True,(0,150,0))
        screen.blit(win_text,(350,200))

    pygame.display.update()

pygame.quit()