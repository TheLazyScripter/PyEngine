from Core import *
from Core.Architecture import *
from Core.Architecture.CONSTANTS import DEBUG_DRAW
from PyMath import Vector2


def main():
    fps = 60
    Window((800, 600), "Test RPG", fps, mode=DEBUG_DRAW)

    app = Application(fps=fps)
    cam = Camera("Main Camera", (800, 600))
    instantiate(cam)
    app.initialize()

    player = Character("Player", "PLAYER", 2, "Assets/Art/Gimp/player_one.png")
    instantiate(player, Vector2.zero(), 0)

    app.execute()


if __name__ == "__main__":
    import pygame
    import sys
    pygame.init()
    main()
    pygame.quit()
    sys.exit()
