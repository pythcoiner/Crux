# P67 — Move BIP-380 checksum helper to descriptor_checksum.c (optional)

**Task ID:** `phase-67.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 4 — factor out BIP-380 checksum**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**New:**
- `main/core/descriptor_checksum.c`
- `main/core/descriptor_checksum.h`

**Modified:**
- `main/core/wallet.c`
- `main/core/wallet.h`
- `main/CMakeLists.txt`

## Scope (single commit)

- Only execute if `wallet.c` is now thin enough that factoring is warranted; otherwise leave helpers in place and mark this phase completed.
- Extract `desc_polymod`, `desc_compute_checksum`, `wallet_get_descriptor_string`, `wallet_get_descriptor_checksum` (if still used) into `main/core/descriptor_checksum.{c,h}`.
- Update callers to include the new header.
- Register the new `.c` in `main/CMakeLists.txt`.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Move BIP-380 checksum helper to descriptor_checksum.c (optional)` (or a tighter phrasing of it).
