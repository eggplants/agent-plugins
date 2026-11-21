#!/usr/bin/env bash
# Serve the built book (_book) on a free local port and screenshot pages with headless Chrome.
# Look at the PNGs with the Read tool afterwards.
#
#   shoot_pages.sh BOOK_DIR OUT_DIR index.html run/index.html recipes/ci.html
set -euo pipefail

if [ $# -lt 3 ]; then
  echo "usage: $0 BOOK_DIR OUT_DIR PAGE.html..." >&2
  exit 2
fi
book=$1
out=$2
shift 2
[ -f "$book/_book/index.html" ] || { echo "$book/_book is not built; run mise run build" >&2; exit 1; }
mkdir -p "$out"

chrome=""
for c in google-chrome google-chrome-stable chromium chromium-browser; do
  if command -v "$c" >/dev/null 2>&1; then
    chrome=$c
    break
  fi
done
[ -n "$chrome" ] || { echo "google-chrome or chromium is needed" >&2; exit 1; }

port=$(python3 -c 'import socket; s = socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1])')
python3 -m http.server "$port" --bind 127.0.0.1 --directory "$book/_book" >/dev/null 2>&1 &
server=$!
trap 'kill $server 2>/dev/null' EXIT
python3 - "$port" <<'EOF'
import socket, sys, time
for _ in range(50):
    try:
        socket.create_connection(("127.0.0.1", int(sys.argv[1])), timeout=0.2).close()
        break
    except OSError:
        time.sleep(0.1)
EOF

for page in "$@"; do
  png="$out/page_$(echo "$page" | tr '/' '_' | sed 's/\.html$//').png"
  timeout 60 "$chrome" --headless=new --disable-gpu --no-sandbox --hide-scrollbars \
    --window-size=1280,1400 --virtual-time-budget=3000 \
    --screenshot="$png" "http://127.0.0.1:$port/$page" >/dev/null 2>&1 || true
  if [ -s "$png" ]; then echo "ok   $png"; else echo "NG   $page" >&2; fi
done
