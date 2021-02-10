from headers import *
import numpy as np
from object import *
from colorama import Fore, Back, Style

class Ball(Object):

    def __init__(self , POS_X , POS_Y):
        '''
        Initialize with the starting positions of the ball
        '''
        super(Ball, self).__init__(POS_X , HEIGHT - POS_Y)
        self.__speed_x = 0
        self.__speed_y = 3
        self.__ball = 'O'

    def get_xspeed(self):
        return self.__speed_x

    def get_yspeed(self):
        return self.__speed_y

    def set_xspeed(self , new_speed):
        self.__speed_x = new_speed

    def set_yspeed(self , new_speed):
        self.__speed_y = new_speed

    def render_ball(self , POS_X , POS_Y , grid):
        '''
        Render the ball at the paddle's middle
        '''
        grid[HEIGHT - POS_Y][POS_X] = self.__ball

    def move_ball(self , grid , paddle_pos_x , paddle_size , start = 0):
        '''
        Move the ball during each iteration
        '''
        paddle_pos_y = HEIGHT - PADDLE_POS_Y
        if paddle_pos_y - self.get_y()<= 1 and paddle_pos_x <= self.get_x() and paddle_pos_x + paddle_size > self.get_x() and start == 0:
            '''
            Handle When it hits the paddle; reflect
            '''
            x_reflect = (self.get_x() - paddle_pos_x) 
            if x_reflect < paddle_size/2:
                self.set_xspeed(int(-1*(paddle_size/2 - x_reflect)))

            elif x_reflect > paddle_size/2:
                self.set_xspeed(int(x_reflect - paddle_size/2))

            elif abs(x_reflect) == paddle_size/2:
                self.set_xspeed(0)
                
        new_y = self.get_y() + self.get_yspeed()
        new_x = self.get_x() + self.get_xspeed()

        if new_y >= HEIGHT-PADDLE_POS_Y or new_y <= 0:
            self.set_yspeed(-1*self.get_yspeed())

        if new_x > WIDTH-1 or new_x < 0:
            self.set_xspeed(-1*self.get_xspeed())

        if self.get_x() < 0:
            self.set_x(WIDTH + self.get_x())

        grid[self.get_y()][self.get_x()] = ' '
        self.set_y(self.get_y() + self.get_yspeed())
        self.set_x(self.get_x() + self.get_xspeed())
        grid[self.get_y()][self.get_x()] = self.__ball
