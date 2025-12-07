# Devlog

Entries capture meaningful milestones/decisions for continuity between threads.

## 2025-12-06
- Pack system reworked to new rarity table (Common→Divine), pity thresholds (Epic/Legendary/Mythic), and secret/divine behavior; lifetime stats persisted in `logs/rarity_totals.json` and `logs/packs_total.txt`.
- Summary logging stabilized: `logs/pulls_summary.log` shows this-run and lifetime rarity counts plus total cards/packs.
- Gameplay scene placeholder cleaned (removed encoding artifacts; clearer quit hint).
- Notes updated to pack sim v0.4 and logging/pity paths; encoding artifacts removed.
- Captured rarity spec from user devlog: chances Common 0.60, Uncommon 0.25, Rare 0.10, Epic 0.039, Legendary 0.001, Mythic 0.00001, Secret 0.000001 (hidden), Divine 0.0000005 (invisible); pools: 150/100/60/30/10/5/3/1; pity applies only to Epic/Legendary/Mythic (200/2000/200000 misses); pack types: standard 5 cards, box = 10 packs; index hides Secret/Divine until owned.
- Devlog note (2025-12-06, Nullirae/Neotus): Project Lumenfall bootstrapped (renamed from Aevum's Prism by Kepler); PyGame chosen as engine; core directory tree established; rarity structure finalized for CCG alpha; CCG pack opening and pull logging working (terminal); devlog used for continuity between threads.
- Added PyGame pack opener UI (800x600, button-driven) using shared pack logic; displays last pack and short history, with rarity color cues.
- UI polish: pack opener now sequences card reveals with a flash, staggered reveal, and flair pulses for 1% or rarer pulls (Legendary/Mythic/Secret/Divine); keeps using shared pack logic and defaults.
- Arena/currency stub integrated into pack UI: currency (Vel base, Erun/Zeth/Velarun derived) with costs (pack 250 Vel, box 1 Erun); arena spawns enemies/bosses; kills award Vel, every 10th kill spawns boss dropping 1 Erun; pack/box buttons disabled if funds insufficient.
- Collection modal added to pack UI: button opens modal grid backed by `saves/collection.json`; tracks owned cards from packs; undiscovered shown as ??? (Secret/Divine hidden until found); sort toggle rarest/common first; hover shows name/rarity/count; scrollable.

## 2025-12-06
- Currency names (Vel, Erun, Zeth, Velarun) originate from Nyavul (Nullirae/Neotus); planned deeper worldbuilding hooks (lore, NPC dialogue, quests, achievements, flavor text).
- Core currencies auto-accumulate and “convert” upward implicitly (single balance with breakdown); no manual exchange needed for core stack. Future special currencies (event tokens, soulshards) will require explicit exchange—keep currency logic modular.
- Purchases draw from total balance seamlessly (e.g., box costs 1 Erun = 1000 Vel); currency always visible in UI; icons planned.
- Instruction for future UX: shared currency source for ARPG/pack systems, clean mode switching, and a living devlog tracking currency/mechanic evolution.

## 2025-12-06
- UI split into helpers (`aevum_prism/ui/pack_opener.py`) and main loop (`aevum_prism/ui/main_ui.py`) for easier expansion and cleaner layout.
- Added always-visible equip bar (3 slots, Common–Mythic) with modal selector filtered to owned cards; saved to `saves/equips.json` (no stat effects yet).
- Pack screen unified into a single "Packs" view (last pack + scrollable history), while arena shares the same top bar (currency + equips) and keeps boss/HP/game-over flow.

## 2025-12-07
- Main UI launch fixed (display flip inside loop) and collection tooltip import wired.
- Fullscreen by default with F11 toggle between fullscreen/windowed (still uses 800x600 logical layout).
- Added Astral rarity placeholder and card instance/essence scaffold (instances saved to `saves/card_instances.json`, essence tallies included; elements/tiers recorded per pull).
- Added Sharenbaal technical spec (`docs/sharenbaal_spec.md`) covering unlock rules, behavior tracking, paths, and save structure scaffold.
- Copied full spec suite into `docs/specs/` (Lumenfall_Core index + per-system YAMLs and lore markdowns) for long-term reference.
- Added Sharenbaal integration guide `docs/specs/README_sharenbaal.md` (mechanics/lore pointers, integration notes); awaiting `Lumenfall_Sharenbaal_Mechanics_v1.yaml` and `Sharenbaal_Lore_v1.md` placements when provided.

## 2025-12-07
- Repository access confirmed via PAT: configured `origin` to https://github.com/RexiousArg/Lumenfall, fetched `main`, and established local tracking for ongoing syncs.
