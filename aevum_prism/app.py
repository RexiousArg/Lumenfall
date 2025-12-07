import pygame

from .scenes.gameplay import GameplayScene
from .settings import Settings


class App:
    def __init__(self) -> None:
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.width, self.settings.height)
        )
        pygame.display.set_caption(self.settings.window_title)
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene = GameplayScene(self.settings)

    def run(self) -> None:
        while self.running:
            dt = self.clock.tick(self.settings.fps) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                else:
                    self.scene.handle_event(event)

            self.scene.update(dt)
            self.scene.draw(self.screen)
            pygame.display.flip()
