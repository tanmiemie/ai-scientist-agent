#!/usr/bin/env bash
# Download the GPU price data pack from this repo's GitHub release, verify it and unpack it next to gpu_scientist/
# (where config.py looks by default). Usage: bash get_pack.sh [dest_dir]
set -euo pipefail
DEST="$(cd "${1:-$(dirname "$0")/..}" && pwd)"
NAME=gpu-price-pack-v0.1.1-handover
ZIP="${NAME}_pack-only.zip"
SHA=f0b52af28c52545732208bcc4905facd9b941aa5779da683e1d9884c283b7c7c
URL="${GPU_PACK_URL:-https://github.com/tanmiemie/ai-scientist-agent/releases/download/data-pack-v0.1.1/$ZIP}"

if [ -d "$DEST/$NAME" ]; then
  echo "$DEST/$NAME already exists"; exit 0
fi
if [ ! -f "$DEST/$ZIP" ]; then
  echo "downloading $URL (about 285 MB)"
  curl -fL --retry 3 -o "$DEST/$ZIP.part" "$URL"
  mv "$DEST/$ZIP.part" "$DEST/$ZIP"
fi
if command -v sha256sum >/dev/null; then got=$(sha256sum "$DEST/$ZIP" | cut -d' ' -f1); else got=$(shasum -a 256 "$DEST/$ZIP" | cut -d' ' -f1); fi
if [ "$got" != "$SHA" ]; then
  echo "checksum mismatch: $got (expected $SHA); delete $DEST/$ZIP and retry" >&2; exit 1
fi
TMP="$DEST/.$NAME.partial"
rm -rf "$TMP"
unzip -q "$DEST/$ZIP" -d "$TMP"
mv "$TMP/$NAME" "$DEST/$NAME"
rmdir "$TMP"
echo "unpacked to $DEST/$NAME"
echo "keep its ATTRIBUTION.md (CC BY 4.0) with any work that uses it"
