from headers import *
import numpy as np
import time
from object import *
from colorama import Fore, Back, Style

class Player:

    def __init__(self):
        self.__lives = 5
        self.__score = 0
        self.__start_time = time.time()

    def set_score(self , new_score):
        self.__score = new_score

    def set_time(self , new_time):
        self.__time = new_time

    def set_lives(self , new_life):
        self.__lives = new_life

    def get_score(self):
        return self.__score

    def get_elapsed_time(self):
        return (time.time() - self.__start_time) 
    
    def get_lives(self):
        return self.__lives
        