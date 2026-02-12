# app.py
# eerste project om mijn architecturale kennis van python en pygame te testen
# DOEL: een 3x3 schuiver spelletje waarin een image in 9 stukken geknipt wordt
# random verspreid wordt over het gameboard en de user de tekening terug "heel"
# moet maken

# possible states: START, PLAYING, SOLVED, QUITTING

import pygame
import traceback # to get clear error messages
import random

solved_board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
play_board = solved_board[:]
tiles = [None] * 10
GRID = 3    # playboard is a 3x3 grid, divided into 9 tiles
TILE = 200  # tiles are 200x200 pixels
MOVE_DELTAS = (-1, +1, -GRID, +GRID) # possible moves inside the grid
SCRAMBLE_MOVES = 3
DEBUG_PRINTING = True

# Debug printing statements, set True or False with DEBUG_PRINTING
def dprint(msg):
    if DEBUG_PRINTING:
        print(msg)
        return

def get_possible_slides(empty_slot):
    legal_moves = []
    # check horizontal possible sliding neighbours
    if empty_slot in (2, 5, 8):
        # dprint("moving to the left and to the right is legal")
        legal_moves.append(-1)
        legal_moves.append(1)
    elif empty_slot in (3, 6, 9):
        # dprint("moving to the left is legal")
        legal_moves.append(-1)
    else: # (1, 4, 7):
        # dprint("moving to the right is legal")
        legal_moves.append(1)
    # check vertical possible sliding neighbours
    if empty_slot in (4, 5, 6):
        # dprint("moving up and down is legal")
        legal_moves.append(-GRID)
        legal_moves.append(GRID)
    elif empty_slot in (1, 2, 3): 
        # dprint("moving down is legal")
        legal_moves.append(GRID)
    else: # empty_slot in (7, 8, 9):
        # dprint("moving up is legal")
        legal_moves.append(-GRID)
    return legal_moves

def move(b, empty_slot):
    # When move() is entered we are sure that b is a legal move
    # Nevertheless extra robustness checks for illegal moves have been included
    # swap the selected tile with the empty slot
    # dprint("Entering move function, b is now:", b)
    # dprint("before move playboard:", play_board)
    moved = False
    if type(b) != int:
        return empty_slot
    elif type(b) == int:
        # dprint("The empty slot is on pos", empty_slot, "- the tile that moved is now on", moving_tile )
        to_pos = empty_slot
        from_pos = empty_slot + b
        # prevent accidental out of bounds results
        if from_pos < 1 or from_pos > 9: return empty_slot
        # prevent wraps between 3-4 and 6-7
        if abs(b) == 1 and ((to_pos-1)//GRID != (from_pos-1)//GRID): return empty_slot
        # MUTATE the play board
        play_board[to_pos-1], play_board[from_pos-1] = play_board[from_pos -1], play_board[to_pos-1]
        # dprint("if moved playboard:", play_board)
    return from_pos


def game_loop():
    # initialise pygame
    pygame.init()
    font = pygame.font.Font(None, 40)
    medfont = pygame.font.Font(None, 80)
    bigfont = pygame.font.Font(None, 120)

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
        # dprint("The picture has the correct dimensions")
    
    # SLICING LOOP
        
    for tile_id in range(1,10): # keep only 1-9
        # row/col math
        row = (tile_id - 1) // GRID
        col = (tile_id - 1) % GRID
        # left/top math
        rect = pygame.Rect(col * TILE, row * TILE, w//GRID, h//GRID)
        # subsurface
        tile = anon.subsurface(rect)
        # tiles[tile_id] = ...
        tiles[tile_id] = tile
    # dprint(tiles)

    # OVERLAY DEFINITION - KEEP IT AS A REFERENCE
    # overlay = pygame.Surface((w,h), pygame.SRCALPHA) # define transparent overlay covering screen
    # overlay.fill((0, 0, 0, 160)) # last number = opacity

    # BUTTON DEFINITIONS

    # Define rectangle for start button (used only upon launch)
    start_button = pygame.Rect(150,500,300,70)    
    # font rendering for start button
    start_txt_surface = medfont.render("START", True, (200,0,0))
    start_txt_rect = start_txt_surface.get_rect(center=start_button.center)
    start_txt_rect.y += 6   # visual tweak to vertically center the text
    # Define rectangle for SOLVED message after state is SOLVED
    solved_area = pygame.Rect(20,20,560,200)
    # Define rectangles for "quit" and "play again" buttons (used after SOLVED)
    quit_button = pygame.Rect(70,500,200,70)
    again_button = pygame.Rect(330, 500, 200, 70)
    # font rendering
    solved_message_surface = bigfont.render("SOLVED!", True, "red")
    solved_message_rect = solved_message_surface.get_rect(center=solved_area.center)
    quit_txt_surface = font.render("QUIT", True, (200,200,200))
    quit_txt_rect = quit_txt_surface.get_rect(center=quit_button.center)
    quit_txt_rect.y += 2
    again_txt_surface = font.render("PLAY AGAIN", True, (200,200,200))
    again_txt_rect = again_txt_surface.get_rect(center=again_button.center)
    again_txt_rect.y += 2
    
    # set a caption for the window
    pygame.display.set_caption("Sliding Puzzle")
    
    # create a clock
    clock = pygame.time.Clock()
    
    # set dt
    # dt = 0.0

    # STARTING CONDITIONS
    play_board[:] = solved_board
    empty_slot = 9
    state = "START"

    # SCRAMBLE FUNCTION
    def scramble(empty_slot):
        # make moves x times to scramble the playboard
        for n in range(1, SCRAMBLE_MOVES):
            # the list that holds the legal moves (deltas) given the position of the empty slot
            legal_moves = get_possible_slides(empty_slot)
            # pick one of the legal moves
            b = random.choice(legal_moves)
            # show the legal moves and the chosen move in the console
            # dprint(legal_moves)
            # dprint(b)
            empty_slot = move(b, empty_slot)
            # dprint("Result:", play_board, empty_slot)
        return empty_slot
    
    while state != "QUITTING":
        # 1) Check Events
        for event in pygame.event.get():
            # check for window close
            if event.type == pygame.QUIT: 
                state = "QUITTING"
                # dprint("quit was chosen")
            # check for mousebutton press
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                (mx, my) = event.pos
                # dprint("mouse coordinates are",mx,my)
                if state == "START":
                    # check if mouseclick occurs inside start rectangle
                    if start_button.collidepoint(mx, my):
                        # dprint("start hit")
                        play_board[:] = solved_board
                        empty_slot = 9  
                        empty_slot = scramble(empty_slot)
                        # dprint(empty_slot)
                        state = "PLAYING"

                elif state =="PLAYING":
                    legal_moves = get_possible_slides(empty_slot)
                    # dprint(legal_moves, empty_slot)
                    row = my//TILE
                    col = mx//TILE
                    # calculate tile position 1-9
                    pos = (row*3)+col+1
                    # dprint("pos is",pos)
                    # compute pos
                    delta = pos - empty_slot
                    # dprint("delta is",delta)
                    # map delta → direction string
                    if delta in legal_moves:
                        # dprint("Mousedirection is",b)
                        # dprint("legal move")
                        empty_slot = move(delta,empty_slot)
                        # dprint("empty slot has moved to",empty_slot)
                        tile_id = play_board[pos-1]
                    else:
                        # dprint("NOT legal")
                        delta = None
                        continue

                elif state =="SOLVED":
                    # check if mouseclick occurs inside quit or again rectangles
                    if quit_button.collidepoint(mx, my):
                        # dprint("quit hit")
                        state = "QUITTING"
                    elif again_button.collidepoint(mx, my):
                        # dprint("again hit")
                        play_board[:] = solved_board
                        empty_slot = 9
                        empty_slot = scramble(empty_slot)
                        state = "PLAYING"

            # check for keypress
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "QUITTING"
                    # dprint("escape was pressed")
                elif state == "PLAYING":
                    legal_moves = get_possible_slides(empty_slot)
                    # dprint(legal_moves, empty_slot)
                    if event.key == pygame.K_LEFT and -1 in legal_moves:
                        b = -1
                    elif event.key == pygame.K_RIGHT and +1 in legal_moves:
                        b = 1
                    elif event.key == pygame.K_UP and -GRID in legal_moves:
                        b = -GRID
                    elif event.key == pygame.K_DOWN and GRID in legal_moves:
                        b = GRID
                    else: # any other key should be ignored
                        continue
                    empty_slot = move(b, empty_slot)
                    # dprint("Result2:", play_board, empty_slot)
                # dprint("Result2:", play_board, empty_slot)

        # check for solved
        if state == "PLAYING" and play_board == solved_board:
            state = "SOLVED"

        # 2) Advance Game time
        clock.tick(60)
        # 3) Update game (simulation)
        # 4) Draw (read-only)
        screen.fill((0,0,0))
        if state == "START":
            # dprint("started")
            screen.blit(anon) # SHOW COMPLETE IMAGE 
            pygame.draw.rect(screen, (0,0,0), start_button) # button surface
            pygame.draw.rect(screen, (200,200,200), start_button, 3)    # button border
            mx, my = pygame.mouse.get_pos()
            start_hover = start_button.collidepoint(mx, my)
            if start_hover:
                pygame.draw.rect(screen, (50,50,50), start_button) # button surface
                pygame.draw.rect(screen, (250,250,250), start_button, 3)    # button border    
            screen.blit(start_txt_surface, start_txt_rect)  # button text
        elif state == "PLAYING":
            # dprint("playing")
            for pos in range(1,10):
                row = (pos - 1) // GRID
                col = (pos - 1) % GRID
                position = (col*TILE, row*TILE)
                tile_id = play_board[pos-1]
                if tile_id != 9: 
                    #blit tile at that position
                    screen.blit(tiles[tile_id], position)
            # draw grid for tile edges
            pygame.draw.line(screen, (200,200,200), (200,0), (200,600), width=1)
            pygame.draw.line(screen, (200,200,200), (400,0), (400,600), width=1)
            pygame.draw.line(screen, (200,200,200), (0,200), (600,200), width=1)
            pygame.draw.line(screen, (200,200,200), (0,400), (600,400), width=1)
        elif state == "SOLVED":
            # dprint("solved")
            screen.blit(anon)
            # screen.blit(overlay,(0,0))  # shadow over screen, defined earlier, starting top left
            # NOT USED, KEEP AS REFERENCE

            # draw two button rects (solid) with text
            pygame.draw.rect(screen, (0,0,0), quit_button)  # button surface
            pygame.draw.rect(screen, (200,200,200), quit_button, 3)     # button border
            pygame.draw.rect(screen, (0,0,0), again_button) # button surface
            pygame.draw.rect(screen, (200,200,200), again_button, 3)    # button border
            mx, my = pygame.mouse.get_pos()
            again_hover = again_button.collidepoint(mx, my)
            quit_hover  = quit_button.collidepoint(mx, my)
            if again_hover:
                pygame.draw.rect(screen, (50,50,50), again_button) # button surface
                pygame.draw.rect(screen, (250,250,250), again_button, 3)    # button border    
            if quit_hover:
                pygame.draw.rect(screen, (50,50,50), quit_button)  # button surface
                pygame.draw.rect(screen, (250,250,250), quit_button, 3)     # button border
            # show a SOLVED! message AND the button texts
            screen.blit(solved_message_surface, solved_message_rect)
            screen.blit(again_txt_surface, again_txt_rect)  # button text
            screen.blit(quit_txt_surface, quit_txt_rect)    # button text
        pygame.display.flip()

        if state == "QUITTING":
            continue
    
    pygame.quit()

def main():
    # dprint("Empty slot is 9")
    try:
        # raise Exception("testing my exception handling")
        game_loop()
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    main()