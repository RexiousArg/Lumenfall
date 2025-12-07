# Lumenfall – Workflow Pipeline

## AI Roles
### Neotus (Design Architect)
- Creates specs
- Defines systems and structure
- Provides questions and answers for subsystem clarity

### Kepler (Engineering)
- Implements YAML + MD specs into code
- Updates codebase
- Outputs diffs where necessary

### Atlas (Project Brain)
- Maintains all documentation
- Logs decisions and updates
- Prevents spec drift
- Maintains TODO pipeline

## Workflow Cycle
1. Neotus designs → 2. Atlas logs → 3. Kepler implements → 4. Atlas records → repeat.

## Governance Rules (Atlas enforces)
- Never delete or overwrite canonical files; integrate changes and keep append-only logs where noted.
- Every spec addition or revision must update Spec Index, Devlog, and TODO (if it impacts work).
- Maintain version numbers across specs and reflect them in `docs/Lumenfall_Spec_Index.yaml`.
- Cross-thread continuity: reload all docs on session start, especially `/docs/specs/`.
