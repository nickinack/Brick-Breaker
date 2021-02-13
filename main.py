import numpy as np
import sys,tty
import os
from colorama import Fore, Back, Style
import time
from multiprocessing import Process
from headers import *
from paddle import *
from board import *
from input import *
from ball import *
from brick import *
from player import *
from powerup import *

player = Player()
board = Board(HEIGHT , WIDTH)
paddle = Paddle(PADDLE_POS_X , PADDLE_POS_Y)
paddle.render_paddle(board.get_grid())
ball = []
ball.append(Ball(BALL_POS_X , BALL_POS_Y))

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
        paddle.move_paddle(-1 , board.get_grid() , ball[0])

    if key == 'd':
        paddle.move_paddle(1 , board.get_grid() , ball[0])

    if key == 'q':
        break

    powerups = get_powerup() 
    for powerup in powerups:
        if powerup.get_type() == "expand_paddle":
            powerup.move_powerup(board.get_grid() , paddle , paddle)

        if powerup.get_type() == "shrink_paddle":
            powerup.move_powerup(board.get_grid() , paddle , paddle)

        if powerup.get_type() == "fast_ball":
            powerup.move_powerup(board.get_grid() , ball[0] , paddle)

        if powerup.get_type() == "ball_multiplier":
            powerup.move_powerup(board.get_grid() , ball , paddle)

        if powerup.get_type() == "thru_ball":
            powerup.move_powerup(board.get_grid() , ball , paddle)

        if powerup.get_type() == "paddle_grab":
            powerup.move_powerup(board.get_grid() , ball[0] , paddle)

        if powerup.get_type() == "paddle_grab" and key == 'f':
            powerup.delete(ball[0] , board.get_grid() , paddle)

    os.system('clear')
    for i in ball:
        i.move_ball(board.get_grid() , paddle.get_x() , paddle.get_length() , paddle , player , powerups , ball)
    for i in range(0,BRICK_LEVEL_1_NO):
        brick_level_1[i].render_brick(board.get_grid())
        for j in ball:
            brick_level_1[i].brick_ball_collisions(j , board.get_grid() , player)
    for i in range(0,BRICK_LEVEL_2_NO):
        brick_level_2[i].render_brick(board.get_grid())
        for j in ball:
            brick_level_2[i].brick_ball_collisions(j , board.get_grid() , player)
    for i in range(0,BRICK_LEVEL_3_NO):
        brick_level_3[i].render_brick(board.get_grid())
        for j in ball:
            brick_level_3[i].brick_ball_collisions(j , board.get_grid() , player)
    
    print(Fore.RED + "Score: " + str(player.get_score()))
    print(Fore.GREEN + "Time Elapsed: " , str(player.get_elapsed_time()))
    print(Fore.BLUE + "Lives Remaining: " , str(player.get_lives()))
    print(Fore.YELLOW + "Ball Speed: " , str(ball[0].get_yspeed()))
    for i in powerups:
        print(i.get_type())
    board.display()
    


