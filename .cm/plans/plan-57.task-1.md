# P57 — wallet.c: simplify wallet_init(network) to network-record only

**Task ID:** `phase-57.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — simplify wallet_init**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/wallet.c`
- `main/core/wallet.h`

## Scope (single commit)

- Reduce `wallet_init(network)` to: record `wallet_network = network`; set `wallet_initialized = true`. Nothing else.
- Registry init is triggered externally (already wired in P29).

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet.c: simplify wallet_init(network) to network-record only` (or a tighter phrasing of it).
