from headers import *
import numpy as np
from object import *
from colorama import Fore, Back, Style
from powerup import *

class Brick(Object):

    def __init__(self , POS_X , POS_Y , lives):
        '''
        Initialise positions of the brick
        '''
        super(Brick, self).__init__(POS_X , HEIGHT - POS_Y)
        self.__lives = lives
        self.__color = Fore.BLACK
        self.__type = 'normal'
        if lives == 3:
            self.__color = Back.GREEN
        elif lives == 2:
            self.color = Back.YELLOW
        elif lives == 1:
            self.color = Back.BLACK
        elif lives == 4:
            self.color = Back.MAGENTA
        elif lives == 5:
            self.color = Back.RED
        self.brick = list((
                ("++++++++"),
                ("++++++++"),
                ("++++++++")
        ))
        if lives == 5:
            self.brick = list((
                ("EEEEEEEE"),
                ("EEEEEEEE")
            ))
        self.__score = lives*10

    def change_lives(self):
        if self.__lives == 4 or self.__lives == 5:
            return
        self.__lives = self.__lives - 1
        if self.__lives == 2:
            self.__color = Back.YELLOW
        elif self.__lives == 1:
            self.__color = Back.BLACK

    def rainbow_live(self):
        self.__lives = np.random.randint(1,4)
        
    def update_brick(self):
         self.brick = list((
                ("±±±±±±±±"),
                ("|  "+str(self.__lives)+"   |"),
                ("±±±±±±±±")
        ))  
    
    def kill(self):
        del self

    def get_type(self):
        return self.__type
    
    def set_type(self , val):
        self.__type = val

    def get_lives(self):
        return self.__lives

    def check_out(self , paddle):
        if self.get_x() == 'Nan' or self.get_y() == 'Nan':
            return -2
        if HEIGHT - 2 - self.get_y() <= 2:
            return -1
        return -2

    def bring_down(self):
        if self.get_x() != 'Nan' and self.get_y() != 'Nan':
            self.set_y(self.get_y() + 1)

    def render_brick(self , grid):
        '''
        Render the brick on the screen
        '''
        if self.get_x() == 'Nan' and self.get_y() == 'Nan':
            return
        
        self.update_brick()
        for i in range(0 , len(self.brick)):
            for j in range(0 , len(self.brick[0])):
                grid[self.get_y() + i][self.get_x() + j] = self.__lives

    def clear_brick(self , grid):
        '''
        Clear brick from area
        '''
        if self.get_y() == 'Nan' or self.get_x() == 'Nan':
            return
        for i in range(0 , len(self.brick)):
            for j in range(0 , len(self.brick[0])):
                grid[self.get_y() + i][self.get_x() + j] = ' '

    def set_to_nan(self):
        self.set_x('Nan')
        self.set_y('Nan')

    def brick_ball_collisions(self , ball , grid , player , pos , brick_level , balls):
        '''
        Check for brick ball collissions
        '''
        x = 0
        if self.get_x() == 'Nan' and self.get_y() == 'Nan':
            return

        if ball.get_y() - self.get_y() - len(self.brick) <= abs(ball.get_yspeed()) and ball.get_y() - self.get_y() - len(self.brick) >= 0 and self.get_x() <= ball.get_x() and self.get_x() + len(self.brick[0]) >= ball.get_x() and ball.get_yspeed() < 0:
            '''
            Invert the ball in -y direction
            '''
            if ball.get_type() == "shooting":
                balls.remove(ball)
                grid[ball.get_y()][ball.get_x()] = ' '
            if ball.get_type() != "shooting":
                self.set_type('normal')
            x = 1
            player.set_score(player.get_score() + self.__score)
            self.change_lives()
            if self.__lives == 5:
                visited = np.zeros(BRICK_LEVEL_4_NO)
                explode(brick_level , grid , pos , visited)
            if self.__lives <= 0 or ball.get_type() == 'thru':
                if ball.get_type() == 'thru':
                    player.set_score(player.get_score() + self.__score * 2)
                self.clear_brick(grid)
                choice = np.random.choice(powerup_types)
                if choice == 'paddle_grab':
                    update_powerup(paddleGrab(self.get_x() , self.get_y() , "paddle_grab" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                elif choice == 'thru_ball':
                    update_powerup(thruBall(self.get_x() , self.get_y() , "thru_ball" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                else:
                    update_powerup(Powerup(self.get_x() , self.get_y() , choice , ball.get_yspeed() , ball.get_xspeed()) , grid)
                self.set_x('Nan')
                self.set_y('Nan')
                self.kill()
            ball.set_yspeed(-1*ball.get_yspeed())

        elif ((self.get_x() - ball.get_x() >= 0 and self.get_x() - ball.get_x() <= 2) or (ball.get_x() - self.get_x() - len(self.brick[0]) >=0 and ball.get_x() - self.get_x() - len(self.brick[0]) <= 2))  and self.get_y() <= ball.get_y() and self.get_y() + len(self.brick) >= ball.get_y():
            x = 3
            if ball.get_type() == "shooting":
                balls.remove(ball)
                grid[ball.get_y()][ball.get_x()] = ' '
            if ball.get_type() != "shooting":
                self.set_type('normal')
            player.set_score(player.get_score() + self.__score)
            self.change_lives()
            if self.__lives == 5:
                visited = np.zeros(BRICK_LEVEL_4_NO)
                explode(brick_level , grid , pos , visited)
            if self.__lives <= 0 or ball.get_type() == 'thru':
                if ball.get_type() == 'thru':
                    player.set_score(player.get_score() + self.__score * 2)
                self.clear_brick(grid)
                choice = np.random.choice(powerup_types)
                if choice == 'paddle_grab':
                    update_powerup(paddleGrab(self.get_x() , self.get_y() , "paddle_grab" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                elif choice == 'thru_ball':
                    update_powerup(thruBall(self.get_x() , self.get_y() , "thru_ball" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                else:
                    update_powerup(Powerup(self.get_x() , self.get_y() , choice , ball.get_yspeed() , ball.get_xspeed()) , grid)
                self.set_x('Nan')
                self.set_y('Nan')
                self.kill()
            ball.set_yspeed(-1*ball.get_yspeed())

        elif ball.get_y() - self.get_y() >= -1*ball.get_yspeed() and ball.get_y() - self.get_y() <= 0 and self.get_x() <= ball.get_x() and self.get_x() + len(self.brick[0]) >= ball.get_x() and ball.get_yspeed() > 0:
            '''
            Invert the ball in +y direction
            '''
            if ball.get_type() == "shooting":
                balls.remove(ball)
                grid[ball.get_y()][ball.get_x()] = ' '
            if ball.get_type() != "shooting":
                self.set_type('normal')
            x = 2
            player.set_score(player.get_score() + self.__score)
            self.change_lives()
            if self.__lives == 5:
                visited = np.zeros(BRICK_LEVEL_4_NO)
                explode(brick_level , grid , pos , visited)
            if self.__lives <= 0 or ball.get_type() == 'thru':
                if ball.get_type() == 'thru':
                    player.set_score(player.get_score() + self.__score * 2)
                self.clear_brick(grid)
                choice = np.random.choice(powerup_types)
                if choice == 'paddle_grab':
                    update_powerup(paddleGrab(self.get_x() , self.get_y() , "paddle_grab" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                elif choice == 'thru_ball':
                    update_powerup(thruBall(self.get_x() , self.get_y() , "thru_ball" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                else:
                    update_powerup(Powerup(self.get_x() , self.get_y() , choice , ball.get_yspeed() , ball.get_xspeed()) , grid)
                self.set_x('Nan')
                self.set_y('Nan')
                self.kill()
            ball.set_yspeed(-1*ball.get_yspeed())

        elif (((self.get_y() + len(self.brick) - ball.get_y() <= 1 and self.get_y() + len(self.brick) - ball.get_y() >= 0)) and (abs(self.get_x() - ball.get_x()) <=1 or abs(ball.get_x() - self.get_x() - len(self.brick[0])) <= 1) and ball.get_yspeed() > 0):
            '''
            Deflect in x axis
            '''
            if ball.get_type() == "shooting":
                balls.remove(ball)
                grid[ball.get_y()][ball.get_x()] = ' '
            if ball.get_type() != "shooting":
                self.set_type('normal')
            x = 4
            player.set_score(player.get_score() + self.__score)
            self.change_lives()
            if self.__lives == 5:
                visited = np.zeros(BRICK_LEVEL_4_NO)
                explode(brick_level , grid , pos , visited)
            if self.__lives <= 0 or ball.get_type() == 'thru':
                if ball.get_type() == 'thru':
                    player.set_score(player.get_score() + self.__score * 2)
                self.clear_brick(grid)
                choice = np.random.choice(powerup_types)
                if choice == 'paddle_grab':
                    update_powerup(paddleGrab(self.get_x() , self.get_y() , "paddle_grab" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                elif choice == 'thru_ball':
                    update_powerup(thruBall(self.get_x() , self.get_y() , "thru_ball" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                else:
                    update_powerup(Powerup(self.get_x() , self.get_y() , choice , ball.get_yspeed() , ball.get_xspeed()) , grid)
                self.set_x('Nan')
                self.set_y('Nan')
                self.kill()
            ball.set_yspeed(-1*ball.get_yspeed())

        
        elif (((self.get_y() - ball.get_y() <= 1 and self.get_y() - ball.get_y() >= 0)) and (abs(self.get_x() - ball.get_x()) <=1 or abs(ball.get_x() - self.get_x() - len(self.brick[0])) <= 1) and ball.get_yspeed() > 0):
            '''
            Deflect in y axis
            '''
            if ball.get_type() == "shooting":
                balls.remove(ball)
                grid[ball.get_y()][ball.get_x()] = ' '
            if ball.get_type() != "shooting":
                self.set_type('normal')
            x = 5
            player.set_score(player.get_score() + self.__score)
            self.change_lives()
            if self.__lives == 5:
                visited = np.zeros(BRICK_LEVEL_4_NO)
                explode(brick_level , grid , pos , visited)
            if self.__lives <= 0 or ball.get_type() == 'thru':
                if ball.get_type() == 'thru':
                    player.set_score(player.get_score() + self.__score * 2)
                self.clear_brick(grid)
                choice = np.random.choice(powerup_types)
                if choice == 'paddle_grab':
                    update_powerup(paddleGrab(self.get_x() , self.get_y() , "paddle_grab" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                elif choice == 'thru_ball':
                    update_powerup(thruBall(self.get_x() , self.get_y() , "thru_ball" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                else:
                    update_powerup(Powerup(self.get_x() , self.get_y() , choice , ball.get_yspeed() , ball.get_xspeed()) , grid)
                self.set_x('Nan')
                self.set_y('Nan')
                self.kill()
            ball.set_yspeed(-1*ball.get_yspeed())

        elif (((ball.get_y() - self.get_y() - len(self.brick) <= 2) and (ball.get_y() - self.get_y() - len(self.brick) >= 0)) and (abs(self.get_x() - ball.get_x()) <=1 or abs(ball.get_x() - self.get_x() - len(self.brick[0])) <= 1) and ball.get_yspeed() < 0):
            '''
            Deflect in y axis
            '''
            if ball.get_type() == "shooting":
                balls.remove(ball)
                grid[ball.get_y()][ball.get_x()] = ' '
            if ball.get_type() != "shooting":
                self.set_type('normal')
            x = 6
            player.set_score(player.get_score() + self.__score)
            self.change_lives()
            if self.__lives == 5:
                visited = np.zeros(BRICK_LEVEL_4_NO)
                explode(brick_level , grid , pos , visited)
            if self.__lives <= 0 or ball.get_type() == 'thru':
                if ball.get_type() == 'thru':
                    player.set_score(player.get_score() + self.__score * 2)
                self.clear_brick(grid)
                choice = np.random.choice(powerup_types)
                if choice == 'paddle_grab':
                    update_powerup(paddleGrab(self.get_x() , self.get_y() , "paddle_grab" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                elif choice == 'thru_ball':
                    update_powerup(thruBall(self.get_x() , self.get_y() , "thru_ball" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                else:
                    update_powerup(Powerup(self.get_x() , self.get_y() , choice , ball.get_yspeed() , ball.get_xspeed()) , grid)
                self.set_x('Nan')
                self.set_y('Nan')
                self.kill()
            ball.set_yspeed(-1*ball.get_yspeed())

        elif (((ball.get_y() - self.get_y() <= 2) and (ball.get_y() - self.get_y()  >= 0)) and (abs(ball.get_x() - self.get_x() - len(self.brick[0])) <= 1) and ball.get_yspeed() < 0):
            if ball.get_type() == "shooting":
                balls.remove(ball)
                grid[ball.get_y()][ball.get_x()] = ' '
            if ball.get_type() != "shooting":
                self.set_type('normal')
            player.set_score(player.get_score() + self.__score)
            self.change_lives()
            if self.__lives == 5:
                visited = np.zeros(BRICK_LEVEL_4_NO)
                explode(brick_level , grid , pos , visited)
            if self.__lives <= 0 or ball.get_type() == 'thru':
                if ball.get_type() == 'thru':
                    player.set_score(player.get_score() + self.__score * 2)
                self.clear_brick(grid)
                choice = np.random.choice(powerup_types)
                if choice == 'paddle_grab':
                    update_powerup(paddleGrab(self.get_x() , self.get_y() , "paddle_grab" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                elif choice == 'thru_ball':
                    update_powerup(thruBall(self.get_x() , self.get_y() , "thru_ball" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                else:
                    update_powerup(Powerup(self.get_x() , self.get_y() , choice , ball.get_yspeed() , ball.get_xspeed()) , grid)
                self.set_x('Nan')
                self.set_y('Nan')
                self.kill()
            ball.set_yspeed(-1*ball.get_yspeed())

        elif ((self.get_y() - ball.get_y() <= abs(ball.get_yspeed()) and self.get_y() - ball.get_y() >= 0 and self.get_x() <= ball.get_x() and self.get_x() + len(self.brick[0]) >= ball.get_x())):
            if ball.get_type() == "shooting":
                balls.remove(ball)
                grid[ball.get_y()][ball.get_x()] = ' '
            if ball.get_type() != "shooting":
                self.set_type('normal')
            player.set_score(player.get_score() + self.__score)
            self.change_lives()
            if self.__lives == 5:
                visited = np.zeros(BRICK_LEVEL_4_NO)
                explode(brick_level , grid , pos , visited)
            if self.__lives <= 0 or ball.get_type() == 'thru':
                if ball.get_type() == 'thru':
                    player.set_score(player.get_score() + self.__score * 2)
                self.clear_brick(grid)
                choice = np.random.choice(powerup_types)
                if choice == 'paddle_grab':
                    update_powerup(paddleGrab(self.get_x() , self.get_y() , "paddle_grab" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                elif choice == 'thru_ball':
                    update_powerup(thruBall(self.get_x() , self.get_y() , "thru_ball" , ball.get_yspeed() , ball.get_xspeed()) , grid)
                else:
                    update_powerup(Powerup(self.get_x() , self.get_y() , choice , ball.get_yspeed() , ball.get_xspeed()) , grid)
                self.set_x('Nan')
                self.set_y('Nan')
                self.kill()
            ball.set_yspeed(-1*ball.get_yspeed())
