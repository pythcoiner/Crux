# P20 — test_registry_parse.c (wpkh / wsh(sortedmulti) / tr / miniscript)

**Task ID:** `phase-20.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 2 — Tests (registry parse)**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

**New:**
- `main/core/test/test_registry_parse.c`

**Modified:**
- `main/core/test/CMakeLists.txt`

## Scope (single commit)

- Add `test_registry_parse.c`: for each of these descriptor strings (with hardcoded checksum), call `registry_add_from_string(id, str, STORAGE_FLASH, /*persist=*/false)` and assert the origin path extraction matches the expected `uint32_t[]`.
- `wpkh([fp/84'/0'/0']xpub.../<0;1>/*)#cksum`
- `wsh(sortedmulti(2,[fp/48'/0'/0'/2']xpub...,[fp2/48'/0'/0'/2']xpub...))#cksum`
- `tr([fp/86'/0'/0']xpub.../<0;1>/*)#cksum`
- A simple miniscript sample (e.g. `wsh(or_d(pk([fp/84'/0'/0']xpub...),pkh([fp/84'/0'/0']xpub.../0)))`)
- Use a test mnemonic whose fingerprint matches `fp`.
- Register test in `main/core/test/CMakeLists.txt`.

## Done when

- `just build wave_4b` passes clean.
- New/updated tests in `main/core/test/` pass (`just test`).
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: test_registry_parse.c (wpkh / wsh(sortedmulti) / tr / miniscript)` (or a tighter phrasing of it).
