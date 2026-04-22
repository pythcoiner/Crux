# P30 — Rewrite psbt_sign body to use classifier + claim_regenerate

**Task ID:** `phase-30.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 6 — psbt_sign rewrite**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 10**

## Files touched

**Modified:**
- `main/core/psbt.c`
- `main/core/psbt.h`

## Scope (single commit)

- Replace the body of `psbt_sign` (lines 258-357) with:
- Loop over inputs `i`.
- Call `psbt_classify_input(psbt, i, is_testnet)`.
- If `ownership.owned && ownership.verified`: derive the key at `ownership.claim.derived_path` via `key_get_derived_key`, call `wally_psbt_sign` with `EC_FLAG_GRIND_R`. Maintain per-input verified-claim list for self-cosign (sign once per claim).
- If `ownership.owned && ownership.requires_ack`: invoke a UI ACK callback (function pointer parameter added to `psbt_sign` or via a context struct). If confirmed, derive at the raw keypath and sign; else skip.
- Else: skip.
- Delete the inline BIP84/BIP48 branches (lines 295-334) — all that logic now lives in `psbt_classify_input`.
- Update `psbt.h` signature of `psbt_sign` if the UI ACK callback needs to be passed as a parameter.

## Notes

Existing callers of psbt_sign may need updating if the signature changes — verify with grep after editing.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Rewrite psbt_sign body to use classifier + claim_regenerate` (or a tighter phrasing of it).
