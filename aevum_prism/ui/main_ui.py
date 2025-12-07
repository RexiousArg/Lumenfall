from typing import List, Tuple

import pygame

from aevum_prism.packs import open_pack
from aevum_prism.instances import InstanceStore
from .pack_opener import (
    Arena,
    BUTTON_TEXT,
    BOX_COST,
    PACK_COST,
    PANEL_BORDER,
    PANEL_COLOR,
    REVEAL_DELAY,
    FLASH_DURATION,
    draw_background,
    draw_button,
    draw_collection,
    draw_currency,
    draw_equip_modal,
    draw_equip_slots,
    draw_history,
    draw_messages,
    draw_pack,
    draw_tooltip,
    equip_option_at_pos,
    make_vertical_gradient,
    CollectionManager,
    CurrencyBank,
    EquipManager,
    build_equippable_options,
)

WIDTH, HEIGHT = 800, 600


def run_ui() -> None:
    pygame.init()
    def make_screen(full: bool) -> pygame.Surface:
        flags = pygame.SCALED | (pygame.FULLSCREEN if full else 0)
        return pygame.display.set_mode((WIDTH, HEIGHT), flags)

    fullscreen = True
    screen = make_screen(fullscreen)
    pygame.display.set_caption("Lumenfall: Pack Opener")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 18)
    big_font = pygame.font.SysFont("consolas", 24)
    gradient = make_vertical_gradient((WIDTH, HEIGHT), (18, 20, 30), (8, 9, 16))

    button_pack = pygame.Rect(0, 0, 200, 54)
    button_pack.center = (WIDTH // 2 - 110, 210)
    button_box = pygame.Rect(0, 0, 200, 54)
    button_box.center = (WIDTH // 2 + 110, 210)
    button_mode = pygame.Rect(WIDTH - 180, 20, 150, 40)
    button_collection = pygame.Rect(WIDTH - 180, 70, 150, 40)
    button_sort = pygame.Rect(WIDTH - 200, 120, 170, 36)

    last_pack = None
    history: List[List[Tuple[str, str]]] = []
    packs_opened = 0
    reveal_start = None
    flash_timer = 0.0
    elapsed = 0.0

    mode = "pack"
    collection_open = False
    sort_rarest_first = True
    collection_scroll = 0.0
    collection_target_scroll = 0.0
    history_scroll = 0.0
    history_target_scroll = 0.0
    equip_modal_open = False
    equip_slot_index = None
    equip_scroll = 0.0
    equip_target_scroll = 0.0
    hover_text = ""

    bank = CurrencyBank(base_vel=1000)
    equip_manager = EquipManager()
    arena = Arena()
    messages: List[str] = []
    collection = CollectionManager()
    instance_store = InstanceStore()

    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        elapsed += dt
        mouse_pos = pygame.mouse.get_pos()
        clicks_left = []
        clicks_right = []
        attack_pressed = False
        hover_text = ""

        # Clear frame early to avoid any stale buffer edge cases.
        screen.fill((12, 14, 22))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if equip_modal_open:
                        equip_modal_open = False
                        equip_slot_index = None
                    elif collection_open:
                        collection_open = False
                    else:
                        running = False
                if event.key == pygame.K_TAB and not collection_open and not equip_modal_open:
                    mode = "arena" if mode == "pack" else "pack"
                if event.key == pygame.K_SPACE and mode == "arena":
                    attack_pressed = True
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    screen = make_screen(fullscreen)
                    gradient = make_vertical_gradient((WIDTH, HEIGHT), (18, 20, 30), (8, 9, 16))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicks_left.append(event.pos)
                if event.button == 3:
                    clicks_right.append(event.pos)
            elif event.type == pygame.MOUSEWHEEL:
                if equip_modal_open:
                    equip_target_scroll -= event.y * 40
                elif collection_open:
                    collection_target_scroll -= event.y * 40
                else:
                    history_target_scroll -= event.y * 40

        hovering_mode = button_mode.collidepoint(mouse_pos)
        hovering_collection = button_collection.collidepoint(mouse_pos)
        if not collection_open and not equip_modal_open and any(button_mode.collidepoint(c) for c in clicks_left):
            mode = "arena" if mode == "pack" else "pack"
        if not collection_open and not equip_modal_open and any(button_collection.collidepoint(c) for c in clicks_left):
            collection_open = True
            collection_scroll = 0.0
            collection_target_scroll = 0.0

        # Safety debug marker to ensure something visible every frame.
        pygame.draw.rect(screen, (255, 60, 60), (10, 10, 20, 20))
        screen.blit(font.render("DBG", True, (255, 255, 255)), (36, 10))

        if mode == "pack":
            hover_pack = button_pack.collidepoint(mouse_pos)
            hover_box = button_box.collidepoint(mouse_pos)
            can_pack = bank.can_afford(PACK_COST)
            can_box = bank.can_afford(BOX_COST)
            # Debug marker to confirm rendering loop is active.
            screen.blit(font.render("PACK MODE", True, (255, 255, 100)), (10, HEIGHT - 24))
            top_panel = pygame.Rect(16, 16, WIDTH - 32, 90)
            slot_w, slot_h = 140, 42
            start_x = top_panel.right - (slot_w + 10) * len(equip_manager.slots) - 12
            slot_rects = [
                pygame.Rect(start_x + i * (slot_w + 10), top_panel.y + 12, slot_w, slot_h)
                for i in range(len(equip_manager.slots))
            ]
            hover_slot_index = next((i for i, r in enumerate(slot_rects) if r.collidepoint(mouse_pos)), None)

            if not collection_open and not equip_modal_open:
                for idx, rect in enumerate(slot_rects):
                    if any(rect.collidepoint(c) for c in clicks_left):
                        equip_modal_open = True
                        equip_slot_index = idx
                        equip_scroll = 0.0
                        equip_target_scroll = 0.0
                if hover_slot_index is not None and any(slot_rects[hover_slot_index].collidepoint(c) for c in clicks_right):
                    equip_manager.clear_slot(hover_slot_index)
                    messages.append(f"Slot {hover_slot_index + 1} cleared")

                if any(button_pack.collidepoint(c) for c in clicks_left) and can_pack:
                    if bank.spend(PACK_COST):
                        last_pack = open_pack()
                        unlocked = collection.add_pack(last_pack)
                        equip_manager.sync_with_collection(collection)
                        messages.extend(unlocked)
                        packs_opened += 1
                        history.append(last_pack)
                        history = history[-50:]
                        reveal_start = elapsed
                        flash_timer = FLASH_DURATION

                if any(button_box.collidepoint(c) for c in clicks_left) and can_box:
                    if bank.spend(BOX_COST):
                        for _ in range(10):
                            pack = open_pack()
                            unlocked = collection.add_pack(pack)
                            equip_manager.sync_with_collection(collection)
                            messages.extend(unlocked)
                            last_pack = pack
                            packs_opened += 1
                            history.append(pack)
                        history = history[-50:]
                        reveal_start = elapsed
                        flash_timer = FLASH_DURATION

            flash_timer = max(0.0, flash_timer - dt)

            draw_background(screen, gradient, elapsed)
            pygame.draw.rect(screen, PANEL_COLOR, top_panel, border_radius=12)
            pygame.draw.rect(screen, PANEL_BORDER, top_panel, width=2, border_radius=12)
            header = big_font.render(f"Packs opened: {packs_opened}", True, (230, 230, 230))
            screen.blit(header, (top_panel.x + 12, top_panel.y + 10))
            draw_currency(screen, font, bank)
            draw_equip_slots(screen, font, slot_rects, equip_manager.slots, hover_slot_index)

            btn_panel = pygame.Rect(16, top_panel.bottom + 12, WIDTH - 32, 90)
            pygame.draw.rect(screen, PANEL_COLOR, btn_panel, border_radius=12)
            pygame.draw.rect(screen, PANEL_BORDER, btn_panel, width=2, border_radius=12)
            draw_button(
                screen, button_pack, f"{BUTTON_TEXT} ({PACK_COST} Vel)", big_font, hover_pack, enabled=can_pack and not collection_open and not equip_modal_open
            )
            draw_button(
                screen, button_box, "Open Box (1 Erun)", big_font, hover_box, enabled=can_box and not collection_open and not equip_modal_open
            )

            pack_panel = pygame.Rect(16, btn_panel.bottom + 16, WIDTH - 32, 140)
            pygame.draw.rect(screen, PANEL_COLOR, pack_panel, border_radius=12)
            pygame.draw.rect(screen, PANEL_BORDER, pack_panel, width=2, border_radius=12)
            pack_title = font.render("Last Pack", True, (220, 220, 220))
            screen.blit(pack_title, (pack_panel.x + 12, pack_panel.y + 8))
            if last_pack:
                draw_pack(screen, last_pack, font, y=pack_panel.y + 28, reveal_start=reveal_start, now=elapsed)

            hist_panel = pygame.Rect(16, pack_panel.bottom + 14, WIDTH - 32, 160)
            pygame.draw.rect(screen, PANEL_COLOR, hist_panel, border_radius=12)
            pygame.draw.rect(screen, PANEL_BORDER, hist_panel, width=2, border_radius=12)
            hist_title = font.render("History", True, (220, 220, 220))
            screen.blit(hist_title, (hist_panel.x + 12, hist_panel.y + 8))
            draw_history(screen, history, font, start_y=hist_panel.y + 32, scroll=history_scroll, height=hist_panel.height - 40)
            content_h = max(0, len(history) * 22)
            max_h_scroll = max(0.0, content_h - (hist_panel.height - 50))
            history_target_scroll = max(0.0, min(history_target_scroll, max_h_scroll))
            history_scroll += (history_target_scroll - history_scroll) * min(1.0, dt * 10.0)
            if abs(history_scroll - history_target_scroll) < 0.5:
                history_scroll = history_target_scroll

            if flash_timer > 0:
                alpha = int(140 * (flash_timer / FLASH_DURATION))
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((255, 255, 255, alpha))
                screen.blit(overlay, (0, 0))

        else:
            top_panel = pygame.Rect(16, 16, WIDTH - 32, 90)
            slot_w, slot_h = 140, 42
            start_x = top_panel.right - (slot_w + 10) * len(equip_manager.slots) - 12
            slot_rects = [
                pygame.Rect(start_x + i * (slot_w + 10), top_panel.y + 12, slot_w, slot_h)
                for i in range(len(equip_manager.slots))
            ]
            hover_slot_index = next((i for i, r in enumerate(slot_rects) if r.collidepoint(mouse_pos)), None)
            if not equip_modal_open:
                for idx, rect in enumerate(slot_rects):
                    if any(rect.collidepoint(c) for c in clicks_left):
                        equip_modal_open = True
                        equip_slot_index = idx
                        equip_scroll = equip_target_scroll = 0.0
                    if any(rect.collidepoint(c) for c in clicks_right):
                        equip_manager.clear_slot(idx)
                        messages.append(f"Slot {idx + 1} cleared")
            draw_background(screen, gradient, elapsed)
            pygame.draw.rect(screen, PANEL_COLOR, top_panel, border_radius=12)
            pygame.draw.rect(screen, PANEL_BORDER, top_panel, width=2, border_radius=12)
            header = big_font.render("Arena", True, (230, 230, 230))
            screen.blit(header, (top_panel.x + 12, top_panel.y + 10))
            draw_currency(screen, font, bank)
            draw_equip_slots(screen, font, slot_rects, equip_manager.slots, hover_slot_index)
            instr = font.render("WASD/Arrows move, click enemies or Space to attack. Tab to switch back.", True, (220, 220, 220))
            screen.blit(instr, (top_panel.x + 12, top_panel.y + 44))
            screen.blit(font.render("ARENA MODE", True, (255, 255, 120)), (10, HEIGHT - 24))

            arena_clicks = [] if equip_modal_open else clicks_left
            arena_attack = attack_pressed and not equip_modal_open
            arena.update(dt, bank, messages, arena_clicks, arena_attack)
            arena.draw(screen, font, messages)
            if messages:
                draw_messages(screen, font, messages)

        mode_label = "Go Arena" if mode == "pack" else "Go Packs"
        draw_button(screen, button_mode, mode_label, font, hovering_mode, enabled=not collection_open and not equip_modal_open)
        draw_button(screen, button_collection, "Collection", font, hovering_collection, enabled=not equip_modal_open)

        if equip_modal_open:
            equip_manager.sync_with_collection(collection)
            options = build_equippable_options(collection)
            equip_panel = pygame.Rect(80, 70, WIDTH - 160, HEIGHT - 140)
            max_scroll = draw_equip_modal(
                screen, font, big_font, options, equip_scroll, equip_manager.slots, equip_slot_index
            )
            equip_target_scroll = max(0.0, min(equip_target_scroll, max_scroll))
            equip_scroll += (equip_target_scroll - equip_scroll) * min(1.0, dt * 10.0)
            if abs(equip_scroll - equip_target_scroll) < 0.5:
                equip_scroll = equip_target_scroll

            if not options:
                warn = font.render("No owned equippable cards yet. Open packs to fill these slots.", True, (230, 220, 220))
                screen.blit(warn, warn.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

            for click in clicks_left:
                idx = equip_option_at_pos(click, equip_panel, options, equip_scroll)
                if idx is not None and equip_slot_index is not None and idx < len(options):
                    rarity, card, _ = options[idx]
                    equip_manager.set_slot(equip_slot_index, rarity, card)
                    messages.append(f"Equipped {card} ({rarity}) in slot {equip_slot_index + 1}")
                    equip_modal_open = False
                    equip_slot_index = None
                    break
            if equip_slot_index is not None and any(equip_panel.collidepoint(c) for c in clicks_right):
                equip_manager.clear_slot(equip_slot_index)
                messages.append(f"Slot {equip_slot_index + 1} cleared")
                equip_modal_open = False
                equip_slot_index = None

        if collection_open:
            hover_text, max_scroll = draw_collection(
                screen,
                font,
                big_font,
                collection,
                instance_store,
                mouse_pos,
                sort_rarest_first,
                collection_scroll,
                clicks_left,
                clicks_right,
                messages,
            )
            collection_target_scroll = max(0.0, min(collection_target_scroll, max_scroll))
            collection_scroll += (collection_target_scroll - collection_scroll) * min(1.0, dt * 10.0)
            if abs(collection_scroll - collection_target_scroll) < 0.5:
                collection_scroll = collection_target_scroll

            sort_label = "Sort: Rarest First" if sort_rarest_first else "Sort: Common First"
            sort_hover = button_sort.collidepoint(mouse_pos)
            draw_button(screen, button_sort, sort_label, font, sort_hover, enabled=True)
            if any(button_sort.collidepoint(c) for c in clicks_left):
                sort_rarest_first = not sort_rarest_first

            close_rect = pygame.Rect(button_sort.x, button_sort.y + 46, button_sort.width, button_sort.height)
            close_hover = close_rect.collidepoint(mouse_pos)
            draw_button(screen, close_rect, "Close", font, close_hover, enabled=True)
            if any(close_rect.collidepoint(c) for c in clicks_left):
                collection_open = False

            if hover_text:
                draw_tooltip(screen, font, hover_text, mouse_pos)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run_ui()
