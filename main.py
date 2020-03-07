import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('back.png')



# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemy4Img = []
enemy4X = []
enemy4Y = []
enemy4X_change = []
enemy4Y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy4Img.append(pygame.image.load('enemy4.png'))
    enemy4X.append(random.randint(0, 735))
    enemy4Y.append(random.randint(50, 150))
    enemy4X_change.append(6)
    enemy4Y_change.append(40)

# Fire

# ready - you can't see the bullet on the screen
# fire - bullet is currently moving
fireImg = pygame.image.load('fire.png')
fireX = 0
fireY = 480
fireX_change = 0
fireY_change = 10
fire_state = "ready"

# Score

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER!", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy4(x, y, i):
    screen.blit(enemy4Img[i], (x, y))


def fire_fire(x, y):
    global fire_state
    fire_state = "fire"
    screen.blit(fireImg, (x + 16, y + 10))


# is_collision
def isCollision(enemy4X, enemy4Y, fireX, fireY):
    distance = math.sqrt((math.pow(enemy4X - fireX, 2)) + (math.pow(enemy4Y - fireY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:

    # RGB red, green, blue
    screen.fill((0, 0, 0))

    # background
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If key stroke is pressed check weather its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -6
            if event.key == pygame.K_RIGHT:
                playerX_change = 6
            if event.key == pygame.K_SPACE:
                if fire_state is "ready":
                    fire_Sound = mixer.Sound('laser.wav')
                    fire_Sound.play()
                    fireX = playerX
                    fire_fire(fireX, fireY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking for boundaries of spaceship
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemy4Y[i] > 440:
            for j in range(num_of_enemies):
                enemy4Y[j] = 2000
            game_over_text()
            break




        enemy4X[i] += enemy4X_change[i]

        if enemy4X[i] <= 0:
            enemy4X_change[i] = 6
            enemy4Y[i] += enemy4Y_change[i]
        elif enemy4X[i] >= 736:
            enemy4X_change[i] = -6
            enemy4Y[i] += enemy4Y_change[i]

        # Collision
        collision = isCollision(enemy4X[i], enemy4Y[i], fireX, fireY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            fireY = 480
            fire_state = "ready"
            score_value += 1

            enemy4X[i] = random.randint(0, 735)
            enemy4Y[i] = random.randint(50, 150)

        enemy4(enemy4X[i], enemy4Y[i], i)

    # Bullet movement
    if fireY <= 0:
        fireY = 480
        fire_state = "ready"

    if fire_state is "fire":
        fire_fire(fireX, fireY)
        fireY -= fireY_change



    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
