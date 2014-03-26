# This was hacked during recitation and may contain bugs. It is just an example
# of how awesome animation and games and python can be.

from Tkinter import *

class Struct: pass

def make2dBoard(rows, cols, initValue = 0):
    return [ [initValue]*cols for row in xrange(rows) ]

def mousePressed(canvas, event):
    redrawAll(canvas)

def keyPressed(canvas, event):
    if (canvas.data.gameOver == False):
        if (event.keysym == "Left"):
            changeDirection(canvas, "left", 2)
        elif (event.keysym == "Right"):
            changeDirection(canvas, "right", 2)
        elif (event.keysym == "Up"):
            changeDirection(canvas, "up", 2)
        elif (event.keysym == "Down"):
            changeDirection(canvas, "down", 2)
        elif (event.keysym == "a"):
            changeDirection(canvas, "left", 1)
        elif (event.keysym == "d"):
            changeDirection(canvas, "right", 1)
        elif (event.keysym == "w"):
            changeDirection(canvas, "up", 1)
        elif (event.keysym == "s"):
            changeDirection(canvas, "down", 1)
        else:
            redrawAll(canvas)

    if (event.keysym == "r"):
        init(canvas)
        canvas.data.message.text = "Game On!"
        redrawAll(canvas)

def timerFired(canvas):
    if (canvas.data.gameOver == False):
        movePlayers(canvas)
    else:
        canvas.data.message.text = "Game Over!"

    redrawAll(canvas)
    delay = 50 # milliseconds
    # pause, then call timerFired again
    canvas.after(delay, lambda: timerFired(canvas))

def redrawAll(canvas):
    canvas.delete(ALL)
    drawBoard(canvas)
    drawMessage(canvas)

def drawBoard(canvas):
    rows, cols = canvas.data.rows, canvas.data.cols
    board = canvas.data.board
    data = canvas.data
    cellSize = min(data.width/data.cols, data.height/data.rows)

    for row in xrange(rows):
        for col in xrange(cols):
            x0, y0 = col*cellSize, row*cellSize
            x1, y1 = x0+cellSize, y0+cellSize

            if (board[row][col] == 1):
                color = data.p1.color
                border = 0
                borderColor = data.p1.color
            elif (board[row][col] == 11):
                color = data.p1.trailColor
                border = data.p1.border
                borderColor = data.p1.borderColor
            elif (board[row][col] == 2):
                color = data.p2.color
                border = 0
                borderColor = data.p2.borderColor
            elif (board[row][col] == 22):
                color = data.p2.trailColor
                border = data.p2.border
                borderColor = data.p2.borderColor
            else:
                color = data.boardColor
                border = 0
                borderColor = data.boardColor

            canvas.create_rectangle(x0, y0, x1, y1, fill=color,
                                    width=border, outline=borderColor)

def drawMessage(canvas):
    message = canvas.data.message
    canvas.create_text(message.position[0], message.position[1],
                       text=message.text, fill=message.color,
                       font=message.font)


def changeDirection(canvas, direction, player):
    data = canvas.data
    directions = {"left": (0,-1), "right": (0,1), "up": (-1,0), "down": (1,0)}

    if (direction in directions):
        if (player == 1 and
            not ((direction == "up" and data.p1.dir == directions["down"]) or
            (direction == "down" and data.p1.dir == directions["up"]) or
            (direction == "left" and data.p1.dir == directions["right"]) or
            (direction == "right" and data.p1.dir == directions["left"]))):
            data.p1.dir = directions[direction]
            return True
        elif (player == 2 and
            not ((direction == "up" and data.p2.dir == directions["down"]) or
            (direction == "down" and data.p2.dir == directions["up"]) or
            (direction == "left" and data.p2.dir == directions["right"]) or
            (direction == "right" and data.p2.dir == directions["left"]))):
            data.p2.dir = directions[direction]
            return True
        else:
            return False
    else:
        return False

def movePlayers(canvas):
    data = canvas.data
    board = data.board
    rows, cols = data.rows, data.cols
    p1NewPos = (data.p1.headPosition[0] + data.p1.dir[0],
                data.p1.headPosition[1] + data.p1.dir[1])
    p2NewPos = (data.p2.headPosition[0] + data.p2.dir[0],
                data.p2.headPosition[1] + data.p2.dir[1])
    if (p1NewPos[0] < 0 or p1NewPos[1] < 0  or
        p1NewPos[0] >= rows or p1NewPos[1] >= cols or
        p2NewPos[0] < 0 or p2NewPos[1] < 0  or
        p2NewPos[0] >= rows or p2NewPos[1] >= cols):
        data.gameOver = True
        return False
    elif (board[p1NewPos[0]][p1NewPos[1]] != 0 or
          board[p2NewPos[0]][p2NewPos[1]] != 0):
        data.gameOver = True
        return False
    elif (p1NewPos == p2NewPos):
        data.gameOver = True
        return False
    else:
        board[p1NewPos[0]][p1NewPos[1]] = 1
        board[p2NewPos[0]][p2NewPos[1]] = 2
        board[data.p1.headPosition[0]][data.p1.headPosition[1]] = 11
        board[data.p2.headPosition[0]][data.p2.headPosition[1]] = 22
        data.p1.headPosition = p1NewPos
        data.p2.headPosition = p2NewPos

        if ((abs(p1NewPos[0] - p2NewPos[0]) <= data.nearMissDistance) and
            (abs(p1NewPos[1] - p2NewPos[1]) <= data.nearMissDistance)):
            data.message.text = "Near miss!"
    return True

def init(canvas):
    data = canvas.data

    # Player Initiation
    # Coordinates represented as (row, col) tuple
    data.p1 = Struct()
    data.p1.dir = (1, 0) # Player direction represented as (drow, dcol) tuple
    data.p1.headPosition = (10, 10)
    data.p1.color = "OrangeRed3"
    data.p1.trailColor = "OrangeRed2"
    data.p1.borderColor = "OrangeRed1"
    data.p1.border = 0
    data.p2 = Struct()
    data.p2.dir = (-1, 0) # Player direction represented as (row, col) tuple
    data.p2.headPosition = (30, 30)
    data.p2.color = "cyan3"
    data.p2.trailColor = "cyan2"
    data.p2.borderColor = "cyan1"
    data.p2.border = 0

    # Game board data and initiation.
    data.width = 800
    data.height = 800
    data.rows = 40
    data.cols = 40
    data.board = make2dBoard(data.rows, data.cols)
    data.board[data.p1.headPosition[0]][data.p1.headPosition[1]] = 1
    data.board[data.p2.headPosition[0]][data.p2.headPosition[1]] = 2
    data.boardColor = "black"

    # Message Settings
    data.message = Struct()
    data.message.position = (data.width/2, 100)
    data.message.text = "Game On!"
    data.message.font = "Helvetica 20 bold"
    data.message.color = "white"

    # Miscellaneous
    data.nearMissDistance = 2

    data.gameOver = False

def run():
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=800, height=800)
    canvas.pack()
    # Set up canvas data and call init
    canvas.data = Struct()
    init(canvas) # DK: init() --> init(canvas)
    # set up events
    # DK: You can use a local function with a closure
    # to store the canvas binding, like this:
    def f(event): mousePressed(canvas, event)
    root.bind("<Button-1>", f)
    # DK: Or you can just use an anonymous lamdba function,
    # like this:
    root.bind("<Key>", lambda event: keyPressed(canvas, event))
    timerFired(canvas) # DK: timerFired() --> timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()
