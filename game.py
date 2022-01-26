import pygame
from pygame.math import Vector2
import sys
import os
import random


def render_points():
    font = pygame.font.Font(None, 25)
    text = font.render(f"{points}", True, (100, 255, 100))
    screen.blit(text, (350, 0))


def rotatePivoted(im, angle, pivot):
    # rotate the leg image around the pivot
    image = pygame.transform.rotate(im, angle)
    rect = image.get_rect()
    rect.center = pivot
    return image, rect


def load_image(name):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():
    pygame.quit()
    sys.exit()


def stars_generation(height, width):
    list_ = []
    for i in range(height):
        list_.append([pygame.Color('white'),
                    (random.random() * width,
                     random.random() * height * 2, 1, 1)])
    return list_


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, *group):
        super().__init__(*group)
        if x1 == x2:        # horizontal
            if x1 < 20 and x2 < 20:
                self.add(a_border)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
            elif x1 > height - 10 and x2 > height - 10:
                self.add(d_border)
                self.image = pygame.Surface([1, y2 - y1])
                self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        elif y1 == y2:       # vertical
            if y1 < 20 and y2 < 20:
                self.add(w_border)
                self.image = pygame.Surface([x2 - x1, 1])
                self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
            elif y1 > height - 10 and y2 > height - 10:
                self.add(s_border)
                self.image = pygame.Surface([x2 - x1, 1])
                self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


class Player(pygame.sprite.Sprite):
    def __init__(self, screen, *group):
        super().__init__(*group)
        self.image = load_image('airplane.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = height // 2 - 40, width // 2 - 50
        self.x, self.y = 350, 200
        self.size = 50      # for animation_appearance(screen)
        self.ammo = 5
        self.bullets = []
        self.bullets_group = pygame.sprite.Group()
        self.hp = 100
        self.keys = []
        self.freq = 0

    def update(self, *args):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_a]:
            if not pygame.sprite.spritecollideany(self, a_border) and 'a' in self.keys:
                self.keys.remove('a')
            if pygame.sprite.spritecollideany(self, a_border) and 'a' not in self.keys:
                self.keys.append('a')
            if 'a' not in self.keys:
                self.rect = self.rect.move(-fpsv, 0)

        if key_pressed[pygame.K_d]:
            if not pygame.sprite.spritecollideany(self, d_border) and 'd' in self.keys:
                self.keys.remove('d')
            if pygame.sprite.spritecollideany(self, d_border) and 'd' not in self.keys:
                self.keys.append('d')
            if 'd' not in self.keys:
                self.rect = self.rect.move(fpsv, 0)

        if key_pressed[pygame.K_w]:
            if not pygame.sprite.spritecollideany(self, w_border) and 'w' in self.keys:
                self.keys.remove('w')
            if pygame.sprite.spritecollideany(self, w_border) and 'w' not in self.keys:
                self.keys.append('w')
            if 'w' not in self.keys:
                self.rect = self.rect.move(0, -fpsv)

        if key_pressed[pygame.K_s]:
            if not pygame.sprite.spritecollideany(self, s_border) and 's' in self.keys:
                self.keys.remove('s')
            if pygame.sprite.spritecollideany(self, s_border) and 's' not in self.keys:
                self.keys.append('s')
            if 's' not in self.keys:
                self.rect = self.rect.move(0, fpsv)
        if key_pressed[pygame.K_SPACE]:
            self.freq += 1
            if self.freq % 10 == 0:
                self.shooting()

    def animation_appearance(self, screen):
        screen.fill((0, 0, 0))
        x, y = self.x, self.y
        for i in range(self.size):
            for j in range(self.size):
                pygame.draw.rect(screen, pygame.Color('red'), (x, y, 1, 1))
                x += 1
            pygame.display.flip()
            pygame.time.delay(20)
            x = self.x
            y += 1

    def shooting(self):
        b = BulletUsually()
        self.bullets_group.add(b)
        self.bullets.append(b)
        # self.bullets_group.remove(self.bullets[0])        # Если столкнулся с метеоритом
        # self.bullets.remove(self.bullets[0])

    def empty_ammo_magaz(self):
        pass

    def health_points(self):
        pygame.draw.rect(screen, pygame.Color('green'), (2, 2, self.hp, 10))
        pygame.draw.rect(screen, pygame.Color('white'), (1, 1, 102, 12), width=2)
        if self.hp <= 0:
            menu.end_screen()


class Planet(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image('Boss2.png'), (400, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.y = 450

        self.hp = 1000

    def health_points(self):
        pygame.draw.rect(screen, pygame.Color('blue'), (2, 20, self.hp // 10, 10))
        pygame.draw.rect(screen, pygame.Color('white'), (1, 19, 102, 12), width=2)
        if self.hp <= 0:
            menu.end_screen()


class BulletUsually(pygame.sprite.Sprite):
    def __init__(self, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image('Shoot1.png'), (15, 15))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y

    def update(self):
        self.rect = self.rect.move(0, -10)

    def __repr__(self):
        return 'Bullet'


class Meteor1(pygame.sprite.Sprite):
    def __init__(self, time, pos, *group):
        super().__init__()
        self.count = 0
        self.time = time
        self.image = load_image('TrueMeteor.png')
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.meteor_group = pygame.sprite.Group()
        self.meteor_group.add(self)
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.x = pos[0]
        self.y = -pos[1]
        self.rect.x = self.x
        self.rect.y = self.y
        if 0 < self.x <= 100:
            self.xn = random.randrange(-125, 500, 125) / 1000
        elif 100 < self.x <= 200:
            self.xn = random.randrange(-500, 500, 125) / 1000
        elif 200 < self.x <= 300:
            self.xn = random.randrange(-500, 500, 125) / 1000
        elif 300 < self.x <= 400:
            self.xn = random.randrange(-500, 125, 125) / 1000
        self.yn = 2
        self.pos = Vector2(pos)
        self.angle = 0
        self.hp = 10

    def update(self):
        global points
        self.angle += 2
        self.pos = self.x + self.xn, self.y + self.yn
        self.y += self.yn
        self.x += self.xn
        self.rotate()
        if pygame.sprite.collide_mask(self, planet):
            planet.hp -= 10
            meteors.remove(self)
            meteors2.remove(self)
        elif pygame.sprite.collide_mask(self, player):
            player.hp -= 12
            meteors.remove(self)
            meteors2.remove(self)
            points += 1
            print(points)
        elif pygame.sprite.spritecollideany(self, player.bullets_group):
            self.hp -= 2.5
            for i in player.bullets_group:
                intermed = pygame.sprite.Group()
                intermed.add(i)
                if pygame.sprite.spritecollideany(self, intermed):
                    player.bullets_group.remove(i)
                    player.bullets.remove(i)
            if self.hp <= 0:
                meteors2.remove(self)
                points += 1
                print(points)
        elif self.y > 650:
            meteors.remove(self)
            meteors2.remove(self)

    def rotate(self):
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        self.rect.center = self.pos

    def create_meteor(self):
        meteors.append(Meteor1(
            random.randrange(1, 400),
            (random.randrange(1, 400), random.randrange(1, 400))))


class Boss(pygame.sprite.Sprite):
    pass


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.count = 0
        self.y = 70
        self.direct = '+'

    def play_bttn(self, flag):
        theme = load_image('MainTheme.png')
        screen.blit(theme, (-50, self.y))
        if flag:
            dl1 = pygame.transform.scale(load_image('Start_Light.png'), (100, 50))
            screen.blit(dl1, (150, 200))
        else:
            dl1 = pygame.transform.scale(load_image('Start_Dark.png'), (100, 50))
            screen.blit(dl1, (150, 200))
        if self.y == 75:
            self.direct = '-'
        elif self.y == 70:
            self.direct = '+'

    def start_screen(self, stars):
        on_play_button = False
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                elif event.type == pygame.MOUSEMOTION:
                    pygame.display.set_caption(f'{event.pos[0], event.pos[1]}')
                    if (event.pos[0] > 150 and event.pos[1] > 200) and (event.pos[0] < 250 and event.pos[1] < 250):
                        on_play_button = True
                    else:
                        on_play_button = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (event.pos[0] > 150 and event.pos[1] > 200) and (event.pos[0] < 250 and event.pos[1] < 250):
                        screen.fill((0, 0, 0))
                        return Player(screen)
            screen.fill((0, 0, 0))
            if self.count == 15:
                if self.direct == '+':
                    self.y += 1
                else:
                    self.y -= 1
                self.count = 0
            self.count += 1
            for i in stars:
                screen.fill(i[0], i[1])
            self.play_bttn(on_play_button)
            pygame.display.flip()
            clock.tick(fps)

    def end_screen(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
            pygame.display.flip()


pygame.init()
size = height, width = 400, 600
screen = pygame.display.set_mode(size)
fps = 60
v = 10
fpsv = fps / v
clock = pygame.time.Clock()

menu = MainMenu(screen)
stars = stars_generation(height, width)
player = menu.start_screen(stars)
player_group = pygame.sprite.Group()
player_group.add(player)

planet = Planet()
planet_group = pygame.sprite.Group()
planet_group.add(planet)

a_border = pygame.sprite.Group()
d_border = pygame.sprite.Group()
s_border = pygame.sprite.Group()
w_border = pygame.sprite.Group()
Border(3, 3, height - 3, 3)
Border(3, width - 3, height - 3, width - 3)
Border(3, 3, 3, width - 3)
Border(height - 3, 3, height - 3, width - 3)
meteors = []
# for _ in range(10):
#     meteors.append(Meteor1(
#         random.randrange(1, 400),
#         (random.randrange(1, 400), random.randrange(1, 400))))
meteors2 = []
meteor_born = 0
points = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
    if meteor_born == 0:
        meteors.append(Meteor1(random.randrange(1, 400),
                               (random.randrange(1, 400), random.randrange(1, 400))))
    meteor_born = 0 if meteor_born == 25 else meteor_born + 1
    screen.fill((0, 0, 0))
    for i in stars:
        screen.fill(i[0], i[1])
    player_group.draw(screen)
    player_group.update()
    player.bullets_group.draw(screen)
    player.bullets_group.update()
    for i in meteors:
        i.count += 1
        if i.time == i.count:
            meteors2.append(i)
    for i in meteors2:
        i.meteor_group.draw(screen)
        i.update()
    render_points()
    player.health_points()
    planet_group.draw(screen)
    planet.health_points()
    pygame.display.set_caption(f'{clock.get_fps()}')
    pygame.display.flip()
    clock.tick(fps)
