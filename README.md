# Lumenfall (working title)

PyGame scaffold for experimenting with the CCG core loop and UI.

## Setup
- `python -m venv .venv`
- `.\.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (macOS/Linux)
- `pip install -r requirements.txt`

## Run (UI)
- `python -m aevum_prism.ui.main_ui` (launches fullscreen; uses 800x600 logical resolution scaled to your display)

## Pack simulation (quick rarity test)
- `python -m aevum_prism.packs`
- Default pack size: 5 cards. Rarity chances/pity thresholds are defined in `aevum_prism/packs.py` (includes Astral between Secret and Divine).

## Pack opener UI
- Entry point: `python -m aevum_prism.ui.main_ui`
- Window 800x600 with pack opener and arena toggle (Tab or on-screen button); unified "Packs" view shows last pack + scrollable history.
- Packs cost 250 Vel; boxes cost 1 Erun (10 packs). Currency is earned in the arena (kill enemies).
- Arena stub: move with WASD/arrows, click enemies to defeat; every kill +100 Vel, every 10th kill spawns a boss worth 1 Erun.
- UI shows currency breakdown and pack history; rare pulls animate with flair. Equip bar (3 slots) is always visible; click to choose any owned Common–Mythic card from your collection, right-click to clear.
- Collection modal: click "Collection" in the UI to view owned cards; undiscovered cards show ??? (Secret/Astral/Divine hidden until found); includes rarity sort toggle and completion indicators (stars/crowns). Hover a card to see tier/element/lock (first instance); left-click toggles lock; right-click exchanges tier ≥ 2 for essence.
- Known issue: launching via `--help` exits after showing pygame banner; run without `--help` to use the UI.
- Saves: owned cards `saves/collection.json`, equipped cards `saves/equips.json`, instances/essence `saves/card_instances.json`.
