# app.py
# 3x3 sliding puzzle with START screen + mouse-only moves + simple slide animation

import pygame
import traceback
import random

# --- CONFIG / CONSTANTS ---
GRID = 3
TILE = 200
W, H = 600, 600

SCRAMBLE_MOVES = 50
ANIM_FRAMES = 10
DEBUG_PRINTING = False

solved_board = [1, 2, 3, 4, 5, 6, 7, 8, 9]   # tile 9 is the empty slot (not drawn)
play_board = solved_board[:]
tiles = [None] * 10  # dummy index 0


def dprint(*args):
    if DEBUG_PRINTING:
        print(*args)


def get_possible_slides(empty_slot: int) -> list[int]:
    legal = []

    # Horizontal (±1) without wrap:
    # empty has a neighbor on the right if it's not in the rightmost column
    if empty_slot in (1, 2, 4, 5, 7, 8):
        legal.append(1)
    # empty has a neighbor on the left if it's not in the leftmost column
    if empty_slot in (2, 3, 5, 6, 8, 9):
        legal.append(-1)

    # Vertical (±GRID)
    if empty_slot in (1, 2, 3, 4, 5, 6):
        legal.append(GRID)      # tile below slides up (empty moves down)
    if empty_slot in (4, 5, 6, 7, 8, 9):
        legal.append(-GRID)     # tile above slides down (empty moves up)

    return legal


def move(delta: int, empty_slot: int) -> int:
    """Mutate play_board by swapping the tile at (empty_slot + delta) into empty_slot.
    Returns new empty_slot position (old tile position). No-op if invalid.
    """
    if type(delta) is not int:
        return empty_slot

    to_pos = empty_slot
    from_pos = empty_slot + delta

    # bounds
    if from_pos < 1 or from_pos > GRID * GRID:
        return empty_slot

    # prevent horizontal wrap for ±1
    if abs(delta) == 1 and ((to_pos - 1) // GRID != (from_pos - 1) // GRID):
        return empty_slot

    play_board[to_pos - 1], play_board[from_pos - 1] = play_board[from_pos - 1], play_board[to_pos - 1]
    return from_pos


def scramble(empty_slot: int) -> int:
    for _ in range(SCRAMBLE_MOVES):
        delta = random.choice(get_possible_slides(empty_slot))
        empty_slot = move(delta, empty_slot)
    return empty_slot


def game_loop():
    pygame.init()

    # Fonts
    font = pygame.font.Font(None, 40)
    medfont = pygame.font.Font(None, 80)
    bigfont = pygame.font.Font(None, 120)

    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Sliding Puzzle")
    clock = pygame.time.Clock()

    if not pygame.image.get_extended():
        print("This pygame version does not support JPG images, sorry")
        return

    anon = pygame.image.load("assets/anon.jpg").convert()
    if anon.get_size() != (W, H):
        print("Oh no, this picture is not", W, "x", H, "pixels!")
        return

    # Slice image into 9 subsurfaces
    for tile_id in range(1, 10):
        row = (tile_id - 1) // GRID
        col = (tile_id - 1) % GRID
        rect = pygame.Rect(col * TILE, row * TILE, TILE, TILE)
        tiles[tile_id] = anon.subsurface(rect)

    # Buttons
    start_button = pygame.Rect(150, 500, 300, 70)
    start_txt_surface = medfont.render("START", True, (200, 0, 0))
    start_txt_rect = start_txt_surface.get_rect(center=start_button.center)
    start_txt_rect.y += 6

    solved_area = pygame.Rect(20, 20, 560, 200)
    quit_button = pygame.Rect(70, 500, 200, 70)
    again_button = pygame.Rect(330, 500, 200, 70)

    solved_message_surface = bigfont.render("SOLVED!", True, "red")
    solved_message_rect = solved_message_surface.get_rect(center=solved_area.center)

    quit_txt_surface = font.render("QUIT", True, (200, 200, 200))
    quit_txt_rect = quit_txt_surface.get_rect(center=quit_button.center)
    quit_txt_rect.y += 2

    again_txt_surface = font.render("PLAY AGAIN", True, (200, 200, 200))
    again_txt_rect = again_txt_surface.get_rect(center=again_button.center)
    again_txt_rect.y += 2

    # State
    state = "START"
    empty_slot = 9
    play_board[:] = solved_board

    # Animation locals (commit-first animation)
    anim_from_pos = 0
    anim_to_pos = 0
    anim_tile_id = 0
    anim_frame = 0

    def draw_grid():
        pygame.draw.line(screen, (200, 200, 200), (200, 0), (200, 600), width=1)
        pygame.draw.line(screen, (200, 200, 200), (400, 0), (400, 600), width=1)
        pygame.draw.line(screen, (200, 200, 200), (0, 200), (600, 200), width=1)
        pygame.draw.line(screen, (200, 200, 200), (0, 400), (600, 400), width=1)

    def draw_board(skip_pos: int | None = None):
        for pos in range(1, 10):
            if skip_pos is not None and pos == skip_pos:
                continue
            tile_id = play_board[pos - 1]
            if tile_id == 9:
                continue
            row = (pos - 1) // GRID
            col = (pos - 1) % GRID
            screen.blit(tiles[tile_id], (col * TILE, row * TILE))

    while state != "QUITTING":
        # --- EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = "QUITTING"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = "QUITTING"
                # Arrow keys intentionally removed

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                if state == "START":
                    if start_button.collidepoint(mx, my):
                        play_board[:] = solved_board
                        empty_slot = 9
                        empty_slot = scramble(empty_slot)
                        state = "PLAYING"

                elif state == "PLAYING":
                    row = my // TILE
                    col = mx // TILE
                    pos = row * GRID + col + 1

                    legal = get_possible_slides(empty_slot)
                    delta = pos - empty_slot

                    if delta in legal:
                        old_empty = empty_slot
                        from_pos = pos
                        to_pos = old_empty
                        moved_tile_id = play_board[from_pos - 1]  # before commit

                        empty_slot = move(delta, empty_slot)      # commit now

                        # animation setup (commit-first)
                        anim_from_pos = from_pos
                        anim_to_pos = to_pos
                        anim_tile_id = moved_tile_id
                        anim_frame = 0
                        state = "ANIMATE"

                elif state == "SOLVED":
                    if quit_button.collidepoint(mx, my):
                        state = "QUITTING"
                    elif again_button.collidepoint(mx, my):
                        play_board[:] = solved_board
                        empty_slot = 9
                        empty_slot = scramble(empty_slot)
                        state = "PLAYING"

                # ignore clicks during ANIMATE

        # --- SOLVED CHECK (only in PLAYING) ---
        if state == "PLAYING" and play_board == solved_board:
            state = "SOLVED"

        # --- TIME / UPDATE ---
        clock.tick(60)

        if state == "ANIMATE":
            anim_frame += 1
            if anim_frame >= ANIM_FRAMES:
                state = "PLAYING"

        # --- DRAW ---
        screen.fill((0, 0, 0))

        if state == "START":
            screen.blit(anon, (0, 0))
            pygame.draw.rect(screen, (0, 0, 0), start_button)
            pygame.draw.rect(screen, (200, 200, 200), start_button, 3)

            mx, my = pygame.mouse.get_pos()
            if start_button.collidepoint(mx, my):
                pygame.draw.rect(screen, (50, 50, 50), start_button)
                pygame.draw.rect(screen, (250, 250, 250), start_button, 3)

            screen.blit(start_txt_surface, start_txt_rect)

        elif state == "PLAYING":
            draw_board()
            draw_grid()

        elif state == "ANIMATE":
            # draw board + grid first (grid visible), but skip the moving tile at its destination slot
            # (because board was already committed, moving tile is now at anim_to_pos)
            draw_board(skip_pos=anim_to_pos)
            draw_grid()

            # interpolated position of moving tile on top (covers grid where it passes)
            t = anim_frame / ANIM_FRAMES

            fr = (anim_from_pos - 1) // GRID
            fc = (anim_from_pos - 1) % GRID
            tr = (anim_to_pos - 1) // GRID
            tc = (anim_to_pos - 1) % GRID

            fx, fy = fc * TILE, fr * TILE
            tx, ty = tc * TILE, tr * TILE

            x = fx + (tx - fx) * t
            y = fy + (ty - fy) * t

            screen.blit(tiles[anim_tile_id], (round(x), round(y)))

        elif state == "SOLVED":
            screen.blit(anon, (0, 0))

            # buttons
            pygame.draw.rect(screen, (0, 0, 0), quit_button)
            pygame.draw.rect(screen, (200, 200, 200), quit_button, 3)
            pygame.draw.rect(screen, (0, 0, 0), again_button)
            pygame.draw.rect(screen, (200, 200, 200), again_button, 3)

            mx, my = pygame.mouse.get_pos()
            if again_button.collidepoint(mx, my):
                pygame.draw.rect(screen, (50, 50, 50), again_button)
                pygame.draw.rect(screen, (250, 250, 250), again_button, 3)
            if quit_button.collidepoint(mx, my):
                pygame.draw.rect(screen, (50, 50, 50), quit_button)
                pygame.draw.rect(screen, (250, 250, 250), quit_button, 3)

            # solved text + labels
            screen.blit(solved_message_surface, solved_message_rect)
            screen.blit(again_txt_surface, again_txt_rect)
            screen.blit(quit_txt_surface, quit_txt_rect)

        pygame.display.flip()

    pygame.quit()


def main():
    try:
        game_loop()
    except Exception:
        traceback.print_exc()


if __name__ == "__main__":
    main()
