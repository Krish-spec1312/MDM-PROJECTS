import pygame
import random
import time

pygame.init()

WIDTH = 900
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spiderman Jungle Adventure")

clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial",28)
big_font = pygame.font.SysFont("Arial",50)

# ---------- LOAD IMAGES ----------
spiderman_img = pygame.image.load("spiderman.png")
spiderman_img = pygame.transform.scale(spiderman_img,(60,70))

tiger_img = pygame.image.load("tiger.png")
tiger_img = pygame.transform.scale(tiger_img,(60,40))

snake_img = pygame.image.load("snake.png")
snake_img = pygame.transform.scale(snake_img,(60,30))

coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img,(25,25))

tree_img = pygame.image.load("tree.png")
tree_img = pygame.transform.scale(tree_img,(120,180))

bg_img = pygame.image.load("background.png")
bg_img = pygame.transform.scale(bg_img,(900,500))

# ---------- PLAYER ----------
player = pygame.Rect(200,350,40,60)

velocity_y = 0
gravity = 0.6
jump_power = -12
speed = 6

# ---------- GROUND ----------
platforms = []
for i in range(6):
    platforms.append(pygame.Rect(i*200,420,200,80))

def spawn_platform():
    last_x = platforms[-1].x
    return pygame.Rect(last_x + 200,420,200,80)

# ---------- FLOATING PLATFORMS ----------
air_platforms = []

def spawn_air_platform():
    x = random.randint(900,1600)  # better spacing
    y = random.randint(220,350)
    return pygame.Rect(x,y,120,15)

for i in range(4):
    air_platforms.append(spawn_air_platform())

# ---------- COINS ----------
coins = []
for i in range(8):
    coins.append(pygame.Rect(random.randint(300,1200),
                             random.randint(200,350),20,20))

# ---------- COIN PARTICLES ----------
particles = []

# ---------- ENEMIES ----------
enemies = []
enemy_types = []
enemy_spacing = 300

for i in range(4):
    enemies.append(pygame.Rect(600 + i*enemy_spacing,390,40,30))
    enemy_types.append(random.choice(["tiger","snake"]))

enemy_speed = 1.2

# ---------- FLAG ----------
flag = None

# ---------- TIMER ----------
TIME_LIMIT = 600
start_time = time.time()

score = 0
game_over = False
game_won = False

# ---------- CLOUDS ----------
clouds = []

for i in range(5):
    clouds.append([random.randint(0,900),random.randint(20,150)])

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

    keys = pygame.key.get_pressed()

    if not game_over and not game_won:

        if keys[pygame.K_LEFT]:
            player.x -= speed

        if keys[pygame.K_RIGHT]:
            player.x += speed

        if keys[pygame.K_UP] and velocity_y == 0:
            velocity_y = jump_power

    # ---------- GRAVITY ----------
    velocity_y += gravity
    player.y += velocity_y

    # ---------- GROUND COLLISION ----------
    for platform in platforms:
        if player.colliderect(platform) and velocity_y > 0:
            player.bottom = platform.top
            velocity_y = 0

    # ---------- AIR PLATFORM COLLISION ----------
    for ap in air_platforms:
        if player.colliderect(ap) and velocity_y > 0:
            player.bottom = ap.top
            velocity_y = 0

    # ---------- ENEMY MOVEMENT ----------
    for enemy in enemies:
        enemy.x -= enemy_speed

    # reset enemies
    if enemies[0].x < -100:
        enemies.pop(0)
        enemy_types.pop(0)

        new_x = enemies[-1].x + enemy_spacing
        enemies.append(pygame.Rect(new_x,390,40,30))
        enemy_types.append(random.choice(["tiger","snake"]))

    # enemy collision
    for enemy in enemies:
        if player.colliderect(enemy):
            game_over = True

    # ---------- COIN COLLECTION ----------
    for coin in coins[:]:

        if player.colliderect(coin):

            coins.remove(coin)
            score += 1

            # particles
            for i in range(12):
                particles.append([coin.x,coin.y,
                                  random.randint(-3,3),
                                  random.randint(-3,3)])

            # keep spawning until 50
            if score < 50:
                coins.append(pygame.Rect(random.randint(900,1500),
                                         random.randint(200,350),20,20))

    # ---------- FLAG ----------
    if score >= 50 and flag is None:
        flag = pygame.Rect(1200,350,30,70)

    if flag and player.colliderect(flag):
        game_won = True

    # ---------- SCROLL WORLD ----------
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

    # remove old platforms
    platforms = [p for p in platforms if p.x > -200]

    while platforms[-1].x < WIDTH + 200:
        platforms.append(spawn_platform())

    # regenerate air platforms
    air_platforms = [ap for ap in air_platforms if ap.x > -200]

    while len(air_platforms) < 4:
        air_platforms.append(spawn_air_platform())

    # ---------- DRAW ----------
    screen.blit(bg_img,(0,0))

    # clouds
    for cloud in clouds:

        pygame.draw.circle(screen,(255,255,255),(cloud[0],cloud[1]),25)
        pygame.draw.circle(screen,(255,255,255),(cloud[0]+25,cloud[1]),25)

        cloud[0] -= 0.5

        if cloud[0] < -50:
            cloud[0] = 900

    # trees
    for i in range(0,1200,250):
        screen.blit(tree_img,(i,250))

    # ground
    pygame.draw.rect(screen,(34,139,34),(0,400,900,100))

    for platform in platforms:
        pygame.draw.rect(screen,(139,69,19),platform)

    # floating platforms
    for ap in air_platforms:
        pygame.draw.rect(screen,(100,60,30),ap)

    # coins
    for coin in coins:
        screen.blit(coin_img,(coin.x,coin.y))

    # enemies
    for i,enemy in enumerate(enemies):

        if enemy_types[i] == "tiger":
            screen.blit(tiger_img,(enemy.x,enemy.y-10))
        else:
            screen.blit(snake_img,(enemy.x,enemy.y))

    # player
    screen.blit(spiderman_img,(player.x,player.y))

    # particles
    for p in particles:
        pygame.draw.circle(screen,(255,215,0),(p[0],p[1]),3)
        p[0] += p[2]
        p[1] += p[3]

    # flag
    if flag:
        pygame.draw.rect(screen,(0,0,0),(flag.x,flag.y,5,70))
        pygame.draw.polygon(screen,(255,0,0),
                            [(flag.x+5,flag.y),
                             (flag.x+35,flag.y+15),
                             (flag.x+5,flag.y+30)])

    # birds
    for i in range(3):
        pygame.draw.polygon(screen,(0,0,0),
                            [(200+i*200,100),
                             (210+i*200,90),
                             (220+i*200,100)])

    # score
    score_text = font.render("Coins: "+str(score),True,(0,0,0))
    screen.blit(score_text,(10,10))

    minutes = remaining // 60
    seconds = remaining % 60

    timer = font.render(f"Time {minutes:02}:{seconds:02}",True,(0,0,0))
    screen.blit(timer,(750,10))

    if game_won:
        text = big_font.render("YOU WIN!",True,(0,150,0))
        screen.blit(text,(350,200))

    if game_over and not game_won:
        text = big_font.render("BETTER LUCK NEXT TIME",True,(200,0,0))
        screen.blit(text,(180,200))

    pygame.display.update()

pygame.quit()