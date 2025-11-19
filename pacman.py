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
from turtle import * #BK: Turtle Graphic
from freegames import floor, vector #BK: Vector math + grid allignment from freegames

# ---------------------- GAME SETTINGS ----------------------
SPEED = 5  # BK: Change this number to make Pacman faster or slower

# ---------------------- GAME STATE ------------------------
score_ = {'score': 0} #BK: display the score as zero when the game starts

# ---------------------- TURTLE SETUP ---------------------
path = Turtle(visible=False)   # For drawing maze
writer = Turtle(visible=False) # For showing score

# Pacman starting position and direction
pacman = vector(-40, -80) #BK: pacman's direction of movement
pacman_dir = vector(SPEED, 0)  # Uses SPEED variable #BK: this is where the pacman start(starting position)

# Ghosts with starting positions and directions
ghosts = [
    [vector(-180, 160), vector(SPEED, 0)],
    [vector(-180, -160), vector(0, SPEED)],
    [vector(100, 160), vector(0, -SPEED)],
    [vector(100, -160), vector(-SPEED, 0)],
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

def world(): #SC: The function creates the overall game board for the Pac-Man game, so the maze with its walls, as well as the dots
    bgcolor('black')  #SC: Sets the background color for the game as black
    path.color('blue')  #SC: Sets the maze path color blue to tell the difference between the path and the walls
    for index in range(len(tiles)): #SC: This is a for loop that loops through all the tiles in the map. Since there are 400 tiles in the map, it will loop through this function 400 times
        tile = tiles[index] #SC: Sets a new variable for each specific tile due to the index going through all 400 positions
        if tile > 0: #SC: If statement, if the tile is a one on the map (the 20x20 grid above), also converting the 1D list to a 2D grid postion which is why you need to %20 and //20 to convert to column and row
            x = (index % 20) * 20 - 200  #SC: Since the x-coordinate system works the same in code and in the game, to center the game, the x coordinates need to shift over -200, the *20 converts grid units to pixels
            y = 180 - (index // 20) * 20  #SC: Y-coordinate system for the game is inversely proportional to the computer coordinate system, so that is why you need to inverse it
            square(x, y) #SC: At that postion draws a blue pathway for pac-man to go on to
            if tile == 1: #SC: If statement, if the tile is equal to one which represenets the white pellet/dot
                path.up() #SC: lifts the "pen" or object/turtle's pen so it doesn't draw anything
                path.goto(x + 10, y + 10) #SC: moves the "pen" to the center of the cell
                path.dot(2, 'white') #SC: Draws the white dot/pellet for the Pac-Man to eat

# ---------------------- GAME OVER -------------------------
def game_over():
    path.up()
    path.goto(-100, 0)
    path.color('white')
    path.write("GAME OVER!", font=("Arial", 20, "bold"))
    path.goto(-100, -30)
    path.write("Press R to restart or Q to quit", font=("Arial", 12, "normal"))
    listen()
    onkey(restart, "r")
    onkey(exit_game, "q")

def restart():
    """Restart the game"""
    global game_over, pacman, pacman_dir, ghosts, score_
    if game_over:
        path.clear()  # Remove Game Over text
        game_over = False
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
        ghosts[0][1].x = SPEED
        ghosts[0][1].y = 0

        ghosts[1][0].x = -180
        ghosts[1][0].y = -160
        ghosts[1][1].x = 0
        ghosts[1][1].y = SPEED

        ghosts[2][0].x = 100
        ghosts[2][0].y = 160
        ghosts[2][1].x = 0
        ghosts[2][1].y = SPEED

        ghosts[3][0].x = 100
        ghosts[3][0].y = -160
        ghosts[3][1].x = SPEED
        ghosts[3][1].y = 0

        # Reset map dots
        for i in range(len(tiles)):
            if tiles[i] == 2:   # restore eaten dots
                tiles[i] = 1

        world()
        move()

def exit_game():
    bye()

# ---------------------- GAME LOOP -------------------------
def move(): #SC: This function runs the entire game, as it does movement for everything and the game logic for the game
    writer.undo() #SC: clears the last thing the writer wrote, aka the score
    writer.write(score_['score']) #SC: writes the new current score of the game
    clear() #SC: Clears all moving elements of the game, but not things drawn in the world function as they do not change 
    
    if valid(vector(pacman.x + pacman_dir.x, pacman.y + pacman_dir.y)): #SC: this is how Pac-Man moves and how it detects collisions coming from valid checking if it's not a wall, the vector packages both of these into a position object
        pacman.x = pacman.x + pacman_dir.x  #SC: pacman.x calculates the x-position of the pacman in the next frame
        pacman.y = pacman.y + pacman_dir.y  #SC: does the same as pacman.x but for the y-coordinate 
    
    index = offset(pacman) #SC: recalls the offset function, translating the pixel position of Pac-Man to the grid index to tell the game what Pac-Man is standing on
    if tiles[index] == 1:  #SC: If statement, if the tile Pac-Man is on is a dot(because of the 1 on the grid)
        tiles[index] = 2  #SC: This marks the dot as collected, so it will no longer show up
        score_['score'] = score_['score'] + 1  #SC: updates the score after the dot has been collected
        x = (index % 20) * 20 - 200  #SC: the position is then redrawn with another square, with the dot no longer appearing with the square function
        y = 180 - (index // 20) * 20
        square(x, y)
    
    up()  #SC: Lifts the "pen" of the object or turtle's pen so it stops drawing
    goto(pacman.x + 10, pacman.y + 10)  #SC: Goes to the center of the cell 
    dot(20, 'yellow')  #SC: Draws the pacman as the yellow dot in the center of the cell
    
    for ghost in ghosts:  #SC: Ghost movement loop/ movement AI
        point = ghost[0] #SC: the position point of the ghost with a list containing its x and y coordinates
        course = ghost[1] #SC: the direction of the ghost  with its x and y properties
        if valid(vector(point.x + course.x, point.y + course.y)): #SC: calculates the ghosts' next position, checking if it's valid or not, so not a wall
            point.x = point.x + course.x #SC: if the next position is valid, it continues in that direction in both x and y
            point.y = point.y + course.y
        else: #SC: if the ghost is blocked (the new position is not valid)
            plan = choice([vector(SPEED,0), vector(-SPEED,0), vector(0,SPEED), vector(0,-SPEED)]) #SC: randomly picks a new choice out of the 4 available, left, right, up, or down
            course.x = plan.x #SC: these then make the ghost go in the desired direction. If the new direction the ghost chooses is also a wall, it chooses a new direction until a valid direction is chosen
            course.y = plan.y
        up() #SC: Lifts the "pen" of the object or turtle's pen so it stops drawing
        goto(point.x + 10, point.y + 10)  #SC: Goes to the center of the cell 
        dot(20, 'red') #SC: draws the ghost as a red dot
    
    update() #SC: this function then refreshes the graphics, so it gives all the latest changes
    
    for ghost in ghosts: #SC: this for ghost in ghosts loop is for collision detection of the ghost and Pac-Man
        point = ghost[0] #SC: Grabs the ghost's current position
        if abs(pacman.x - point.x) < 20 and abs(pacman.y - point.y) < 20: #SC: This if statement checks if Pac-Man and a ghost are within 20 pixels both vertically and horizontally of each other
            game_over() #SC: if both are true, then there is a collision and the game ends
            return #SC: if the collision is detected, it stops the move function and doesn't execute the next frame, and the onTimer function won't be called
    
    ontimer(move, 20) #SC: schedules the next frame to run after 20 milliseconds 

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
