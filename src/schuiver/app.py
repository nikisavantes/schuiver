# app.py
# eerste project om mijn architecturale kennis van python en pygame te testen
# DOEL: een 3x3 schuiver spelletje waarin een image in 9 stukken geknipt wordt
# random verspreid wordt over het gameboard en de user de tekening terug "heel"
# moet maken

# possible states: PLAYING, SOLVED, QUITTING

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
        # print("The picture has the correct dimensions")
    
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
    # print(tiles)

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

    play_board[:] = solved_board

    empty_slot = 9
    nr_moves = 50

    # SCRAMBLE FUNCTION

    def scramble(empty_slot):
        # make moves x times to scramble the playboard
        for n in range(1, nr_moves):
            # the list that holds the legal moves given the position of the empty slot
            legal_moves = get_possible_slides(empty_slot)
            # pick one of the legal moves
            b = random.choice(legal_moves)
            # show the legal moves and the chosen move in the console
            # print("legal moves are:", legal_moves, "Chosen move:", b)
            empty_slot = move(b, empty_slot)
            # print("Result:", play_board, empty_slot)
        return empty_slot
    
    state = "START"

    while state != "QUITTING":
        # 1) Check Events
        for event in pygame.event.get():
            # check for window close
            if event.type == pygame.QUIT: 
                state = "QUITTING"
                # print("quit was chosen")
            # check for mousebutton press
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                (mx, my) = event.pos
                # print("mouse coordinates are",mx,my)
                if state == "START":
                    # check if mouseclick occurs inside start rectangle
                    if start_button.collidepoint(mx, my):
                        # print("start hit")
                        play_board[:] = solved_board
                        empty_slot = 9  
                        empty_slot = scramble(empty_slot)
                        # print(empty_slot)
                        state = "PLAYING"
                elif state =="PLAYING":
                    legal_moves = get_possible_slides(empty_slot)
                    # print(legal_moves, empty_slot)
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
                elif state =="SOLVED":
                    # check if mouseclick occurs inside quit or again rectangles
                    if quit_button.collidepoint(mx, my):
                        # print("quit hit")
                        state = "QUITTING"
                    elif again_button.collidepoint(mx, my):
                        # print("again hit")
                        play_board[:] = solved_board
                        empty_slot = 9
                        empty_slot = scramble(empty_slot)
                        state = "PLAYING"
            # check for keypress
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "QUITTING"
                    # print("escape was pressed")
                elif state == "PLAYING":
                    legal_moves = get_possible_slides(empty_slot)
                    # print(legal_moves, empty_slot)
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

        # check for solved
        if state == "PLAYING" and play_board == solved_board:
            state = "SOLVED"

        # 2) Advance Game time
        clock.tick(60)
        # 3) Update game (simulation)
        # 4) Draw (read-only)
        screen.fill((0,0,0))
        if state == "START":
            # print("started")
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
            # print("playing")
            for pos in range(1,10):
                row = (pos - 1) // GRID
                col = (pos - 1) % GRID
                position = (col*TILE, row*TILE)
                tile_id = play_board[pos-1]
                if tile_id != 9: 
                    #blit tile at that position
                    screen.blit(tiles[tile_id], position)
        elif state == "SOLVED":
            # print("solved")
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
    # print("Empty slot is 9")
    try:
        # raise Exception("testing my exception handling")
        game_loop()
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    main()