from headers import *
import numpy as np
from object import *
from colorama import Fore, Back, Style
import os

class Ball(Object):

    def __init__(self , POS_X , POS_Y , ball_type="normal"):
        '''
        Initialize with the starting positions of the ball
        '''
        super(Ball, self).__init__(POS_X , HEIGHT - POS_Y)
        self.__speed_x = 0
        self.__speed_y = 3
        if ball_type == "normal":
            self.__ball = 'O'
        else:
            self.__ball = '|'
        self.__type = ball_type
        self.storage_xspeed = 0
        self.storage_yspeed = 3
        if self.__type == "boss":
            self.speed_x = -3
            self.__ball = '§'

    def get_xspeed(self):
        return self.__speed_x

    def get_yspeed(self):
        return self.__speed_y

    def set_xspeed(self , new_speed):
        self.__speed_x = new_speed

    def set_yspeed(self , new_speed):
        self.__speed_y = new_speed

    def set_storage(self , x , y):
        self.storage_xspeed = x
        self.storage_yspeed = y

    def get_x_storage(self):
        return self.storage_xspeed

    def get_y_storage(self):
        return self.storage_yspeed

    def render_ball(self , POS_X , POS_Y , grid):
        '''
        Render the ball at the paddle's middle
        '''
        grid[HEIGHT - POS_Y][POS_X] = self.__ball

    def remove_ball(self , grid , obj):
        '''
        Remove the ball
        '''
        grid[self.get_y()][self.get_x()] = ' '
        del obj

    def set_type(self , val):
        self.__type = val

    def get_type(self):
        return self.__type

    def get_shape(self):
        return self.__ball

    def reset_ball(self , paddle , grid , ball):
        grid[self.get_y()][self.get_x()] = ' '
        self.set_xspeed(0)
        self.set_yspeed(-1*self.get_yspeed())           
        self.set_x(np.random.randint(PADDLE_POS_X , PADDLE_POS_X + paddle.get_length()))            
        self.set_y(HEIGHT - BALL_POS_Y)
        paddle.clear_paddle(grid)             
        paddle.set_x(PADDLE_POS_X)             
        paddle.set_y(PADDLE_POS_Y)
        paddle.move_paddle(0 , grid , ball)

 
    def move_ball(self , grid , paddle_pos_x , paddle_size , paddle , player , powerups , ball, brick_level_1, brick_level_2, brick_level_3, brick_level_4, start = 0):
        '''
        Move the ball during each iteration
        '''
        out = 0
        paddle_pos_y = HEIGHT - PADDLE_POS_Y
        if self.__type == "shooting" and (((self.get_y() + self.get_yspeed()) >= paddle_pos_y and self.get_yspeed() < 0) or (self.get_y()+self.get_yspeed() <= 0 and self.get_yspeed() < 0)):
            grid[self.get_y()][self.get_x()] = ' '
            ball.remove(self)
            return

        if paddle_pos_y - self.get_y()<= 2 and paddle_pos_x <= self.get_x() and paddle_pos_x + paddle_size > self.get_x() and start == 0:
            '''
            Handle When it hits the paddle; reflect
            '''
            os.system('afplay paddle_ball.mp3 &')
            x_reflect = (self.get_x() - paddle_pos_x) 
            if x_reflect < paddle_size/2 and paddle.move_ball != 1 and self.__type == "normal":
                self.set_xspeed(int(-1*(paddle_size/2 - x_reflect)))

            elif x_reflect > paddle_size/2 and paddle.move_ball != 1 and self.__type == "normal":
                self.set_xspeed(int(x_reflect - paddle_size/2))

            elif x_reflect == paddle_size/2 and paddle.move_ball != 1 and self.__type == "normal":
                self.set_xspeed(0)

            if paddle.move_ball == 0 and self.__type != "shooting":
                for i in range(0 , len(brick_level_1)):
                    brick_level_1[i].clear_brick(grid)
                    brick_level_1[i].bring_down()
                
                for i in range(0 , len(brick_level_2)):
                    brick_level_2[i].clear_brick(grid)
                    brick_level_2[i].bring_down()

                for i in range(0 , len(brick_level_3)):
                    brick_level_3[i].clear_brick(grid)
                    brick_level_3[i].bring_down()

                for i in range(0 , len(brick_level_4)):
                    brick_level_4[i].clear_brick(grid)
                    brick_level_4[i].bring_down()
                
        new_y = self.get_y() + self.get_yspeed()
        new_x = self.get_x() + self.get_xspeed()

        if new_y <= 0:
            self.set_yspeed(-1*self.get_yspeed())

        elif new_y >= HEIGHT-PADDLE_POS_Y and paddle.get_x() <= self.get_x() and paddle.get_x() + paddle.get_length() >= self.get_x() and self.__type == "boss":
            paddle.clear_paddle(grid)             
            paddle.set_x(PADDLE_POS_X)             
            paddle.set_y(PADDLE_POS_Y)
            grid[self.get_y()][self.get_x()] = ' '
            paddle.move_paddle(0 , grid , ball)
            player.set_lives(player.get_lives() - 1)
            for i in powerups[:]:
                if i.get_type() == "expand_paddle":
                    i.delete(paddle , grid , paddle)
                    on_clear(i , paddle , grid , paddle)

                elif i.get_type() == "shrink_paddle":
                    i.delete(paddle , grid , paddle)
                    on_clear(i , paddle , grid , paddle)

                elif i.get_type() == "fast_ball":
                    i.delete(self , grid , paddle)
                    on_clear(i , self , grid , paddle)

                elif i.get_type() == "ball_multiplier":
                    i.delete(ball , grid , paddle)
                    on_clear(i , self , grid , paddle)

                elif i.get_type() == "thru_ball":
                    i.delete(ball , grid , paddle)
                    on_clear(i , self , grid , paddle)

                elif i.get_type() == "shooting_paddle":
                    i.delete(ball , grid , paddle)
                grid[i.y][i.x] = ' '
            set_powerup()
            for i in ball[:]:
                if i.get_type() == "boss":
                    grid[i.get_y()][i.get_x()] = ' '
                    ball.remove(i)
            return

        elif new_y >= HEIGHT-PADDLE_POS_Y and self.__type == "boss":
            grid[self.get_y()][self.get_x()] = ' '
            ball.remove(self)
            for i in ball[:]:
                if i.get_type() == "boss":
                    grid[i.get_y()][i.get_x()] = ' '
                    ball.remove(i)
            return


        elif new_y >= HEIGHT-PADDLE_POS_Y and paddle.get_x() <= self.get_x() and paddle.get_x() + paddle.get_length() >= self.get_x():
            self.set_yspeed(-1*self.get_yspeed())

        elif new_y >= HEIGHT-PADDLE_POS_Y:
            grid[self.get_y()][self.get_x()] = ' '
            cnt_normal = 0
            for i in range(0 , len(ball)):
                if ball[i].get_type() == "normal":
                    cnt_normal = cnt_normal + 1
            len_ball = len(ball)
            if cnt_normal > 1:
                ball.remove(self)
            if cnt_normal <= 1:
                flag = 0
                ball_ind = -1
                for i in range(0 , len(ball)):
                    if ball[i].get_type() == "normal":
                        ball_ind = i
                if ball[ball_ind].get_y() + ball[ball_ind].get_yspeed() != new_y:
                    flag = 1
                if flag == 0 or cnt_normal == 0:
                    out = 3
                    self.set_xspeed(0)
                    self.set_yspeed(-1*self.get_yspeed())           
                    self.set_x(np.random.randint(PADDLE_POS_X , PADDLE_POS_X + paddle.get_length()))            
                    self.set_y(HEIGHT - BALL_POS_Y)
                    paddle.clear_paddle(grid)             
                    paddle.set_x(PADDLE_POS_X)             
                    paddle.set_y(PADDLE_POS_Y)
                    paddle.move_paddle(0 , grid , ball)
                    player.set_lives(player.get_lives() - 1)
                    for i in powerups[:]:
                        if i.get_type() == "expand_paddle":
                            i.delete(paddle , grid , paddle)
                            on_clear(i , paddle , grid , paddle)

                        elif i.get_type() == "shrink_paddle":
                            i.delete(paddle , grid , paddle)
                            on_clear(i , paddle , grid , paddle)

                        elif i.get_type() == "fast_ball":
                            i.delete(self , grid , paddle)
                            on_clear(i , self , grid , paddle)

                        elif i.get_type() == "ball_multiplier":
                            i.delete(ball , grid , paddle)
                            on_clear(i , self , grid , paddle)

                        elif i.get_type() == "thru_ball":
                            i.delete(ball , grid , paddle)
                            on_clear(i , self , grid , paddle)

                        elif i.get_type() == "shooting_paddle":
                            i.delete(ball , grid , paddle)
                        grid[i.y][i.x] = ' '
                    set_powerup()
                    for i in ball[:]:
                        if i.get_type() == "boss":
                            grid[i.get_y()][i.get_x()] = ' '
                            ball.remove(i)

            return

        if new_x > WIDTH-1 or new_x < 0:
            self.set_xspeed(-1*self.get_xspeed())

        if self.get_x() < 0:
            self.set_x(WIDTH + self.get_x())

        grid[self.get_y()][self.get_x()] = ' '
        if out == 0:
            self.set_y(self.get_y() + self.get_yspeed())
            self.set_x(self.get_x() + self.get_xspeed())
        grid[self.get_y()][self.get_x()] = self.__ball



        