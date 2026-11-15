"""Runtime guard for processes that load LLM-written models (coder.py, task E).

Installed before any generated code is imported. A Python audit hook (it cannot be removed once
added) refuses, for the rest of the process:
  - network:   socket creation/connect/bind/DNS, urllib requests;
  - processes: subprocess, os.system/exec*/spawn*/fork, pty;
  - native:    ctypes / dlopen;
  - files:     opening for writing outside the allowed write folders, opening for reading outside
               Python's own install, the project folder, the data pack and the run's folders,
               and deleting or renaming files outside the write folders.
The one process allowed is the framework's own call of the official scorer on files in the run
folders (evaluate.py). The static gate is the first line of defence; this one does not depend on spotting every
file or network helper that numpy/pandas/scipy expose.
"""
from __future__ import annotations

import os
import site
import sys
import sysconfig

_WRITE_FLAGS = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_APPEND | os.O_TRUNC
_BLOCK = ("socket.", "urllib.", "http.", "ftplib.", "smtplib.", "subprocess.", "os.system", "os.exec",
          "os.spawn", "os.posix_spawn", "os.fork", "os.forkpty", "os.kill", "os.killpg", "pty.", "ctypes.",
          "webbrowser.", "sqlite3.connect", "os.chdir")
_FILE_CHANGE = {"os.remove": 0, "os.unlink": 0, "os.rmdir": 0, "os.rename": (0, 1), "os.replace": (0, 1),
                "os.truncate": 0, "os.chmod": 0, "os.chown": 0, "os.link": (0, 1), "os.symlink": (0, 1),
                "shutil.rmtree": 0, "shutil.move": (0, 1), "shutil.copyfile": 1, "os.mkdir": 0}
_installed = False


class SandboxViolation(PermissionError):
    pass


def _norm(p) -> str | None:
    if isinstance(p, int):
        return None                       # an already-open descriptor
    try:
        return os.path.realpath(os.fsdecode(p))
    except (TypeError, ValueError):
        return None


def _under(path: str, roots) -> bool:
    return any(path == r or path.startswith(r.rstrip(os.sep) + os.sep) for r in roots)


def install(write_dirs=(), read_dirs=()):
    """Allow writes only under write_dirs; reads under write_dirs, read_dirs and the standard roots."""
    global _installed
    if _installed:
        return
    import config as C
    writes = [_norm(d) for d in write_dirs if d] + ["/dev/null"]
    reads = writes + [_norm(d) for d in read_dirs if d] + [
        _norm(x) for x in (sys.prefix, sys.base_prefix, sys.exec_prefix, C.ROOT, C.PACK,
                           *sysconfig.get_paths().values(), *site.getsitepackages(), site.getusersitepackages(),
                           *[p for p in sys.path if p])] + ["/usr/lib", "/usr/lib64", "/usr/share", "/usr/local/lib",
                                                            "/lib", "/lib64", "/etc/localtime", "/proc/self",
                                                            "/sys/devices/system/cpu", "/dev/null", "/dev/urandom"]
    reads = [r for r in reads if r]

    scorer = _norm(C.STARTER / "scorer.py")
    env_at_install = dict(os.environ)
    outputs = {"--out", "--per-cell", "--forecast"}

    def scorer_call(argv) -> bool:
        """The framework's own call of the official scorer (evaluate.py) on files inside the run."""
        argv = [os.fsdecode(a) for a in (argv or [])]
        if argv[:3] != [sys.executable, "-B", scorer] or len(argv) % 2 == 0:
            return False
        for flag, val in zip(argv[3::2], argv[4::2]):
            if not flag.startswith("--"):
                return False
            if flag in outputs and not _under(_norm(val) or "", writes):
                return False
            if "/" in val and not _under(_norm(val) or "", reads):
                return False
        return True

    def hook(event, args):
        if event == "subprocess.Popen" and args[0] in (None, sys.executable) and args[2] is None \
                and args[3] is None and dict(os.environ) == env_at_install and scorer_call(args[1]):
            return
        if event.startswith(_BLOCK):
            raise SandboxViolation(f"{event} is not allowed for generated models")
        if event == "open":
            path, mode, flags = (list(args) + [None, None, None])[:3]
            p = _norm(path)
            if p is None:
                return
            if os.path.isdir(p):   # no directory descriptors, so no dir_fd-relative paths
                raise SandboxViolation(f"opening the directory {p} is not allowed for generated models")
            writing = (isinstance(mode, str) and any(c in mode for c in "wax+")) or \
                      (isinstance(flags, int) and flags & _WRITE_FLAGS)
            if writing and not _under(p, writes):
                raise SandboxViolation(f"writing {p} is not allowed for generated models")
            if not writing and not _under(p, reads):
                raise SandboxViolation(f"reading {p} is not allowed for generated models")
        elif event in _FILE_CHANGE:
            idx = _FILE_CHANGE[event]
            for i in (idx if isinstance(idx, tuple) else (idx,)):
                p = _norm(args[i]) if len(args) > i else None
                if p is not None and not _under(p, writes):
                    raise SandboxViolation(f"{event} on {p} is not allowed for generated models")

    sys.addaudithook(hook)
    _installed = True
