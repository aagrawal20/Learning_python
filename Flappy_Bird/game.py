import pygame
import time
import random

black = (0, 0, 0)
white = (255, 255, 255)

pygame.init()

surfaceWidth = 1200
surfaceHeight = 500
surface = pygame.display.set_mode((surfaceWidth, surfaceHeight))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

img = pygame.transform.scale(pygame.image.load('bird.png'), (40, 40))
imgSize = img.get_size()


def blocks(x_block, y_block, block_width, block_height, gap):
    pygame.draw.rect(surface, white, [x_block, y_block, block_width, block_height])
    pygame.draw.rect(surface, white, [x_block, y_block + block_height + gap, block_width, block_height])


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
    text_surface = font.render(text, True, white)
    return text_surface, text_surface.get_rect()


def msg_surface(text):
    # define texts
    small_text = pygame.font.Font('freesansbold.ttf', 20)
    large_text = pygame.font.Font('freesansbold.ttf', 150)

    # where the text should exist in the screen
    title_text_surface, title_text_rectangle = make_text_objects(text, large_text)
    title_text_rectangle.center = surfaceWidth/2, surfaceHeight/2
    surface.blit(title_text_surface, title_text_rectangle)

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
def gameOver():
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
    block_height = random.randint(0, (surfaceWidth/2))
    gap = imgSize[1] * 3
    block_move = 3

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    y_move = 5

        y += y_move

        surface.fill(black)
        flappy_bird(x, y, img)

        blocks(x_block, y_block, block_width, block_height, gap)
        x_block -= block_move

        if y > surfaceHeight-40 or y < -5:
            gameOver()

        if x_block < (-1 * block_width):
            x_block = surfaceWidth
            block_height = random.randint(0, (surfaceWidth/2))

        pygame.display.update()
        clock.tick(1000)


main()
pygame.quit()
quit()
