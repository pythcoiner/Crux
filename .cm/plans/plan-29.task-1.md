# P29 — Boot wiring: registry_init called after wallet_init in key_confirmation.c

**Task ID:** `phase-29.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 8 — boot wiring**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 12**

## Files touched

**Modified:**
- `main/pages/shared/key_confirmation.c`

## Scope (single commit)

- In the post-mnemonic handler (lines 25-46), after `wallet_init(net)`, add a call to `registry_init(net == WALLET_NETWORK_TESTNET)` (or equivalent is_testnet check matching the existing code's network type).
- Include `"core/registry.h"` at the top of the file.
- Do NOT yet remove the `settings_get_default_policy()` / `wallet_set_policy(...)` calls — those live until P53. This phase is purely additive.
- Log line from `registry_init` should appear in device logs on boot confirming auto-load.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Boot wiring: registry_init called after wallet_init in key_confirmation.c` (or a tighter phrasing of it).
