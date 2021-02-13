HEIGHT = 42
WIDTH = 90
PADDLE_POS_Y = 2
PADDLE_POS_X = 35
PADDLE_SIZE = 10
BALL_POS_Y = 3
BALL_POS_X = int(PADDLE_POS_X + PADDLE_SIZE/2)
BRICK_LEVEL_1_NO = 4
BRICK_LEVEL_2_NO = 2
BRICK_LEVEL_3_NO = 1
BRICK_START_Y_1 = 39
BRICK_START_X_1 = [17]
BRICK_START_Y_2 = 30
BRICK_START_X_2 = [25]
BRICK_START_Y_3 = 20
BRICK_START_X_3 = [33]
powerup_class = []
powerup_types = ["ball_multiplier" , "thru_ball" , "paddle_grab" , "expand_paddle" , "shrink_paddle" , "fast_ball"]

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


def on_clear(powerup , obj , grid , paddle):
    global powerup_class
    powerup_class.remove(powerup)
    powerup.delete(obj , grid , paddle)


for i in range(1,BRICK_LEVEL_1_NO):
    BRICK_START_X_1.append(BRICK_START_X_1[i-1] + 15)

for i in range(1,BRICK_LEVEL_2_NO):
    BRICK_START_X_2.append(BRICK_START_X_2[i-1] + 15)

for i in range(1,BRICK_LEVEL_3_NO):
    BRICK_START_X_3.append(BRICK_START_X_3[i-1] + 15)