# .app
# eerste project om mijn architecturale kennis van python en pygame te testen
# DOEL: een 3x3 schuiver spelletje waarin een image in 9 stukken geknipt wordt
# random verspreid wordt over het gameboard en de user de tekening terug "heel"
# moet maken

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