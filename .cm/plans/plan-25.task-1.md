# P25 — claim_regenerate whitelist branch + test

**Task ID:** `phase-25.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 5 — claim_regenerate (whitelist)**
- `.cm/spec/PLAN.md` (context, behavioural spec)
- `.cm/spec/SNIP.md` → **SNIP 08**

## Files touched

**Modified:**
- `main/core/psbt.c`
- `main/core/test/test_psbt_classify.c`

## Scope (single commit)

- Implement the whitelist branch of `claim_regenerate`: call `ss_scriptpubkey_with_redeem` for the claim's (script, account, chain, index). Fill `expected_scripts_t`: spk always; redeem only for P2SH_P2WPKH; witness empty.
- Create `main/core/test/test_psbt_classify.c` (Unity harness) with a first test: for each of the four script types, regenerate via `claim_regenerate` and compare expected scripts to hardcoded reference hex (cross-checked offline against Sparrow or `bitcoin-cli getdescriptorinfo`).
- Register `test_psbt_classify.c` in `main/core/test/CMakeLists.txt`.

## Notes

This test will grow in P26-P28 as more branches land. Initial skeleton sets up the test fixture data.

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: claim_regenerate whitelist branch + test` (or a tighter phrasing of it).
