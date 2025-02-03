import random 
import sys 
import pygame
from pygame.locals import *


FPS = 60  # Increased FPS for smoother gameplay
SCREENWIDTH = 1000
SCREENHEIGHT = 1000
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER1 = 'C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/bird1.png'
PLAYER2 = 'C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/bird2.png'
BACKGROUND = 'C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/background.jpg'
PIPE = 'C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/pipe.png'


def welcomeScreen():
    """Shows welcome screen"""
    playerx = int(SCREENWIDTH / 5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player1'].get_height()) / 2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.13)
    basex = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player1'], (playerx, playery))
                SCREEN.blit(GAME_SPRITES['message'], (messagex, messagey))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    """Handles the main game logic"""
    score1, score2 = 0, 0
    player1x = int(SCREENWIDTH / 5 + 200)
    player1y = int(SCREENWIDTH / 2)
    player2x = int(SCREENWIDTH / 5)
    player2y = int(SCREENWIDTH / 2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [{'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']}, {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[0]['y']}]
    lowerPipes = [{'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']}, {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']}]

    pipeVelX = -4

    playerMaxVelY = 10
    playerAccY = 1
    playerFlapAccv = -8

    player1VelY = -9
    player1Flapped = False

    player2VelY = -9
    player2Flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player1y > 0:
                    player1VelY = playerFlapAccv
                    player1Flapped = True

            if event.type == KEYDOWN and (event.key == K_w):
                if player2y > 0:
                    player2VelY = playerFlapAccv
                    player2Flapped = True

        crashTest1 = isCollide(player1x, player1y, upperPipes, lowerPipes)
        crashTest2 = isCollide(player2x, player2y, upperPipes, lowerPipes)
        if crashTest1 or crashTest2:
            if gameOverScreen(score1, score2):  # Game over screen and restart
                return

        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() / 2

            if pipeMidPos <= player1x < pipeMidPos + 4:
                score1 += 1
                print(f"Player 1 Score: {score1}")
                GAME_SOUNDS['point'].play()

            if pipeMidPos <= player2x < pipeMidPos + 4:
                score2 += 1
                print(f"Player 2 Score: {score2}")
                GAME_SOUNDS['point'].play()

        if player1VelY < playerMaxVelY and not player1Flapped:
            player1VelY += playerAccY
        if player1Flapped:
            player1Flapped = False
        player1y = player1y + min(player1VelY, GROUNDY - player1y - GAME_SPRITES['player1'].get_height())

        if player2VelY < playerMaxVelY and not player2Flapped:
            player2VelY += playerAccY
        if player2Flapped:
            player2Flapped = False
        player2y = player2y + min(player2VelY, GROUNDY - player2y - GAME_SPRITES['player2'].get_height())

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player1'], (player1x, player1y))
        SCREEN.blit(GAME_SPRITES['player2'], (player2x, player2y))

        myDigits1 = [int(x) for x in list(str(score1))]
        width1 = sum(GAME_SPRITES['numbers'][digit].get_width() for digit in myDigits1)
        Xoffset1 = (SCREENWIDTH - width1) / 2

        for digit in myDigits1:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset1, SCREENHEIGHT * 0.12))
            Xoffset1 += GAME_SPRITES['numbers'][digit].get_width()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(playerx, playery, upperPipes, lowerPipes):
    """Checks for collisions"""
    if playery >= GROUNDY - 25 or playery < 0:
        GAME_SOUNDS['hit'].play()
        return True

    bird_width = GAME_SPRITES['player1'].get_width()
    bird_height = GAME_SPRITES['player1'].get_height()
    pipe_width = GAME_SPRITES['pipe'][0].get_width()

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if (playery < pipeHeight + pipe['y'] and
            playerx + bird_width > pipe['x'] and
            playerx < pipe['x'] + pipe_width):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + bird_height > pipe['y'] and
            playerx + bird_width > pipe['x'] and
            playerx < pipe['x'] + pipe_width):
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    """Generates random pipe positions"""
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT / 3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [{'x': pipeX, 'y': -y1}, {'x': pipeX, 'y': y2}]
    return pipe


if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Multiplayer')

    # Load images and sounds
    GAME_SPRITES['numbers'] = (
        pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/0.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/1.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/2.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/3.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/4.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/5.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/6.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/7.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/8.png').convert_alpha(),
        pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/PNG/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    GAME_SOUNDS['die'] = pygame.mixer.Sound('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/Sounds/die.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/Sounds/hit.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/Sounds/point.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('C:/Users/sagar/Desktop/Codes/FLAPPYBIRD/Sounds/swoosh.mp3')

    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player1'] = pygame.image.load(PLAYER1).convert_alpha()
    GAME_SPRITES['player2'] = pygame.image.load(PLAYER2).convert_alpha()

    while True:
        welcomeScreen()
        mainGame()
