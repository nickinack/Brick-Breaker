import numpy as np
import sys,tty
import os
from colorama import Fore, Back, Style
import time
from multiprocessing import Process
from paddle import *
from board import *
from input import *
from ball import *
from brick import *

board = Board(HEIGHT , WIDTH)
paddle = Paddle(PADDLE_POS_X , PADDLE_POS_Y)
paddle.render_paddle(board.get_grid())
ball = Ball(BALL_POS_X , BALL_POS_Y)

brick_level_1 = []
brick_level_2 = []
brick_level_3 = []
for i in range(0,BRICK_LEVEL_1_NO):
    brick_level_1.append(Brick(BRICK_START_X_1[i] , BRICK_START_Y_1 , lives=3))

for i in range(0,BRICK_LEVEL_2_NO):
    brick_level_2.append(Brick(BRICK_START_X_2[i] , BRICK_START_Y_2 , lives=2))

for i in range(0,BRICK_LEVEL_3_NO):
    brick_level_3.append(Brick(BRICK_START_X_3[i] , BRICK_START_Y_3 , lives=1))
    

while True:
    key = input_to(Get())
    if key == 'a':
        paddle.move_paddle(-1 , board.get_grid())

    if key == 'd':
        paddle.move_paddle(1 , board.get_grid())

    if key == 'q':
        break

    os.system('clear')
    ball.move_ball(board.get_grid() , paddle.get_x() , paddle.get_length())
    for i in range(0,BRICK_LEVEL_1_NO):
        brick_level_1[i].render_brick(board.get_grid())
        brick_level_1[i].brick_ball_collisions(ball , board.get_grid())
    for i in range(0,BRICK_LEVEL_2_NO):
        brick_level_2[i].render_brick(board.get_grid())
        brick_level_2[i].brick_ball_collisions(ball , board.get_grid())
    for i in range(0,BRICK_LEVEL_3_NO):
        brick_level_3[i].render_brick(board.get_grid())
        brick_level_3[i].brick_ball_collisions(ball , board.get_grid())

    print("Speed: " , ball.get_yspeed())
    board.display()


