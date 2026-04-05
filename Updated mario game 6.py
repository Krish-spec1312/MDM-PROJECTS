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

# Player
player = pygame.Rect(200,350,40,60)

velocity_y = 0
gravity = 0.6
jump_power = -12
speed = 6

# ---------- ENDLESS GROUND ----------
platforms = []
for i in range(6):
    platforms.append(pygame.Rect(i*200,420,200,80))

def spawn_platform():
    last_x = platforms[-1].x
    return pygame.Rect(last_x + 200,420,200,80)

# ---------- FLOATING PLATFORMS ----------
air_platforms = []

def spawn_air_platform():
    x = random.randint(900,1200)
    y = random.randint(220,350)
    return pygame.Rect(x,y,100,15)

for i in range(4):
    air_platforms.append(spawn_air_platform())

# ---------- COINS ----------
coins = []
for i in range(8):
    coins.append(pygame.Rect(random.randint(300,1200),
                             random.randint(200,350),20,20))

# ---------- ENEMIES WITH SPACING ----------
enemies = []
enemy_spacing = 250

for i in range(4):
    enemies.append(pygame.Rect(600 + i*enemy_spacing,390,40,30))

enemy_speed = 1.2

# ---------- FLAG ----------
flag = None

# ---------- TIMER ----------
TIME_LIMIT = 600
start_time = time.time()
remaining = TIME_LIMIT

score = 0
game_over = False
game_won = False

running = True

while running:

    clock.tick(60)

    # TIMER
    if not game_over and not game_won:
        elapsed = int(time.time() - start_time)
        remaining = max(0, TIME_LIMIT - elapsed)

        if remaining == 0:
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

        if keys[pygame.K_DOWN]:
            player.height = 40
        else:
            player.height = 60

    # gravity
    velocity_y += gravity
    player.y += velocity_y

    # collision with ground
    for platform in platforms:
        if player.colliderect(platform) and velocity_y > 0:
            player.bottom = platform.top
            velocity_y = 0

    # collision with air platforms
    for ap in air_platforms:
        if player.colliderect(ap) and velocity_y > 0:
            player.bottom = ap.top
            velocity_y = 0

    # enemy movement
    for enemy in enemies:
        enemy.x -= enemy_speed

    # enemy reset with spacing
    if enemies[0].x < -100:
        enemies.pop(0)
        new_x = enemies[-1].x + enemy_spacing
        enemies.append(pygame.Rect(new_x,390,40,30))

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
                                     random.randint(200,350),20,20))

    # spawn flag
    if score >= 50 and flag is None:
        flag = pygame.Rect(1200,350,30,70)

    if flag and player.colliderect(flag):
        game_won = True

    # scrolling world
    if player.x > 400:
        shift = player.x - 400
        player.x = 400

        for platform in platforms:
            platform.x -= shift

        for ap in air_platforms:
            ap.x -= shift

        for coin in coins:
            coin.x -= shift

        for enemy in enemies:
            enemy.x -= shift

        if flag:
            flag.x -= shift

    # remove old ground
    platforms = [p for p in platforms if p.x > -200]

    while platforms[-1].x < WIDTH + 200:
        platforms.append(spawn_platform())

    # air platforms regeneration
    air_platforms = [ap for ap in air_platforms if ap.x > -200]

    while len(air_platforms) < 4:
        air_platforms.append(spawn_air_platform())

    # ---------- DRAW ----------
    screen.fill(SKY)

    pygame.draw.circle(screen,YELLOW,(750,80),40)

    pygame.draw.rect(screen,GREEN,(0,400,900,100))

    for platform in platforms:
        pygame.draw.rect(screen,GROUND,platform)

    for ap in air_platforms:
        pygame.draw.rect(screen,(100,60,30),ap)

    for coin in coins:
        pygame.draw.circle(screen,YELLOW,(coin.x+10,coin.y+10),10)

    for enemy in enemies:
        pygame.draw.rect(screen,ORANGE,enemy)

    # spiderman
    pygame.draw.rect(screen,RED,player)
    pygame.draw.circle(screen,BLACK,(player.x+12,player.y+15),3)
    pygame.draw.circle(screen,BLACK,(player.x+28,player.y+15),3)

    if flag:
        pygame.draw.rect(screen,BLACK,(flag.x,flag.y,5,70))
        pygame.draw.polygon(screen,(255,0,0),
                            [(flag.x+5,flag.y),
                             (flag.x+35,flag.y+15),
                             (flag.x+5,flag.y+30)])

    score_text = font.render("Coins: "+str(score),True,BLACK)
    screen.blit(score_text,(10,10))

    minutes = remaining // 60
    seconds = remaining % 60
    timer = font.render(f"Time {minutes:02}:{seconds:02}",True,BLACK)
    screen.blit(timer,(750,10))

    if game_won:
        text = big_font.render("YOU WIN!",True,(0,150,0))
        screen.blit(text,(350,200))

    if game_over and not game_won:
        text = big_font.render("BETTER LUCK NEXT TIME",True,(200,0,0))
        screen.blit(text,(180,200))

    pygame.display.update()

pygame.quit()