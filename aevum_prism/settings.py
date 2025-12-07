from dataclasses import dataclass
from typing import Tuple


Color = Tuple[int, int, int]


@dataclass
class Settings:
    width: int = 960
    height: int = 540
    fps: int = 60
    window_title: str = "Lumenfall (working title)"
    background_color: Color = (10, 12, 20)
    text_color: Color = (220, 225, 235)
