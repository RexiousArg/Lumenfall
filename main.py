import pygame

from aevum_prism.app import App


def main() -> None:
    pygame.init()
    try:
        App().run()
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
