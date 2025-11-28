#Steven Everett Chris Bradly
"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""

from random import * #BK: This is for random ghost movement
from turtle import * #BK: Turtle Graphic
from freegames import floor, vector #BK: Vector math + grid allignment from freegames

# ---------------------- GAME SETTINGS ----------------------
SPEED = 5  # BK: Change this number to make Pacman faster or slower
ghost_SPEED = 5

freeze_active = False
ghost_colour = 'red'

# ---------------------- GAME STATE ------------------------
score_ = {'score': 0} #BK: display the score as zero when the game starts

game_over_flag = False

# ---------------------- TURTLE SETUP ---------------------
path = Turtle(visible=False)   # For drawing maze
writer = Turtle(visible=False) # For showing score

# Pacman starting position and direction
pacman = vector(-40, -80) #BK: pacman's direction of movement
pacman_dir = vector(SPEED, 0)  # Uses SPEED variable #BK: this is where the pacman start(starting position)

# Ghosts with starting positions and directions
ghosts = [
    [vector(-180, 160), vector(ghost_SPEED, 0)],
    [vector(-180, -160), vector(0, ghost_SPEED)],
    [vector(100, 160), vector(0, -ghost_SPEED)],
    [vector(100, -160), vector(-ghost_SPEED, 0)],
]

# ---------------------- MAP ------------------------------
#BK: Make a map 20 by 20 grid using 0 which is a wall, and 1 which is the tile
tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

tiles_copy = tiles.copy()

#----------------------ADDING POWERUP-------------------------
#CJ: choose a random spot to be a speed powerup
def create_powerups():
    randomtile = 0
    while True:
        randomtile = randint(0,len(tiles)-1) #CJ: gets random index from the list
        if tiles[randomtile] == 1: #CJ: makes sure its not a wall
            tiles[randomtile] = 3
            
            x = (randomtile % 20) * 20 - 200
            y = 180 - (randomtile // 20) * 20

            path.up()
            path.goto(x + 10, y + 10)
            path.dot(8, 'cyan')
               
            break
        
create_powerups()

def unfreeze_ghosts():
    global freeze_active,ghost_colour
    
    ghost_colour = 'red'
    freeze_active = False
    create_powerups()
    

def freeze_ghosts(time=8000):
    global freeze_active,ghost_colour
    
    freeze_active = True
    ghost_colour = 'cyan'
    ontimer(unfreeze_ghosts,time)

# ---------------------- DRAWING FUNCTIONS -----------------
def square(x, y): 
    path.up() 
    path.goto(x, y) 
    path.down() 
    path.begin_fill()
    path.forward(20)
    path.left(90) 
    path.forward(20)
    path.left(90)
    path.forward(20)
    path.left(90)
    path.forward(20)
    path.left(90)
    path.end_fill() 

def offset(point): 
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
    index = offset(point)
    if tiles[index] == 0:
        return False
    index = offset(vector(point.x + 19, point.y + 19))
    if tiles[index] == 0:
        return False
    if point.x % 20 == 0 or point.y % 20 == 0:
        return True
    else:
        return False

def world(): 
    bgcolor('black')  
    path.color('blue') 
    for index in range(len(tiles)): 
        tile = tiles[index] 
        if tile > 0: 
            x = (index % 20) * 20 - 200  
            y = 180 - (index // 20) * 20  
            square(x, y) 
            if tile == 1: 
                path.up()
                path.goto(x + 10, y + 10) 
                path.dot(2, 'white') 
                
            if tile == 3:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(8, 'cyan') 

# ---------------------- GAME OVER -------------------------
def game_over():
    global game_over_flag
    game_over_flag = True
    path.up()
    path.goto(-100, 0)
    path.color('white')
    path.write("GAME OVER!", font=("Arial", 20, "bold"))
    path.goto(-100, -30)
    path.write("Press R to restart or Q to quit", font=("Arial", 12, "normal"))
    listen()
    onkey(restart, "r")
    onkey(exit_game, "q")
    
def win():
    global game_over_flag
    game_over_flag = True
    path.up()
    path.goto(-100, 0)
    path.color('white')
    path.write("YOU WON!", font=("Arial", 20, "bold"))
    path.goto(-100, -30)
    path.write("Press R to restart or Q to quit", font=("Arial", 12, "normal"))
    listen()
    onkey(restart, "r")
    onkey(exit_game, "q")


def restart():
    """Restart the game"""
    global game_over_flag, pacman, pacman_dir, ghosts, score_, tiles, tiles_copy
    if game_over_flag:
        path.clear()  # Remove Game Over text
        game_over_flag = False
        score_['score'] = 0
        writer.clear()
        writer.goto(160, 160)
        writer.write(score_['score'])

        # Reset Pacman to starting position and full speed
        pacman.x = -40
        pacman.y = -80
        pacman_dir.x = SPEED
        pacman_dir.y = 0

        # Reset ghosts to starting positions and full speed
        ghosts[0][0].x = -180
        ghosts[0][0].y = 160
        ghosts[0][1].x = ghost_SPEED
        ghosts[0][1].y = 0

        ghosts[1][0].x = -180
        ghosts[1][0].y = -160
        ghosts[1][1].x = 0
        ghosts[1][1].y = ghost_SPEED

        ghosts[2][0].x = 100
        ghosts[2][0].y = 160
        ghosts[2][1].x = 0
        ghosts[2][1].y = ghost_SPEED

        ghosts[3][0].x = 100
        ghosts[3][0].y = -160
        ghosts[3][1].x = ghost_SPEED
        ghosts[3][1].y = 0

        # Reset map
        tiles = tiles_copy
        
        for i in range(len(tiles)):
            if tiles[i] != 0:
                tiles[i] = 1
            
        create_powerups()
        
        world()
        move()
    

def exit_game():
    bye()

# ---------------------- GAME LOOP -------------------------
def move(): 
    writer.undo() 
    writer.write(score_['score']) 
    clear() 
    
    if valid(vector(pacman.x + pacman_dir.x, pacman.y + pacman_dir.y)): 
        pacman.x = pacman.x + pacman_dir.x  
        pacman.y = pacman.y + pacman_dir.y  
    
    index = offset(pacman) 
    if tiles[index] == 1:  
        tiles[index] = 2  
        score_['score'] = score_['score'] + 1  
        x = (index % 20) * 20 - 200  
        y = 180 - (index // 20) * 20
        square(x, y)
        
    if tiles[index] == 3:
        tiles[index] = 2   # remove power-up
        x = (index % 20) * 20 - 200  
        y = 180 - (index // 20) * 20
        square(x, y)
        freeze_ghosts()
    
    up()  
    goto(pacman.x + 10, pacman.y + 10) 
    dot(20, 'yellow')  
    
    for ghost in ghosts:  
        point = ghost[0] 
        course = ghost[1] 
        
        if not freeze_active:
            if valid(vector(point.x + course.x, point.y + course.y)): 
                point.x = point.x + course.x 
                point.y = point.y + course.y
            else:
                plan = choice([vector(ghost_SPEED,0), vector(-ghost_SPEED,0), vector(0,ghost_SPEED), vector(0,-ghost_SPEED)]) 
                course.x = plan.x 
                course.y = plan.y
                
        up() 
        goto(point.x + 10, point.y + 10)  
        dot(20, ghost_colour) 
    
    update() 
    
    for ghost in ghosts: 
        point = ghost[0] 
        if abs(pacman.x - point.x) < 20 and abs(pacman.y - point.y) < 20: 
            game_over() 
            return 
    pellets_remaining = False
    for tile in tiles:
        if tile == 1:
            pellets_remaining = True
            break
     
    if not pellets_remaining:
         win()
         return
    
    ontimer(move, 20) 

# ---------------------- CONTROLS -------------------------
def change(x, y):
    if valid(vector(pacman.x + x, pacman.y + y)):
        pacman_dir.x = x
        pacman_dir.y = y

# ---------------------- INITIALIZE -----------------------
setup(470, 450, 450, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(score_['score'])
listen()
onkey(lambda: change(SPEED,0), "Right")
onkey(lambda: change(-SPEED,0), "Left")
onkey(lambda: change(0,SPEED), "Up")
onkey(lambda: change(0,-SPEED), "Down")
world()
move()
done()
