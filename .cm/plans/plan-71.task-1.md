# P71 — CHANGELOG entry for the rework

**Task ID:** `phase-71.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Cleanup — CHANGELOG**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `CHANGELOG.md`

## Scope (single commit)

- Add a user-facing CHANGELOG entry describing the rework:
- No more policy selection; any whitelisted BIP44/49/84/86 account is accepted.
- Registered descriptors auto-load at boot.
- Permissive signing available as opt-in for unknown paths.
- Account setting migrated away: existing users' PSBTs still sign (account is now inferred from the PSBT keypath).

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: CHANGELOG entry for the rework` (or a tighter phrasing of it).
