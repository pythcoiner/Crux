# P78 — Device: WARN-dialog gating on mismatched descriptor registration

**Task ID:** `phase-78.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 15 — device verification (WARN dialog)**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

## Scope (single commit)

- Attempt to register a mismatched descriptor: `tr([fp/84'/0'/0']xpub...)` — the WARN dialog should appear.
- Cancel the dialog → descriptor NOT registered; no file on flash.
- Re-attempt and confirm → descriptor registered; signs PSBTs that reference it.
- Also try `wsh(sortedmulti(2,[fp/86'/0'/0']xpub,...))` → WARN dialog.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Device: WARN-dialog gating on mismatched descriptor registration` (or a tighter phrasing of it).
