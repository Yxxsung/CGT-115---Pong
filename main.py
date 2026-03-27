#Sophia Alexander
#Pong Assignment
#Last Updated: 03/26/26

#To Turn this into pong, I need to make it two player by adding a paddle at the top
#That is controlled by different keys (a and d) and make it so whoever fails loses
#Also make it so the score is based off paddle hits and has two counters
#one for each player

import random
import pygame
import pymunk

#constants and globals
#I changed the speed of PADDLEMOVE to 1.5 (previously 0.5) to speed up the movement
PADDLEMOVE = 1.5
#I changed the start speed from 30 to 15 to make the ball easier to follow
STARTSPEED = 15
score1 = 0
score2 = 0
done = False

#collision stuff
COLLTYPE_TOP = 1  #The collision for the top needs to be made into a loss barrier
COLLTYPE_BOTTOM = 2 #Already a loss barrier
COLLTYPE_BALL = 3
COLLTYPE_PADDLE = 4

def reset_ball():
    ballBody.position = (400,300)
    ballBody.velocity = (0,0)

    impulse = (
        random.randint(-STARTSPEED, STARTSPEED),
        random.randint(-STARTSPEED, STARTSPEED)
    )

    ballBody.apply_impulse_at_local_point(impulse)

#These two def sections make the top and bottom colliders lose barriers
def collide_top(space, arbiter, data):
    global score1
    score1 +=1 #adds one to the bottom player's score
    reset_ball() #resets the ball for continuous play
    return False

def collide_bottom(space, arbiter, data):
    global score2
    score2 +=1 #Adds one to the top player's score
    reset_ball()
    return False


#paddle mover
def MovePaddle(body, shape, left, right):
    deltaX = 0
    pos = body.position
    if left:
        deltaX = deltaX - PADDLEMOVE
    if right:
        deltaX = deltaX + PADDLEMOVE
    bounds = shape.bb
    width = bounds.right - bounds.left
    newX = pos.x+deltaX
#    newX = max(newX, width/2+20)
#    newX = min(newX, 780-width/2)
    body.position = (newX, pos.y)


# Initialize the game
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 600))
space = pymunk.Space()
space.gravity = (0, 0)
#load font
font = pygame.font.SysFont('Arial', 30)

topBody = pymunk.Body(1,100, pymunk.Body.STATIC)
topBody.position = (400, 10)
topShape = pymunk.Poly.create_box(topBody, (800, 20))
topShape.elasticity = 1.0
topShape.collision_type = COLLTYPE_TOP
space.add(topBody, topShape)

bottomBody = pymunk.Body(1,100, pymunk.Body.STATIC)
bottomBody.position = (400, 590)
bottomShape = pymunk.Poly.create_box(bottomBody, (800, 20))
bottomShape.elasticity = 1.0
bottomShape.collision_type = COLLTYPE_BOTTOM
space.add(bottomBody, bottomShape)

leftBody = pymunk.Body(1,100, pymunk.Body.STATIC)
leftBody.position = (10, 300)
leftShape = pymunk.Poly.create_box(leftBody, (20, 800))
leftShape.elasticity = 1.0
space.add(leftBody, leftShape)

rightBody = pymunk.Body(1,100, pymunk.Body.STATIC)
rightBody.position = (790, 300)
rightShape = pymunk.Poly.create_box(rightBody, (20, 800))
rightShape.elasticity = 1.0
space.add(rightBody, rightShape)

ballBody = pymunk.Body(1,100)
#changed the 3 value parameters in the bellow line to change where the ball spawns
ballBody.position = (random.randint(250,775), 250)
ballShape = pymunk.Circle(ballBody, 10)
ballShape.elasticity = 1.0
ballShape.collision_type = COLLTYPE_BALL
ballBody.apply_impulse_at_local_point(
    (random.randint(-STARTSPEED, STARTSPEED), random.randint(0,STARTSPEED)))
space.add(ballBody, ballShape)

#I changed space.add_collision_handler to space.on_collision
#To correct old syntax
#topCollisionHandler = space.on_collision(COLLTYPE_TOP, COLLTYPE_BALL)
#topCollisionHandler.begin = collide_top

#bottomCollisionHandler = space.on_collision(COLLTYPE_BOTTOM, COLLTYPE_BALL)
#bottomCollisionHandler.begin = collide_bottom

#I then had to replace the above lines (93-100) with the following
space.on_collision(COLLTYPE_TOP, COLLTYPE_BALL, begin=collide_top)
space.on_collision(COLLTYPE_BOTTOM, COLLTYPE_BALL, begin=collide_bottom)

#First Paddle (added 1 after the name to make a second paddle
paddleBody1 = pymunk.Body(1,100, pymunk.Body.KINEMATIC)
paddleBody1.position = (400, 570)
paddleShape1 = pymunk.Poly.create_box(paddleBody1, (100, 20))
paddleShape1.elasticity = 1.0
#Added this line so that the paddle has a collision type and can collide with the ball
paddleShape1.collision_type = COLLTYPE_PADDLE
space.add(paddleBody1, paddleShape1)

#Second Paddle (copied code section above and made it fit the top of the window
paddleBody2 = pymunk.Body(1,100, pymunk.Body.KINEMATIC)
paddleBody2.position = (400, 100)
paddleShape2 = pymunk.Poly.create_box(paddleBody2, (100, 20))
paddleShape2.elasticity = 1.0
#Added this line so that the paddle has a collision type and can collide with the ball
paddleShape2.collision_type = COLLTYPE_PADDLE
space.add(paddleBody2, paddleShape2)


def drawBox(screen, body, shape):
    pos = body.position
    bb = shape.bb
    width = bb.right-bb.left
    height = bb.top - bb.bottom
    topLeft = (pos[0] - width / 2, pos[1] - height / 2)
    pygame.draw.rect(screen, (255, 255, 255),
                     (topLeft[0],topLeft[1],width,height))


#Works with the mechanics of both paddles
leftArrowDown = False
rightArrowDown = False
AKeyDown = False
DKeyDown = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                leftArrowDown = True
            if event.key == pygame.K_RIGHT:
                rightArrowDown = True
            if event.key == pygame.K_a:
                AKeyDown = True
            if event.key == pygame.K_d:
                DKeyDown = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                leftArrowDown = False
            if event.key == pygame.K_RIGHT:
                rightArrowDown = False
            if event.key == pygame.K_a:
                AKeyDown = False
            if event.key == pygame.K_d:
                DKeyDown = False

    #Moves both Paddles according to the new mechanics
    MovePaddle(paddleBody1, paddleShape1,leftArrowDown,rightArrowDown)
    MovePaddle(paddleBody2, paddleShape2,AKeyDown,DKeyDown)

    space.step(1/60.0)
    screen.fill((0, 0, 0))
    pygame.draw.circle(screen, (255, 255, 255), ballBody.position, 10)
    drawBox(screen, topBody, topShape)
    drawBox(screen, leftBody, leftShape)
    drawBox(screen, rightBody, rightShape)
    drawBox(screen, bottomBody, bottomShape)
    drawBox(screen, paddleBody1, paddleShape1)
    drawBox(screen, paddleBody2, paddleShape2)

    #display score
    scoreSurface1 = font.render("P1: " + str(score1), True, (255,255,255))
    screen.blit(scoreSurface1, (20,20))

    scoreSurface2 = font.render("P2: " + str(score2), True, (255,255,255))
    screen.blit(scoreSurface2, (650,20))

    pygame.display.update()

doneSurface = font.render("GameOver", True, (255, 255, 255))
textSize = doneSurface.get_size()
textX = int(400 - (textSize[0] / 2))
textY = int(300 - (textSize[1] / 2))
screen.blit(doneSurface, (textX, textY))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)