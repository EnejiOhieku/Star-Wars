import pygame

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
'''
back_btn_img = pygame.image.load('./img/buttons/back.png')
credits_btn_img = pygame.image.load('./img/buttons/credits.png')
exit_btn_img = pygame.image.load('./img/buttons/exit.png')
help_btn_img = pygame.image.load('./img/buttons/help.png')
main_menu_btn_img = pygame.image.load('./img/buttons/main_menu.png')
restart_btn_img = pygame.image.load('./img/buttons/restart.png')
resume_btn_img = pygame.image.load('./img/buttons/resume.png')
start_btn_img = pygame.image.load('./img/buttons/start.png')
'''


def game_loading_screen():
    screen_icon = pygame.image.load('img/icon.png')
    screen = pygame.display.set_mode((400, 300), pygame.NOFRAME)
    pygame.font.init()
    font = pygame.font.SysFont('FreeMono', 30, bold=True)
    text = font.render('Star Wars ...', True, (0, 0, 255))
    screen.blit(pygame.transform.scale(pygame.image.load('img/background.png'), (400, 300)), (0, 0))
    pygame.draw.rect(screen, WHITE, (0, 0, 400, 300), 4)
    screen.blit(text, (150, 160))
    screen.blit(pygame.transform.scale(screen_icon, (120, 120)), (20, 80))
    w = 20
    for block in range(14):
        pygame.draw.rect(screen, GREEN, (40, 260, w, 20))
        pygame.display.update()
        pygame.time.wait(50)
        w += 20
    pygame.display.update()
    pygame.display.quit()


class Button:
    def __init__(self, image, x, y, scale, function):
        self.image = pygame.transform.scale(image, (70, 70))
        self.rect = self.image.get_rect()
        self.x, self.y = (x, y)
        self.action = function

    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(*pos):
            self.rect.size = (self.rect.width * 1.1, self.rect.height * 1.1)
            self.rect.center = (self.x, self.y)
            pygame.draw.rect(screen, GREEN, self.rect)
            print(pygame.mouse.get_pressed())
        else:
            pygame.draw.rect(screen, RED, self.rect)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        # screen.blit(self.image, self.rect.center)


def load_images():
    items = ['missile', 'space_craft']
    images = []
    for i in range(len(items)):
        for item in items:
            image = []
            if i == 1 and item == 'missile':
                res = (40, 40)
            elif item == 'missile':
                res = (30, 30)
            else:
                res = (64, 64)
            for j in range(4):
                pic = pygame.transform.scale(pygame.image.load(f'img/{item + str(i)}/{j}.png'), res).convert_alpha()
                image.append(pic)
            images.append(image)
    return images


def draw_text(screen, text, x, y, font_size):
    font = pygame.font.SysFont('Courier 10 Pitch', font_size, True)
    img = font.render(text, False, WHITE)
    screen.blit(img, (x, y))
    return img.get_rect()
