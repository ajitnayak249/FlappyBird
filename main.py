from enum import Flag
from json.tool import main

import random #for generateing random number
import sys
from turtle import Screen # we will ise sys.exit tp exit the programe
import pygame
from pygame.locals import * #basic pygame import

#global varibale for the game

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511 
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUND = {}
PLAYER = 'gallary/sprites/bird.png'
BACKGROUND = 'gallary/sprites/background.png'
PIPE = 'gallary/sprites/pipe.png'


def welcomeScreen():
    '''
    show welcome screen 
    '''
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT- GAME_SPRITES['player'].get_height())/3)
    messagex = int((SCREENWIDTH- GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex =0
    while True:
        for event in pygame.event.get():
            #if user clicks on cross button, close the game 
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

                #if the user presses space or up key start the game for them
            elif event.type == KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(messagex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0

    # create 2 pipes for blitting on screen
    newPipe1 = getrandomPipe()
    newPipe2 = getrandomPipe()

    # my liset of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[0]['y']},
    ]

    # my list of lower pipes
    lowerPipes= [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH/2), 'y': newPipe2[1]['y']},
    ]

    pipeVelx = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8   # velocity while flapping
    playerFlapped = False   #it is true only when the bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event .key == K_UP): 
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUND['wing'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)

        if crashTest:
            return

        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"your score is {score}")
                GAME_SOUND['point'].play()






        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)


        #move pipes to the left
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x']  += pipeVelx

        #add a new pipe hen the first is about to cross the lefgt part of the system 

        if 0<upperPipes[0]['x']<5:
            newpipe = getrandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])     


        # if the pipes is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        # LETS BLITS OUR SPRITES NOW 

        SCREEN.blit(GAME_SPRITES['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))



            
        SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx, playery))

        myDigits = [int(x) for x in list(str(score))] 
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['number'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2


        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['number'][digit],(Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['number'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)            


def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25 or playery <0:
        GAME_SOUND['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUND['hit'].play()
            return True

    for pipe in lowerPipes:
        if(playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUND['hit'].play()
            return True

    return False




def getrandomPipe():
    """ Generate position of two pipes(one bottom straight and one rotated) for blitting on the screen """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT -  GAME_SPRITES['base'].get_height() - 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2 }
    ]
    return pipe



if __name__ == "__main__":
    #this will be th main point from wwher our game will start
    pygame.init() #initilize all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('flappy bird')
    GAME_SPRITES['number'] = (
        pygame.image.load('gallary/sprites/0.png').convert_alpha(),
        pygame.image.load('gallary/sprites/1.png').convert_alpha(),
        pygame.image.load('gallary/sprites/2.png').convert_alpha(),
        pygame.image.load('gallary/sprites/3.png').convert_alpha(),
        pygame.image.load('gallary/sprites/4.png').convert_alpha(),
        pygame.image.load('gallary/sprites/5.png').convert_alpha(),
        pygame.image.load('gallary/sprites/6.png').convert_alpha(),
        pygame.image.load('gallary/sprites/7.png').convert_alpha(),
        pygame.image.load('gallary/sprites/8.png').convert_alpha(),
        pygame.image.load('gallary/sprites/9.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('gallary/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallary/sprites/base.png').convert_alpha()  
    GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha()
    )

    #GAME SOUND
    GAME_SOUND['die'] = pygame.mixer.Sound('gallary/Audio/die.wav')
    GAME_SOUND['hit'] = pygame.mixer.Sound('gallary/Audio/hit.wav')
    GAME_SOUND['point'] = pygame.mixer.Sound('gallary/Audio/point.wav')
    GAME_SOUND['wing'] = pygame.mixer.Sound('gallary/Audio/wing.wav')
    GAME_SOUND['swoosh'] = pygame.mixer.Sound('gallary/Audio/swoosh.wav')

    GAME_SPRITES['background']= pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert()

    while True:
        welcomeScreen() #shows welcome screen to the user until he presses a button 
        mainGame() #This is the main game function


