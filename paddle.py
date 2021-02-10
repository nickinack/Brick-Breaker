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
        self.__paddle = "$--------$"
    
    def clear_paddle(self , grid):
        '''
        Clear the paddle
        '''
        for i in range(self.get_x() , self.get_x() + len(self.__paddle)):
            grid[HEIGHT - PADDLE_POS_Y][i] = ' '

    def get_length(self):
        return len(self.__paddle)

    def move_paddle(self , direction , grid):
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
            for i in range(self.get_x() , self.get_x() + len(self.__paddle)):
            #Move paddle
                grid[HEIGHT - PADDLE_POS_Y][i] = self.__paddle[i - self.get_x()]
                

    def render_paddle(self , grid):
        '''
        Render paddle initially
        '''
        for i in range(self.get_x() , self.get_x() + len(self.__paddle)):
            grid[HEIGHT - PADDLE_POS_Y][i] = self.__paddle[i - self.get_x()]






    
    
        