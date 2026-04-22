# P36 — addresses.c: account input + remove 'descriptor required' empty state + rename Load->Register

**Task ID:** `phase-36.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 10 — account input + cleanup**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/pages/home/addresses.c`

## Scope (single commit)

- Add an inline account number input (0..99) visible only when source ∈ {Native SegWit, Taproot, Legacy, Wrapped SegWit}. Default 0, session-scoped (no NVS).
- Hide the account input when source is a registered descriptor.
- Remove the 'descriptor required' empty-state branch at lines 316-324 — every source has something to show now; if registry is empty the dropdown simply omits those entries.
- Rename the 'Load descriptor' button to 'Register descriptor'. Its handler still opens the existing descriptor-loader flow.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: addresses.c: account input + remove 'descriptor required' empty state + rename Load->Register` (or a tighter phrasing of it).
