#Steven Everett Chris Bradly
"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""

from random import choice #BK: This is for random ghost movement
from turtle import *      #BK: Turtle Graphic

from freegames import floor, vector #BK: Vector math + grid allignment from freegames
SPEED = 5
score_ = {'score': 0} #BK: display the score as zero when the game starts
path = Turtle(visible=False) 
writer = Turtle(visible=False)
pacman_dir = vector(5, 0) #BK: pacman's direction of movement
pacman = vector(-40, -80) #BK: this is where the pacman start(starting position)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
#BK: Make a map 20 by 20 grid using 0 which is a wall and 1 which is the tile
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
#----------------------BK Comment Ends Here------------------------------------
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
    """Return True if point is valid in tiles."""
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
#----------------------ES Comment Ends Here------------------------------------

def world():
    """Draw world using path."""
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
    """Change pacman, pacman_dir if valid."""
    if valid(pacman + vector(x, y)):
        pacman_dir.x = x
        pacman_dir.y = y

# ---------------------- INITIALIZE -----------------------

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(score_['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()
#----------------------CJ Comment Ends Here------------------------------------
