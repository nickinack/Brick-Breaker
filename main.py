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

os.system('clear')
start_game()
time.sleep(1)

player = Player()
board = Board(HEIGHT , WIDTH)
paddle = Paddle(PADDLE_POS_X , PADDLE_POS_Y)
paddle.render_paddle(board.get_grid())
ball = []
BALL_POS_X = np.random.randint(PADDLE_POS_X+2 , PADDLE_POS_X + paddle.get_length()-2)
ball.append(Ball(BALL_POS_X , BALL_POS_Y))

brick_level_1 = []
brick_level_2 = []
brick_level_3 = []
brick_level_4 = []
brick_level_4.append(Brick(7,31,lives=5))
for i in range(0,BRICK_LEVEL_1_NO):
    brick_level_1.append(Brick(BRICK_START_X_1[i] , BRICK_START_Y_1 , lives=3))

for i in range(0,BRICK_LEVEL_2_NO):
    brick_level_2.append(Brick(BRICK_START_X_2[i] , BRICK_START_Y_2 , lives=2))

for i in range(0,BRICK_LEVEL_3_NO):
    brick_level_3.append(Brick(BRICK_START_X_3[i] , BRICK_START_Y_3 , lives=1))

for i in range(0, BRICK_LEVEL_4_NO-2):
    if i == 1 or i == 2 or i==3 or i==4:
         brick_level_4.append(Brick(BRICK_START_X_4[i] , BRICK_START_Y_4 , lives=5))
    else:
        brick_level_4.append(Brick(BRICK_START_X_4[i] , BRICK_START_Y_4 , lives=2))
    
brick_level_1.append(Brick(UNBREAKABLE_X , UNBREAKABLE_Y , lives=4))
brick_level_4.append(Brick(63,31,lives=5))
BRICK_LEVEL_1_NO = BRICK_LEVEL_1_NO + 1


while True:

    key = input_to(Get())
    if key == 'a':
        paddle.move_paddle(-1 , board.get_grid() , ball[0])

    if key == 'd':
        paddle.move_paddle(1 , board.get_grid() , ball[0])

    if key == 'q':
        break

    powerups = get_powerup()
    cnt_grab = 0
    active = 0
    index = []
    i = 0
    for powerup in powerups[:]:
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
            cnt_grab = cnt_grab + 1
            if powerup.active != 2 and active == 2:
                index.append(i)
            elif powerup.active == 2:
                active = 2
            powerup.move_powerup(board.get_grid() , ball[0] , paddle)

        if powerup.get_type() == "paddle_grab" and key == 'f':
            powerup.delete(ball[0] , board.get_grid() , paddle)
            index = []
            break
        i = i+1

        if cnt_grab > 1 and active == 2:
            for i in index:
                powerups.remove(powerups[i])

    os.system('clear')
    total_lives = 0
    total_lives1 = 0
    zero_lives = 0
    for i in ball:
        i.move_ball(board.get_grid() , paddle.get_x() , paddle.get_length() , paddle , player , powerups , ball)
    for i in range(0,BRICK_LEVEL_1_NO):
        brick_level_1[i].render_brick(board.get_grid())
        total_lives = total_lives + brick_level_1[i].get_lives()
        total_lives1 = total_lives
        if brick_level_1[i].get_lives() == 0:
            zero_lives = zero_lives + 1
        for j in ball:
            brick_level_1[i].brick_ball_collisions(j , board.get_grid() , player, i , brick_level_1)
    for i in range(0,BRICK_LEVEL_2_NO):
        brick_level_2[i].render_brick(board.get_grid())
        total_lives = total_lives + brick_level_2[i].get_lives()
        for j in ball:
            brick_level_2[i].brick_ball_collisions(j , board.get_grid() , player , i , brick_level_2)
    for i in range(0,BRICK_LEVEL_3_NO):
        brick_level_3[i].render_brick(board.get_grid())
        total_lives = total_lives + brick_level_3[i].get_lives()
        for j in ball:
            brick_level_3[i].brick_ball_collisions(j , board.get_grid() , player , i , brick_level_3)
    for i in range(0,BRICK_LEVEL_4_NO):
        brick_level_4[i].render_brick(board.get_grid())
        total_lives = total_lives + brick_level_4[i].get_lives()
        for j in ball:
            brick_level_4[i].brick_ball_collisions(j , board.get_grid() , player , i , brick_level_4)
    
    print(Fore.RED + "Score: " + str(player.get_score()))
    print(Fore.GREEN + "Time Elapsed: " , str(player.get_elapsed_time()))
    print(Fore.BLUE + "Lives Remaining: " , str(player.get_lives()))
    print(Fore.YELLOW + "Ball Speed: " , str(ball[0].get_yspeed()))
    for i in range(0 , len(powerups)):
        print(powerups[i].type)

    if player.get_lives() == 0:
        game_over()
        time.sleep(1)
        break

    if player.get_lives() > 0 and ((total_lives == 0) or (total_lives == 4 and total_lives1 == 4 and zero_lives > 1)):
        win()
        time.sleep(1)
        break
    board.display(powerups)
    