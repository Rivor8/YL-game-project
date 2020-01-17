from engine import *


all_sprites = pygame.sprite.Group()

tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
entity_group = pygame.sprite.Group()
dynamic_walls_group = pygame.sprite.Group()


class LavaTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        self.frame = 0
        self.tick = 0

    def update(self):
        if self.tick < 60:
            self.tick += 1
        else:
            self.tick = 0
        if self.tick % 10 == 0:
            if self.frame < 7:
                self.frame += 1
            else:
                self.frame = 0
        self.image = images[f'lava{self.frame}']
        if pygame.sprite.spritecollideany(self, player_group):
            player_group.sprites()[0].dead()


class StaticTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class SolidTile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)


class WallDoor(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, num):
        super().__init__(dynamic_walls_group, all_sprites)
        self.image = images['wall_door']
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        self.num = num
        self.state = True
        self.col = False

    def update(self):
        if player_group.sprites()[0].buttons[self.num] == 1:
            self.image = images['floor']
            self.state = False
            if self in dynamic_walls_group.sprites():
                player_group.sprites()[0].wall_door[dynamic_walls_group.sprites().index(self)] = 0
        else:
            self.image = images['wall_door']
            self.state = True
            if self in dynamic_walls_group.sprites():
                player_group.sprites()[0].wall_door[dynamic_walls_group.sprites().index(self)] = 1
        self.col = pygame.sprite.spritecollideany(self, player_group)


class Box(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(box_group, all_sprites)
        self.image = images[tile_type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        self.prevPos = self.rect

    def update(self):
        self.prevPos = self.rect
        if pygame.sprite.spritecollideany(self, player_group):
            if not pygame.sprite.spritecollideany(self, walls_group):
                self.rect = self.image.get_rect().move(self.rect.x + player_group.sprites()[0].speed[0],
                                                       self.rect.y + player_group.sprites()[0].speed[1])
        if pygame.sprite.spritecollideany(self, walls_group):
            if self in box_group.sprites():
                player_group.sprites()[0].stop[box_group.sprites().index(self)] = 1
            self.rect = self.prevPos
        else:
            if self in box_group.sprites():
                player_group.sprites()[0].stop[box_group.sprites().index(self)] = 0


class Entity(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, type, key=0):
        super().__init__(entity_group, all_sprites)
        self.image = images[tile_type]
        self.type = type
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x, TILE_HEIGHT * pos_y)
        self.state = 0
        self.key = key

    def update(self):
        if self.type == 'door':
            if player_group.sprites()[0].key == 1:
                self.image = images['opened_door']
        if pygame.sprite.spritecollideany(self, player_group):
            if self.type == 'diamond':
                player_group.sprites()[0].diamonds += 1
                self.kill()
            elif self.type == 'door':
                if player_group.sprites()[0].key == 1:
                    save_game(player_group.sprites()[0].diamonds, next_level())
                    text_screen(next_phrase())
                    start_level(next_level())
            elif self.type == 'key':
                player_group.sprites()[0].key = 1
                self.kill()
        if pygame.sprite.spritecollideany(self, player_group) or pygame.sprite.spritecollideany(self, box_group):
            if self.type == 'button':
                player_group.sprites()[0].buttons[self.key] = 1
        else:
            if self.type == 'button':
                player_group.sprites()[0].buttons[self.key] = 0


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = pygame.transform.scale(images['p1'], (TILE_WIDTH - 7, TILE_HEIGHT - 7))
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x + 15, TILE_HEIGHT * pos_y + 5)
        self.speed = [0, 0]
        self.max_speed = 2
        self.prevPos = self.rect

        self.diamonds = 0
        self.key = 0

        self.stop = [0 for _ in range(100)]
        self.wall_door = [0 for _ in range(900)]
        self.buttons = [0 for _ in range(4)]

    def dead(self):
        text_screen('СМЭЭЭРТЬ')
        start_level(this_level())

    def wall_door_col(self):
        for el in dynamic_walls_group.sprites():
            if el.col and self.wall_door[dynamic_walls_group.sprites().index(el)] == 1:
                return 1
        return 0

    def update(self):
        self.prevPos = self.rect
        if keys['UP']:
            self.image = pygame.transform.scale(images['p4'], (TILE_WIDTH - 7, TILE_HEIGHT - 7))
            self.speed[1] = -self.max_speed
        elif keys['DOWN']:
            self.image = pygame.transform.scale(images['p1'], (TILE_WIDTH - 7, TILE_HEIGHT - 7))
            self.speed[1] = self.max_speed
        else:
            self.speed[1] = 0
            self.image = pygame.transform.scale(images['p1'], (TILE_WIDTH - 7, TILE_HEIGHT - 7))
        if keys['LEFT']:
            self.image = pygame.transform.scale(images['p2'], (TILE_WIDTH - 7, TILE_HEIGHT - 7))
            self.speed[0] = -self.max_speed
        elif keys['RIGHT']:
            self.image = pygame.transform.scale(images['p3'], (TILE_WIDTH - 7, TILE_HEIGHT - 7))
            self.speed[0] = self.max_speed
        else:
            self.speed[0] = 0
        self.rect = self.image.get_rect().move(self.rect.x + self.speed[0], self.rect.y + self.speed[1])
        if pygame.sprite.spritecollideany(self, walls_group) or (1 in self.stop) or \
                (pygame.sprite.spritecollideany(self, dynamic_walls_group) and self.wall_door_col()):
            self.rect = self.prevPos
