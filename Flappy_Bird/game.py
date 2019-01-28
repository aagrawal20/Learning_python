import pygame
import time
import random

black = (0, 0, 0)
white = (255, 255, 255)
light_blue = (173, 216, 230)
green = (34, 139, 34)
sunset = (253, 72, 47)
green_yellow = (76, 153, 0)
bright_blue = (47, 228, 253)
dull_green = (0, 102, 0)
dark_green = (0, 51, 0)
really_green = (0, 153, 0)

color_choices = [green_yellow, green, dull_green, dark_green, really_green]

pygame.init()

total_score = 0
surfaceWidth = 800
surfaceHeight = 500
surface = pygame.display.set_mode((surfaceWidth, surfaceHeight))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

img = pygame.transform.scale(pygame.image.load('bird.png'), (40, 40))
background_image = pygame.image.load("background.jpg").convert()
pygame.display.set_icon(pygame.image.load('bird.png'))
imgSize = img.get_size()


def score(count):
    font = pygame.font.Font('./font/Flappy-Bird.ttf', 50)
    text = font.render("Score:" + str(count), True, sunset)
    surface.blit(text, [0, 0])


def blocks(x_block, y_block, block_width, block_height, gap, color_choice):
    pygame.draw.rect(surface, color_choice, [x_block, y_block, block_width, block_height])
    pygame.draw.rect(surface, color_choice, [x_block, y_block + block_height + gap, block_width, surfaceHeight])


def replay_or_quit():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        elif event.type == pygame.KEYDOWN:
            continue

        return event.key

    return None


def make_text_objects(text, font):
    text_surface = font.render(text, True, sunset)
    return text_surface, text_surface.get_rect()


def msg_surface(text):
    surface.blit(background_image, [0, 0])
    # define texts
    small_text = pygame.font.Font('./font/Flappy-Bird.ttf', 60)
    large_text = pygame.font.Font('./font/Flappy-Bird.ttf', 150)

    # where the text should exist in the screen
    title_text_surface, title_text_rectangle = make_text_objects(text, large_text)
    title_text_rectangle.center = surfaceWidth/2, ((surfaceHeight/2) - 100)
    surface.blit(title_text_surface, title_text_rectangle)

    score_text_surface, score_text_rectangle = make_text_objects('Score:' + str(total_score), small_text)
    score_text_rectangle.center = surfaceWidth / 2, (surfaceHeight / 2)
    surface.blit(score_text_surface, score_text_rectangle)

    typ_text_surface, typ_text_rectangle = make_text_objects('Press any key to continue', small_text)
    typ_text_rectangle.center = surfaceWidth/2, ((surfaceHeight/2) + 100)
    surface.blit(typ_text_surface, typ_text_rectangle)

    pygame.display.update()
    time.sleep(1)

    # wait for player response
    while replay_or_quit() is None:
        clock.tick()

    main()


# after crash actions
def game_over():
    msg_surface('Crash Alert!')


# put the bird on the screen
def flappy_bird(x, y, image):
    surface.blit(image, (x, y))


# Game starts here
def main():
    x = 150
    y = 200
    y_move = 0

    x_block = surfaceWidth
    y_block = 0

    block_width = 75
    block_height = random.randint(0, int(surfaceHeight / 2))
    gap = imgSize[1] * 3
    block_move = 3

    current_score = 0

    block_color = color_choices[random.randrange(0, len(color_choices))]

    is_game_over = False

    while not is_game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -3

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = 3

        y += y_move

        surface.blit(background_image, [0, 0])
        # surface.fill(light_blue)
        flappy_bird(x, y, img)

        blocks(x_block, y_block, block_width, block_height, gap, block_color)
        score(current_score)
        x_block -= block_move

        if y > surfaceHeight-40 or y < -5:
            game_over()

        # generate continuous blocks
        if x_block < (-1 * block_width):
            x_block = surfaceWidth
            block_height = random.randint(0, (surfaceHeight/2))
            block_color = color_choices[random.randrange(0, len(color_choices))]

        # obstacle logic for the upper block
        if x + imgSize[0] > x_block:
            if x < x_block + block_width:
                if y < block_height:
                    if x - imgSize[0] < block_width + x_block:
                        game_over()

        # obstacle logic for the lower block
        if x + imgSize[0] > x_block:
            if y + imgSize[1] > block_height + gap:
                if x < block_width + x_block:
                    game_over()

        if x_block < (x - block_width) < x_block + block_move:
            current_score += 1
        
        global total_score
        total_score = current_score
        pygame.display.update()
        clock.tick(100)


main()
pygame.quit()
quit()
