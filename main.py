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

## Start with declaring layouts
brick_level_1 = []
brick_level_2 = []
brick_level_3 = []
brick_level_4 = []

def layout1():
    global BRICK_LEVEL_1_NO 
    global BRICK_LEVEL_2_NO 
    global BRICK_LEVEL_3_NO 
    global BRICK_LEVEL_4_NO 
    global BRICK_START_Y_1 
    global BRICK_START_X_1 
    global BRICK_START_Y_2  
    global BRICK_START_X_2  
    global BRICK_START_Y_3
    global BRICK_START_X_3  
    global BRICK_START_Y_4 
    global BRICK_START_X_4  
    global UNBREAKABLE_X 
    global UNBREAKABLE_Y
    BRICK_LEVEL_1_NO = 4
    BRICK_LEVEL_2_NO = 3
    BRICK_LEVEL_3_NO = 1
    BRICK_LEVEL_4_NO = 8
    BRICK_START_Y_1 = 42
    BRICK_START_X_1 = [23]
    BRICK_START_Y_2 = 32
    BRICK_START_X_2 = [21]
    BRICK_START_Y_3 = 19
    BRICK_START_X_3 = [31]
    BRICK_START_Y_4 = 28
    BRICK_START_X_4 = [15]
    UNBREAKABLE_X = 5
    UNBREAKABLE_Y = 42
    brick_level_4.append(Brick(7,31,lives=5))
    for i in range(1,BRICK_LEVEL_1_NO):
        BRICK_START_X_1.append(BRICK_START_X_1[i-1] + 15)

    for i in range(1,BRICK_LEVEL_2_NO):
        BRICK_START_X_2.append(BRICK_START_X_2[i-1] + 15)

    for i in range(1,BRICK_LEVEL_3_NO):
        BRICK_START_X_3.append(BRICK_START_X_3[i-1] + 15)

    for i in range(1,BRICK_LEVEL_4_NO-2):
        BRICK_START_X_4.append(BRICK_START_X_4[i-1] + 8)

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
    
    brick_level_1[1].set_type('rainbow')
    brick_level_1.append(Brick(UNBREAKABLE_X , UNBREAKABLE_Y , lives=4))
    brick_level_4.append(Brick(63,BRICK_START_Y_4+2,lives=5))
    BRICK_LEVEL_1_NO = BRICK_LEVEL_1_NO + 1

def layout2():
    global BRICK_LEVEL_1_NO
    global BRICK_LEVEL_2_NO
    global BRICK_LEVEL_3_NO
    global BRICK_LEVEL_4_NO
    global BRICK_START_X_1
    global BRICK_START_Y_1
    global BRICK_START_Y_4
    global BRICK_START_X_2
    global BRICK_START_Y_2
    global BRICK_START_X_3
    global BRICK_START_X_4 
    BRICK_LEVEL_1_NO = 3
    BRICK_LEVEL_2_NO = 2
    BRICK_LEVEL_3_NO = 1
    BRICK_LEVEL_4_NO = 8
    BRICK_START_Y_1 = 39
    BRICK_START_X_1 = [25]
    BRICK_START_X_2 = [23]
    BRICK_START_X_3 = [31]
    BRICK_START_X_4 = [15]
    BRICK_START_Y_4 = 24
    BRICK_START_Y_2 = 31
    brick_level_4.append(Brick(7,27,lives=5))
    for i in range(0 , BRICK_LEVEL_1_NO):
        BRICK_START_X_1.append(BRICK_START_X_1[i-1] + 12)
    
    for i in range(0 , BRICK_LEVEL_2_NO):
        BRICK_START_X_2.append(BRICK_START_X_2[i-1] + 10)
    
    for i in range(0 , BRICK_LEVEL_3_NO):
        BRICK_START_X_3.append(BRICK_START_X_3[i-1] + 12)

    for i in range(1,BRICK_LEVEL_4_NO-2):
        BRICK_START_X_4.append(BRICK_START_X_4[i-1] + 8)

    for i in range(0,BRICK_LEVEL_1_NO):
        brick_level_1.append(Brick(BRICK_START_X_1[i] , BRICK_START_Y_1 , lives=2))

    for i in range(0,BRICK_LEVEL_2_NO):
        brick_level_2.append(Brick(BRICK_START_X_2[i] , BRICK_START_Y_2 , lives=3))

    for i in range(0,BRICK_LEVEL_3_NO):
        brick_level_3.append(Brick(BRICK_START_X_3[i] , BRICK_START_Y_3 , lives=1))

    for i in range(0, BRICK_LEVEL_4_NO-2):
        if i == 1 or i == 2 or i==3 or i==4:
            brick_level_4.append(Brick(BRICK_START_X_4[i] , BRICK_START_Y_4 , lives=5))
        else:
            brick_level_4.append(Brick(BRICK_START_X_4[i] , BRICK_START_Y_4 , lives=2))
    
    brick_level_3[0].set_type('rainbow')
    brick_level_1.append(Brick(UNBREAKABLE_X , BRICK_START_Y_1 , lives=4))
    brick_level_4.append(Brick(63,27,lives=5))
    BRICK_LEVEL_1_NO = BRICK_LEVEL_1_NO + 1

def switch_layouts(val , grid , ball , paddle):
    global brick_level_1
    global brick_level_2
    global brick_level_3
    global brick_level_4
    for i in range(0 , BRICK_LEVEL_1_NO):
        brick_level_1[i].clear_brick(grid)
        brick_level_1[i].set_to_nan()
        brick_level_1[i].kill()
    for i in range(0 , BRICK_LEVEL_2_NO):
        brick_level_2[i].clear_brick(grid)
        brick_level_2[i].set_to_nan()
        brick_level_2[i].kill()
    for i in range(0 , BRICK_LEVEL_3_NO):
        brick_level_3[i].clear_brick(grid)
        brick_level_3[i].set_to_nan()
        brick_level_3[i].kill()
    for i in range(0 , BRICK_LEVEL_4_NO):
        brick_level_4[i].clear_brick(grid)
        brick_level_4[i].set_to_nan()
        brick_level_4[i].kill()

    brick_level_1 = []
    brick_level_2 = []
    brick_level_3 = []
    brick_level_4 = []

    powerups = get_powerup()
    for powerup in powerups[:]:
        if powerup.get_type() == "expand_paddle":
            powerup.delete(paddle , grid, paddle)

        if powerup.get_type() == "shrink_paddle":
            powerup.delete(paddle , grid, paddle)

        if powerup.get_type() == "fast_ball":
            powerup.delete(ball[0] , grid, paddle)

        if powerup.get_type() == "ball_multiplier":
            powerup.delete(ball , grid, paddle)

        if powerup.get_type() == "thru_ball":
            powerup.delete(ball , grid, paddle)

        if powerup.get_type() == "paddle_grab":
            powerup.delete(ball , grid, paddle)

    for i in range(0 , len(ball)):
        ball[i].reset_ball(paddle , grid , ball)

    if val == 2:
        layout2()
    if val == 1:
        layout1()
    
cur_layout = 1
layout1()
while True:

    key = input_to(Get())
    if key == 'a':
        paddle.move_paddle(-1 , board.get_grid() , ball[0])

    if key == 'd':
        paddle.move_paddle(1 , board.get_grid() , ball[0])

    if key == 'q':
        break

    if key == 'z':
        switch_layouts(1 , board.get_grid(), ball , paddle)
        cur_layout = 1

    if key == 'x':
        switch_layouts(2 , board.get_grid(),  ball , paddle)
        cur_layout = 2

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

        if powerup.get_type() == "shooting_paddle":
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
        i.move_ball(board.get_grid() , paddle.get_x() , paddle.get_length() , paddle , player , powerups , ball, brick_level_1 , brick_level_2 , brick_level_3 , brick_level_4)
    for i in range(0,BRICK_LEVEL_1_NO):
        if brick_level_1[i].get_type() == 'rainbow':
            brick_level_1[i].rainbow_live()
        player.set_lives(brick_level_1[i].check_out(paddle))
        brick_level_1[i].render_brick(board.get_grid())
        total_lives = total_lives + brick_level_1[i].get_lives()
        total_lives1 = total_lives
        if brick_level_1[i].get_lives() == 0:
            zero_lives = zero_lives + 1
        for j in ball:
            brick_level_1[i].brick_ball_collisions(j , board.get_grid() , player, i , brick_level_1 , ball)
    for i in range(0,BRICK_LEVEL_2_NO):
        if brick_level_2[i].get_type() == 'rainbow':
            brick_level_2[i].rainbow_live()
        player.set_lives(brick_level_2[i].check_out(paddle))
        brick_level_2[i].render_brick(board.get_grid())
        total_lives = total_lives + brick_level_2[i].get_lives()
        for j in ball:
            brick_level_2[i].brick_ball_collisions(j , board.get_grid() , player , i , brick_level_2 , ball)
    for i in range(0,BRICK_LEVEL_3_NO):
        if brick_level_3[i].get_type() == 'rainbow':
            brick_level_3[i].rainbow_live()
        player.set_lives(brick_level_3[i].check_out(paddle))
        brick_level_3[i].render_brick(board.get_grid())
        total_lives = total_lives + brick_level_3[i].get_lives()
        for j in ball:
            brick_level_3[i].brick_ball_collisions(j , board.get_grid() , player , i , brick_level_3 , ball)
    print(len(brick_level_4) , BRICK_LEVEL_4_NO)
    for i in range(0,BRICK_LEVEL_4_NO):
        brick_level_4[i].render_brick(board.get_grid())
        player.set_lives(brick_level_4[i].check_out(paddle))
        total_lives = total_lives + brick_level_4[i].get_lives()
        for j in ball:
            brick_level_4[i].brick_ball_collisions(j , board.get_grid() , player , i , brick_level_4 , ball)
    
    print(Fore.RED + "Score: " + str(player.get_score()))
    print(Fore.GREEN + "Time Elapsed: " , str(player.get_elapsed_time()))
    print(Fore.BLUE + "Lives Remaining: " , str(player.get_lives()))
    print(Fore.YELLOW + "Ball Speed: " , str(ball[0].get_yspeed()))
    for i in range(0 , len(powerups)):
        print(powerups[i].type , powerups[i].active , time.time() - powerups[i].time_limit)

    if player.get_lives() == 0:
        game_over()
        time.sleep(1)
        break

    if player.get_lives() > 0 and ((total_lives == 0) or (total_lives == 4 and total_lives1 == 4 and zero_lives > 1)):
        if (cur_layout == 1):
            cur_layout = 2
            switch_layouts(2 , board.get_grid(),  ball , paddle)
        if (cur_layout == 2):
            win()
            time.sleep(1)
            break
    board.display(powerups)
    