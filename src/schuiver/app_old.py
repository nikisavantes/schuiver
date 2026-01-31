# .app
# eerste project om mijn architecturale kennis van python en pygame te testen
# DOEL: een 3x3 schuiver spelletje waarin een image in 9 stukken geknipt wordt
# rangdom verspreid wordt over het gameboard en de user de tekening terug "heel"
# moet maken

def game_loop():
    pygame.init()
    pygame.mixer.init()
    clock = pygame.time.Clock()
    dt = 0.0

    # groups
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    # --------- GAME STATE ----------
    # We maken een reset-functie zodat ENTER restart proper is.
    def reset_game_state():
        nonlocal score, survival_timer, overlay_timer, overlay_level
        nonlocal lives, last_level_seen, respawn_invuln
        nonlocal player, asteroid_field
        nonlocal mode
        nonlocal score_screen_timer, freeze_timer, show_timer, blink_timer
        nonlocal hiscore_list, entered_initials, new_entry_index, pending_hiscore

        # clear sprites
        updatable.empty()
        drawable.empty()
        
        # gameplay state
        score = 0
        
        mode = "PLAY"
   # init objects + state
    player = None
    asteroid_field = None
    score = 0

    # ---- FLOW / MODES ----
    mode = "PLAY"
    score_screen_timer = 0.0
    reset_game_state()

while True:
        log_state()

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.KEYDOWN:
                # Restart flow: ENTER
                if mode == "RESTART_PROMPT":
                    if event.key == pygame.K_RETURN:
                        reset_game_state()
                    elif event.key == pygame.K_ESCAPE:
                        return

                # Initials entry
                elif mode == "HISCORE_ENTRY":
                    if event.key == pygame.K_BACKSPACE:
                        entered_initials = entered_initials[:-1]
                    elif event.key == pygame.K_RETURN:
                        if len(entered_initials) == 3:
                            hiscore_list = hiscores.add_hiscore(entered_initials, score, hiscore_list)
                            hiscores.save_hiscores(hiscore_list)

                            # index van nieuwe entry bepalen
                            new_entry_index = None
                            for i, (ini, sc) in enumerate(hiscore_list):
                                if ini == entered_initials.upper() and sc == score:
                                    new_entry_index = i
                                    break

                            mode = "HISCORE_SHOW"
                            show_timer = 5.0
                            blink_timer = 0.0
                    else:
                        ch = event.unicode.upper()
                        if ch.isalnum() and len(ch) == 1 and len(entered_initials) < 3:
                            entered_initials += ch

                # Allow ESC to quit in non-play screens
                elif mode in ("SCORE_SCREEN", "HISCORE_CONGRATS", "HISCORE_SHOW"):
                    if event.key == pygame.K_ESCAPE:
                        return

        # -------- FRAME START --------
        screen.fill("black")

        # -------- GAMEPLAY (alleen in PLAY) --------
        if mode == "PLAY":
            updatable.update(dt)

            # nieuw level gestart → speler centraal
            if asteroid_field.level != last_level_seen:
                last_level_seen = asteroid_field.level
                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.rotation = 0

            # invulnerability timer
            if respawn_invuln > 0:
                respawn_invuln -= dt
                if respawn_invuln < 0:
                    respawn_invuln = 0

            # survival score: 1 punt per 10 seconden
            survival_timer += dt
            while survival_timer >= 10.0:
                score += 1
                survival_timer -= 10.0

            # level completion bonus
            if asteroid_field.level_completed:
                score += 100
                overlay_timer = 2.0
                overlay_level = asteroid_field.completed_level

                player.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                player.rotation = 0

            # overlay timer (level complete)
            if overlay_timer > 0:
                overlay_timer -= dt
                if overlay_timer <= 0:
                    overlay_timer = 0
                    overlay_level = None
            # ---------- DRAW WORLD (alleen in PLAY) ----------
            # Kleur wordt bepaald door main (zoals jij het nu hebt)
            player.color = "green" if respawn_invuln > 0 else "white"
            for thing in drawable:
                thing.draw(screen)

            # ---------- HUD (alleen in PLAY) ----------
            level_surf = hud_font.render(f"Level: {asteroid_field.level}", True, "white")
            score_surf = hud_font.render(f"Score: {score}", True, "white")
            lives_surf = hud_font.render(f"Lives: {lives}", True, "white")
            screen.blit(level_surf, (10, 10))
            screen.blit(score_surf, (SCREEN_WIDTH - score_surf.get_width() - 10, 10))
            screen.blit(lives_surf, (10, SCREEN_HEIGHT - lives_surf.get_height() - 10))
        pygame.display.flip()
        dt = clock.tick(60) / 1000.0


def main():
    print("Hello from schuiver!")

    try:
        game_loop()
    except SystemExit:
        raise
    except Exception:
        traceback.print_exc()
        pygame.time.wait(3000)
        raise

if __name__ == "__main__":
    main()