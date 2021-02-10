import numpy as np

class Object:

    def __init__(self, POS_X , POS_Y):
        self.__x = POS_X
        self.__y = POS_Y

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def set_x(self , x):
        self.__x = x

    def set_y(self , y):
        self.__y = y
        