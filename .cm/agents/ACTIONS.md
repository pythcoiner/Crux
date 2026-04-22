# Build and Test Actions

Kern builds with ESP-IDF via the project's `.justfile`. The `just` commands
below are the canonical entry points — they handle ESP-IDF environment
setup and per-board build directories.

## Build Commands

### Primary Build (per-phase verification)

```bash
just build wave_4b
```

Phases run this after each commit. `build_wave_4b/` is the per-board build
output directory; switching between boards does not require a clean.

### Three-board Build (Phase 72 gate)

```bash
just build wave_4b && just build wave_35 && just build wave_5
```

Only exercised during Phase 72 (device verification group). Not part of
per-phase verification — too slow.

## Lint Commands

### Format check

```bash
just format
```

Wraps `scripts/format.sh`. Must pass before a phase is considered complete.

### CI checks

```bash
./scripts/ci-checks.sh
```

Full CI parity locally. Run at group boundaries (end of Group A, B, …) to
catch drift early.

## Test Commands

### Unit tests (host-side, Unity harness)

```bash
just test
```

Wraps `scripts/test.sh`. Runs all tests under `main/core/test/`. New tests
added by a phase must pass here.

### Single test (manual)

```bash
cd main/core/test && make test_<name>
```

Per-test make target. Use when iterating on a single test file.

## Device Verification (Phase 72–78)

Flash a physical device. Pattern:

```bash
just flash wave_35
just monitor wave_35
```

Only done manually during Phase 72+. Not part of per-phase verification.

### Simulator (UI iteration only — not a substitute for device flash)

```bash
just sim wave_4b        # default 720x720
just sim wave_35        # 320x480
just sim wave_5         # 720x1280
```

Useful for exercising UI changes (Phases 34–41, 47–52) before flashing.

## Verification Sequence

Per-phase (automated via cm `build_commands`):

1. `just build wave_4b` — clean build.
2. (cm) review agent reviews the diff.
3. If tests were added by this phase, the review agent verifies they pass.

At group boundaries (manual):

1. `just format` — format check.
2. `just test` — all host tests pass.
3. `./scripts/ci-checks.sh` — full CI parity.

At Phase 72 (manual gate):

1. `just build wave_4b && just build wave_35 && just build wave_5` — all three boards clean.
2. Device-verification phases (P73–P78) run manually with flashed firmware.

## Environment Setup

The `.justfile` sets `IDF_PATH` and sources `$IDF_PATH/export.sh` when
`idf.py` isn't on PATH, so no manual setup is typically required.

```bash
# Override ESP-IDF location (default: $HOME/esp/esp-idf)
export IDF_PATH=/path/to/esp-idf
```

## Clean Commands

```bash
just clean
```

Removes `build_wave_*`, `sdkconfig`, `compile_commands.json`, `.cache/`,
`simulator/build`, and test-harness build artifacts.

## Notes

- **Per-phase `build_commands` is wave_4b only.** This is the cheapest build; if a change is board-specific we catch it at Phase 72.
- **Don't invoke `idf.py` directly** — use `just` wrappers so per-board build dirs stay correct.
- **Tests live under `main/core/test/`.** New `.c` files there must be added to the local CMakeLists `SRCS`.
- **Test reference values.** Tests that regenerate scripts/addresses should cross-check against fixtures generated offline with `bitcoin-cli getdescriptorinfo` + `deriveaddresses` on a throwaway mnemonic.
