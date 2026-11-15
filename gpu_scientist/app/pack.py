"""Fetch the data pack from the repo's GitHub release (same as get_pack.sh, for hosts without a shell)."""
from __future__ import annotations

import hashlib
import os
import shutil
import urllib.request
import zipfile

import config as C

NAME = "gpu-price-pack-v0.1.1-handover"
SHA256 = "f0b52af28c52545732208bcc4905facd9b941aa5779da683e1d9884c283b7c7c"
URL = os.environ.get("GPU_PACK_URL", "https://github.com/tanmiemie/ai-scientist-agent/releases/download/"
                                     f"data-pack-v0.1.1/{NAME}_pack-only.zip")


def downloadable() -> bool:
    """Only the default location is filled automatically; a custom GPU_PACK is the user's to provide."""
    return C.PACK.name == NAME and not C.PACK.exists()


def fetch(progress=None) -> None:
    dest = C.PACK.parent
    zpath = dest / f"{NAME}_pack-only.zip"
    if not zpath.exists():
        part = zpath.with_suffix(".zip.part")
        with urllib.request.urlopen(URL, timeout=60) as r, open(part, "wb") as fh:
            total, done = int(r.headers.get("Content-Length") or 0), 0
            while chunk := r.read(1 << 20):
                fh.write(chunk)
                done += len(chunk)
                if progress and total:
                    progress(done / total)
        part.rename(zpath)
    h = hashlib.sha256()
    with open(zpath, "rb") as fh:
        while chunk := fh.read(1 << 20):
            h.update(chunk)
    if h.hexdigest() != SHA256:
        zpath.unlink()
        raise RuntimeError(f"checksum mismatch for {zpath.name}; deleted it, try again")
    tmp = dest / f".{NAME}.partial"
    shutil.rmtree(tmp, ignore_errors=True)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(tmp)
    (tmp / NAME).rename(C.PACK)
    tmp.rmdir()
    zpath.unlink()
