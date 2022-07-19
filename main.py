
from extras import *
from random import *

# initialize pygame module
pygame.init()

# screen parameters ##
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen_icon = pygame.image.load('img/icon.png')
pygame.display.set_icon(screen_icon)
pygame.display.set_caption('Star Wars')
screen_background = pygame.transform.scale(pygame.image.load('img/background.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
####################


## colors ##
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
##############


### load sounds ##
pygame.mixer.music.load('music/background.mp3')
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1)
enemy_explosion_fx = pygame.mixer.Sound('music/enemy_explosion.mp3')
launch_fx = pygame.mixer.Sound('music/launch.mp3')
launch_fx.set_volume(0.1)
player_hit_fx = pygame.mixer.Sound('music/player_hit.mp3')
player_hit_fx.set_volume(1)
game_over_fx = pygame.mixer.Sound('music/game_over.mp3')
game_over_fx.set_volume(1)
###################


### load and create game screen ###
game_loading_screen()
pygame.display.set_icon(screen_icon)
pygame.display.set_caption('Star Wars')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen_rect = screen.get_rect()
############################


##### loading images #####
images = load_images()
player_missile_img = images[0]
enemy_missile_img = images[2]
player_img = images[1]
enemy_img = images[3]


###########################


class SpaceCraft(pygame.sprite.Sprite):
    def __init__(self, craft_type, pos):
        pygame.sprite.Sprite.__init__(self)

        self.speed_x = 0
        self.speed_y = 0
        self.moving_up = False
        self.moving_down = False
        self.moving_right = False
        self.moving_left = False
        self.alive = True
        self.health = 100
        self.max_health = self.health
        self.craft_type = craft_type
        self.orientation = randint(0, 3)
        self.movement = ['up', 'down', 'right', 'left', 'idle']
        ## AI specific variables
        self.move_cooldown = 300
        self.move_counter = 280
        self.launch_cooldown = 0
        self.idling = False
        self.idling_counter = 0
        self.vision_lenght = 160
        self.vision_width = 30
        self.vision = pygame.Rect(0, 0, self.vision_width, self.vision_lenght)
        #####################

        if self.craft_type == 'player':
            self.img = player_img
            self.speed = 2
        elif self.craft_type == 'enemy':
            self.img = enemy_img
            self.speed = 1
        self.pos = pos
        self.rect = self.img[self.orientation].get_rect()
        self.rect.center = self.pos

    def draw(self):
        screen.blit(self.image, self.rect)

    def move(self):
        if self.alive and player.alive:
            if self.moving_up:
                self.orientation = 0
                self.speed_y = -self.speed
                self.speed_x = 0
            elif self.moving_down:
                self.orientation = 1
                self.speed_y = self.speed
                self.speed_x = 0
            elif self.moving_right:
                self.orientation = 2
                self.speed_x = self.speed
                self.speed_y = 0
            elif self.moving_left:
                self.orientation = 3
                self.speed_x = -self.speed
                self.speed_y = 0
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
            ### CHECKING IF IT HIT SCREEN BOUNDARIES ###
            # Right
            if self.rect.right >= screen_rect.width:
                self.rect.right = screen_rect.width
                self.move_counter = 0
                self.update_movement('left')
            # left
            if self.rect.x <= 0:
                self.rect.x = 0
                self.move_counter = 0
                self.update_movement('right')
            # bottom
            if self.rect.bottom >= screen_rect.height:
                self.rect.bottom = screen_rect.height
                self.move_counter = 0
                self.update_movement('up')
            # top
            if self.rect.y <= 0:
                self.rect.y = 0
                self.move_counter = 0
                self.update_movement('down')

    def launch(self):
        if self.orientation == 0:
            missile = Missile(self.rect.centerx, self.rect.top - 17, self.orientation, self.craft_type)
        elif self.orientation == 1:
            missile = Missile(self.rect.centerx, self.rect.bottom + 17, self.orientation, self.craft_type)
        elif self.orientation == 2:
            missile = Missile(self.rect.right + 17, self.rect.centery, self.orientation, self.craft_type)
        else:
            missile = Missile(self.rect.left - 17, self.rect.centery, self.orientation, self.craft_type)
        launch_fx.play()
        missile_group.add(missile)

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False

            if self.craft_type == 'enemy':
                pass

    def update_movement(self, action):
        if self.craft_type == 'enemy':
            if action == 'up':
                self.moving_up = True
                self.moving_down = False
                self.moving_right = False
                self.moving_left = False
            elif action == 'down':
                self.moving_up = False
                self.moving_down = True
                self.moving_right = False
                self.moving_left = False
            elif action == 'right':
                self.moving_up = False
                self.moving_down = False
                self.moving_right = True
                self.moving_left = False
            elif action == 'left':
                self.moving_up = False
                self.moving_down = False
                self.moving_right = False
                self.moving_left = True
            elif action == 'idle':
                self.moving_up = False
                self.moving_down = False
                self.moving_right = False
                self.moving_left = False

    def ai(self):
        if self.alive and player.alive:
            if not self.idling and randint(1, 300) == 2:
                self.idling_counter = 100
                self.idling = True
                self.speed = 0
            if self.vision.colliderect(player.rect):
                self.speed = 0
                if self.launch_cooldown == 0:
                    self.launch_cooldown = 100
                    self.launch()
            else:
                self.speed = 0
                if not self.idling:
                    self.speed = 1
                    self.move_counter += 1
                    if self.moving_up:
                        self.vision.size = (self.vision_width, self.vision_lenght)
                        self.vision.midbottom = self.rect.midtop
                    elif self.moving_down:
                        self.vision.midtop = self.rect.midbottom
                        self.vision.size = (self.vision_width, self.vision_lenght)
                    elif self.moving_right:
                        self.vision.midleft = self.rect.midright
                        self.vision.size = (self.vision_lenght, self.vision_width)
                    elif self.moving_left:
                        self.vision.size = (self.vision_lenght, self.vision_width)
                        self.vision.midright = self.rect.midleft
                    if self.move_counter > self.move_cooldown:
                        self.move_counter = 0
                        action = choice(self.movement[:4])
                        self.update_movement(action)
                #   pygame.draw.rect(screen, RED, self.vision)
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

    def update(self):
        self.image = self.img[self.orientation]
        self.draw()
        self.move()
        self.check_alive()
        if self.launch_cooldown > 0:
            self.launch_cooldown -= 1


class Missile(pygame.sprite.Sprite):

    def __init__(self, x, y, orientation, space_craft):
        pygame.sprite.Sprite.__init__(self)
        self.space_craft = space_craft
        if self.space_craft == 'player':
            self.img = player_missile_img
            self.speed = 4
        elif self.space_craft == 'enemy':
            self.img = enemy_missile_img
            self.speed = 2
        self.orientation = orientation
        self.image = self.img[self.orientation]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        if self.orientation == 0:
            self.rect.y -= self.speed
        elif self.orientation == 1:
            self.rect.y += self.speed
        elif self.orientation == 2:
            self.rect.x += self.speed
        else:
            self.rect.x -= self.speed

        if self.rect.x + 10 < 0 or self.rect.right - 10 > screen_rect.width or self.rect.y + 10 < 0 \
                or self.rect.bottom - 10 > screen_rect.height:
            self.kill()

        if self.space_craft == 'player':
            for ship in enemy_group:
                if ship.alive and self.rect.colliderect(ship.rect):
                    global score
                    score += 1
                    print(score)
                    enemy_explosion_fx.play()
                    explosion = Explosion(*ship.rect.center)
                    ship.kill()
                    self.kill()
                    explosion_group.add(explosion)
                    new_ship = SpaceCraft('enemy', (randint(0, 800), randint(0, 600)))
                    enemy_group.add(new_ship)
        elif self.space_craft == 'enemy':
            if player.alive and self.rect.colliderect(player.rect):
                player.health -= 5
                if player.health > 0:
                    player_hit_fx.play()
                else:
                    game_over_fx.play()
                    explosion = Explosion(*player.rect.center)
                    player.kill()
                    explosion_group.add(explosion)
                self.kill()


class HealthBar:
    def __init__(self, x, y, health, max_heath):
        self.rect = pygame.rect.Rect(x, y, 120, 20)
        self.ratio = health / max_heath

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.rect.x - 2, self.rect.y - 2, self.rect.width + 4, self.rect.height + 4))
        pygame.draw.rect(screen, RED, self.rect)
        pygame.draw.rect(screen, GREEN, (self.rect.x, self.rect.y, self.rect.width * self.ratio, self.rect.height))

    def update(self):
        self.draw()


class HealthPickUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for k in range(3):
            frame = pygame.image.load(f'img/explosion/{k}.png')
            frame = pygame.transform.scale(frame, (64, 64))
            self.images.append(frame)
        self.frame_index = 0
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.counter = 0

    def update(self):
        explosion_speed = 10
        self.counter += 1
        if self.counter >= explosion_speed:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index >= len(self.images):
                self.kill()
            else:
                self.image = self.images[self.frame_index]


### GAME SPECIFIC VARIABLES ###
running = True
fps = 60
clock = pygame.time.Clock()
player_launch = False
score = 0
########################

#### game Groups ####
missile_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
#####################

##### character initialization ####
player = SpaceCraft('player', screen_rect.center)
for _ in range(5):
    enemy = SpaceCraft('enemy', choice(((randint(0, 800), randint(0, 800)),
                                        (randint(0, 800), randint(0, 800)),

                                        )))
    enemy_group.add(enemy)

#####################

test = Button(player_missile_img[0], 200, 300, 1, load_images)


def update_game():
    global player_launch
    screen.blit(screen_background, (0, 0))
    # test.draw(screen)
    health_bar = HealthBar(10, 10, player.health, player.max_health)
    health_bar.update()
    player.update()
    missile_group.update()
    missile_group.draw(screen)
    explosion_group.update()
    explosion_group.draw(screen)
    for ship in enemy_group:
        ship.update()
        ship.ai()
    if player.alive and player_launch:
        player_launch = False
        player.launch()
    pygame.display.update()


def main():
    global player_launch, running
    clock.tick(fps)

    # main game loop
    while running:
        screen.fill((0, 0, 0))
        screen.blit(screen_background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_UP:
                    player.moving_up = True
                if event.key == pygame.K_DOWN:
                    player.moving_down = True
                if event.key == pygame.K_RIGHT:
                    player.moving_right = True
                if event.key == pygame.K_LEFT:
                    player.moving_left = True
                if event.key == pygame.K_SPACE:
                    player_launch = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    player.moving_up = False
                if event.key == pygame.K_DOWN:
                    player.moving_down = False
                if event.key == pygame.K_RIGHT:
                    player.moving_right = False
                if event.key == pygame.K_LEFT:
                    player.moving_left = False
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]:
                    player.speed_x = 0
                    player.speed_y = 0
                if event.key == pygame.K_SPACE:
                    player_launch = False

        update_game()


if __name__ == '__main__':
    main()
