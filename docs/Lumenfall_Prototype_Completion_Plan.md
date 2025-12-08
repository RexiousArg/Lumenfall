# Lumenfall_Prototype_Completion_Plan.md
Version: 1
Status: Active Prototype Directive

## 1. Purpose
Define the criteria for prototype completion and identify which systems must be implemented, excluded, or represented only as placeholders.

## 2. Required Systems for Prototype Completion

### 2.1 Card System
Required:
- Card instance creation (rarity, tier, element, charges, lock state)
- Collection view (basic)
- Equip slots (3)
- Pack opening for standard + box packs
- Pity rules
- Essence generation + basic exchange

Excluded:
- Class synergy modifiers
- Advanced card types
- Castle Pack logic
- Badge gating

### 2.2 ARPG Prototype Field
Required:
- Player movement
- Enemy spawn loop (common + simple boss cycle)
- Basic combat loop
- Currency drops
- Simple region “identity bias” (enemy pools only)

Excluded:
- Full regions system
- Esthrels
- Hazards
- Terrain systems

### 2.3 Packs
Required:
- Standard pack opening
- Box pack opening
- Rarity tables
- Pity system
- Logging + persistence

Excluded:
- Castle Packs
- Badge-based unlocking

### 2.4 Sharenbaal (Prototype Skeleton Only)
Required:
- Open/close behavior
- Forced-close rules (combat, hazards)
- Dimming behavior
- One placeholder functional page

Excluded:
- Page-folding
- Domain transitions
- Guide content
- Chapters and unlocks

### 2.5 UI/UX
Required:
- Main HUD
- Packs screen
- Arena screen
- Collection modal
- Equip modal
- Single Sharenbaal page
- Basic transitions (fade/slide)
- Implemented via ui_components/ modular pattern

Excluded:
- Custom art
- Full menu systems
- Castle UI screens

## 3. Systems Explicitly Out of Scope for Prototype
(Not implemented until Pre-Alpha)

- Regions system (subregions, hazards, Esthrels)
- Classes and subclasses
- Castle (badges, Castle Packs, Forge, Shrine)
- Events (blight pulses, weather, world events)
- Full Sharenbaal (all chapters, folding, multi-domain content)
- 3D rendering or engine transition
- Narrative systems

## 4. Prototype Goals
The prototype must demonstrate:
- Functional loop: Combat → Currency → Packs → Cards → Power → Combat
- Modular system boundaries (ARPG ↔ CCG)
- Stable data flow and persistence
- Sharenbaal skeleton behavior
- UI structure aligned with the Component Tree spec
- Compatibility with Triad workflows

## 5. Prototype Completion Criteria
Prototype is considered complete when:
- All required systems are implemented and stable
- No blocking progression bugs
- Sharenbaal skeleton functions correctly
- Packs, ARPG field, and card systems integrate without data loss
- UI matches the Component Tree implementation
- Atlas and Kepler can process updates without failure

After this point, development transitions to Pre-Alpha.
