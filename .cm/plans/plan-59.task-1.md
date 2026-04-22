# P59 — wallet.c: delete statics

**Task ID:** `phase-59.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — delete statics**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**Modified:**
- `main/core/wallet.c`

## Scope (single commit)

- Delete module-level statics in wallet.c: `wallet_type`, `wallet_policy`, `wallet_account`, `derivation_path_buffer`, `loaded_descriptor`, `account_key` (and any related helpers that referenced them exclusively).
- After this commit, `wallet.c` should only contain: network recording, init/cleanup, and possibly the BIP-380 checksum helper.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: wallet.c: delete statics` (or a tighter phrasing of it).
