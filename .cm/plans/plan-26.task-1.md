# P26 — claim_regenerate registry branch (wsh / sh(wsh) / sh(multi)) + test

**Task ID:** `phase-26.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 5 — claim_regenerate (registry)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 08**

## Files touched

**Modified:**
- `main/core/psbt.c`
- `main/core/test/test_psbt_classify.c`

## Scope (single commit)

- Implement the registry branch of `claim_regenerate`:
- `wally_descriptor_to_script(desc, mp, child_num, depth=0, ...)` → spk.
- If outer is `wsh(...)` → `depth=1` → witness script.
- If outer is `sh(wsh(...))` → `depth=1` → redeem (the p2wsh wrapper = `OP_0 <32> sha256(witness)`); `depth=2` → witness.
- If outer is `sh(multi(...))` or `sh(sortedmulti(...))` non-nested → `depth=1` → redeem (bare multisig).
- Otherwise: spk only.
- Determine outer shape via `wally_descriptor_to_script`'s depth semantics or a libwally tokenizer helper (see SNIP 08 for the decision tree).
- Extend `test_psbt_classify.c` with a test per outer shape: wsh(sortedmulti(2,[fp/48'/0'/0'/2']xpub,…)), sh(wsh(wpkh([fp/49'/0'/0']xpub))), sh(multi(2,[fp/…]xpub,…)), tr([fp/86'/0'/0']xpub). Compare to hardcoded reference hex.

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: claim_regenerate registry branch (wsh / sh(wsh) / sh(multi)) + test` (or a tighter phrasing of it).
