from headers import *
import numpy as np
from object import *
from colorama import Fore, Back, Style
from ball import *
import time

class Powerup:

    def __init__(self , START_X , START_Y , powerup):
        self.x = START_X
        self.y = HEIGHT - START_Y
        self.type = powerup
        self.yspeed = -2
        self.shape = 'P'
        self.active = 0
        self.start_time = time.time()
        self.time_limit = 15

    def render_powerup(self , grid):
        grid[self.y][self.x] = self.shape

    def isactive(self):
        return self.active

    def get_type(self):
        return self.type

    def delete(self , obj , grid , paddle):

        grid[self.y][self.x] = " "
        grid[self.y + 2][self.x] = " "

        if self.active == 0:
            self.active = -1
            return

        if self.type == "expand_paddle" and self.active == 2:
            obj.reshape_paddle(grid , "expand")

        if self.type == "shrink_paddle" and self.active == 2:
            obj.reshape_paddle(grid , "shrink")

        if self.type == "fast_ball" and self.active == 2:
            if obj.get_yspeed() > 0:
                obj.set_yspeed(obj.get_yspeed() - 2)

            if obj.get_yspeed() < 0:
                obj.set_yspeed(obj.get_yspeed() + 2)

        if self.type == "ball_multiplier" and self.active == 2:
            if len(obj) > 1:
                for i in range(int(len(obj)/2) , len(obj)):
                    grid[obj[i].get_y()][obj[i].get_x()] = ' '
                    del obj[i]
                    
                obj = obj[:len(obj) - int(len(obj)/2)]

        self.active = -1

    def move_powerup(self , grid , obj , paddle):
        grid[self.y][self.x] = ' '
        new_y = self.y + 3
        if (self.active == 2 and time.time() - self.start_time >= self.time_limit):
            if self.type == "expand_paddle":
                obj.reshape_paddle(grid , "expand")

            if self.type == "shrink_paddle":
                obj.reshape_paddle(grid , "shrink")

            if self.type == "fast_ball":
                if obj.get_yspeed() > 0:
                    obj.set_yspeed(obj.get_yspeed() - 2)
                if obj.get_yspeed() < 0:
                    obj.set_yspeed(obj.get_yspeed() + 2)

            if self.type == "ball_multiplier":
                if len(obj) > 1:
                    ind = []
                    for i in range(int(len(obj)/2) , len(obj)):
                        grid[obj[i].get_y()][obj[i].get_x()] = ' '
                        ind.append(i)
                    ind_len = len(ind)
                    for i in range(0 , ind_len):
                        grid[obj[len(ind) - 1].get_y()][obj[len(ind) - 1].get_x()] = ' '
                        del obj[len(ind) - 1]
                        
            self.active = -1
            delete_powerup(self)
            return

        elif new_y >= HEIGHT-PADDLE_POS_Y and paddle.get_x() <= self.x and paddle.get_x() + paddle.get_length() >= self.x and self.active == 0:
            self.active = 1
            return

        elif ((new_y > HEIGHT - PADDLE_POS_Y or new_y < 0) and self.active == 0):
            delete_powerup(self)
            self.active = -1
            return

        elif self.active != 0:
            self.make_change(grid , obj , paddle)
            self.active = 2
            return

        if self.active != -1:
            self.y = new_y
            grid[self.y][self.x] = self.shape

    def make_change(self, grid , obj , paddle):

        if self.active == 1:
            if self.type == "expand_paddle":
                obj.update_shape(grid , "expand")

            elif self.type == "shrink_paddle":
                obj.update_shape(grid , "shrink")

            elif self.type == "fast_ball":
                if obj.get_yspeed() > 0:
                    obj.set_yspeed(obj.get_yspeed() + 2)

                if obj.get_yspeed() < 0:
                    obj.set_yspeed(obj.get_yspeed() - 2)
            
            elif self.type == "ball_multiplier":
                ball_len = len(obj)
                for _ in range(0 , ball_len):
                    obj.append(Ball(np.random.randint(40 , 50) , 24))

class paddleGrab(Powerup):

    def __init__(self , START_X , START_Y , powerup):
        super(paddleGrab , self).__init__(START_X , START_Y , powerup)
        self.time_limit = 8

    def delete(self , obj , grid , paddle):
        grid[self.y][self.x] = " "
        grid[self.y + 2][self.x] = " "

        if self.active == -1:
            return 
        if self.active == 0:
            self.active = -1
            return
            
        obj.set_xspeed(obj.storage_xspeed)
        obj.set_yspeed(-1*abs(obj.storage_yspeed))
        paddle.move_ball = 0
        if self.active == 0:
            grid[self.y][self.x] = ' '

        delete_powerup(self)

    def move_powerup(self , grid , obj , paddle):
        grid[self.y][self.x] = ' '
        new_y = self.y + 3

        if self.active == -1:
            return

        if (self.active == 2 and time.time() - self.start_time >= self.time_limit):
            paddle.move_ball = 0
            self.active = -1
            delete_powerup(self)
            return


        elif new_y >= HEIGHT-PADDLE_POS_Y and paddle.get_x() <= self.x and paddle.get_x() + paddle.get_length() >= self.x and self.active == 0:
            self.active = 1
            return

        elif ((new_y > HEIGHT - PADDLE_POS_Y or new_y < 0) and self.active == 0):
            delete_powerup(self)
            self.active == -1
            return

        elif self.active != 0:
            self.make_change(grid , obj , paddle)
            self.active = 2
            return

        self.y = new_y
        grid[self.y][self.x] = self.shape

    def make_change(self, grid , obj , paddle):

        if self.active == 1:
            obj.set_storage(obj.get_xspeed() , obj.get_yspeed())
            grid[obj.get_y()][obj.get_x()] = ' '
            obj.set_x(paddle.get_x() + int(paddle.get_length()/2) + obj.get_xspeed())
            if paddle.get_y() < 10:
                obj.set_y(HEIGHT - paddle.get_y() - 1)
            elif paddle.get_y() > 30:
                obj.set_y(paddle.get_y() - 1)
            obj.set_xspeed(0)
            obj.set_yspeed(0)
            paddle.move_ball = 1

    def relaunch_paddle(self , paddle , obj):
        paddle.move_ball = 0
        obj.set_xspeed(obj.get_x_storage())
        obj.set_yspeed(-1*abs(obj.get_y_storage()))
        delete_powerup(self)
        self.active = -1

class thruBall(Powerup):

    def __init__(self , START_X , START_Y , powerup):
        super(thruBall , self).__init__(START_X , START_Y , powerup)
        self.time_limit = 15

    def delete(self , obj , grid , paddle):
        grid[self.y][self.x] = " "
        grid[self.y + 2][self.x] = " "

        if self.active == 0:
            self.active = -1
            return

        for j in range(0 , len(obj)):
            obj[j].set_type('normal')
        
        delete_powerup(self)

    def move_powerup(self , grid , obj , paddle):
        grid[self.y][self.x] = ' '
        new_y = self.y + 3
        if (self.active == 2 and time.time() - self.start_time >= self.time_limit):
            for j in range(0 , len(obj)):
                obj[j].set_type('normal')
            self.active = -1
            delete_powerup(self)
            return

        elif new_y >= HEIGHT-PADDLE_POS_Y and paddle.get_x() <= self.x and paddle.get_x() + paddle.get_length() >= self.x and self.active == 0:
            self.active = 1
            return

        elif ((new_y > HEIGHT - PADDLE_POS_Y or new_y < 0) and self.active == 0):
            delete_powerup(self)
            self.active == -1
            return

        elif self.active != 0:
            self.make_change(grid , obj , paddle)
            self.active = 2
            return

        

        self.y = new_y
        grid[self.y][self.x] = self.shape

    def make_change(self, grid , obj , paddle):
        ball_len = len(obj)
        for j in range(0 , ball_len):
            obj[j].set_type('thru')

