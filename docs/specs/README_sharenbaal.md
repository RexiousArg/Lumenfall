# Lumenfall – Sharenbaal System Overview (Integration Guide for Kepler)

This guide explains how the Sharenbaal subsystem interacts with the current prototype and which future architectural decisions it will influence. It sits beside the spec files:

- `docs/specs/Lumenfall_Sharenbaal_Mechanics_v1.yaml` (mechanics)
- `docs/specs/Sharenbaal_Lore_v1.md` (lore)

## 1. Purpose of the Sharenbaal
Meta-system that:
- Records player identity, mirrors decisions, reveals world knowledge
- Acts as core codex, bridging ARPG + CCG + world progression
- Feeds into The Guide’s late-game interactions
- Renders as a player-bound UI micro-dimension (“pages”)

## 2. Integration Layer
Sharenbaal currently does not touch combat or pack logic. Treat it as a future UI/environment subsystem that plugs into:
- Player state (page reveals)
- Collections & card instances
- Essence / tiering (referenced later)
- ARPG progression (content visibility)
- World events (future page triggers)

## 3. Opening / Closing Rules (for later)
- Open only when: not in combat, not in hazard, no incoming enemies, no story-locked scene.
- On open: spawn projection, load page domain, disable ARPG input, anchor camera, play open animation.
- On close: play close animation, restore camera/controls, remove projection.

## 4. Page Domains (concept)
- Fixed square domain with boundaries; content visible per discoveries.
- Transition: fold along a cardinal axis, ~2s, player centered, no collision with plane.

## 5. Persistence (plan ahead)
- Session: reopen to last viewed page.
- Long-term: entry at Chapter 1, Page 1 on fresh load.

## 6. Trigger Examples (future hooks)
- Elemental encounter → elemental pillar
- Card pull → CCG section update
- Region entry → regional history
- Class tier unlock → class section
Pages start empty; triggers populate content.

## 7. Guide Interaction (late game)
- Uses stored context: tone classification, tendencies, path assignment (8 Paths), personalized dialogue cues.

## 8. What to do now
- ✅ Keep YAML as authoritative mechanics; MD as narrative context.
- ✅ Maintain flexible architecture for UI scene insertion and state-based locks.
- ✅ Ensure player state can reference Sharenbaal later.
- ✅ Keep ARPG/CCG data separate from Sharenbaal meta-state.
- ❌ No rendering/animation/trigger logic yet.

## 9. Impact on future systems
- Regional/biome pipelines, elemental/class systems, story tracking, Guide interactions, adaptive world systems, codex metadata. All major systems will eventually register into the Sharenbaal.

## 10. File index (expected)
- `docs/specs/Lumenfall_Sharenbaal_Mechanics_v1.yaml`
- `docs/specs/Sharenbaal_Lore_v1.md`
- `docs/specs/README_sharenbaal.md` (this file)
