from headers import *
import numpy as np
from object import *
from colorama import Fore, Back, Style
from ball import *
import time

class Powerup:

    def __init__(self , START_X , START_Y , powerup):
        self.__x = START_X
        self.__y = HEIGHT - START_Y
        self.__type = powerup
        self.__yspeed = -2
        self.__shape = 'P'
        self.__active = 0
        self.__start_time = time.time()

    def render_powerup(self , grid):
        grid[self.__y][self.__x] = self.__shape

    def active(self):
        return self.__active

    def get_type(self):
        return self.__type

    def delete(self , obj , grid):
        if self.__type == "expand_paddle" and self.__active == 2:
            obj.reshape_paddle(grid , "expand")

        if self.__type == "shrink_paddle" and self.__active == 2:
            obj.reshape_paddle(grid , "shrink")

        if self.__type == "fast_ball" and self.__active == 2:
            if obj.get_yspeed() > 0:
                obj.set_yspeed(obj.get_yspeed() - 1)

            if obj.get_yspeed() < 0:
                obj.set_yspeed(obj.get_yspeed() + 1)

        if self.__type == "fast_ball" and self.__active == 2:
            obj = obj[0]

        if self.__type == "ball_multiplier" and self.__active == 2:
            obj = []

        if self.__type == "thru_ball":
            for j in range(0 , len(obj)):
                obj[j].set_type('normal')

        if self.__type == "paddle_grab":
            obj.set_xspeed(obj.storage_xspeed)
            obj.set_yspeed(-1*abs(obj.storage_yspeed))

        if self.__active == 0:
            grid[self.__y][self.__x] = ' '

    def move_powerup(self , grid , obj , paddle):
        grid[self.__y][self.__x] = ' '
        new_y = self.__y + 3
        if (self.__active == 2 and time.time() - self.__start_time >= 6):
            if self.__type == "expand_paddle":
                obj.reshape_paddle(grid , "expand")

            if self.__type == "shrink_paddle":
                obj.reshape_paddle(grid , "shrink")

            if self.__type == "fast_ball":
                if obj.get_yspeed() > 0:
                    obj.set_yspeed(obj.get_yspeed() - 1)
                if obj.get_yspeed() < 0:
                    obj.set_yspeed(obj.get_yspeed() + 1)

            if self.__type == "ball_multiplier":
                if len(obj) > 1:
                    for i in range(int(len(obj)/2) , len(obj)):
                        obj[i].remove_ball(grid)
                        del obj[i]
                    
                    obj = obj[:len(obj) - int(len(obj)/2)]

            if self.__type == "thru_ball":
                for j in range(0 , len(obj)):
                    obj[j].set_type('normal')

            if self.__type == "paddle_grab":
                obj.set_xspeed(obj.storage_xspeed)
                obj.set_yspeed(-1*abs(obj.storage_yspeed))

            self.__active = -1
            delete_powerup(self)
            return

        elif new_y >= HEIGHT-PADDLE_POS_Y and paddle.get_x() <= self.__x and paddle.get_x() + paddle.get_length() >= self.__x and self.__active == 0:
            self.__active = 1
            return

        elif ((new_y > HEIGHT - PADDLE_POS_Y or new_y < 0) and self.__active == 0):
            delete_powerup(self)
            self.__active == -1
            return

        elif self.__active != 0:
            self.make_change(grid , obj , paddle)
            self.__active = 2
            return

        self.__y = new_y
        grid[self.__y][self.__x] = self.__shape

    def make_change(self, grid , obj , paddle):

        if self.__active == 1:
            if self.__type == "expand_paddle":
                obj.update_shape(grid , "expand")

            elif self.__type == "shrink_paddle":
                obj.update_shape(grid , "shrink")

            elif self.__type == "fast_ball":
                if obj.get_yspeed() > 0:
                    obj.set_yspeed(obj.get_yspeed() + 1)

                if obj.get_yspeed() < 0:
                    obj.set_yspeed(obj.get_yspeed() - 1)
            
            elif self.__type == "ball_multiplier":
                ball_len = len(obj)
                for _ in range(0 , ball_len):
                    obj.append(Ball(np.random.randint(40 , 50) , np.random.randint(20 , 30)))

            elif self.__type == "thru_ball":
                ball_len = len(obj)
                for j in range(0 , ball_len):
                    obj[j].set_type('thru')

            elif self.__type == "paddle_grab":
                obj.set_storage(obj.get_xspeed() , obj.get_yspeed())
                grid[obj.get_y()][obj.get_x()] = ' '
                obj.set_x(paddle.get_x() + int(paddle.get_length()/2) + obj.get_xspeed())
                obj.set_y(paddle.get_y() - 2)
                obj.set_xspeed(0)
                obj.set_yspeed(0)
                paddle.move_ball = 1

    def relaunch_paddle(self , paddle , obj):
        paddle.move_ball = 0
        obj.set_xspeed(obj.get_x_storage())
        obj.set_yspeed(-1*abs(obj.get_y_storage()))
        delete_powerup(self)




            