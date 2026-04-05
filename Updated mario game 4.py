import pygame
import random
import time

pygame.init()

WIDTH = 900
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spiderman Jungle Adventure")

clock = pygame.time.Clock()

# Colors
SKY = (135,206,235)
GROUND = (139,69,19)
GREEN = (34,139,34)
YELLOW = (255,223,0)
RED = (200,0,0)
BLACK = (0,0,0)
ORANGE = (255,165,0)

font = pygame.font.SysFont("Arial",28)
big_font = pygame.font.SysFont("Arial",50)

# Player (Spiderman style)
player = pygame.Rect(200,350,40,60)

velocity_y = 0
gravity = 0.6
jump_power = -12
speed = 6
crouch = False

# Platforms
platforms = [
    pygame.Rect(0,420,1200,80),
    pygame.Rect(300,330,120,20),
    pygame.Rect(550,260,120,20),
    pygame.Rect(750,200,120,20)
]

# Coins
coins = []
for i in range(8):
    coins.append(pygame.Rect(random.randint(300,1200),
                             random.randint(100,350),20,20))

# Enemies (lion/tiger)
enemies = []
for i in range(4):
    enemies.append(pygame.Rect(random.randint(500,1200),390,40,30))

enemy_speed = 1.2   # slower enemies

# Flag
flag = None

# Timer
TIME_LIMIT = 600
start_time = time.time()

score = 0
game_over = False
game_won = False

running = True

while running:

    clock.tick(60)

    elapsed = int(time.time() - start_time)
    remaining = max(0, TIME_LIMIT - elapsed)

    if remaining == 0 and not game_won:
        game_over = True

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

        # crouch
        if keys[pygame.K_DOWN]:
            player.height = 40
        else:
            player.height = 60

    # gravity
    velocity_y += gravity
    player.y += velocity_y

    # platform collision
    for platform in platforms:
        if player.colliderect(platform) and velocity_y > 0:
            player.bottom = platform.top
            velocity_y = 0

    # enemy movement (slow)
    for enemy in enemies:
        enemy.x -= enemy_speed
        if enemy.x < -50:
            enemy.x = random.randint(900,1200)

    # enemy collision
    for enemy in enemies:
        if player.colliderect(enemy):
            game_over = True

    # coin collection
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            score += 1
            coins.append(pygame.Rect(random.randint(900,1200),
                                     random.randint(100,350),20,20))

    # spawn flag at 50 coins
    if score >= 50 and flag is None:
        flag = pygame.Rect(1200,350,30,70)

    # win if reach flag
    if flag and player.colliderect(flag):
        game_won = True

    # scrolling world
    if player.x > 400:
        shift = player.x - 400
        player.x = 400

        for platform in platforms:
            platform.x -= shift

        for coin in coins:
            coin.x -= shift

        for enemy in enemies:
            enemy.x -= shift

        if flag:
            flag.x -= shift

    # draw background
    screen.fill(SKY)

    # sun
    pygame.draw.circle(screen,YELLOW,(750,80),40)

    # jungle ground
    pygame.draw.rect(screen,GREEN,(0,400,900,100))

    # platforms
    for platform in platforms:
        pygame.draw.rect(screen,GROUND,platform)

    # coins
    for coin in coins:
        pygame.draw.circle(screen,YELLOW,(coin.x+10,coin.y+10),10)

    # enemies (lion/tiger look)
    for enemy in enemies:
        pygame.draw.rect(screen,ORANGE,enemy)
        pygame.draw.circle(screen,BLACK,(enemy.x+10,enemy.y+10),3)

    # spiderman player
    pygame.draw.rect(screen,RED,player)
    pygame.draw.circle(screen,BLACK,(player.x+12,player.y+15),3)
    pygame.draw.circle(screen,BLACK,(player.x+28,player.y+15),3)

    # flag
    if flag:
        pygame.draw.rect(screen,BLACK,(flag.x,flag.y,5,70))
        pygame.draw.polygon(screen,(255,0,0),
                            [(flag.x+5,flag.y),
                             (flag.x+35,flag.y+15),
                             (flag.x+5,flag.y+30)])

    # score
    score_text = font.render("Coins: "+str(score),True,BLACK)
    screen.blit(score_text,(10,10))

    # timer
    minutes = remaining // 60
    seconds = remaining % 60
    timer = font.render(f"Time {minutes:02}:{seconds:02}",True,BLACK)
    screen.blit(timer,(750,10))

    # win message
    if game_won:
        text = big_font.render("YOU WIN!",True,(0,150,0))
        screen.blit(text,(350,200))

    # time over
    if game_over and not game_won:
        text = big_font.render("BETTER LUCK NEXT TIME",True,(200,0,0))
        screen.blit(text,(180,200))

    pygame.display.update()

pygame.quit()