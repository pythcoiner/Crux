#!/bin/bash
# Diagnose why the simulator doesn't show a window over ssh -X.
#
# Run this INSIDE the ssh -X session (not on the local host) from the
# Kern repo root:
#
#   scripts/diag-sim-ssh-x.sh
#
# Captures enough environment + SDL driver info to pinpoint the bug.
# Paste the output back for review.

set -u

SEP="----------------------------------------------------------------------"
log() { printf '\n%s\n%s\n%s\n' "$SEP" "$1" "$SEP"; }

log "X11 FORWARDING"
echo "DISPLAY='${DISPLAY:-UNSET}'"
echo "XAUTHORITY='${XAUTHORITY:-UNSET}'"
echo "XDG_SESSION_TYPE='${XDG_SESSION_TYPE:-UNSET}'"
echo "WAYLAND_DISPLAY='${WAYLAND_DISPLAY:-UNSET}'"

log "XAUTH + XDPYINFO"
command -v xauth >/dev/null && xauth list 2>&1 | head -5 || echo "xauth not installed"
echo
command -v xdpyinfo >/dev/null \
    && xdpyinfo 2>&1 | head -6 \
    || echo "xdpyinfo not installed (sudo apt install x11-utils)"

log "SDL2 VERSION + LINKAGE"
dpkg -l libsdl2-2.0-0 2>/dev/null | awk '/libsdl2/ {print}' | head -3
ldd simulator/build/kern_simulator 2>/dev/null \
    | grep -E "libSDL2|libwayland|libX11|libdrm|libgbm" | head -10

log "SIM BINARY STARTUP (verbose SDL, 3s timeout)"
# Force X11; log all SDL subsystem events; run only long enough to see
# the driver-selection messages, then kill.
env SDL_VIDEODRIVER=x11 \
    SDL_RENDER_DRIVER=software \
    SDL_LOGGING='*=verbose' \
    timeout --foreground 3 \
    ./simulator/build/kern_simulator --width 480 --height 480 2>&1 \
    | head -80

log "WINDOW LIST"
command -v xwininfo >/dev/null \
    && xwininfo -root -children 2>&1 | grep -Ei "kern|simulator" || echo "xwininfo not installed (sudo apt install x11-utils)"

log "DONE — paste everything above"
