# app.py
# eerste project om mijn architecturale kennis van python en pygame te testen
# DOEL: een 3x3 schuiver spelletje waarin een image in 9 stukken geknipt wordt
# random verspreid wordt over het gameboard en de user de tekening terug "heel"
# moet maken
import pygame
import traceback # to get clear error messages

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
    running = True
    play_board = solved_board[:]
    empty_slot = 9
    moving_tile = None

    # keeping track of which modules are loaded
    # print("Pygame Core initiated:", pygame.get_init())
    # print("Pygame Display initiated:", pygame.display.get_init())

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
                # print(legal_moves, empty_slot)
                if event.key == pygame.K_ESCAPE:
                    print("escape was pressed")
                    running = False
                else:
                    if event.key == pygame.K_LEFT and "left" in legal_moves:
                        # print("LEFT was pressed")
                        moving_tile = empty_slot 
                        empty_slot -= 1
                        moved = True
                    elif event.key == pygame.K_RIGHT and "right" in legal_moves:
                        # print("RIGHT was pressed") 
                        moving_tile = empty_slot 
                        empty_slot += 1
                        moved = True
                    elif event.key == pygame.K_UP and "up" in legal_moves:
                        # print("UP was pressed") 
                        moving_tile = empty_slot 
                        empty_slot -= 3
                        moved = True
                    elif event.key == pygame.K_DOWN and "down" in legal_moves:
                        # print("DOWN was pressed") 
                        moving_tile = empty_slot 
                        empty_slot += 3
                        moved = True
                    else:
                        print("The only allowed moves are:", legal_moves)
                        moved = False
                # print(play_board)
                # print("The empty slot is", empty_slot, "- the tile that moved is now on", moving_tile )
                if moved:
                    play_board[empty_slot-1], play_board[moving_tile-1] = play_board[moving_tile-1], play_board[empty_slot-1]
                print(play_board)
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