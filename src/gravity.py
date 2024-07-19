#!/usr/bin/env python3
import pygame, sys, random
from pygame.math import Vector2
from phybody import Body

SET_FPS = 60
SCALE = 1
VEL_DEBUG_SCALE = 100
ACC_DEBUG_SCALE = 10_000
CAM_CENTER_ON = [0, 0]
SAVE_CAM_CENTER_ON = [0, 0]

DRAG = False
MOUSE_OG = (0, 0)

FAST = False

DEBUG = False

MOUSE_GRAVITY = False

""" bodies: list[Body] = [
    Body(0, (255, 0, 0), 100, 1000, Vector2(0, 100), Vector2(0, 0)),
    Body(1, (0, 255, 0), 50, 10, Vector2(-500, -1000), Vector2(2.5, 0)),
] """
bodies: list[Body] = [
    Body(0, (255, 0, 0), 10, 10, Vector2(200, 0), Vector2(0, -0.2)),
    Body(1, (0, 255, 0), 10, 10, Vector2(-200, 0), Vector2(0, 0.2)),
    #Body(2, (0, 0, 255), 10, 50, Vector2(0, 50), Vector2(0, 0)),
]

""" bodies: list[Body] = [
    Body(0, (255, 0, 0), 10, 10, Vector2(200, 0), Vector2(0, 0)),
    Body(1, (0, 255, 0), 10, 10, Vector2(-200, 0), Vector2(0, 0))
] """

FPS = SET_FPS
pygame.init()
window = pygame.display.set_mode((900, 700), pygame.RESIZABLE)
pygame.display.set_caption("Grav")
clock = pygame.time.Clock()

while True:
    width, height = window.get_size()

    pygame.display.set_caption(f"Grav {'[FAST FORWARD]' if FAST else ''} {'[DEBUG]' if DEBUG else ''} {'[MOUSE GRAVITY]' if MOUSE_GRAVITY else ''}")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEWHEEL and event.y == 1:
            SCALE += 0.1
        elif event.type == pygame.MOUSEWHEEL and event.y == -1:
            SCALE -= 0.1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            DRAG = True
            MOUSE_OG = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and DRAG:
            DRAG = False
            SAVE_CAM_CENTER_ON = CAM_CENTER_ON[::]
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not DRAG:
            SAVE_CAM_CENTER_ON = [0, 0]
            CAM_CENTER_ON = [0, 0]
            SCALE = 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not FAST:
            FAST = True
            FPS = 1000
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE and FAST:
            FAST = False
            FPS = SET_FPS
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            DEBUG = not DEBUG
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
            MOUSE_GRAVITY = not MOUSE_GRAVITY

    if DRAG:
        mousex, mousey = pygame.mouse.get_pos()
        delta = (mousex - MOUSE_OG[0], mousey - MOUSE_OG[1])
        CAM_CENTER_ON[0] = delta[0] + SAVE_CAM_CENTER_ON[0]
        CAM_CENTER_ON[1] = delta[1] + SAVE_CAM_CENTER_ON[1]

    random.shuffle(bodies)

    window.fill((0, 0, 0))

    for body in bodies:
        body.gravity_calc(bodies)
        

    """ for body in bodies:
        body.update() """

    #pygame.draw.circle(window, (255, 255, 255), (width//2, height//2), 5)
    #print(CAM_CENTER_ON)
    for body in bodies:
        body_pos = Vector2((CAM_CENTER_ON[0] + body.pos.x)*SCALE + width//2, (CAM_CENTER_ON[1] - body.pos.y) * SCALE + height//2)
        pygame.draw.circle(window, body.color, body_pos, body.size * SCALE)
        if DEBUG:
            vel_line = (body.velocity * VEL_DEBUG_SCALE * SCALE)
            pygame.draw.line(window, 
                             (0, 255, 0), 
                             ((CAM_CENTER_ON[0] + body.pos.x)*SCALE + width//2, (CAM_CENTER_ON[1] - body.pos.y) * SCALE + height//2),
                             ((CAM_CENTER_ON[0] + (body.pos + vel_line).x )*SCALE + width//2, (CAM_CENTER_ON[1] - (body.pos + vel_line).y) * SCALE + height//2),
                             )

            acc_line = (body.acceleration * ACC_DEBUG_SCALE * SCALE)
            pygame.draw.line(window, 
                             (0, 0, 255), 
                             ((CAM_CENTER_ON[0] + body.pos.x)*SCALE + width//2, (CAM_CENTER_ON[1] - body.pos.y) * SCALE + height//2),
                             ((CAM_CENTER_ON[0] + (body.pos + acc_line).x )*SCALE + width//2, (CAM_CENTER_ON[1] - (body.pos + acc_line).y) * SCALE + height//2),
                             )

    #print(bodies[1].acceleration)
    pygame.display.flip()
    clock.tick(FPS)