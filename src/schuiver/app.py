# app.py
# eerste project om mijn architecturale kennis van python en pygame te testen
# DOEL: een 3x3 schuiver spelletje waarin een image in 9 stukken geknipt wordt
# random verspreid wordt over het gameboard en de user de tekening terug "heel"
# moet maken
import pygame
import traceback # to get clear error messages
import random

solved_board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
play_board = solved_board[:]
tiles = [None] * 10
GRID = 3    # playboard is a 3x3 grid, divided into 9 tiles
TILE = 200  # tiles are 200x200 pixels

def get_possible_slides(empty_slot):
    legal_moves = []
    # check horizontal possible sliding neighbours
    if empty_slot in (2, 5, 8):
        # print("moving to the left and to the right is legal")
        legal_moves.append("left")
        legal_moves.append("right")
    elif empty_slot in (3, 6, 9):
        # print("moving to the left is legal")
        legal_moves.append("left")
    else: # (1, 4, 7):
        # print("moving to the right is legal")
        legal_moves.append("right")
    # check vertical possible sliding neighbours
    if empty_slot in (4, 5, 6):
        # print("moving up and down is legal")
        legal_moves.append("up")
        legal_moves.append("down")
    elif empty_slot in (1, 2, 3): 
        # print("moving down is legal")
        legal_moves.append("down")
    else: # empty_slot in (7, 8, 9):
        # print("moving up is legal")
        legal_moves.append("up")
    return legal_moves

def move(b, empty_slot):
    # When move() is entered we are sure that b is a legal move
    # swap the moving tile with the empty slot
    # print("Entering move function, b is now:", b)
    # print("before move playboard:", play_board)
    moved = False
    if b == "left":
        moving_tile = empty_slot 
        empty_slot -= 1
        moved = True
    elif b == "right":
        moving_tile = empty_slot 
        empty_slot += 1
        moved = True
    elif b == "up":
        moving_tile = empty_slot 
        empty_slot -= 3
        moved = True
    elif b == "down":
        moving_tile = empty_slot 
        empty_slot += 3
        moved = True
    else:
        return
    if moved: 
        # print("The empty slot is on pos", empty_slot, "- the tile that moved is now on", moving_tile )
        play_board[empty_slot-1], play_board[moving_tile-1] = play_board[moving_tile-1], play_board[empty_slot-1]
        # print("if moved playboard:", play_board)
    return empty_slot  


def game_loop():
    # initialise pygame
    pygame.init()

    # set screen width and height
    w = 600
    h = 600
    # create the display surface
    screen = pygame.display.set_mode((w, h))
    # Check if pygame supports anything else than .bmp
    if pygame.image.get_extended() == False:
        print("This pygame version does not support JPG images, sorry")
        return
    # load assets/anon.jpg
    anon = pygame.image.load("assets/anon.jpg")
    # call .convert()
    anon = pygame.Surface.convert(anon)
    # print its size with get_size()
    c = anon.get_size()
    if c != (w, h):
        print("Oh no, this picture is not",w,"x",h,"pixels!")
        return
    # else: 
        # print("The picture has the correct dimensions")
    
    # SLICING LOOP
        
    for tile_id in range(1,10): # keep only 1-9
        # row/col math
        row = (tile_id - 1) // GRID
        col = (tile_id - 1) % GRID
        # left/top math
        # Rect
        rect = pygame.Rect(col * TILE, row * TILE, w//GRID, h//GRID)
        # subsurface
        tile = anon.subsurface(rect)
        # tiles[tile_id] = ...
        tiles[tile_id] = tile
    # print(tiles)

    # set a caption for the window
    pygame.display.set_caption("Pypuzzle")

    # create a clock
    clock = pygame.time.Clock()
    # set dt
    dt = 0.0
    play_board[:] = solved_board
    
    running = False
    # moved = False
    scrambling = True
    empty_slot = 9
    # moving_tile = None

    # make moves x times to scramble the playboard
    for n in range(1,10):
        # the list that holds the legal moves given the position of the empty slot
        legal_moves = get_possible_slides(empty_slot)
        # pick one of the legal moves
        b = random.choice(legal_moves)
        # show the legal moves and the chosen move in the console
        # print("legal moves are:", legal_moves, "Chosen move:", b)
        empty_slot = move(b, empty_slot)
        # print("Result:", play_board, empty_slot)
    
    scrambling = False
    running = True
    # Turn the solve into an overlay!
    print()
    print("Solve the puzzle!")
    print()

    while running:
        # 1) Check Events
        for event in pygame.event.get():
            # check for mousebutton press
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # print("Left mouse button was pressed succesfully!")
                legal_moves = get_possible_slides(empty_slot)
                moved = False
                # print(legal_moves, empty_slot)
                (mx, my) = event.pos
                # print("mouse coordinates are",mx,my)
                row = my//TILE
                col = mx//TILE
                # calculate tile position 1-9
                pos = (row*3)+col+1
                # print("pos is",pos)
                # compute pos
                delta = pos - empty_slot
                # print("delta is",delta)
                # map delta → direction string
                if delta == -1 and "left" in legal_moves:
                    b = "left"
                elif delta == +1 and "right" in legal_moves:
                    b = "right"
                elif delta == -3 and "up" in legal_moves:
                    b = "up"
                elif delta == +3 and "down" in legal_moves:
                    b = "down"
                else:
                    # print("Not a legal move")
                    b = ""
                    continue
                if b != "":
                    # print("Mousedirection is",b)
                    empty_slot = move(b,empty_slot)
                    # print("empty slot has moved to",empty_slot)
                    tile_id = play_board[pos-1]
            # check for keypress
            if event.type == pygame.KEYDOWN:
                legal_moves = get_possible_slides(empty_slot)
                moved = False
                # print(legal_moves, empty_slot)
                if event.key == pygame.K_ESCAPE:
                    running = False   
                    # print("escape was pressed")
                else:
                    if event.key == pygame.K_LEFT and "left" in legal_moves:
                        b = "left"
                    elif event.key == pygame.K_RIGHT and "right" in legal_moves:
                        b = "right"
                    elif event.key == pygame.K_UP and "up" in legal_moves:
                        b = "up"
                    elif event.key == pygame.K_DOWN and "down" in legal_moves:
                        b = "down"
                    else: # any other key should be ignored
                        continue
                    empty_slot = move(b, empty_slot)
                    # print("Result2:", play_board, empty_slot)
                # print("Result2:", play_board, empty_slot)
            if play_board == solved_board:
                running = False
                # Make this into an overlay!
                print("Congratulations, you solved the puzzle!")
            # check for window close
            if event.type == pygame.QUIT:
                running = False   
                # print("quit was chosen")
        # 2) Advance Game time
        clock.tick(60)
        # 3) Update game (simulation)
        # 4) Draw (read-only)
        screen.fill((0,0,0))
        for pos in range(1,10):
            row = (pos - 1) // GRID
            col = (pos - 1) % GRID
            position = (col*TILE, row*TILE)
            tile_id = play_board[pos-1]
            if tile_id != 9: 
                #blit tile at that position
                screen.blit(tiles[tile_id], position)
        pygame.display.flip()

    # print("quitting")
    pygame.quit()

def main():
    # print("Empty slot is 9")
    try:
        # raise Exception("testing my exception handling")
        game_loop()
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    main()