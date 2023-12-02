import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score = score_font.render(f"score:  {current_time}", False, 'Orange')
    score_rectangle = score.get_rect(center=(675, 100))
    screen.blit(score, score_rectangle)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= randint(11, 19)
            if obstacle_rect.midbottom[1] == 370:
                screen.blit(kunai, obstacle_rect)
            else:
                screen.blit(shuriken, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles, player_mask, obstacle_masks):
    player_mask_offset = (player.x - naruto_rectangle.x, player.y - naruto_rectangle.y)

    if obstacles:
        for i, obstacle_rect in enumerate(obstacles):
            obstacle_mask = obstacle_masks[i]
            offset = (obstacle_rect.x - naruto_rectangle.x, obstacle_rect.y - naruto_rectangle.y)

            if player_mask.overlap(obstacle_mask, offset):
                return False
    return True

def naruto_animation():
    global naruto, naruto_index

    if naruto_rectangle.bottom < 438:
        naruto = naruto_jump
    else:
        naruto_index += 0.2
        if naruto_index >= len(naruto_run):
            naruto_index = 0
        naruto = naruto_run[int(naruto_index)]

pygame.init()
screen = pygame.display.set_mode((1350, 480))
pygame.display.set_caption('shippuden')
clock = pygame.time.Clock()
background_surface = pygame.image.load('graphics/forest_background.png').convert_alpha()
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)
start_time = 0
background_music = pygame.mixer.Sound('audio/music.mp3')
background_music.play(loops = -1)


game_name = score_font.render('shippuden', False, 'Orange')
game_name_rectangle = game_name.get_rect(center=(680, 55))
game_message = score_font.render("press space to start", False, 'Orange')
game_message_rectangle = game_message.get_rect(center=(680, 434))
game_running = False

# obstacles
kunai = pygame.image.load('graphics/kunai.png').convert_alpha()
kunai = pygame.transform.scale(kunai, (90, 23))
kunai_mask = pygame.mask.from_surface(kunai)

shuriken1 = pygame.image.load('graphics/shuriken1.png').convert_alpha()
shuriken1 = pygame.transform.scale(shuriken1, (45, 45))
shuriken2 = pygame.image.load('graphics/shuriken2.png').convert_alpha()
shuriken2 = pygame.transform.scale(shuriken2, (45, 45))
shuriken_frames = [shuriken1, shuriken2]
shuriken_frame_index = 0
shuriken = shuriken_frames[shuriken_frame_index]

shuriken_mask = pygame.mask.from_surface(shuriken)

obstacle_rect_list = []

naruto1 = pygame.image.load('graphics/naruto1.png').convert_alpha()
naruto1 = pygame.transform.scale(naruto1, (210, 297))
naruto2 = pygame.image.load('graphics/naruto2.png').convert_alpha()
naruto2 = pygame.transform.scale(naruto2, (210, 297))
naruto3 = pygame.image.load('graphics/naruto3.png').convert_alpha()
naruto3 = pygame.transform.scale(naruto3, (210, 297))
naruto4 = pygame.image.load('graphics/naruto4.png').convert_alpha()
naruto4 = pygame.transform.scale(naruto4, (210, 297))

naruto_run = [naruto1, naruto2, naruto3, naruto4]
naruto_index = 0
naruto_jump = pygame.image.load('graphics/naruto1.png').convert_alpha()
naruto_jump = pygame.transform.scale(naruto_jump, (210, 297))

naruto = naruto_run[naruto_index]
naruto_rectangle = naruto.get_rect(midbottom=(175, 438))
naruto_mask = pygame.mask.from_surface(naruto)
naruto_gravity = 0

naruto_head = pygame.image.load('graphics/naruto_head.png').convert_alpha()
naruto_head = pygame.transform.scale(naruto_head, (290, 295))
naruto_head_rectangle = naruto_head.get_rect(center=(675, 240))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
shuriken_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(shuriken_animation_timer, 500)

while True:
    mouse_position = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_running:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if naruto_rectangle.collidepoint(event.pos) and naruto_rectangle.bottom >= 438:
                    naruto_gravity = -21
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and naruto_rectangle.bottom >= 438:
                    naruto_gravity = -21
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_running = True
                start_time = int(pygame.time.get_ticks()/1000)
        if game_running:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(kunai.get_rect(midbottom=(randint(1450, 1800), 370)))
                else:
                    obstacle_rect_list.append(shuriken.get_rect(midbottom=(randint(1450, 1800), 250)))
            if event.type == shuriken_animation_timer:
                shuriken_frame_index = (shuriken_frame_index + 1) % len(shuriken_frames)

    if game_running:
        screen.blit(background_surface, (0, 0))

        current_time = display_score()

        # player(naruto)
        naruto_gravity += 1
        naruto_rectangle.y += naruto_gravity
        if naruto_rectangle.bottom >= 438:
            naruto_rectangle.bottom = 438
        naruto_animation()
        screen.blit(naruto, naruto_rectangle)
        # obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        # Update shuriken animation
        shuriken = shuriken_frames[shuriken_frame_index]
        # collision
        game_running = collisions(
            naruto_rectangle, obstacle_rect_list,
            naruto_mask, [kunai_mask, shuriken_mask]
        )

        if current_time != 0:
            game_message = score_font.render(f"latest score: {current_time}", False, 'Orange')
            game_message_rectangle = game_message.get_rect(center=(680, 434))

    else:
        screen.fill((23, 23, 40))
        screen.blit(game_name, game_name_rectangle)
        screen.blit(naruto_head, naruto_head_rectangle)
        screen.blit(game_message, game_message_rectangle)
        obstacle_rect_list.clear()
        naruto_rectangle.midbottom = (175, 438)
        player_gravity = 0
    pygame.display.update()
    clock.tick(60)
