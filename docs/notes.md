# Lumenfall – Project Notes

## High-level vision
- Genre: TCG/MMO/RPG hybrid; current focus on the CCG core.
- Goal: Ship a solid prototype that could become a polished release.
- Codename: Lumenfall (placeholder names removed to avoid spoilers).

## Current codebase (PyGame scaffold)
- Prototype entry: `python -m aevum_prism.ui.main_ui` (pack opener + arena + collection).
- Legacy scene scaffold (`main.py`, `aevum_prism.app`) still exists but is superseded by the new UI loop.
- UI helpers live in `aevum_prism/ui/pack_opener.py`; main loop/layout wiring is in `aevum_prism/ui/main_ui.py`.
- Saves: collection `saves/collection.json`, equips `saves/equips.json`, logging under `logs/`.
- Environment: `requirements.txt` (PyGame), `.gitignore` for Python, `README.md` documents setup/run.

## Next implementation steps (near term)
- Define core domain models: Card, Cost, Effect, Zone, PlayerState, GameState, Stack/Queue for actions, Turn/Phase model.
- Data source: decide on JSON/YAML/card registry module for card definitions; include id, name, type, cost, stats, abilities, rules text.
- Action system: input events → actions → validation → resolution; deterministic order for multiplayer sync.
- Rendering: basic board layout (player hand, battlefield, deck/discard, mana/energy), simple hover/select interactions.
- Testing: start a lightweight simulation layer to unit test rules without PyGame loop (pure functions where possible).

## Pack simulation (v0.5)
- Module: `aevum_prism/packs.py` (run with `python -m aevum_prism.packs`).
- Rarities/chances: Common 0.60, Uncommon 0.25, Rare 0.10, Epic 0.039, Legendary 0.001, Mythic 0.00001, Secret 0.000001, Astral 0.0000001, Divine 0.0000005.
- Pools: Common 150, Uncommon 100, Rare 60, Epic 30, Legendary 10, Mythic 5, Secret 3, Astral 2, Divine 1 (Aevum's Prism).
- Pity: Epic after 200 misses, Legendary after 2,000 misses, Mythic after 200,000 misses. Secret/Divine never pity.
- Pack size: 5 by default (can adjust for box/event types).
- Logging: `logs/pulls_summary.log` (overwrites per run) shows this-run and lifetime counts; lifetime packs in `logs/packs_total.txt`; lifetime rarity totals in `logs/rarity_totals.json`; pity counters in `logs/pity_state.json`.
- Instances: every pull creates an entry in `saves/card_instances.json` with rarity, tier (Rare+ start at 1, capped by rarity), element (Fire/Ice/Nature/Light/Void/Metal/Arcane/Astral), charges (None), locked flag. Essence tallies live in the same file; exchanging (tier>=2) grants essence=tier and removes the instance/count.

## Pack opener UI (with arena/currency/equip stubs)
- Module: `aevum_prism/ui/main_ui.py` (run with `python -m aevum_prism.ui.main_ui`).
- Window 800x600, toggle between pack opener and arena (Tab or on-screen button); unified "Packs" view shows last pack + scrollable history.
- Currency: Vel base; Erun = 1000 Vel; Zeth = 100 Erun; Velarun = 100 Zeth (derived). Packs cost 250 Vel; box = 1 Erun (10 packs). Currency earned in arena.
- Arena stub: player (blue circle), enemies (red squares/bosses) spawn and chase; collision damages player and kills enemy; +100 Vel per kill, boss every 10 kills drops 1 Erun; HP bar and game-over reset.
- UI: currency breakdown, pack history, rarity-color cards; rare pulls animate (staggered reveal, flair for very rare).
- Equip bar: 3 slots always visible (Common–Mythic). Click to open selection modal filtered to owned equippable cards; right-click clears; saved in `saves/equips.json`. (No stat effects yet.)
- Collection modal: button "Collection" opens grid backed by `saves/collection.json`; undiscovered cards show ??? (Secret/Divine hidden until found); rarity sort toggle; completion % and star/crown flair when finishing a rarity; optional profile flair selection.

## Questions to settle
- Resources: mana/energy model? One resource or multiple types?
- Turn structure: phases? stack/priority system vs simultaneous resolution?
- Card types: unit/creature, spell/instant, artifact/equipment, hero/commander?
- Rarity/progression: how MMO aspects integrate (crafting, xp, drops) later?
- Networking: is early multiplayer needed, or local/AI first?

## Roles
- Assistant handle (this chat): Kepler

## Conventions (proposed)
- Code: keep game logic in pure modules (no PyGame) to enable testing; PyGame scenes adapt state → view.
- Data: card definitions as data files, parsed on load; avoid hardcoding into logic.
- Naming: continue using “Lumenfall” in UI/window; keep references to the old name only in history notes.

## Trio operational roles (meta)
- See `docs/TRIO_STATE.md` for how Nullirae (vision), Neotus (architecture), and Kepler (implementation) coordinate.

## Potential roadmap (short)
1) Implement domain models and pure simulation loop.
2) Build minimal UI to play a sample turn (draw, play card, attack/cast).
3) Add 5–10 sample cards to exercise core rules.
4) Add tests for rules engine and deterministic resolution order.
