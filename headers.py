import numpy as np

HEIGHT = 44
WIDTH = 90
PADDLE_POS_Y = 2
PADDLE_POS_X = 35
PADDLE_SIZE = 10
BALL_POS_Y = 3
BALL_POS_X = int(PADDLE_POS_X + PADDLE_SIZE/2)
BRICK_LEVEL_1_NO = 4
BRICK_LEVEL_2_NO = 3
BRICK_LEVEL_3_NO = 1
BRICK_LEVEL_4_NO = 8
BRICK_START_Y_1 = 42
BRICK_START_X_1 = [23]
BRICK_START_Y_2 = 32
BRICK_START_X_2 = [21]
BRICK_START_Y_3 = 19
BRICK_START_X_3 = [31]
BRICK_START_Y_4 = 28
BRICK_START_X_4 = [15]
UNBREAKABLE_X = 5
UNBREAKABLE_Y = 42
powerup_class = []
powerup_types = ["ball_multiplier" , "thru_ball" , "paddle_grab" , "expand_paddle" , "shrink_paddle" , "fast_ball"]

def set_brick_level_1(val):
    global BRICK_LEVEL_1_NO
    BRICK_LEVEL_1_NO = val

def set_brick_level_2(val):
    global BRICK_LEVEL_2_NO
    BRICK_LEVEL_2_NO = val

def set_brick_level_3(val):
    global BRICK_LEVEL_3_NO
    BRICK_LEVEL_3_NO = val

def set_brick_level_4(val):
    global BRICK_LEVEL_4_NO
    BRICK_LEVEL_4_NO = val

def update_powerup(powerup , grid):
    global powerup_class
    powerup.render_powerup(grid)
    powerup_class.append(powerup)

def get_powerup():
    global powerup_class
    return powerup_class

def delete_powerup(powerup):
    global powerup_class
    powerup_class.remove(powerup)

def set_powerup():
    global powerup_class
    powerup_class = []

def on_clear(powerup , obj , grid , paddle):
    global powerup_class
    grid[powerup.y][powerup.x] = ' '

def explode(brick_level , grid , i , visited):
    if visited[i]:
        return
    if i<0 or i>BRICK_LEVEL_4_NO-1:
        return

    visited[i] = 1
    if brick_level[i].get_y() != 'Nan' and brick_level[i].get_x() != 'Nan':
        brick_level[i].clear_brick(grid)
        brick_level[i].set_x('Nan')
        brick_level[i].set_y('Nan')
        brick_level[i].kill()

    if i-1 >= 0:
        if brick_level[i-1].get_y() != 'Nan' and brick_level[i-1].get_x() != 'Nan':
            brick_level[i-1].clear_brick(grid)
            brick_level[i-1].set_x('Nan')
            brick_level[i-1].set_y('Nan')
        if brick_level[i-1].get_lives() == 5 and visited[i-1] == 0:
            explode(brick_level , grid , i-1 , visited)

    if i+1 <= BRICK_LEVEL_4_NO-1 :
        if brick_level[i+1].get_y() != 'Nan' and brick_level[i+1].get_x() != 'Nan':
            brick_level[i+1].clear_brick(grid)
            brick_level[i+1].set_x('Nan')
            brick_level[i+1].set_y('Nan')
        if brick_level[i+1].get_lives() == 5 and visited[i+1] == 0:
            explode(brick_level , grid , i+1 , visited)


    return
    

for i in range(1,BRICK_LEVEL_1_NO):
    BRICK_START_X_1.append(BRICK_START_X_1[i-1] + 15)

for i in range(1,BRICK_LEVEL_2_NO):
    BRICK_START_X_2.append(BRICK_START_X_2[i-1] + 15)

for i in range(1,BRICK_LEVEL_3_NO):
    BRICK_START_X_3.append(BRICK_START_X_3[i-1] + 15)

for i in range(1,BRICK_LEVEL_4_NO-2):
    BRICK_START_X_4.append(BRICK_START_X_4[i-1] + 8)


welcome = '''
██     ██ ███████ ██       ██████  ██████  ███    ███ ███████ 
██     ██ ██      ██      ██      ██    ██ ████  ████ ██      
██  █  ██ █████   ██      ██      ██    ██ ██ ████ ██ █████   
██ ███ ██ ██      ██      ██      ██    ██ ██  ██  ██ ██      
 ███ ███  ███████ ███████  ██████  ██████  ██      ██ ███████ 
                                                              
                                                                 '''

lost = '''

██       ██████  ███████ ████████ 
██      ██    ██ ██         ██    
██      ██    ██ ███████    ██    
██      ██    ██      ██    ██    
███████  ██████  ███████    ██    
                                  
                                       
                                           
                                           '''

won = '''

██     ██ ██ ███    ██ ██ 
██     ██ ██ ████   ██ ██ 
██  █  ██ ██ ██ ██  ██ ██ 
██ ███ ██ ██ ██  ██ ██    
 ███ ███  ██ ██   ████ ██ 
                          
                            '''

def start_game():
    print(welcome)  

def game_over():
    print(lost)

def win():
    print(win)
