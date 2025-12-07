"""
Pack opener UI with currency, arena combat stub, collection modal, and equip slots stub.
"""

import json
import math
import random
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pygame

from aevum_prism.packs import CARD_POOL, open_pack

WIDTH, HEIGHT = 800, 600
TITLE = "Lumenfall: Pack Opener"
BUTTON_TEXT = "Open Pack!"
PACK_SIZE = 5
MAX_HISTORY = 50

REVEAL_DELAY = 0.18
REVEAL_RAMP = 0.25
FLASH_DURATION = 0.4

VEL_PER_ERUN = 1000
VEL_PER_ZETH = VEL_PER_ERUN * 100
VEL_PER_VELARUN = VEL_PER_ZETH * 100
PACK_COST = 250
BOX_COST = VEL_PER_ERUN

RARITY_COLORS: Dict[str, Tuple[int, int, int]] = {
    "Common": (180, 180, 180),
    "Uncommon": (100, 200, 100),
    "Rare": (80, 140, 220),
    "Epic": (180, 80, 200),
    "Legendary": (220, 160, 60),
    "Mythic": (200, 60, 60),
    "Secret": (40, 40, 40),
    "Astral": (120, 200, 255),
    "Divine": (250, 250, 120),
}

BG_TOP = (18, 20, 30)
BG_BOTTOM = (8, 9, 16)
PANEL_COLOR = (26, 30, 44)
PANEL_BORDER = (74, 86, 118)

RARITY_ORDER = ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Mythic", "Secret", "Astral", "Divine"]
FLAIR_RARITIES = {"Legendary", "Mythic", "Secret", "Divine"}
EQUIPPABLE_RARITIES = {"Common", "Uncommon", "Rare", "Epic", "Legendary", "Mythic"}
EQUIP_SLOT_COUNT = 3


class CollectionManager:
    def __init__(self, path: Path | None = None) -> None:
        self.path = path or Path("saves/collection.json")
        self.data: Dict[str, Dict[str, int]] = {r: {} for r in CARD_POOL.keys()}
        self.meta: Dict[str, object] = {
            "completed": {r: {"star": False, "crown": False} for r in CARD_POOL.keys()},
            "flair": None,
        }
        self._ensure_dir()
        self._load()

    def _ensure_dir(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _load(self) -> None:
        if self.path.exists():
            try:
                loaded = json.loads(self.path.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    for rarity, cards in loaded.items():
                        if rarity in self.data and isinstance(cards, dict):
                            self.data[rarity] = {c: int(v) for c, v in cards.items()}
                    if "completed" in loaded or "flair" in loaded:
                        self.meta["completed"] = {
                            r: {
                                "star": bool(loaded.get("completed", {}).get(r, {}).get("star", False)),
                                "crown": bool(loaded.get("completed", {}).get(r, {}).get("crown", False)),
                            }
                            for r in CARD_POOL.keys()
                        }
                        self.meta["flair"] = loaded.get("flair", None)
            except Exception:
                pass

    def _save(self) -> None:
        self._ensure_dir()
        payload = {**self.data, "completed": self.meta["completed"], "flair": self.meta["flair"]}
        self.path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def add_pack(self, pack: Sequence[Tuple[str, str]]) -> List[str]:
        unlocked: List[str] = []
        for card, rarity in pack:
            if rarity not in self.data:
                self.data[rarity] = {}
            self.data[rarity][card] = self.data[rarity].get(card, 0) + 1
        for rarity in CARD_POOL.keys():
            owned, total = self.rarity_completion(rarity)
            complete_cards = total > 0 and owned == total
            if complete_cards and not self.meta["completed"][rarity]["star"]:
                self.meta["completed"][rarity]["star"] = True
                unlocked.append(f"Completed {rarity} collection!")
            if complete_cards and not self.meta["completed"][rarity]["crown"]:
                self.meta["completed"][rarity]["crown"] = True
        self._save()
        return unlocked

    def owned_count(self, rarity: str, card: str) -> int:
        return self.data.get(rarity, {}).get(card, 0)

    def rarity_completion(self, rarity: str) -> Tuple[int, int]:
        total = len(CARD_POOL.get(rarity, []))
        owned = sum(1 for c in CARD_POOL.get(rarity, []) if self.owned_count(rarity, c) > 0)
        return owned, total

    def overall_completion(self) -> Tuple[int, int]:
        owned = 0
        total = 0
        for rarity, cards in CARD_POOL.items():
            total += len(cards)
            owned += sum(1 for c in cards if self.owned_count(rarity, c) > 0)
        return owned, total

    def set_flair(self, rarity: str, flair_type: str) -> None:
        if rarity in CARD_POOL:
            self.meta["flair"] = {"rarity": rarity, "type": flair_type}
            self._save()

    def flair_label(self) -> str:
        flair = self.meta.get("flair")
        if not flair:
            return "Flair: None"
        return f"Flair: {flair['rarity']} {flair['type']}"

    def remove_card(self, rarity: str, card: str, count: int = 1) -> None:
        if rarity not in self.data:
            return
        current = self.data[rarity].get(card, 0)
        new_val = max(0, current - count)
        if new_val <= 0 and card in self.data[rarity]:
            self.data[rarity].pop(card, None)
        else:
            self.data[rarity][card] = new_val
        self._save()


class CurrencyBank:
    def __init__(self, base_vel: int = 0) -> None:
        self.base_vel = base_vel

    def add_vel(self, amount: int) -> None:
        self.base_vel += amount

    def add_erun(self, amount: int = 1) -> None:
        self.base_vel += amount * VEL_PER_ERUN

    def can_afford(self, cost: int) -> bool:
        return self.base_vel >= cost

    def spend(self, cost: int) -> bool:
        if self.can_afford(cost):
            self.base_vel -= cost
            return True
        return False

    def breakdown(self) -> Tuple[int, int, int, int]:
        velarun = self.base_vel // VEL_PER_VELARUN
        remainder = self.base_vel % VEL_PER_VELARUN
        zeth = remainder // VEL_PER_ZETH
        remainder %= VEL_PER_ZETH
        erun = remainder // VEL_PER_ERUN
        vel = remainder % VEL_PER_ERUN
        return velarun, zeth, erun, vel

    def format_line(self) -> str:
        velarun, zeth, erun, vel = self.breakdown()
        return f"Velarun: {velarun}  Zeth: {zeth}  Erun: {erun}  Vel: {vel}"


class EquipManager:
    def __init__(self, path: Path | None = None, slot_count: int = EQUIP_SLOT_COUNT) -> None:
        self.path = path or Path("saves/equips.json")
        self.slot_count = slot_count
        self.slots: List[Dict[str, str] | None] = [None for _ in range(slot_count)]
        self._ensure_dir()
        self._load()

    def _ensure_dir(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def _valid_entry(self, entry: object) -> Dict[str, str] | None:
        if not isinstance(entry, dict):
            return None
        rarity = entry.get("rarity")
        card = entry.get("card")
        if isinstance(rarity, str) and isinstance(card, str) and rarity in EQUIPPABLE_RARITIES:
            return {"rarity": rarity, "card": card}
        return None

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            loaded = json.loads(self.path.read_text(encoding="utf-8"))
            if isinstance(loaded, list):
                parsed: List[Dict[str, str] | None] = []
                for entry in loaded[: self.slot_count]:
                    parsed.append(self._valid_entry(entry))
                while len(parsed) < self.slot_count:
                    parsed.append(None)
                self.slots = parsed
        except Exception:
            pass

    def _save(self) -> None:
        self._ensure_dir()
        self.path.write_text(json.dumps(self.slots, indent=2), encoding="utf-8")

    def sync_with_collection(self, collection: CollectionManager) -> None:
        changed = False
        for idx, slot in enumerate(self.slots):
            if slot and collection.owned_count(slot["rarity"], slot["card"]) <= 0:
                self.slots[idx] = None
                changed = True
        if changed:
            self._save()

    def set_slot(self, index: int, rarity: str, card: str) -> None:
        if 0 <= index < self.slot_count and rarity in EQUIPPABLE_RARITIES:
            self.slots[index] = {"rarity": rarity, "card": card}
            self._save()

    def clear_slot(self, index: int) -> None:
        if 0 <= index < self.slot_count:
            self.slots[index] = None
            self._save()

    def labels(self) -> List[str]:
        labels: List[str] = []
        for slot in self.slots:
            if slot:
                labels.append(f"{slot['card']} ({slot['rarity']})")
            else:
                labels.append("Empty")
        return labels


def build_equippable_options(collection: CollectionManager) -> List[Tuple[str, str, int]]:
    """Return (rarity, card, count) for owned equippable cards sorted by rarity then name."""
    options: List[Tuple[str, str, int]] = []
    for rarity in RARITY_ORDER:
        if rarity not in EQUIPPABLE_RARITIES:
            continue
        for card in CARD_POOL.get(rarity, []):
            count = collection.owned_count(rarity, card)
            if count > 0:
                options.append((rarity, card, count))
    return options


# --- UI Helpers ---


def make_vertical_gradient(size: Tuple[int, int], top: Tuple[int, int, int], bottom: Tuple[int, int, int]) -> pygame.Surface:
    width, height = size
    gradient = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height - 1)
        color = (
            int(top[0] + (bottom[0] - top[0]) * t),
            int(top[1] + (bottom[1] - top[1]) * t),
            int(top[2] + (bottom[2] - top[2]) * t),
        )
        pygame.draw.line(gradient, color, (0, y), (width, y))
    return gradient.convert()


def draw_background(surface: pygame.Surface, gradient: pygame.Surface, elapsed: float) -> None:
    surface.blit(gradient, (0, 0))


def draw_button(surface: pygame.Surface, rect: pygame.Rect, text: str, font: pygame.font.Font, hovered: bool, enabled: bool = True) -> None:
    base_color = (70, 110, 180) if hovered and enabled else (60, 90, 150)
    if not enabled:
        base_color = (50, 60, 80)
    pygame.draw.rect(surface, base_color, rect, border_radius=10)
    pygame.draw.rect(surface, (255, 255, 255), rect, width=2, border_radius=10)
    label_color = (255, 255, 255) if enabled else (160, 160, 160)
    label = font.render(text, True, label_color)
    surface.blit(label, label.get_rect(center=rect.center))


def draw_pack(surface: pygame.Surface, pack: Sequence[Tuple[str, str]], font: pygame.font.Font, y: int, reveal_start: float | None, now: float) -> None:
    margin = 32
    box_width = (WIDTH - margin * 2 - 12 * (PACK_SIZE - 1)) // PACK_SIZE
    box_height = 110
    for idx, (card, rarity) in enumerate(pack):
        x = margin + idx * (box_width + 12)
        color = RARITY_COLORS.get(rarity, (200, 200, 200))
        reveal_time = None if reveal_start is None else (reveal_start + idx * REVEAL_DELAY)
        revealed = reveal_time is None or now >= reveal_time
        progress = 0.0
        if revealed and reveal_time is not None:
            progress = min(1.0, (now - reveal_time) / REVEAL_RAMP)

        scale = 1.0 + 0.06 * (1.0 - math.cos(progress * math.pi)) if revealed else 1.0
        scaled_w = int(box_width * scale)
        scaled_h = int(box_height * scale)
        sx = x + (box_width - scaled_w) // 2
        sy = y + (box_height - scaled_h) // 2

        shadow = pygame.Rect(sx + 4, sy + 6, scaled_w, scaled_h)
        pygame.draw.rect(surface, (0, 0, 0, 80), shadow, border_radius=12)
        pygame.draw.rect(surface, color, (sx, sy, scaled_w, scaled_h), border_radius=12)
        pygame.draw.rect(surface, (20, 20, 20), (sx, sy, scaled_w, scaled_h), width=2, border_radius=12)

        if revealed and rarity in FLAIR_RARITIES:
            pulse = 0.4 + 0.6 * abs(math.sin(now * 6.0 + idx))
            glow_color = tuple(min(255, int(c * (1.0 + 0.4 * pulse))) for c in color)
            pygame.draw.rect(
                surface,
                glow_color,
                (sx - 4, sy - 4, scaled_w + 8, scaled_h + 8),
                width=3,
                border_radius=14,
            )
            if rarity == "Divine":
                star_color = (255, 255, 200)
                cx, cy = sx + scaled_w // 2, sy + scaled_h // 2
                pygame.draw.line(surface, star_color, (cx - 6, cy), (cx + 6, cy), width=2)
                pygame.draw.line(surface, star_color, (cx, cy - 6), (cx, cy + 6), width=2)

        if revealed:
            text = font.render(f"{card}", True, (10, 10, 10))
            rarity_text = font.render(rarity, True, (10, 10, 10))
        else:
            text = font.render("???", True, (30, 30, 30))
            rarity_text = font.render("...", True, (30, 30, 30))

        surface.blit(text, (sx + 8, sy + 8))
        surface.blit(rarity_text, (sx + 8, sy + 34))


def draw_history(surface: pygame.Surface, history, font: pygame.font.Font, start_y: int, scroll: float, height: int) -> None:
    list_y = start_y - scroll
    line_h = 22
    for idx, pack in enumerate(history):
        line = f"#{len(history)-idx}: " + " | ".join(r for _, r in pack)
        lbl = font.render(line, True, (210, 210, 210))
        if start_y <= list_y <= start_y + height - 16:
            surface.blit(lbl, (20, list_y))
        list_y += line_h


def draw_currency(surface: pygame.Surface, font: pygame.font.Font, bank: CurrencyBank) -> None:
    line = bank.format_line()
    label = font.render(line, True, (230, 230, 230))
    surface.blit(label, (20, 60))


def draw_messages(surface: pygame.Surface, font: pygame.font.Font, messages: List[str]) -> None:
    y = HEIGHT - 80
    for msg in messages[-3:]:
        label = font.render(msg, True, (220, 220, 220))
        surface.blit(label, (20, y))
        y += 18


def draw_tooltip(surface: pygame.Surface, font: pygame.font.Font, text: str, pos: Tuple[int, int]) -> None:
    if not text:
        return
    padding = 6
    label = font.render(text, True, (240, 240, 240))
    rect = label.get_rect()
    rect.topleft = (pos[0] + 12, pos[1] + 12)
    bg = pygame.Rect(rect.x - padding, rect.y - padding, rect.width + 2 * padding, rect.height + 2 * padding)
    pygame.draw.rect(surface, (20, 20, 20), bg, border_radius=4)
    pygame.draw.rect(surface, (200, 200, 200), bg, width=1, border_radius=4)
    surface.blit(label, rect)


def draw_equip_slots(
    surface: pygame.Surface, font: pygame.font.Font, slot_rects: List[pygame.Rect], slots: List[Dict[str, str] | None], hover_idx: int | None
) -> None:
    for idx, rect in enumerate(slot_rects):
        slot = slots[idx]
        rarity = slot["rarity"] if slot else None
        color = RARITY_COLORS.get(rarity or "Common", (90, 100, 130))
        bg = tuple(max(0, c - 40) for c in color)
        if hover_idx == idx:
            bg = tuple(min(255, c + 30) for c in bg)
        pygame.draw.rect(surface, bg, rect, border_radius=8)
        border = color if rarity else (160, 160, 180)
        pygame.draw.rect(surface, border, rect, width=2, border_radius=8)
        label = slot["card"] if slot else "Equip Card"
        sub = slot["rarity"] if slot else "Slot"
        lbl_surf = font.render(label, True, (15, 15, 20))
        sub_surf = font.render(sub, True, (35, 35, 60))
        surface.blit(lbl_surf, (rect.x + 10, rect.y + 6))
        surface.blit(sub_surf, (rect.x + 10, rect.y + 22))


def draw_equip_modal(
    surface: pygame.Surface,
    font: pygame.font.Font,
    big_font: pygame.font.Font,
    options: List[Tuple[str, str, int]],
    scroll: float,
    slots: List[Dict[str, str] | None],
    slot_index: int | None,
) -> float:
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))

    panel = pygame.Rect(80, 70, WIDTH - 160, HEIGHT - 140)
    pygame.draw.rect(surface, PANEL_COLOR, panel, border_radius=12)
    pygame.draw.rect(surface, PANEL_BORDER, panel, width=2, border_radius=12)

    title = "Select a card to equip" if slot_index is None else f"Equip Slot {slot_index + 1}"
    surface.blit(big_font.render(title, True, (230, 230, 230)), (panel.x + 14, panel.y + 14))
    current = slots[slot_index]["card"] if slot_index is not None and slots[slot_index] else "None"
    surface.blit(font.render(f"Current: {current}", True, (200, 200, 220)), (panel.x + 14, panel.y + 42))

    list_area = pygame.Rect(panel.x + 12, panel.y + 70, panel.width - 24, panel.height - 90)
    pygame.draw.rect(surface, (20, 22, 30), list_area, border_radius=8)
    pygame.draw.rect(surface, PANEL_BORDER, list_area, width=1, border_radius=8)

    y = list_area.y + 6 - scroll
    line_h = 26
    for rarity, card, count in options:
        if y + line_h < list_area.y or y > list_area.bottom:
            y += line_h
            continue
        row_rect = pygame.Rect(list_area.x + 6, y, list_area.width - 12, line_h - 2)
        base = tuple(max(0, c - 70) for c in RARITY_COLORS.get(rarity, (80, 80, 80)))
        pygame.draw.rect(surface, base, row_rect, border_radius=6)
        pygame.draw.rect(surface, RARITY_COLORS.get(rarity, (130, 130, 130)), row_rect, width=1, border_radius=6)
        surface.blit(font.render(card, True, (240, 240, 240)), (row_rect.x + 8, row_rect.y + 4))
        surface.blit(font.render(rarity, True, (200, 200, 220)), (row_rect.x + 220, row_rect.y + 4))
        surface.blit(font.render(f"x{count}", True, (220, 220, 240)), (row_rect.right - 50, row_rect.y + 4))
        y += line_h

    instr = "Click a row to equip. Press Esc or Close to return. Right-click to clear."
    surface.blit(font.render(instr, True, (200, 200, 200)), (panel.x + 14, panel.bottom - 24))

    content_h = max(0, len(options) * line_h)
    max_scroll = max(0.0, content_h - list_area.height + 8)
    return max_scroll


def equip_option_at_pos(
    pos: Tuple[int, int], panel: pygame.Rect, options: List[Tuple[str, str, int]], scroll: float, line_h: int = 26
) -> int | None:
    list_area = pygame.Rect(panel.x + 12, panel.y + 70, panel.width - 24, panel.height - 90)
    if not list_area.collidepoint(pos):
        return None
    relative_y = pos[1] - list_area.y + scroll - 6
    if relative_y < 0:
        return None
    idx = int(relative_y // line_h)
    if 0 <= idx < len(options):
        return idx
    return None


def draw_collection(
    surface: pygame.Surface,
    font: pygame.font.Font,
    big_font: pygame.font.Font,
    collection: CollectionManager,
    instance_store,
    mouse_pos: Tuple[int, int],
    sort_rarest_first: bool,
    scroll_offset: float,
    clicks_left,
    clicks_right,
    messages,
) -> Tuple[str, float]:
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0, 0))

    panel = pygame.Rect(40, 60, WIDTH - 80, HEIGHT - 120)
    pygame.draw.rect(surface, PANEL_COLOR, panel, border_radius=12)
    pygame.draw.rect(surface, PANEL_BORDER, panel, width=2, border_radius=12)

    owned_overall, total_overall = collection.overall_completion()
    percent_overall = int((owned_overall / total_overall) * 100) if total_overall > 0 else 0
    header = big_font.render(
        f"Collection ({owned_overall}/{total_overall}) • {percent_overall}%", True, (230, 230, 230)
    )
    surface.blit(header, (panel.x + 16, panel.y + 12))

    sub = font.render("Sort: Rarest ⇄ Common", True, (180, 180, 180))
    surface.blit(sub, (panel.x + 16, panel.y + 44))
    flair_line = font.render(collection.flair_label(), True, (180, 180, 180))
    surface.blit(flair_line, (panel.x + 300, panel.y + 44))

    content_x = panel.x + 16
    content_y = panel.y + 70
    visible_h = panel.height - 90
    max_height = 0
    hover_text = ""

    col_width = 110
    row_height = 120
    cards_per_row = max(1, (panel.width - 32) // col_width)

    for rarity in (list(reversed(RARITY_ORDER)) if sort_rarest_first else RARITY_ORDER):
        cards = CARD_POOL.get(rarity, [])
        if rarity in {"Secret", "Astral", "Divine"} and all(collection.owned_count(rarity, c) == 0 for c in cards):
            continue
        owned_r, total_r = collection.rarity_completion(rarity)
        if owned_r <= 0:
            continue
        rarity_pct = int((owned_r / total_r) * 100) if total_r > 0 else 0

        ry = content_y + max_height - scroll_offset
        rarity_label = font.render(rarity, True, (230, 230, 230))
        surface.blit(rarity_label, (content_x, ry))
        pct_label = font.render(f"{owned_r}/{total_r} ({rarity_pct}%)", True, (190, 190, 190))
        surface.blit(pct_label, (content_x + 140, ry))

        star_rect = pygame.Rect(panel.right - 140, ry, 22, 22)
        crown_rect = pygame.Rect(panel.right - 100, ry, 22, 22)
        if collection.meta["completed"].get(rarity, {}).get("star", False):
            pygame.draw.polygon(
                surface,
                RARITY_COLORS.get(rarity, (250, 230, 150)),
                [
                    (star_rect.centerx, star_rect.y),
                    (star_rect.x, star_rect.centery - 4),
                    (star_rect.centerx - 6, star_rect.bottom),
                    (star_rect.centerx + 6, star_rect.bottom),
                    (star_rect.right, star_rect.centery - 4),
                ],
            )
            pygame.draw.rect(surface, (20, 20, 20), star_rect, width=1, border_radius=4)
        if collection.meta["completed"].get(rarity, {}).get("crown", False):
            pygame.draw.rect(surface, RARITY_COLORS.get(rarity, (250, 230, 150)), crown_rect, border_radius=3)
            pygame.draw.rect(surface, (20, 20, 20), crown_rect, width=1, border_radius=3)

        if star_rect.collidepoint(mouse_pos) and collection.meta["completed"].get(rarity, {}).get("star", False):
            hover_text = f"Set flair: {rarity} star"
            if pygame.mouse.get_pressed()[0]:
                collection.set_flair(rarity, "star")
        if crown_rect.collidepoint(mouse_pos) and collection.meta["completed"].get(rarity, {}).get("crown", False):
            hover_text = f"Set flair: {rarity} crown"
            if pygame.mouse.get_pressed()[0]:
                collection.set_flair(rarity, "crown")

        max_height += 20
        for idx, card in enumerate(cards):
            owned = collection.owned_count(rarity, card)
            row = idx // cards_per_row
            col = idx % cards_per_row
            x = content_x + col * col_width
            y = content_y + max_height + row * row_height - scroll_offset
            rect = pygame.Rect(x, y, col_width - 10, row_height - 16)
            if rect.bottom < panel.y + 60 or rect.top > panel.bottom - 20:
                continue
            color = RARITY_COLORS.get(rarity, (160, 160, 160))
            if owned <= 0:
                color = (50, 50, 50)
            pygame.draw.rect(surface, color, rect, border_radius=8)
            pygame.draw.rect(surface, (20, 20, 20), rect, width=2, border_radius=8)

            name_text = "???" if owned <= 0 else card
            label = font.render(name_text, True, (10, 10, 10))
            surface.blit(label, (rect.x + 8, rect.y + 8))
            if owned > 1:
                count_label = font.render(f"x{owned}", True, (10, 10, 10))
                surface.blit(count_label, (rect.right - 10 - count_label.get_width(), rect.bottom - 24))
            if rect.collidepoint(mouse_pos):
                hover_text = f"{card if owned > 0 else '???'} • {rarity} • owned: {owned}"
                if owned > 0:
                    insts = instance_store.instances_for_card(card)
                    if insts:
                        inst = insts[0]
                        tier = inst.get("tier", 0)
                        elem = inst.get("element", "Unknown")
                        locked = inst.get("locked", False)
                        tier_text = "-" if rarity in {"Common", "Uncommon"} else tier
                        hover_text += f" | Tier: {tier_text} | Element: {elem} | Locked: {locked}"
                    if any(rect.collidepoint(c) for c in clicks_left) and insts:
                        inst = insts[0]
                        new_state = not inst.get("locked", False)
                        instance_store.toggle_lock(inst.get("instance_id"), new_state)
                        messages.append(f"{'Locked' if new_state else 'Unlocked'} {card}")
                    if any(rect.collidepoint(c) for c in clicks_right) and insts:
                        inst = insts[0]
                        tier = inst.get("tier", 0)
                        if tier >= 2:
                            gained = instance_store.exchange_instance(inst.get("instance_id"), collection)
                            if gained:
                                messages.append(f"Exchanged {card} for {gained} {rarity} essence")
        rows = math.ceil(len(cards) / cards_per_row)
        max_height += rows * row_height + 20

    content_total_height = max_height
    max_scroll = max(0.0, content_total_height - visible_h)
    return hover_text, max_scroll




# UI helpers (background, buttons, pack display, history, tooltips)

def make_vertical_gradient(size: Tuple[int, int], top: Tuple[int, int, int], bottom: Tuple[int, int, int]) -> pygame.Surface:
    width, height = size
    gradient = pygame.Surface((width, height))
    for y in range(height):
        t = y / max(1, height - 1)
        color = (
            int(top[0] + (bottom[0] - top[0]) * t),
            int(top[1] + (bottom[1] - top[1]) * t),
            int(top[2] + (bottom[2] - top[2]) * t),
        )
        pygame.draw.line(gradient, color, (0, y), (width, y))
    return gradient


def draw_background(surface: pygame.Surface, gradient: pygame.Surface, elapsed: float) -> None:
    surface.blit(gradient, (0, 0))
    stripe = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    alpha = 30
    stripe.fill((255, 255, 255, 0))
    offset = int((math.sin(elapsed * 0.5) + 1) * 20)
    for x in range(-WIDTH, WIDTH * 2, 80):
        pygame.draw.polygon(
            stripe,
            (255, 255, 255, alpha),
            [(x + offset, 0), (x + 40 + offset, 0), (x - 40 + offset, HEIGHT), (x - 80 + offset, HEIGHT)],
        )
    surface.blit(stripe, (0, 0), special_flags=pygame.BLEND_ALPHA_SDL2)


def draw_button(surface: pygame.Surface, rect: pygame.Rect, text: str, font: pygame.font.Font, hovered: bool, enabled: bool = True) -> None:
    base_color = (70, 110, 180) if hovered and enabled else (60, 90, 150)
    if not enabled:
        base_color = (50, 60, 80)
    pygame.draw.rect(surface, base_color, rect, border_radius=10)
    pygame.draw.rect(surface, (255, 255, 255), rect, width=2, border_radius=10)
    label_color = (255, 255, 255) if enabled else (160, 160, 160)
    label = font.render(text, True, label_color)
    surface.blit(label, label.get_rect(center=rect.center))


def draw_pack(surface: pygame.Surface, pack: Sequence[Tuple[str, str]], font: pygame.font.Font, y: int, reveal_start: float | None, now: float) -> None:
    margin = 32
    box_width = (WIDTH - margin * 2 - 12 * (PACK_SIZE - 1)) // PACK_SIZE
    box_height = 110
    for idx, (card, rarity) in enumerate(pack):
        x = margin + idx * (box_width + 12)
        color = RARITY_COLORS.get(rarity, (200, 200, 200))
        reveal_time = None if reveal_start is None else (reveal_start + idx * REVEAL_DELAY)
        revealed = reveal_time is None or now >= reveal_time
        progress = 0.0
        if revealed and reveal_time is not None:
            progress = min(1.0, (now - reveal_time) / REVEAL_RAMP)

        scale = 1.0 + 0.06 * (1.0 - math.cos(progress * math.pi)) if revealed else 1.0
        scaled_w = int(box_width * scale)
        scaled_h = int(box_height * scale)
        sx = x + (box_width - scaled_w) // 2
        sy = y + (box_height - scaled_h) // 2

        shadow = pygame.Rect(sx + 4, sy + 6, scaled_w, scaled_h)
        pygame.draw.rect(surface, (0, 0, 0, 80), shadow, border_radius=12)
        pygame.draw.rect(surface, color, (sx, sy, scaled_w, scaled_h), border_radius=12)
        pygame.draw.rect(surface, (20, 20, 20), (sx, sy, scaled_w, scaled_h), width=2, border_radius=12)

        if revealed and rarity in FLAIR_RARITIES:
            pulse = 0.4 + 0.6 * abs(math.sin(now * 6.0 + idx))
            glow_color = tuple(min(255, int(c * (1.0 + 0.4 * pulse))) for c in color)
            pygame.draw.rect(
                surface,
                glow_color,
                (sx - 4, sy - 4, scaled_w + 8, scaled_h + 8),
                width=3,
                border_radius=14,
            )
            if rarity == "Divine":
                star_color = (255, 255, 200)
                cx, cy = sx + scaled_w // 2, sy + scaled_h // 2
                pygame.draw.line(surface, star_color, (cx - 6, cy), (cx + 6, cy), width=2)
                pygame.draw.line(surface, star_color, (cx, cy - 6), (cx, cy + 6), width=2)

        if revealed:
            text = font.render(f"{card}", True, (10, 10, 10))
            rarity_text = font.render(rarity, True, (10, 10, 10))
        else:
            text = font.render("???", True, (30, 30, 30))
            rarity_text = font.render("...", True, (30, 30, 30))

        surface.blit(text, (sx + 8, sy + 8))
        surface.blit(rarity_text, (sx + 8, sy + 34))


def draw_history(surface: pygame.Surface, history, font: pygame.font.Font, start_y: int, scroll: float, height: int) -> None:
    list_y = start_y - scroll
    line_h = 22
    for idx, pack in enumerate(history):
        line = f"#{len(history)-idx}: " + " | ".join(r for _, r in pack)
        lbl = font.render(line, True, (210, 210, 210))
        if start_y <= list_y <= start_y + height - 16:
            surface.blit(lbl, (20, list_y))
        list_y += line_h


def draw_currency(surface: pygame.Surface, font: pygame.font.Font, bank: CurrencyBank) -> None:
    line = bank.format_line()
    label = font.render(line, True, (230, 230, 230))
    surface.blit(label, (20, 60))


def draw_messages(surface: pygame.Surface, font: pygame.font.Font, messages: List[str]) -> None:
    y = HEIGHT - 80
    for msg in messages[-3:]:
        label = font.render(msg, True, (220, 220, 220))
        surface.blit(label, (20, y))
        y += 18


def draw_tooltip(surface: pygame.Surface, font: pygame.font.Font, text: str, pos: Tuple[int, int]) -> None:
    if not text:
        return
    padding = 6
    label = font.render(text, True, (240, 240, 240))
    rect = label.get_rect()
    rect.topleft = (pos[0] + 12, pos[1] + 12)
    bg = pygame.Rect(rect.x - padding, rect.y - padding, rect.width + 2 * padding, rect.height + 2 * padding)
    pygame.draw.rect(surface, (20, 20, 20), bg, border_radius=4)
    pygame.draw.rect(surface, (200, 200, 200), bg, width=1, border_radius=4)
    surface.blit(label, rect)


# Arena combat stub (will flesh out further)

class Arena:
    def __init__(self) -> None:
        self.player_pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.player_speed = 220.0
        self.player_radius = 14
        self.max_hp = 10
        self.hp = self.max_hp
        self.base_attack = 1
        self.attack_range = 60
        self.enemies: List[Dict] = []
        self.spawn_timer = 0.0
        self.kill_count = 0
        self.boss_pending = False
        self.game_over = False
        self.game_over_timer = 0.0

    def spawn_enemy(self, boss: bool = False) -> None:
        size = 30 if boss else 22
        speed = 70 if boss else 60
        hp = 10 if boss else 2
        dmg = 3 if boss else 1
        pos = pygame.Vector2(random.uniform(30, WIDTH - 30), random.uniform(100, HEIGHT - 30))
        self.enemies.append({"pos": pos, "size": size, "speed": speed, "boss": boss, "hp": hp, "dmg": dmg})

    def update(
        self, dt: float, bank: CurrencyBank, messages: List[str], clicks: List[Tuple[int, int]], attack_pressed: bool
    ) -> None:
        if self.game_over:
            self.game_over_timer -= dt
            if self.game_over_timer <= 0:
                self.reset()
            return

        keys = pygame.key.get_pressed()
        move = pygame.Vector2(
            (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT]),
            (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP]),
        )
        if move.length_squared() > 0:
            move = move.normalize() * self.player_speed * dt
        self.player_pos += move
        self.player_pos.x = max(20, min(WIDTH - 20, self.player_pos.x))
        self.player_pos.y = max(100, min(HEIGHT - 20, self.player_pos.y))

        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_enemy(boss=self.boss_pending)
            self.boss_pending = False
            self.spawn_timer = random.uniform(1.0, 2.0)

        for enemy in list(self.enemies):
            direction = self.player_pos - enemy["pos"]
            dist = direction.length()
            if dist > 0 and dist < 400:
                enemy["pos"] += direction.normalize() * enemy["speed"] * dt
            if dist <= self.player_radius + enemy["size"] * 0.5:
                self.hp -= enemy["dmg"]
                self._kill_enemy(enemy, bank, messages, counted_hit=False)
                if self.hp <= 0:
                    self.hp = 0
                    self.game_over = True
                    self.game_over_timer = 2.0
                    messages.append("Game Over!")

        if clicks:
            for click_pos in clicks:
                for enemy in list(self.enemies):
                    ex, ey = enemy["pos"]
                    half = enemy["size"] * 0.5
                    rect = pygame.Rect(ex - half, ey - half, enemy["size"], enemy["size"])
                    if rect.collidepoint(click_pos):
                        self._kill_enemy(enemy, bank, messages, counted_hit=True)

        if attack_pressed and not self.game_over:
            for enemy in list(self.enemies):
                if (enemy["pos"] - self.player_pos).length() <= self.attack_range:
                    enemy["hp"] -= self.base_attack
                    if enemy["hp"] <= 0:
                        self._kill_enemy(enemy, bank, messages, counted_hit=True)

    def _kill_enemy(self, enemy: Dict, bank: CurrencyBank, messages: List[str], counted_hit: bool = True) -> None:
        self.enemies.remove(enemy)
        self.kill_count += 1
        if counted_hit:
            if enemy["boss"]:
                bank.add_erun(1)
                messages.append("Boss defeated +1 Erun")
            else:
                bank.add_vel(100)
                messages.append("+100 Vel")
        if self.kill_count % 10 == 0:
            self.boss_pending = True

    def reset(self) -> None:
        self.hp = self.max_hp
        self.enemies.clear()
        self.game_over = False
        self.game_over_timer = 0.0

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, messages: List[str]) -> None:
        pygame.draw.circle(surface, (70, 140, 255), self.player_pos, self.player_radius)
        for enemy in self.enemies:
            color = (200, 60, 60) if not enemy["boss"] else (255, 100, 100)
            half = enemy["size"] * 0.5
            pos = (enemy["pos"].x - half, enemy["pos"].y - half, enemy["size"], enemy["size"])
            pygame.draw.rect(surface, color, pos, border_radius=4)
            bar_w = enemy["size"]
            hp_pct = max(0, enemy["hp"]) / (10 if enemy["boss"] else 2)
            pygame.draw.rect(surface, (40, 40, 40), (enemy["pos"].x - bar_w / 2, enemy["pos"].y - half - 8, bar_w, 4))
            pygame.draw.rect(surface, (200, 80, 80), (enemy["pos"].x - bar_w / 2, enemy["pos"].y - half - 8, bar_w * hp_pct, 4))

        kills_text = font.render(f"Kills: {self.kill_count} (boss every 10)", True, (230, 230, 230))
        surface.blit(kills_text, (20, 90))
        if self.boss_pending:
            pending = font.render("Boss incoming!", True, (255, 180, 60))
            surface.blit(pending, (200, 90))

        bar_w, bar_h = 200, 16
        x, y = WIDTH - bar_w - 20, 90
        pygame.draw.rect(surface, (50, 50, 50), (x, y, bar_w, bar_h), border_radius=6)
        hp_w = int(bar_w * (self.hp / self.max_hp))
        pygame.draw.rect(surface, (80, 200, 120), (x, y, hp_w, bar_h), border_radius=6)
        hp_text = font.render(f"HP: {self.hp}/{self.max_hp}", True, (230, 230, 230))
        surface.blit(hp_text, (x, y - 18))

        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            surface.blit(overlay, (0, 0))
            go_text = font.render("Game Over - resetting...", True, (255, 180, 180))
            surface.blit(go_text, go_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
