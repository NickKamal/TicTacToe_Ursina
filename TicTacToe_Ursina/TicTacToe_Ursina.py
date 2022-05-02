from ursina import *
import random

# Name: CameraMovement
# Purpose: Moves the camera angle
# Arguments: None
# Returns: None
def CameraMovement():
    if held_keys["w"]:
        camera.position += (0, time.dt, 0)
    if held_keys["s"]:
        camera.position -= (0, time.dt, 0)
    if held_keys["d"]:
        camera.position += (time.dt, 0, 0)
    if held_keys["a"]:
        camera.position -= (time.dt, 0, 0)


# Name: update
# Purpose: Ursina's update function
# Arguments: None
# Returns: None
def update():
    RotateCubes()
    CameraMovement()


# Name: RotateCubes
# Purpose: rotate cubes in the board
# Arguments: None
# Returns: None
def RotateCubes():
    for entity in board:
        entity.rotation_y += 0.03
        entity.rotation_x += 0.03
        entity.rotation_z += 0.03


# Name: input
# Purpose: Ursina's input function
# Arguments: None
# Returns: None
def input(key):
    global board, gameDone

    if key == "space":
        for entity in board:
            red = random.randrange(10, 255)
            green = random.randrange(10, 255)
            blue = random.randrange(10, 255)
            entity.color = color.rgb(red, green, blue)
    if key == "enter":
        Restart()


# Name: Tie
# Purpose: Checks if there is a tie
# Arguments: None
# Return: bool
def Tie():
    global clickedCubes
    return len(clickedCubes) == 9


# Name: Won
# Purpose: Checks if the current player has won
# Arguments: None
# Return: bool
def Won():
    global currentPlayer, playerTwoMoves, playerOneMoves
    global playerOne, playerTwo, winners

    movesToCheck = None
    if currentPlayer == playerOne:
        movesToCheck = playerOneMoves
    else:
        movesToCheck = playerTwoMoves

    if len(movesToCheck) < 3:
        return False
    movesToCheck.sort()
    for i in winners:
        if set(i).issubset(set(movesToCheck)):
            return True
    return False


# Name: Setup
# Purpose: sets up new game
# Arguments: None
# Returns: None
def Setup():
    window.title = "Tic Tac Toe"
    window.borderless = False
    window.fullscreen = True
    window.exit_button.visible = True
    window.fps_counter.enabled = False
    window.color = color.white

    global board, currentPlayer, board_texture, x_texture, o_texture
    global playerOne, playerTwo, clickedCubes, winners, playerTwoMoves
    global playerOneMoves, gameDone

    board_texture = "pexels-frank-cone-2230796.jpg"
    x_texture = "Trend logo vector created by Rochak Shukla.jpg"
    o_texture = "Energy ball vector created by upklyak.jpg"
    gameDone = False
    board = []
    clickedCubes = []
    winners = [
        ["00", "10", "20"],
        ["01", "11", "21"],
        ["02", "12", "22"],
        ["00", "11", "22"],
        ["10", "11", "12"],
        ["20", "21", "22"],
        ["00", "01", "02"],
        ["20", "11", "02"],
    ]
    playerOneMoves = []
    playerTwoMoves = []
    playerOne = "Player X"
    playerTwo = "Player O"
    currentPlayer = playerOne


# Name: GenerateBoard
# Purpose: Generates a 3x3 Tic Tac Toe board
# Arguments: None
# Returns: None
def GenerateBoard():
    global board, board_texture

    for x in range(3):
        for y in range(3):
            red = random.randrange(10, 255)
            green = random.randrange(10, 255)
            blue = random.randrange(10, 255)
            cube = Entity(
                name=str(x) + str(y),
                model="cube",
                position=(x + x - 2, y + y - 2, 0),
                scale=(1.5, 1.5, 1.5),
                texture=board_texture,
                color=color.rgb(red, green, blue),
                collider="box",
            )
            # Name: HandleCubeClick
            # Purpose: Handles click input on cube
            # Arguments: entity
            # Returns: None
            def HandleCubeClick(entity=cube):

                global currentPlayer, playerOne, x_texture, playerTwo
                global o_texture, clickedCubes, playerTwoMoves, playerOneMoves

                if entity.name in clickedCubes:
                    return
                clickedCubes.append(entity.name)
                if currentPlayer == playerOne:
                    playerOneMoves.append(entity.name)
                    entity.texture = x_texture
                else:
                    playerTwoMoves.append(entity.name)
                    entity.texture = o_texture
                HandelGameDone()
                SwitchPlayer()

            cube.on_click = HandleCubeClick
            board.append(cube)


# Name: HandleWin
# Purpose: display winner
# Arguments: None
# Returns: None
def HandelGameDone():
    global currentPlayer, gameDone

    if Won():
        text = currentPlayer + " won!!!"
    elif Tie():
        text = "Tie"
    else:
        return
    Panel(z=1, scale=10, model="quad")
    t = Text(text, scale=3, origin=(0, 0))
    t = Text("Press Enter to Restart", scale=1, origin=(0, 3))
    gameDone = True


# Name: Restart
# Purpose: restarts the game
# Arguments: None
# Returns: None
def Restart():
    scene.clear()
    Setup()
    GenerateBoard()


# Name: SwitchPlayer
# Purpose: switches between players
# Arguments: None
# Returns: None
def SwitchPlayer():
    global currentPlayer, playerTwo, playerOne

    if currentPlayer == playerOne:
        currentPlayer = playerTwo
    else:
        currentPlayer = playerOne


# Name: Game
# Purpose: Tic Tac Toe Game Play
# Arguments: None
# Returns: None
def Game():
    app = Ursina()
    Setup()
    GenerateBoard()
    app.run()


Game()
