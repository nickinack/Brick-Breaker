from headers import *
import numpy as np
from object import *
from colorama import Fore, Back, Style


class Paddle(Object):

    def __init__(self , POS_X , POS_Y):
        '''
        Initialise the starting positions of the paddle
        '''
        super(Paddle, self).__init__(POS_X , HEIGHT-POS_Y)
        self.__speed = 2
        self.__paddle = "----------"
        self.move_ball = 0
        self.type = "normal"

    def update_shape(self , grid , str):
        self.clear_paddle(grid)
        if str == "expand":
            self.__paddle = self.__paddle + "-----"
        elif str == "shrink":
            if (len(self.__paddle) <= 3):
                return
            self.__paddle = self.__paddle[0: len(self.__paddle)-3]
        self.render_paddle(grid)

    def reshape_paddle(self , grid , str):
        self.clear_paddle(grid)
        if str == "expand":
            self.__paddle = self.__paddle[0:len(self.__paddle)-5]
        elif str == "shrink":
            self.__paddle = self.__paddle + "---"
            if len(self.__paddle) > len("----------"):
                self.__paddle = "----------"
        self.render_paddle(grid)
    
    def clear_paddle(self , grid):
        '''
        Clear the paddle
        '''
        for i in range(self.get_x() , self.get_x() + len(self.__paddle)):
            grid[HEIGHT - PADDLE_POS_Y][i] = ' '

    def get_length(self):
        return len(self.__paddle)

    def move_paddle(self , direction , grid , ball , boss_brick = ''):
        '''
        Move paddle when key stroke is hit
        '''
        new_x = self.get_x() + direction*self.__speed
        if new_x >= WIDTH-len(self.__paddle):
            return grid
        
        if new_x < 0:
            return grid

        else:
            self.clear_paddle(grid)
            new_x = self.get_x() + direction*self.__speed
            self.set_x(new_x)
            if (boss_brick != ''):
                if (boss_brick.get_type() == "boss"):
                    boss_brick.clear_brick(grid)
                    boss_brick.set_x(new_x)
                    if boss_brick.get_lives() > 0:
                        boss_brick.render_brick(grid)
            for i in range(self.get_x() , self.get_x() + len(self.__paddle)):
            #Move paddle
                grid[HEIGHT - PADDLE_POS_Y][i] = self.__paddle[i - self.get_x()]
            if self.move_ball == 1:
                grid[ball.get_y()][ball.get_x()] = ' '
                ball.set_x(ball.get_x() + 2*direction)
                grid[ball.get_y()][ball.get_x()] = ball.get_shape
                

    def render_paddle(self , grid):
        '''
        Render paddle initially
        '''
        for i in range(self.get_x() , self.get_x() + len(self.__paddle)):
            grid[HEIGHT - PADDLE_POS_Y][i] = self.__paddle[i - self.get_x()]

