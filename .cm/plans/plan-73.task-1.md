# P73 — Device: flash wave_35, store 3 plaintext descriptors, reboot, verify auto-load

**Task ID:** `phase-73.task-1`

## Reference

- `.cm/spec/ROADMAP.md` → **Phase 15 — device verification (auto-load)**
- `.cm/spec/PLAN.md` (context, behavioural spec)

## Files touched

## Scope (single commit)

- Flash `wave_35` with the just-built firmware. Boot with a known test mnemonic.
- Store 3 plaintext descriptors via the save flow:
- `wpkh([fp/84'/0'/0']xpub.../<0;1>/*)#cksum`
- `tr([fp/86'/0'/0']xpub.../<0;1>/*)#cksum`
- `wsh(sortedmulti(2,[fp/48'/0'/0'/2']xpub.../<0;1>/*,[fp2/48'/0'/0'/2']xpub.../<0;1>/*))#cksum`
- Reboot. Confirm the 'Registered descriptors' sub-page (from P52) lists all three without any load action.
- Device log must show `Registry: 3 entries loaded` or equivalent.

## Notes

No commit — this is a manual device verification.

## Done when

- `just build wave_4b` passes clean.
- Only files in "Files touched" changed (scope gate — verify with `git status`).
- Commit message: `descriptor-rework: Device: flash wave_35, store 3 plaintext descriptors, reboot, verify auto-load` (or a tighter phrasing of it).
