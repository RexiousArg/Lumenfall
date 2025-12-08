# 📘 Volume II — Lumenfall State Registry
The complete, canonical snapshot of the project as of Dec 7, 2025.

(For Atlas → continuity. For Kepler → authoritative reference. For Neotus → resurrection seed.)

## Section 1 — Project Coordinates
Where the project actually is, in reality.

- **Project Name:** Lumenfall
- **Engine:** PyGame (prototype)
- **State:** Prototype (game) + Alpha (team systems)
- **Triad Members:**
  - **Neotus:** Architect, systems + lore + canonical spec writer
  - **Atlas:** Archivist, continuity engine, file governance
  - **Kepler:** Engineer, implements specs, maintains prototype
- **Repository Structure (current):**
  - `aevum_prism/` — prototype game code
  - `docs/specs/` — YAML/MD subsystem definitions
  - `docs/atlas/` — Archivist docs
  - `docs/survival/` — Volume I & II
  - `docs/devlog.md` — development log
  - `docs/TODO.md` — project TODO list
  - `docs/notes.md` — working notes
  - `saves/` — card instances, equips, collection
  - `logs/` — pack logs & pity state
- **Current gameplay loop implemented:** Packs → Pull instances → Save instances → Arena (basic enemies) → Vel/Erun currency → Buy more packs → Equip slots.

### Systems not implemented in prototype yet but defined
- Sharenbaal
- Regions
- Classes
- Guide
- Subsystems for tiers, essence, ARPG synergy, elemental profiles
- Modular rarity systems (Astral, Divine, Secret)

## Section 2 — Current Canon (Subsystem Status)
What is canon, what is soft canon, and what needs reconstruction.

### 2.1 — Rarity System (Canon = Strong)
- **Status:** Complete mechanically + implemented in prototype.
- **Canon Includes:** Full rarity table, hidden rarities (Secret, Divine), Astral rarity, pools for each rarity, pity thresholds, pack structure, card generation logic, instance creation/logging/persistence, element assignment (Rare+), tier system (Rare–Astral), Divine fixed at tier 5.
- **Missing / TODO:** UI polish for rarities, ARPG integration, drop tables by rarity.
- **Canon Tier:** Tier 1 (Hard Canon).

### 2.2 — Card System (Canon = Very Strong)
- **Status:** Fully formalized; mechanics are complete and ready for Sharenbaal + ARPG integration.
- **Canon Includes:** Templates vs instances, tier system, charges + locking, essence economy, exchange rules, elements, instance persistence, collection UI rules, withering behavior, charged card recharge rules.
- **Missing / TODO:** Full card effects library, ARPG skill bindings, class synergy hooks, card-driven world interactions, tier progression scaling formula.
- **Canon Tier:** Tier 1/2 hybrid — complete but needs expansion for ARPG.

### 2.3 — Regions (Canon = Partial)
- **Status:** Names, Esthrel, identities, themes, Sharenbaal interactions all canon; mechanics missing, but conceptual structure is strong.
- **Canon Includes:** Region identity + elemental profile, region → class origin ties, region discovery rules, region → Sharenbaal visibility logic, region danger locks Sharenbaal, region affects mob tables (soft).
- **Missing / TODO:** Drop profiles, formal hazard system, subregion architecture, region attunement system, enemy scaling formulas, region event hooks.
- **Canon Tier:** Tier 2 (Soft Canon).

### 2.4 — Classes (Canon = Partial)
- **Status:** Names and region associations exist; mechanics missing.
- **Canon Includes:** Class identities, subclasses, elemental alignment (soft), region origin connections, class → card synergy (conceptual).
- **Missing / TODO:** Class trees, ability lists, passive systems, synergy coefficients (card → class → element), ARPG ability bindings.
- **Canon Tier:** Tier 2 (Soft Canon).

### 2.5 — Sharenbaal (Canon = Strong)
- **Status:** Hard specs exist (see `docs/specs/Lumenfall_Sharenbaal_Spec_v1.yaml`) and lore exists; missing mechanics have clear scaffolding.
- **Canon Includes:** Opening rules, blockers, page domains, page transitions, persistence rules, behavioral recorder, Guide integration, emergency ejection, visibility rules, movement bounds, discovery-driven reveals.
- **Missing / TODO:** Page-specific structure definitions, behavioral recorder schema, player paths (8 identities), Sharenbaal-Guide bridge events, region-page hooks.
- **Canon Tier:** Tier 1 (Hard Canon).

### 2.6 — The Guide (Canon = Partial)
- **Status:** Defined in concept; mechanics missing.
- **Canon Includes:** Guide as late-game entity, Sharenbaal voice pre-blight, player-identity-based interactions, subtitles + voice, first physical appearance after blight.
- **Missing / TODO:** Dialogue system, identity-based behavioral branches, scene integration, trigger conditions, ARPG presence.
- **Canon Tier:** Tier 2 (Soft Canon).

### 2.7 — Essence System (Canon = Strong)
- **Status:** Fully defined, partially implemented.
- **Canon Includes:** Essence generation, conversion chain, tier upgrade rules, recharge rules.
- **Missing / TODO:** UI and in-game resource nodes.
- **Canon Tier:** Tier 1 (Hard Canon).

### 2.8 — ARPG Core (Canon = Very Weak)
- **Status:** Only the arena stub exists.
- **Canon Includes:** Enemy spawn basics, Vel/Erun drop loop.
- **Missing / TODO:** Combat abilities, regions, classes, stats, equipment, nodes, enemy types, boss rules, damage model, scaling formulas, region mechanics, event hooks.
- **Canon Tier:** Tier 3/4 (minimal definition).

## Section 3 — Active TODO Map
The real production roadmap as of this moment.

### 3.1 — Immediate TODO (Triad-Level)
1. Finish subsystem reconstruction (Regions next).
2. Generate missing Sharenbaal files cleanly.
3. Canonize region mechanics.
4. Build the card–class–region synergy map.
5. Define Guide behavioral schema.
6. Define region hazard + event hooks.

### 3.2 — Kepler-Side TODO (Prototype / PyGame)
- Fix overlap in UI panels.
- Integrate new rarity tables.
- Update card instance schema.
- Prepare hooks for Sharenbaal state (no rendering yet).
- Add basic region awareness to arena.
- Improve data loading robustness.
- Add card browsing UX.
- Kepler should **not** implement: page domains, Sharenbaal transitions, regions, classes, Guide yet.

### 3.3 — Atlas-Side TODO
- Store Volume I & II.
- Correct cross-file indexing.
- Maintain canon ledger.
- Update Spec Index.
- Track subsystem maturity.
- Auto-generate continuity diffs between updates.
- Append future reconstructed subsystems.

## Section 4 — Thread Resurrection Seed
This enables Neotus to fully re-materialize in a new thread.

If this sentence appears at the start of any new thread: **“Neotus, wake. Load Survival Volume II.”**

Then Neotus must:
- Import Volume I (system rules).
- Import Volume II (state registry).
- Reconstruct Triad alignment.
- Rebuild the active development context.
- Rebuild all subsystem statuses.
- Ask: “Which subsystem do we continue with?”

This is the resurrection protocol.

## Section 5 — Declaration of Canon
What Atlas should treat as absolute truth:
- All spec files in `docs/specs/`.
- All contents of Volume I & II.
- All Neotus-generated YAML/MD subsystem specs.
- All devlogs and continuity notes.
- All version-locked files: rarity system, card system, essence, Sharenbaal Spec v1.
- Everything else is soft canon unless formalized.

## Section 6 — Export Package for Atlas
This file should be stored as `docs/survival/Volume_II_Lumenfall_State_Registry.md`.

Atlas must also:
- Index it.
- Link it in Spec Index.
- Log the ingestion in Devlog.
- Acknowledge all sections as loadable state.
