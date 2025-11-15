#Steven Everett Chris Bradly
"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""

from random import choice
from turtle import *
from freegames import floor, vector

# ---------------------- GAME SETTINGS ----------------------
SPEED = 5  # Change this number to make Pacman faster or slower

# ---------------------- GAME STATE ------------------------
score_ = {'score': 0}

# ---------------------- TURTLE SETUP ---------------------
path = Turtle(visible=False)   # For drawing maze
writer = Turtle(visible=False) # For showing score

# Pacman starting position and direction
pacman = vector(-40, -80)
pacman_dir = vector(SPEED, 0)  # Uses SPEED variable

# Ghosts with starting positions and directions
ghosts = [
    [vector(-180, 160), vector(SPEED, 0)],
    [vector(-180, -160), vector(0, SPEED)],
    [vector(100, 160), vector(0, -SPEED)],
    [vector(100, -160), vector(-SPEED, 0)],
]

# ---------------------- MAP ------------------------------
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

# ---------------------- GAME OVER -------------------------
def game_over():
    path.up()
    path.goto(-100, 0)
    path.color('white')
    path.write("GAME OVER!", font=("Arial", 20, "bold"))
    path.goto(-100, -30)
    path.write("Press R to restart or Q to quit", font=("Arial", 12, "normal"))
    listen()
    onkey(restart_game, "r")
    onkey(exit_game, "q")

def restart_game():
    global pacman, pacman_dir, ghosts, score_, tiles
    pacman = vector(-40, -80)
    pacman_dir = vector(SPEED, 0)
    ghosts = [
        [vector(-180, 160), vector(SPEED, 0)],
        [vector(-180, -160), vector(0, SPEED)],
        [vector(100, 160), vector(0, -SPEED)],
        [vector(100, -160), vector(-SPEED, 0)],
    ]
    # Reset tiles manually
    new_tiles = []
    for t in tiles:
        if t == 2:
            new_tiles.append(1)
        else:
            new_tiles.append(t)
    tiles = new_tiles
    score_ = {'score': 0}
    clear()
    writer.clear()
    writer.goto(160, 160)
    writer.color('white')
    writer.write(score_['score'])
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
    
    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')
    
    for ghost in ghosts:
        point = ghost[0]
        course = ghost[1]
        if valid(vector(point.x + course.x, point.y + course.y)):
            point.x = point.x + course.x
            point.y = point.y + course.y
        else:
            plan = choice([vector(SPEED,0), vector(-SPEED,0), vector(0,SPEED), vector(0,-SPEED)])
            course.x = plan.x
            course.y = plan.y
        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')
    
    update()
    
    for ghost in ghosts:
        point = ghost[0]
        if abs(pacman.x - point.x) < 20 and abs(pacman.y - point.y) < 20:
            game_over()
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
