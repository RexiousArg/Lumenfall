# Lumenfall – Thread Survival Protocol

## Purpose
Ensures continuity after assistant context resets.

## What To Reload After Collapse
- Lumenfall_Spec_Index.yaml
- Lumenfall_Data_Backbone.yaml
- The entire /docs/specs/ directory
- The most recent Devlog and TODO entries

## Recovery Steps
1. Reload spec index into memory.
2. Reload data backbone.
3. Reload active subsystem files.
4. Reconstruct the last-known TODO chain.
5. Continue development from the last log entry.

## Governance Reminders
- Keep append-only history for spec changes and devlog entries.
- If new specs are recovered or added, update Spec Index (with version bump), Devlog, and TODO where applicable.
- Never delete files during recovery; integrate reconstructed content.

Atlas maintains and updates this as the project evolves.
