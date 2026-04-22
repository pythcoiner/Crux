# P76 — Device: Settings UI gone/added as expected; permissive toggle works

**Task ID:** `phase-76.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 15 — device verification (Settings)**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

## Scope (single commit)

- Open wallet_settings page. Confirm:
- No policy dropdown.
- No account spinner.
- No derivation-path preview label.
- 'Permissive signing' toggle present, default off.
- Toggle permissive; rerun the non-standard-keypath PSBT from P75; confirm the ACK prompt gates correctly.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Device: Settings UI gone/added as expected; permissive toggle works` (or a tighter phrasing of it).
