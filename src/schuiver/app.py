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
# empty_slot = len(solved_board)
# empty_slot = 8

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
    # report valid tile indexes for a given position
    # print(legal_moves)
    return legal_moves

def move(b, empty_slot):
    # swap the moving tile with the empty slot
    print("Entering move function, b is now:", b)
    print("before move playboard:", play_board)
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
        print("no valid choice in move. b is", b)
        return
    if moved: 
        print("The empty slot is on pos", empty_slot, "- the tile that moved is now on", moving_tile )
        play_board[empty_slot-1], play_board[moving_tile-1] = play_board[moving_tile-1], play_board[empty_slot-1]
        print("if moved playboard:", play_board)
    return play_board, moving_tile, empty_slot, moved


def game_loop():
    # initialise pygame
    pygame.display.init()

    # set screen width and height
    w = 600
    h = 600
    # create the display surface
    screen = pygame.display.set_mode((w, h))
    # set a caption for the window
    pygame.display.set_caption("Pypuzzle")

    # create a clock
    clock = pygame.time.Clock()
    # set dt
    dt = 0.0
    play_board = solved_board[:]
    
    running = False
    moved = False
    scrambling = True
    empty_slot = 9
    moving_tile = None

    for n in range(1,4):
        legal_moves = get_possible_slides(empty_slot)
        a = random.randint(1,len(legal_moves))
        b = legal_moves[a-1]
        print()
        print("legal moves are:", legal_moves, "a:", a, "b:", b)
        result = move(b, empty_slot)
        play_board,_,_,_ = result
        _,moving_tile,_,_ = result
        _,_,empty_slot,_ = result
        _,_,_,moved = result
        print("Result:", result)
    
    # keeping track of which modules are loaded
    # print("Pygame Core initiated:", pygame.get_init())
    # print("Pygame Display initiated:", pygame.display.get_init())

    scrambling = False
    running = True
    print()
    print("Solve the puzzle!")
    print()

    while running:
        # 1) Check Events
        for event in pygame.event.get():
            # check for mousebutton press
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print("Left mouse button was pressed succesfully!")
            # check for keypress
            if event.type == pygame.KEYDOWN:
                legal_moves = get_possible_slides(empty_slot)
                moved = False
                print(legal_moves, empty_slot)
                if event.key == pygame.K_ESCAPE:
                    print("escape was pressed")
                    running = False
                else:
                    if event.key == pygame.K_LEFT and "left" in legal_moves:
                        b = "left"
                        moved = True
                    elif event.key == pygame.K_RIGHT and "right" in legal_moves:
                        b = "right"
                        moved = True
                    elif event.key == pygame.K_UP and "up" in legal_moves:
                        b = "up"
                        moved = True
                    elif event.key == pygame.K_DOWN and "down" in legal_moves:
                        b = "down"
                        moved = True
                    else:
                        b = ""
                        moved = False
                if moved:
                    result = move(b, empty_slot)
                    play_board,_,_,_ = result
                    _,moving_tile,_,_ = result
                    _,_,empty_slot,_ = result
                    _,_,_,moved = result
                    print("Result 2:", result)
                print(play_board) # is a not updated board!!!
                if play_board == solved_board:
                    print("Congratulations, you solved the puzzle!")
                    running = False
            # check for window close
            if event.type == pygame.QUIT:
                print("quit was chosen")
                running = False
        # 2) Advance Game time
        dt = clock.tick(60) / 1000.0
        # 3) Update game (simulation)
        # 4) Draw (read-only)
        screen.fill((0,0,0))
        pygame.display.flip()
        
    print("quitting")
    pygame.quit()

def main():
    print("Empty slot is 9")
    try:
        # raise Exception("testing my exception handling")
        game_loop()
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    main()