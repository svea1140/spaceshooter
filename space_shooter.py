import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("太空射击游戏")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        pygame.draw.polygon(self.image, (0, 200, 0), [(25, 0), (50, 40), (0, 40)])
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0
        self.max_speed = 7
        self.health = 100
        self.max_health = 100

    def update(self):
        self.speed_x = 0
        self.speed_y = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.speed_x = -self.max_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.speed_x = self.max_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.speed_y = -self.max_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.speed_y = self.max_speed
        
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 15))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 35))
        self.image.fill(RED)
        pygame.draw.polygon(self.image, (200, 0, 0), [(20, 35), (40, 0), (0, 0)])
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 4)
        self.speed_x = random.randrange(-2, 2)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speed_y = random.randrange(1, 4)

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.size = random.randint(20, 50)
        self.image = pygame.Surface((self.size, self.size))
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, (150, 150, 150), (self.size//2, self.size//2), self.size//2)
        pygame.draw.circle(self.image, (100, 100, 100), (self.size//3, self.size//3), self.size//6)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 3)
        self.speed_x = random.randrange(-1, 1)
        self.rotation = 0
        self.rotation_speed = random.randrange(-3, 3)

    def rotate(self):
        self.rotation = (self.rotation + self.rotation_speed) % 360
        old_center = self.rect.center
        new_image = pygame.transform.rotate(self.image, self.rotation)
        self.image = new_image
        self.rect = self.image.get_rect()
        self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT + 10 or self.rect.left < -50 or self.rect.right > WIDTH + 50:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.type = random.choice(['health', 'speed', 'shield'])
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        if self.type == 'health':
            pygame.draw.circle(self.image, (255, 0, 0), (15, 15), 14)
            pygame.draw.rect(self.image, WHITE, (12, 5, 6, 20))
            pygame.draw.rect(self.image, WHITE, (5, 12, 20, 6))
        elif self.type == 'speed':
            pygame.draw.polygon(self.image, (0, 255, 255), [(15, 0), (30, 30), (0, 30)])
        elif self.type == 'shield':
            pygame.draw.circle(self.image, (0, 200, 255), (15, 15), 14, 3)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed_y = 2

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.size = 30
        self.image = pygame.Surface((self.size, self.size))
        self.image.set_colorkey(BLACK)
        pygame.draw.circle(self.image, YELLOW, (self.size//2, self.size//2), self.size//2)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.timer = 20
        self.max_timer = 20

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
        else:
            alpha = int(255 * (self.timer / self.max_timer))
            self.image.set_alpha(alpha)

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 5))
        self.image.fill((random.randint(200, 255), random.randint(100, 200), 0))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 5)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = 30

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.life -= 1
        if self.life <= 0:
            self.kill()

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def spawn_enemy():
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

def spawn_asteroid():
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

def create_explosion(center):
    explosion = Explosion(center)
    all_sprites.add(explosion)
    for _ in range(10):
        particle = Particle(center[0], center[1])
        all_sprites.add(particle)
        particles.add(particle)

def show_game_over_screen():
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, f"最终得分: {score}", 36, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "按任意键重新开始...", 24, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYUP:
                waiting = False
    return True

def show_start_screen():
    screen.fill(BLACK)
    draw_text(screen, "太空射击游戏", 64, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "方向键或WASD移动，空格键射击", 24, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "按任意键开始...", 24, WIDTH // 2, HEIGHT * 3 // 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYUP:
                waiting = False
    return True

all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
powerups = pygame.sprite.Group()
particles = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

clock = pygame.time.Clock()
score = 0
level = 1
shoot_delay = 0

game_active = False
running = True

while running:
    if not game_active:
        if not show_start_screen():
            break
        all_sprites.empty()
        bullets.empty()
        enemies.empty()
        asteroids.empty()
        powerups.empty()
        particles.empty()
        player = Player()
        all_sprites.add(player)
        score = 0
        level = 1
        for i in range(5):
            spawn_enemy()
        for i in range(3):
            spawn_asteroid()
        game_active = True

    clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                if shoot_delay == 0:
                    player.shoot()
                    shoot_delay = 10

    if shoot_delay > 0:
        shoot_delay -= 1

    all_sprites.update()

    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        create_explosion(hit.rect.center)
        spawn_enemy()
        if random.random() > 0.9:
            powerup = PowerUp(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)

    hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
    for hit in hits:
        score += 5
        create_explosion(hit.rect.center)
        if random.random() > 0.5:
            spawn_asteroid()

    hits = pygame.sprite.spritecollide(player, enemies, True)
    for hit in hits:
        player.health -= 20
        create_explosion(hit.rect.center)
        spawn_enemy()
        if player.health <= 0:
            game_active = False

    hits = pygame.sprite.spritecollide(player, asteroids, True)
    for hit in hits:
        player.health -= 10
        create_explosion(hit.rect.center)
        if player.health <= 0:
            game_active = False

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'health':
            player.health = min(player.health + 30, player.max_health)
        elif hit.type == 'speed':
            player.max_speed = 10
            pygame.time.set_timer(pygame.USEREVENT + 1, 5000)
        elif hit.type == 'shield':
            player.health = min(player.health + 10, player.max_health)

    if random.random() < 0.02:
        spawn_asteroid()

    if score > level * 100:
        level += 1
        for i in range(2):
            spawn_enemy()

    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text(screen, f"得分: {score}", 18, WIDTH // 2, 10)
    draw_text(screen, f"等级: {level}", 18, WIDTH - 60, 10)
    draw_health_bar(screen, 10, 10, player.health)
    
    pygame.display.flip()

    if not game_active:
        if not show_game_over_screen():
            break
        else:
            game_active = True

pygame.quit()