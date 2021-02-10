from headers import *
import numpy as np
from colorama import Fore, Back, Style

class Board:

    def __init__(self , x_dim , y_dim):
        self.__grid = []
        self.__rows = x_dim
        self.__columns = y_dim
        self.render()

    def get_grid(self):
        return self.__grid

    def render(self):
        '''
        Render the grid
        '''
        default = ' '
        matrix = []
        for _ in range(0 , self.__rows):
            self.new_row = []
            for _ in range(0 , self.__columns):
                self.new_row.append(default)
            matrix.append(self.new_row)
        self.__grid = np.array(matrix)

    def display(self):
        '''
        Display the board
        '''
        for i in range(self.__rows):
            for j in range(self.__columns):
                if self.__grid[i][j] == 'O':
                    print(Back.BLACK + self.__grid[i][j],end='')
                elif self.__grid[i][j] == '$' or self.__grid[i][j] == '-':
                    print(Back.RED + self.__grid[i][j],end='')
                elif (self.__grid[i][j] == '±' or self.__grid[i][j] == '|' and self.__grid[i][j] != " "):
                    print(Back.BLACK + self.__grid[i][j],end='')
                else:
                    print(Back.LIGHTBLACK_EX + self.__grid[i][j],end='')
            print(Style.RESET_ALL, end='')
            print()


