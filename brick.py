from headers import *
import numpy as np
from object import *
from colorama import Fore, Back, Style

class Brick(Object):

    def __init__(self , POS_X , POS_Y , lives):
        '''
        Initialise positions of the brick
        '''
        super(Brick, self).__init__(POS_X , HEIGHT - POS_Y)
        self.__lives = lives
        self.brick = list((
                ("±±±±±±±±"),
                ("|  "+str(self.__lives)+"   |"),
                ("±±±±±±±±")
        ))

    def change_lives(self):
        self.__lives = self.__lives - 1

    def update_brick(self):
         self.brick = list((
                ("±±±±±±±±"),
                ("|  "+str(self.__lives)+"   |"),
                ("±±±±±±±±")
        ))  
    
    def kill(self):
        del self

    def render_brick(self , grid):
        '''
        Render the brick on the screen
        '''
        if self.get_x() == 'Nan' and self.get_y() == 'Nan':
            return
        
        self.update_brick()
        for i in range(0 , len(self.brick)):
            for j in range(0 , len(self.brick[0])):
                grid[self.get_y() + i][self.get_x() + j] = self.brick[i][j]

    def clear_brick(self , grid):
        '''
        Clear brick from area
        '''
        for i in range(0 , len(self.brick)):
            for j in range(0 , len(self.brick[0])):
                grid[self.get_y() + i][self.get_x() + j] = ' '

    def brick_ball_collisions(self , ball , grid):
        '''
        Check for brick ball collissions
        '''
        x = 0
        if self.get_x() == 'Nan' and self.get_y() == 'Nan':
            return

        if ball.get_y() - self.get_y() - len(self.brick) <= 2 and ball.get_y() - self.get_y() - len(self.brick) >= 0 and self.get_x() <= ball.get_x() and self.get_x() + len(self.brick[0]) >= ball.get_x() and ball.get_yspeed() < 0:
            '''
            Invert the ball in -y direction
            '''
            x = 1
            ball.set_yspeed(-1*ball.get_yspeed())
            self.change_lives()
            if self.__lives <= 0:
                self.clear_brick(grid)
                self.set_x('Nan')
                self.set_y('Nan')
                self.kill()

        elif ball.get_y() - self.get_y() >= -2 and ball.get_y() - self.get_y() <= 0 and self.get_x() <= ball.get_x() and self.get_x() + len(self.brick[0]) >= ball.get_x() and ball.get_yspeed() > 0:
            '''
            Invert the ball in +y direction
            '''
            x = 2
            ball.set_yspeed(-1*ball.get_yspeed())
            self.change_lives()
            if self.__lives <= 0:
                self.clear_brick(grid)
                self.set_x('Nan')
                self.set_y('Nan')
                self.kill()

        elif ((self.get_x() - ball.get_x() >= 0 and self.get_x() - ball.get_x() <= 2) or (ball.get_x() - self.get_x() - len(self.brick[0]) >=0 and ball.get_x() - self.get_x() - len(self.brick[0]) <= 2))  and self.get_y() <= ball.get_y() and self.get_y() + len(self.brick) >= ball.get_y():
            x = 3
            ball.set_xspeed(-1*ball.get_xspeed())
            self.change_lives()
            if self.__lives <= 0:
                self.clear_brick(grid)
                self.set_x('Nan')
                self.set_y('Nan')
                self.kill()

        print(ball.get_y() , self.get_y() , len(self.brick))




    

    

