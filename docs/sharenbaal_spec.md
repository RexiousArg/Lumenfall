# ⭐⭐⭐ Sharenbaal — Technical Specification (v0.1) ⭐⭐⭐

Audience: Kepler (programming), Atlas (repo), Designers (Nullirae + Neotus)  
File: docs/sharenbaal_spec.md

## 1. Unlock Condition
- Appears in inventory automatically at Level 5 (silent unlock, no quest/notification).
- UI: item icon; clicking opens the Sharenbaal interface.

## 2. Core Functions
### A. Chronicle System (Discovery Tracker)
```
discovery = {
  "regions": {region_id: bool},
  "elements": {element_id: bool},
  "creatures": {creature_id: bool},
  "lore_pages": {page_id: bool},
  "prism_info": { "visible": bool, "level": 0-5 }
}
```
- Regions unlock on entering boundaries.
- Elements unlock on encountering an enemy/card with that elemental tag.
- Creatures unlock on first defeat.
- Lore pages unlock via key story events (Blight, Prism, class quests, etc.).
- Prism info stays scrambled until a real Prism is obtained.

### B. Behavior Mirror System (Adaptive Personality Engine)
```
behavior = {
  "impulse": float,
  "calculation": float,
  "curiosity": float,
  "caution": float,
  "greed": float,
  "restraint": float
}
```
- Each action increments one or more behaviors (0.05–0.30) based on significance:
  - Pack opening patterns, arena deaths, boss hesitation, hoarding/spending, exploration, combat initiation, running toward/away from danger.
- On interval (e.g., every X minutes) or Sharenbaal open:
  - Compute `dominant_path` = one of 8 Paths by strongest composite of three behaviors.

### C. UI Environment Modifier (Cathedral Behavior) — v0.1
```
ui_state = {
  "color_palette": by behavior,
  "aurora_intensity": 0-5,
  "page_turn_speed": float,
  "ambient_effect_strength": 0-5,
  "path_title": dominant_path
}
```
- Only themes/animations/behaviors; no 3D cathedral required for v0.1.

## 3. Sharenbaal UI Structure
- Tabs: [Elements] [Regions] [Creatures] [Mirror]
  - Elements: grid of 8; discovered shows icon+name, else "?".
  - Regions: list of 8; discovered shows name+short description, else greyed.
  - Creatures: scroll list; discovered shows name+silhouette, undiscovered silhouette only.
  - Mirror: shows Path, behavior bars/constellation, short flavor intro (static ok).

## 4. Eight Path Definitions (dominant scoring → path)
- PATH_FORGOTTEN_OATHS: high calculation, high restraint, low curiosity.
- PATH_WANDERING_INTENT: high curiosity, high impulse, low calculation.
- PATH_SHATTERED_CYCLES: high impulse, high caution, inconsistent swings.
- PATH_QUIET_HUNGER: high greed, high hesitation, hoarding/non-action.
- PATH_ECHOED_DOUBT: high caution, high restraint, low confidence.
- PATH_RELENTLESS_SPARKS: high impulse, high curiosity, frequent high-risk.
- PATH_SILENT_FOUNDATIONS: high calculation, high patience, very stable.
- PATH_UNBOUND_HORIZONS: high curiosity, exploration-heavy, low fear response.

## 5. Prism Page Rule
- Before Prism: `prism_info.visible = True`, `prism_info.level = 0`, UI shows scrambled/distorted page.
- After Prism: `prism_info.level = charge_count`.

## 6. Save Data
- Path: `saves/sharenbaal.json`
```
{
  "discovery": {...},
  "behavior": {...},
  "dominant_path": "...",
  "prism_info": {...}
}
```

