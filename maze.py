import pygame
import time


# Constants
FPS = 24
WIDTH = 1200
HEIGHT = 900
WALL_WIDTH = 40
WALL_HEIGHT = 400
BACKGROUND = pygame.image.load("images/background.jpg")


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image=None) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.transform.scale(image, (width, height))


class Player(GameSprite):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.x_speed = 0
        self.y_speed = 0

    def update(self, barriers):
        # Horizontal movement
        self.rect.x += self.x_speed
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)

        if self.x_speed > 0:
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.x_speed < 0:
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right)

        # Vertical movement
        self.rect.y += self.y_speed
        platforms_touched = pygame.sprite.spritecollide(self, barriers, False)

        if self.y_speed > 0:
            for p in platforms_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.y_speed < 0:
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

        # Border Check
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
        if self.rect.left <= 0:
            self.rect.left = 0
        
    def fire(self, ammo, direction, speed):
        load_pic = lambda img: pygame.image.load(img)
        if direction == "right":
            bullet = Bullet(self.rect.right, self.rect.centery, 40, 20, load_pic("images/bullet_right.png"), direction, speed)
        else:
            bullet = Bullet(self.rect.left, self.rect.centery, 40, 20, load_pic("images/bullet_left.png"), direction, speed)
        ammo.add(bullet)


class Bullet(GameSprite):
    def __init__(self, x, y, width, height, image, direction, speed):
        super().__init__(x, y, width, height, image)
        self.direction = direction
        if direction == "right":
            self.speed = speed
        else:
            self.speed = -speed

    def fly(self):
        self.rect.x += self.speed
        if self.rect.x < 0 or self.rect.x > WIDTH:
            self.kill()


class Enemy(GameSprite):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)
        self.speed = 5
        self.ceil = 0
        self.floor = 300

    def update(self, vertical_sprite, left_x=0, right_x=0):
        if vertical_sprite:
            self.rect.y += self.speed
            if self.rect.y <= self.ceil or self.rect.y >= self.floor:
                self.speed = -self.speed
        else:
            self.rect.x += self.speed
            if self.rect.x <= left_x or self.rect.right >= right_x:
                self.speed = -self.speed


class Wall(GameSprite):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)


class Bonus(GameSprite):
    def __init__(self, x, y, width, height, image):
        super().__init__(x, y, width, height, image)


def render_end_screen(screen, game_clock, new_background, start_time, victory):
    exit_flag = False
    finish_time = time.time() - start_time

    while not exit_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_flag = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return main()  # Start a new game

        screen.blit(pygame.transform.scale(new_background, (WIDTH, HEIGHT)), (0, 0))
        draw_end_text(screen, round(finish_time, 3), victory)
        game_clock.tick(FPS)
        pygame.display.flip()


def draw_end_text(screen, game_time, victory):
    font = pygame.font.SysFont("Arial", WIDTH//20)
    if victory:
        font_color = (10, 10, 255)
    else:
        font_color = (255, 0, 0)
    caption = font.render(f"Click mouse button to play again", True, font_color)
    screen.blit(caption, (WIDTH//6, HEIGHT//2 + 100))
    caption = font.render(f"Time: {game_time}", True, font_color)
    screen.blit(caption, (WIDTH//2 - 180, HEIGHT//2 + 200))


def main():
    run = True
    game_clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    start_time = time.time()
    player_speed = 7
    bullet_speed = 10

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("Maze")

    # Flags
    defeat = False
    victory = False

    # Loading images
    player_picture_right = pygame.image.load("images/pacman_right.png")
    player_picture_left = pygame.image.load("images/pacman_left.png")
    wall_texture = pygame.image.load("images/bricks.jpg")
    enemy_picture1 = pygame.image.load("images/blinky_left.png")
    enemy_picture2 = pygame.image.load("images/orange.png")
    enemy_picture3 = pygame.image.load("images/blue_ghost.png")
    star_picture = pygame.image.load("images/star.png")
    bonus_picture = pygame.image.load("images/bonus.png")

    # Defining objects
    player = Player(500, 400, 100, 100, player_picture_right)
    enemy1 = Enemy(50, 20, 90, 80, enemy_picture1)
    enemy2 = Enemy(WIDTH - 110, 300, 90, 80, enemy_picture2)
    enemy3 = Enemy(WIDTH//2, HEIGHT - 120, 90, 80, enemy_picture3)
    star = GameSprite(20, HEIGHT - 95, 75, 75, star_picture)  # Final score
    bonus = Bonus(WIDTH - 200, 20, 100, 100, bonus_picture)

    ammo = pygame.sprite.Group()
    monsters = pygame.sprite.Group()
    monsters.add(enemy1)
    monsters.add(enemy2)
    monsters.add(enemy3)
    enemies = [enemy1, enemy2, enemy3]

    # Walls
    wall1 = Wall(200, 300, WALL_WIDTH, WALL_HEIGHT, wall_texture)
    wall2 = Wall(850, 0, WALL_WIDTH, WALL_HEIGHT, wall_texture)
    wall3 = Wall(200, 300, WALL_HEIGHT, WALL_WIDTH, wall_texture)
    wall4 = Wall(200, 700, WALL_HEIGHT, WALL_WIDTH, wall_texture)
    wall5 = Wall(600, 700, WALL_HEIGHT, WALL_WIDTH, wall_texture)
    walls = [wall1, wall2, wall3, wall4, wall5]
    barriers = pygame.sprite.Group()
    for wall in walls:
        barriers.add(wall)

    while run and (not defeat) and (not victory):
        screen.blit(pygame.transform.scale(BACKGROUND, (WIDTH, HEIGHT)), (0, 0))

        # Events handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Movement handler
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w]:
                    player.y_speed = -player_speed
                elif event.key in [pygame.K_DOWN, pygame.K_s]:
                    player.y_speed = player_speed
                elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                    player.x_speed = player_speed
                    player.image = player_picture_right  # Changing looking direction to right
                elif event.key in [pygame.K_LEFT, pygame.K_a]:
                    player.x_speed = -player_speed
                    player.image = player_picture_left  # Changing looking direction to left
                elif event.key == pygame.K_SPACE:  # Shooting
                    if player.image == player_picture_right:
                        player.fire(ammo, "right", bullet_speed)
                    else:
                        player.fire(ammo, "left", bullet_speed)
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s]:  # Vertical
                    player.y_speed = 0
                elif event.key in [pygame.K_RIGHT, pygame.K_d, pygame.K_LEFT, pygame.K_a]:  # Horizontal
                    player.x_speed = 0

        # Movement handler
        player.update(barriers)
        enemy1.update(True)
        enemy2.update(False, WIDTH - 300, WIDTH - 10)
        enemy3.update(False, WIDTH//2 - 200, WIDTH//2 + 200)

        for bullet in ammo:
            screen.blit(pygame.transform.scale(bullet.image, (bullet.width, bullet.height)), bullet.rect)
            bullet.fly()

        # Collision handler
        for monster in monsters:
            for bullet in ammo:
                if pygame.sprite.collide_rect(bullet, monster):
                    bullet.kill()
                    monster.speed = 0
                    monster.rect.x = -500

        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                defeat = True  # Game Over
                time.sleep(0.5)  # Wait 0.5 seconds till show end game screen
                break
        
        if pygame.sprite.collide_rect(player, star):
            victory = True
            time.sleep(0.5)  # Wait 0.5 seconds till show end game screen
            break

        pygame.sprite.groupcollide(ammo, barriers, True, False)

        if pygame.sprite.collide_rect(player, bonus):
            player_speed *= 4
            bullet_speed *= 4
            bonus.rect.x = -300

        # Drawing (updating) objects
        screen.blit(pygame.transform.scale(enemy1.image, (enemy1.width, enemy1.height)), enemy1.rect)  # Enemy 1
        screen.blit(pygame.transform.scale(enemy2.image, (enemy2.width, enemy2.height)), enemy2.rect)  # Enemy 2
        screen.blit(pygame.transform.scale(enemy3.image, (enemy3.width, enemy3.height)), enemy3.rect)  # Enemy 3
        screen.blit(pygame.transform.scale(player.image, (player.width, player.height)), player.rect)  # Player
        screen.blit(pygame.transform.scale(bonus.image, (bonus.width, bonus.height)), bonus.rect)  # Bonus
        screen.blit(pygame.transform.scale(star.image, (star.width, star.height)), star.rect)  # Final Score

        for wall in walls:
            screen.blit(wall.image, wall.rect)

        # Screen render
        game_clock.tick(FPS)
        pygame.display.flip()

    if defeat:
        new_background = pygame.image.load("images/game_over.png")
        render_end_screen(screen, game_clock, new_background, start_time, False)
    elif victory:
        new_background = pygame.image.load("images/victory.png")
        render_end_screen(screen, game_clock, new_background, start_time, True)


if __name__ == "__main__":
    main()
