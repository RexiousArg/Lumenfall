import pygame

from aevum_prism.settings import Settings


class GameplayScene:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.font = pygame.font.SysFont("consolas", 18)
        self.elapsed = 0.0

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        self.elapsed += dt

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill(self.settings.background_color)
        text = self.font.render(
            "CCG prototype loop running...", True, self.settings.text_color
        )
        hint = self.font.render(
            "Escape to quit (wired) -> Replace with UI soon",
            True,
            self.settings.text_color,
        )
        surface.blit(text, (20, 20))
        surface.blit(hint, (20, 50))
