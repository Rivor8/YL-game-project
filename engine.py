import pygame
import sys
import configparser as cfg
from settings import *


pygame.init()
screen = pygame.display.set_mode(SCREENSIZE)
pygame.display.set_caption(GAME_TITLE)
running = True
clock = pygame.time.Clock()

images = {}
levels = {}
keys = {
    'UP': False,
    'DOWN': False,
    'LEFT': False,
    'RIGHT': False
}


def load_game():
    config = cfg.ConfigParser()
    config.read('data/saves/save.ini')
    return config['GAME']['level']


def save_game(diamonds, n_level):
    config = cfg.ConfigParser()
    config.read('data/saves/save.ini')
    all_diamonds = int(config['GAME']['diamonds']) + diamonds
    config['GAME']['diamonds'] = str(all_diamonds)
    config['GAME']['level'] = n_level
    with open('data/saves/save.ini', 'w') as cfgfile:
        config.write(cfgfile)


loaded_level = load_game()


def text_screen(text):
    font = pygame.font.Font('data/fonts/YesevaOne-Regular.ttf', 31)
    intro_text = font.render(text, 1, (255, 255, 255))
    place = intro_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.fill((0, 0, 0))
        screen.blit(intro_text, place)
        pygame.display.flip()
        clock.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/levels/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, 'q'), level_map))


def start_level(level):
    global loaded_level
    for el in all_sprites.sprites():
        el.kill()
    for el, val in keys.items():
        keys[el] = False
    loaded_level = level
    generate_level(load_level(level))


def next_level():
    global loaded_level
    if loaded_level == 'level9.txt':
        config = cfg.ConfigParser()
        config.read('data/saves/save.ini')
        if int(config['GAME']['diamonds']) >= 91:
            return LEVEL_LIST[LEVEL_LIST.index(loaded_level) + 2]
        else:
            return LEVEL_LIST[LEVEL_LIST.index(loaded_level) + 1]
    else:
        return LEVEL_LIST[LEVEL_LIST.index(loaded_level) + 1]


def this_level():
    global loaded_level
    return LEVEL_LIST[LEVEL_LIST.index(loaded_level)]


def next_phrase():
    loaded_phrase = PHRASES[LEVEL_LIST.index(loaded_level) + 1]
    return loaded_phrase


def this_phrase():
    loaded_phrase = PHRASES[LEVEL_LIST.index(loaded_level)]
    return loaded_phrase


from game_objects import StaticTile, Player, SolidTile, Entity, LavaTile, Box, WallDoor, Enemy,\
    all_sprites, tiles_group, player_group, walls_group, box_group, entity_group, dynamic_walls_group, enemy_group


def load_image(name, tile=False):
    fullname = "data/images/" + name
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    if tile:
        image = pygame.transform.scale(image, (TILE_WIDTH, TILE_HEIGHT))
    images[name.split('.')[0]] = image
    return image


def generate_level(level):
    global loaded_level
    if loaded_level == 'level_dark.txt':
        pygame.mixer.music.load('data/music/dark.mp3')
        pygame.mixer.music.play(-1)
    elif loaded_level == 'level_light.txt':
        pygame.mixer.music.load('data/music/light.mp3')
        pygame.mixer.music.play(-1)
    for y in range(len(level)):
        for x in range(len(level[y])):
            # Base
            if level[y][x] == '@':
                if loaded_level == 'level_light.txt':
                    StaticTile('light_floor', x, y)
                    Player(x, y)
                else:
                    StaticTile('floor', x, y)
                    Player(x, y)

            if level[y][x] == '#':
                SolidTile('wall', x, y)

            if level[y][x] == '.':
                StaticTile('floor', x, y)

            if level[y][x] == 'q':
                StaticTile('floor_black', x, y)

            if level[y][x] == ',':
                StaticTile('light_floor', x, y)

            # Special
            if level[y][x] == 'b':
                StaticTile('floor', x, y)
                Box('box', x, y)

            if level[y][x] == 'l':
                LavaTile('lava0', x, y)

            # Entity
            if level[y][x] == 'z':
                if loaded_level == 'level_light.txt':
                    StaticTile('light_floor', x, y)
                    Entity('diamond', x, y, 'diamond')
                else:
                    StaticTile('floor', x, y)
                    Entity('diamond', x, y, 'diamond')

            if level[y][x] == 'd':
                StaticTile('floor', x, y)
                Entity('closed_door', x, y, 'door')

            if level[y][x] == 'k':
                StaticTile('floor', x, y)
                Entity('key', x, y, 'key')

            # Enemy
            if level[y][x] == 'm':
                StaticTile('floor', x, y)
                Enemy(1, x, y)

            if level[y][x] == 'M':
                StaticTile('floor', x, y)
                Enemy(2, x, y)

            # Wall doors
            if level[y][x] == '5':
                StaticTile('floor', x, y)
                Entity('button', x, y, 'button', key=0)

            if level[y][x] == '6':
                StaticTile('floor', x, y)
                Entity('button', x, y, 'button', key=1)

            if level[y][x] == '7':
                StaticTile('floor', x, y)
                Entity('button', x, y, 'button', key=2)

            if level[y][x] == '8':
                StaticTile('floor', x, y)
                Entity('button', x, y, 'button', key=3)

            if level[y][x] == '9':
                StaticTile('floor', x, y)
                Entity('button', x, y, 'button', key=4)

            if level[y][x] == '0':
                StaticTile('floor', x, y)
                WallDoor(x, y, 0)

            if level[y][x] == '1':
                StaticTile('floor', x, y)
                WallDoor(x, y, 1)

            if level[y][x] == '2':
                StaticTile('floor', x, y)
                WallDoor(x, y, 2)

            if level[y][x] == '3':
                StaticTile('floor', x, y)
                WallDoor(x, y, 3)

            if level[y][x] == '4':
                StaticTile('floor', x, y)
                WallDoor(x, y, 4)

            # End
            if level[y][x] == 'c':
                StaticTile('floor', x, y)
                Entity('strange_circle', x, y, 'strange_circle')

            if level[y][x] == 'C':
                StaticTile('light_floor', x, y)
                Entity('light_circle', x, y, 'light_circle')

            if level[y][x] == 'p':
                StaticTile('light_floor', x, y)
                SolidTile('wall_door_l1', x, y)

            if level[y][x] == 'P':
                StaticTile('light_floor', x, y)
                SolidTile('wall_door_l2', x, y)

            if level[y][x] == 'u':
                StaticTile('light_floor', x, y)
                SolidTile('corner1', x, y)

            if level[y][x] == 'U':
                StaticTile('light_floor', x, y)
                SolidTile('corner2', x, y)

            if level[y][x] == 'I':
                StaticTile('light_floor', x, y)
                SolidTile('corner3', x, y)

            if level[y][x] == 'i':
                StaticTile('light_floor', x, y)
                SolidTile('corner4', x, y)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x -= self.dx
        obj.rect.y -= self.dy

    def update(self, target):
        self.dx = target.rect.x - WIDTH // 2
        self.dy = target.rect.y - HEIGHT // 2
