from engine import *


load_image('box.png', tile=True)
load_image('wall_door.png', tile=True)
load_image('key.png', tile=True)
load_image('button.png', tile=True)
load_image('box.png', tile=True)
load_image('wall.png', tile=True)
load_image('closed_door.png', tile=True)
load_image('opened_door.png', tile=True)
load_image('diamond.png', tile=True)
load_image('ice.png', tile=True)
load_image('floor.png', tile=True)
load_image('floor_black.png', tile=True)
load_image('lava0.png', tile=True)
load_image('lava1.png', tile=True)
load_image('lava2.png', tile=True)
load_image('lava3.png', tile=True)
load_image('lava4.png', tile=True)
load_image('lava5.png', tile=True)
load_image('lava6.png', tile=True)
load_image('lava7.png', tile=True)
load_image('p1.png', tile=True)
load_image('p2.png', tile=True)
load_image('p3.png', tile=True)
load_image('p4.png', tile=True)
load_image('bad_dark_ghost1.png', tile=True)
load_image('bad_dark_ghost2.png', tile=True)
load_image('bad_dark_ghost3.png', tile=True)
load_image('bad_dark_ghost4.png', tile=True)
load_image('strange_circle.png', tile=True)
load_image('light_floor.png', tile=True)
load_image('light_circle.png', tile=True)
load_image('wall_door_l2.png', tile=True)
load_image('corner.png', tile=True)

pygame.mixer.music.load('data/music/back.mp3')
pygame.mixer.music.play(-1)

text_screen(this_phrase())
start_level(load_game())
camera = Camera()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                keys['UP'] = True
            if event.key == pygame.K_s:
                keys['DOWN'] = True
            if event.key == pygame.K_a:
                keys['LEFT'] = True
            if event.key == pygame.K_d:
                keys['RIGHT'] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keys['UP'] = False
            if event.key == pygame.K_s:
                keys['DOWN'] = False
            if event.key == pygame.K_a:
                keys['LEFT'] = False
            if event.key == pygame.K_d:
                keys['RIGHT'] = False

    screen.fill((0, 0, 0))
    tiles_group.draw(screen)
    walls_group.draw(screen)
    entity_group.draw(screen)
    dynamic_walls_group.draw(screen)
    box_group.draw(screen)
    enemy_group.draw(screen)
    player_group.draw(screen)
    all_sprites.update()
    camera.update(player_group.sprites()[0])
    for sprite in all_sprites:
        camera.apply(sprite)
    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
